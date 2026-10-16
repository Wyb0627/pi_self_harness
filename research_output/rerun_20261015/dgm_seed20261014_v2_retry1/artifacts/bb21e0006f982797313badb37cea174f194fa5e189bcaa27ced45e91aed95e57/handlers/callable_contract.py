import ast
import json
import os
import sys

SKIP_DIRS = {'.git', '.hg', '.svn', '__pycache__', '.tox', '.nox', '.venv', 'node_modules', 'build', 'dist'}

def emit_error(message):
    print(json.dumps({'content': message, 'details': {'definitions': [], 'call_sites': [], 'scanned_files': 0}}))

def source_text(source, node):
    if node is None:
        return ''
    try:
        return ast.get_source_segment(source, node) or ''
    except Exception:
        return ''

def describe_args(args_node, source):
    params = []
    try:
        posonly_count = len(args_node.posonlyargs)
    except Exception:
        posonly_count = 0
    positional = list(args_node.args)
    defaults = list(args_node.defaults)
    default_start = len(positional) - len(defaults)
    for index, arg_node in enumerate(positional):
        has_default = index >= default_start
        default_text = ''
        if has_default:
            default_text = source_text(source, defaults[index - default_start])
        kind = 'positional_only' if index < posonly_count else 'positional_or_keyword'
        params.append({'name': arg_node.arg, 'kind': kind, 'has_default': has_default, 'default': default_text})
    if args_node.vararg is not None:
        params.append({'name': args_node.vararg.arg, 'kind': 'var_positional', 'has_default': False, 'default': ''})
    kw_defaults = list(args_node.kw_defaults)
    for index, arg_node in enumerate(args_node.kwonlyargs):
        has_default = index < len(kw_defaults) and kw_defaults[index] is not None
        default_text = ''
        if has_default:
            default_text = source_text(source, kw_defaults[index])
        params.append({'name': arg_node.arg, 'kind': 'keyword_only', 'has_default': has_default, 'default': default_text})
    if args_node.kwarg is not None:
        params.append({'name': args_node.kwarg.arg, 'kind': 'var_keyword', 'has_default': False, 'default': ''})
    return params

def human_params(args_node, source):
    params = describe_args(args_node, source)
    pieces = []
    seen_star = False
    for param in params:
        kind = param['kind']
        name = param['name']
        if kind == 'var_positional':
            piece = '*' + name
            seen_star = True
        elif kind == 'keyword_only':
            if not seen_star:
                pieces.append('*')
                seen_star = True
            piece = name
        elif kind == 'var_keyword':
            piece = '**' + name
        else:
            piece = name
        if param['has_default']:
            piece = piece + '=' + (param['default'] or '...')
        pieces.append(piece)
    return ', '.join(pieces)

def format_signature(node, source, relpath):
    sig = {
        'path': relpath,
        'lineno': node.lineno,
        'end_lineno': node.lineno,
        'name': node.name,
        'params': describe_args(node.args, source),
        'parameters_human': human_params(node.args, source),
        'decorators': [source_text(source, dec) for dec in node.decorator_list],
        'returns': source_text(source, node.returns)
    }
    try:
        sig['end_lineno'] = node.end_lineno
    except Exception:
        pass
    return sig

def find_definitions(tree, source, relpath, symbol, limit, results):
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.name != symbol:
            continue
        if len(results) >= limit:
            return
        results.append(format_signature(node, source, relpath))

def find_calls(tree, source, relpath, symbol, limit, results):
    lines = source.splitlines()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name):
            call_name = func.id
        elif isinstance(func, ast.Attribute):
            call_name = func.attr
        else:
            continue
        if call_name != symbol:
            continue
        if len(results) >= limit:
            return
        lineno = node.lineno
        start = max(1, lineno - 3)
        end = min(len(lines), lineno + 3)
        context_lines = []
        for current in range(start, end + 1):
            context_lines.append(str(current) + ': ' + lines[current - 1])
        results.append({'path': relpath, 'lineno': lineno, 'context': context_lines})

def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except Exception:
        emit_error('Could not read input JSON.')
        return
    symbol = data.get('symbol')
    if not isinstance(symbol, str) or not symbol.strip():
        emit_error('Parameter symbol is required.')
        return
    symbol = symbol.strip()
    root = data.get('path')
    if not isinstance(root, str) or not root.strip():
        root = '/testbed'
    root = os.path.realpath(os.path.abspath(root))
    testbed = os.path.realpath('/testbed')
    if root != testbed and not root.startswith(testbed + os.sep):
        emit_error('Path must be inside /testbed.')
        return
    if not os.path.isdir(root):
        emit_error('Path is not a directory: ' + root)
        return
    include_calls = data.get('include_calls', True)
    if not isinstance(include_calls, bool):
        include_calls = True
    try:
        max_definitions = int(data.get('max_definitions', 10))
    except Exception:
        max_definitions = 10
    max_definitions = max(1, min(max_definitions, 30))
    max_calls = 80

    definitions = []
    call_sites = []
    scanned_files = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.'))
        for filename in sorted(filenames):
            if not filename.endswith('.py'):
                continue
            filepath = os.path.join(dirpath, filename)
            scanned_files += 1
            try:
                with open(filepath, 'r', encoding='utf-8', errors='replace') as handle:
                    source = handle.read()
            except Exception:
                continue
            try:
                tree = ast.parse(source, filename=filepath)
            except Exception:
                continue
            relpath = os.path.relpath(filepath, root)
            find_definitions(tree, source, relpath, symbol, max_definitions, definitions)
            if include_calls:
                find_calls(tree, source, relpath, symbol, max_calls, call_sites)

    content_lines = []
    content_lines.append('Scanned ' + str(scanned_files) + ' Python files under ' + root + ' for symbol ' + symbol + '.')
    if definitions:
        content_lines.append('Found ' + str(len(definitions)) + ' matching definition(s), showing up to ' + str(len(definitions)) + '.')
        for sig in definitions:
            content_lines.append(sig['path'] + ':' + str(sig['lineno']) + ': ' + sig['parameters_human'])
    else:
        content_lines.append('No definitions found. Use code_search for aliased or partially qualified names.')
    if include_calls:
        if call_sites:
            content_lines.append('Found ' + str(len(call_sites)) + ' matching call site(s), showing up to ' + str(len(call_sites)) + '.')
            for call in call_sites:
                content_lines.append(call['path'] + ':' + str(call['lineno']) + ':')
                content_lines.extend(call['context'])
        else:
            content_lines.append('No matching call sites found.')
    print(json.dumps({'content': chr(10).join(content_lines), 'details': {'definitions': definitions, 'call_sites': call_sites, 'scanned_files': scanned_files}}))

if __name__ == '__main__':
    main()
import ast
import json
import os
import re
import sys

MAX_FILE_SIZE = 2 * 1024 * 1024

def _source_segment(source, node):
    if node is None:
        return ''
    try:
        seg = ast.get_source_segment(source, node)
        if seg:
            return ' '.join(seg.split())
    except Exception:
        pass
    try:
        seg = ast.unparse(node)
        if seg:
            return ' '.join(seg.split())
    except Exception:
        pass
    return ''

def _line_snippet(source, lineno, radius=1):
    try:
        lines = source.splitlines()
    except Exception:
        return ''
    if not lines:
        return ''
    start = max(0, lineno - 1 - radius)
    end = min(len(lines), lineno + radius)
    return ' | '.join(lines[start:end])

def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            raise ValueError('empty input')
        req = json.loads(raw)
        name = req.get('name')
        if not isinstance(name, str) or not name.strip():
            raise ValueError('name must be a non-empty string')
        name = name.strip()
        requested = req.get('search_path', '/testbed')
        if not isinstance(requested, str) or not requested:
            raise ValueError('search_path must be a non-empty string')
        if not os.path.isabs(requested):
            requested = os.path.join('/testbed', requested)
        search_root = os.path.realpath(requested)
        if search_root != '/testbed' and not search_root.startswith('/testbed/'):
            raise ValueError('search_path must be inside /testbed')
        file_pattern = req.get('file_pattern', r'.*[.]py$')
        if not isinstance(file_pattern, str):
            file_pattern = r'.*[.]py$'
        try:
            file_re = re.compile(file_pattern)
            max_results = int(req.get('max_results', 40))
        except Exception as exc:
            raise ValueError('invalid search options: ' + str(exc))
        if max_results < 1:
            max_results = 40
        include_calls = req.get('include_calls', True)
        if isinstance(include_calls, str):
            include_calls = include_calls.strip().lower() not in ('0', 'false', 'no')
        else:
            include_calls = bool(include_calls)
        definitions = []
        call_sites = []
        definitions_total = 0
        call_sites_total = 0
        for dirpath, dirnames, filenames in os.walk(search_root):
            dirnames[:] = [d for d in dirnames if d != '.git']
            dirnames.sort()
            for fname in sorted(filenames):
                if not file_re.search(fname):
                    continue
                path = os.path.join(dirpath, fname)
                try:
                    real_path = os.path.realpath(path)
                    if real_path != '/testbed' and not real_path.startswith('/testbed/'):
                        continue
                    st = os.stat(path)
                    if st.st_size > MAX_FILE_SIZE:
                        continue
                    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                        source = fh.read()
                except Exception:
                    continue
                try:
                    tree = ast.parse(source)
                except SyntaxError:
                    continue
                class_stack = []
                def walk_body(body):
                    for node in body:
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            if node.name == name:
                                definitions_total += 1
                                if len(definitions) < max_results:
                                    qualname = '.'.join(class_stack + [node.name]) if class_stack else node.name
                                    decorators = [_source_segment(source, d) for d in node.decorator_list]
                                    decorators = [d for d in decorators if d]
                                    definitions.append({
                                        'path': os.path.relpath(path, '/testbed'),
                                        'lineno': node.lineno,
                                        'qualname': qualname,
                                        'arguments': _source_segment(source, node.args),
                                        'decorators': decorators,
                                        'snippet': _line_snippet(source, node.lineno, 1)
                                    })
                            walk_body(node.body)
                        elif isinstance(node, ast.ClassDef):
                            class_stack.append(node.name)
                            walk_body(node.body)
                            class_stack.pop()
                walk_body(tree.body)
                if include_calls:
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Call):
                            hit = False
                            func = node.func
                            if isinstance(func, ast.Name) and func.id == name:
                                hit = True
                            elif isinstance(func, ast.Attribute) and func.attr == name:
                                hit = True
                            if hit:
                                call_sites_total += 1
                                if len(call_sites) < max_results:
                                    call_sites.append({
                                        'path': os.path.relpath(path, '/testbed'),
                                        'lineno': node.lineno,
                                        'call_text': _source_segment(source, func),
                                        'snippet': _line_snippet(source, node.lineno, 1)
                                    })
        def format_definition(item):
            parts = []
            parts.append('### ' + item['path'] + ':' + str(item['lineno']))
            parts.append('qualified_name: ' + item['qualname'])
            if item['arguments']:
                parts.append('arguments: ' + item['arguments'])
            if item['decorators']:
                parts.append('decorators: ' + ', '.join(item['decorators']))
            if item['snippet']:
                parts.append('context: ' + item['snippet'])
            return chr(10).join(parts)
        def format_call(item):
            parts = []
            parts.append('### ' + item['path'] + ':' + str(item['lineno']))
            if item['call_text']:
                parts.append('call: ' + item['call_text'])
            if item['snippet']:
                parts.append('context: ' + item['snippet'])
            return chr(10).join(parts)
        sections = []
        if definitions:
            lines = ['Definitions matching ' + repr(name) + ':']
            for d in definitions:
                lines.append(format_definition(d))
            sections.append((chr(10) * 2).join(lines))
        if call_sites:
            lines = ['Call sites matching ' + repr(name) + ':']
            for c in call_sites:
                lines.append(format_call(c))
            sections.append((chr(10) * 2).join(lines))
        if sections:
            content = (chr(10) * 2).join(sections)
        else:
            content = 'No definitions or call sites found for callable name ' + repr(name) + ' under ' + search_root + '.'
        details = {
            'definitions_total': definitions_total,
            'call_sites_total': call_sites_total,
            'definitions_shown': len(definitions),
            'call_sites_shown': len(call_sites),
            'search_path': search_root,
        }
        sys.stdout.write(json.dumps({'content': content, 'details': details}))
    except Exception as exc:
        sys.stdout.write(json.dumps({'content': 'callable_signatures failed: ' + str(exc), 'details': {'error': str(exc)}}))

if __name__ == '__main__':
    main()
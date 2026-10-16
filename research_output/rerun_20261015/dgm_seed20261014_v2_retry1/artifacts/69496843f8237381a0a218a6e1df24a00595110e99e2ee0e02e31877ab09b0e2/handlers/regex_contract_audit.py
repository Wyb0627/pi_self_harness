import ast
import json
import os
import sys

SKIP_DIRS = {'.git', '.hg', '.svn', '__pycache__', '.tox', '.nox', '.venv', 'node_modules', 'build', 'dist', 'htmlcov'}
RE_FUNCS = {'compile', 'match', 'fullmatch', 'search', 'sub', 'subn', 'split', 'findall', 'finditer'}
BS = chr(92)
SIGNED_DIGIT = '-?' + BS + 'd'
CLASS_SIGNED_DIGIT = '[+-]?' + BS + 'd'

def emit(content, details=None):
    print(json.dumps({'content': content, 'details': details or {}}))

def normalize_root(data):
    root = data.get('path')
    if not isinstance(root, str) or not root.strip():
        root = '/testbed'
    root = os.path.realpath(os.path.abspath(root.strip()))
    testbed = os.path.realpath('/testbed')
    if root != testbed and not root.startswith(testbed + os.sep):
        raise ValueError('Path must be inside /testbed.')
    if not os.path.isdir(root):
        raise ValueError('Path is not a directory: ' + root)
    return root

def extract_literal(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = extract_literal(node.left)
        right = extract_literal(node.right)
        if left is not None and right is not None:
            return left + right
    return None

def read_group(pattern, start):
    n = len(pattern)
    kind = 'capture'
    name = None
    content_start = start + 1
    if pattern.startswith('(?P<', start):
        end = pattern.find('>', start + 4)
        if end != -1:
            kind = 'named'
            name = pattern[start + 4:end]
            content_start = end + 1
    elif pattern.startswith('(?=', start):
        kind = 'lookahead'
        content_start = start + 3
    elif pattern.startswith('(?!', start):
        kind = 'negative_lookahead'
        content_start = start + 3
    elif pattern.startswith('(?<=', start):
        kind = 'lookbehind'
        content_start = start + 4
    elif pattern.startswith('(?<!', start):
        kind = 'negative_lookbehind'
        content_start = start + 4
    elif pattern.startswith('(?:', start):
        kind = 'noncapturing'
        content_start = start + 3
    depth = 0
    in_class = False
    i = start
    while i < n:
        c = pattern[i]
        if c == BS:
            i += 2
            continue
        if c == '[':
            in_class = True
            i += 1
            continue
        if c == ']':
            in_class = False
            i += 1
            continue
        if not in_class:
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
                if depth == 0:
                    return {'kind': kind, 'name': name, 'start': start, 'end': i, 'content': pattern[content_start:i]}
        i += 1
    return {'kind': kind, 'name': name, 'start': start, 'end': n - 1, 'content': pattern[content_start:]}

def scan_groups(pattern):
    groups = []
    i = 0
    n = len(pattern)
    in_class = False
    while i < n:
        c = pattern[i]
        if c == BS:
            i += 2
            continue
        if c == '[':
            in_class = True
            i += 1
            continue
        if c == ']':
            in_class = False
            i += 1
            continue
        if not in_class and c == '(':
            groups.append(read_group(pattern, i))
            i += 1
            continue
        i += 1
    return groups

def analyze_pattern(pattern):
    groups = scan_groups(pattern)
    named = [g['name'] for g in groups if g['kind'] == 'named' and g['name']]
    lookarounds = [g for g in groups if g['kind'] in ('lookahead', 'negative_lookahead', 'lookbehind', 'negative_lookbehind')]
    signed = []
    unsigned_lookaheads = []
    for g in groups:
        if g['kind'] == 'named' and (SIGNED_DIGIT in g['content'] or CLASS_SIGNED_DIGIT in g['content']):
            signed.append({'name': g['name'], 'content': g['content']})
    for g in groups:
        if g['kind'] in ('lookahead', 'negative_lookahead') and (BS + 'd') in g['content']:
            if SIGNED_DIGIT not in g['content'] and CLASS_SIGNED_DIGIT not in g['content']:
                unsigned_lookaheads.append({'kind': g['kind'], 'content': g['content']})
    return {'named_groups': named, 'lookarounds': [{'kind': g['kind'], 'content': g['content']} for g in lookarounds], 'signed_digit_captures': signed, 'unsigned_lookahead_digit_constraints': unsigned_lookaheads}

def collect_files(root, rel_file):
    if rel_file:
        rel = os.path.normpath(rel_file)
        full = os.path.realpath(os.path.join(root, rel))
        if full == root or not full.startswith(root + os.sep):
            raise ValueError('file must be relative to path and stay inside it.')
        return [full] if os.path.isfile(full) else []
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.'))
        for filename in sorted(filenames):
            if filename.endswith('.py'):
                files.append(os.path.join(dirpath, filename))
    return files

def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            raw = '{}'
        data = json.loads(raw)
        root = normalize_root(data)
    except Exception as exc:
        emit('Input error: ' + str(exc))
        return
    rel_file = data.get('file')
    if rel_file is not None and not isinstance(rel_file, str):
        emit('Parameter file must be a string.')
        return
    pattern_substring = data.get('pattern_substring')
    if not isinstance(pattern_substring, str):
        pattern_substring = ''
    try:
        max_results = int(data.get('max_results', 100))
    except Exception:
        max_results = 100
    max_results = max(1, min(max_results, 200))
    try:
        files = collect_files(root, rel_file)
    except Exception as exc:
        emit(str(exc))
        return
    findings = []
    files_scanned = 0
    for filepath in files:
        if not os.path.isfile(filepath):
            continue
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as handle:
                source = handle.read()
            tree = ast.parse(source)
        except Exception:
            continue
        files_scanned += 1
        source_lines = source.splitlines()
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            call_name = ''
            if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) and func.value.id == 're':
                call_name = func.attr
            if call_name not in RE_FUNCS:
                continue
            if not node.args:
                continue
            literal = extract_literal(node.args[0])
            lineno = node.lineno
            src_line = source_lines[lineno - 1].strip() if 0 < lineno <= len(source_lines) else ''
            if pattern_substring:
                haystack = literal if literal is not None else ''
                if pattern_substring not in haystack and pattern_substring not in src_line:
                    continue
            relpath = os.path.relpath(filepath, root)
            if literal is None:
                analysis = {'named_groups': [], 'lookarounds': [], 'signed_digit_captures': [], 'unsigned_lookahead_digit_constraints': []}
            else:
                analysis = analyze_pattern(literal)
            finding = {'path': relpath, 'line': lineno, 'call': 're.' + call_name, 'pattern': literal, 'dynamic': literal is None, 'source_line': src_line}
            finding.update(analysis)
            findings.append(finding)
            if len(findings) >= max_results:
                break
        if len(findings) >= max_results:
            break
    lines = []
    lines.append('Inspected ' + str(files_scanned) + ' Python file(s).')
    lines.append('Found ' + str(len(findings)) + ' regex call(s).')
    if pattern_substring:
        lines.append('Filter: calls whose literal pattern or source line contains ' + repr(pattern_substring) + '.')
    for idx, finding in enumerate(findings, 1):
        lines.append(str(idx) + '. ' + finding['path'] + ':' + str(finding['line']) + ': ' + finding['call'])
        lines.append('   source: ' + finding['source_line'][:160])
        if finding['dynamic']:
            lines.append('   pattern: dynamic expression (not a string literal)')
            if 're.escape' in finding['source_line']:
                lines.append('   already uses re.escape in this call.')
            else:
                lines.append('   if external values are interpolated, consider re.escape() for literal parts.')
        else:
            lines.append('   pattern: ' + repr(finding['pattern'])[:200])
            if finding['named_groups']:
                lines.append('   named groups: ' + ', '.join(finding['named_groups']))
            if finding['lookarounds']:
                lines.append('   lookarounds: ' + '; '.join(item['kind'] for item in finding['lookarounds']))
            if finding['signed_digit_captures']:
                lines.append('   signed digit captures: ' + ', '.join(item['name'] for item in finding['signed_digit_captures']))
            if finding['unsigned_lookahead_digit_constraints']:
                lines.append('   unsigned lookahead digit constraint(s): ' + '; '.join(item['content'][:60] for item in finding['unsigned_lookahead_digit_constraints']))
            if not finding['named_groups'] and not finding['lookarounds'] and not finding['signed_digit_captures'] and not finding['unsigned_lookahead_digit_constraints']:
                lines.append('   no structural groups detected.')
    details = {'files_scanned': files_scanned, 'regex_calls': len(findings), 'filter': pattern_substring or None, 'findings': findings}
    emit(chr(10).join(lines), details)

if __name__ == '__main__':
    main()

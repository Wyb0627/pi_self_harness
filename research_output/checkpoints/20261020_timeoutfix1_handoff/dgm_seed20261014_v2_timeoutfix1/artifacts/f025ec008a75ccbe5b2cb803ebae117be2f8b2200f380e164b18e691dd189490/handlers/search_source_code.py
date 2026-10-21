import json
import os
import re
import sys

ROOT = '/testbed'

SKIP_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'site-packages', '.tox', '.mypy_cache', '.pytest_cache'}

def iter_python_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in SKIP_DIRS]
        for filename in filenames:
            if filename.endswith('.py'):
                yield os.path.join(dirpath, filename)

def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            print(json.dumps({'content': 'No input received.', 'details': {}}))
            return
        data = json.loads(raw)
    except Exception as exc:
        print(json.dumps({'content': 'Invalid JSON input: {0}'.format(exc), 'details': {}}))
        return

    params = data if isinstance(data, dict) and 'query' in data else data.get('parameters', {})
    if not isinstance(params, dict):
        print(json.dumps({'content': 'Parameters must be a JSON object.', 'details': {}}))
        return

    query = params.get('query')
    if not isinstance(query, str) or not query.strip():
        print(json.dumps({'content': 'Missing non-empty string parameter.', 'details': {}}))
        return

    path_substring = params.get('path_include', '')
    if path_substring is None:
        path_substring = ''
    path_substring = str(path_substring)

    try:
        max_results = int(params.get('max_results', 30))
    except (TypeError, ValueError):
        max_results = 30
    max_results = max(1, min(max_results, 200))

    try:
        context_lines = int(params.get('context_lines', 2))
    except (TypeError, ValueError):
        context_lines = 2
    context_lines = max(0, min(context_lines, 10))

    case_sensitive = bool(params.get('case_sensitive', False))
    use_regex = bool(params.get('regex', False))
    flags = 0 if case_sensitive else re.IGNORECASE

    try:
        pattern = re.compile(query if use_regex else re.escape(query), flags)
    except re.error as exc:
        print(json.dumps({'content': 'Invalid regular expression: {0}'.format(exc), 'details': {}}))
        return

    matches = []
    for filepath in iter_python_files():
        relpath = os.path.relpath(filepath, ROOT)
        if path_substring and path_substring not in relpath:
            continue
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as fh:
                lines = fh.readlines()
        except OSError:
            continue
        for line_no, line in enumerate(lines, 1):
            if pattern.search(line):
                start = max(0, line_no - 1 - context_lines)
                end = min(len(lines), line_no + context_lines)
                snippet = ''.join(lines[start:end])
                matches.append({
                    'path': relpath,
                    'line': line_no,
                    'text': line.rstrip(chr(10)),
                    'snippet': snippet
                })
                if len(matches) >= max_results:
                    break
        if len(matches) >= max_results:
            break

    if matches:
        lines_out = []
        for m in matches:
            lines_out.append('{0}:{1}: {2}'.format(m['path'], m['line'], m['text'].strip()))
        content = 'Found {0} match(es).' + chr(10) + chr(10) + chr(10).join(lines_out)
        content = content.format(len(matches))
    else:
        content = 'No matches found for query: {0}'.format(query)

    print(json.dumps({'content': content, 'details': {'count': len(matches), 'matches': matches}}))

if __name__ == '__main__':
    main()
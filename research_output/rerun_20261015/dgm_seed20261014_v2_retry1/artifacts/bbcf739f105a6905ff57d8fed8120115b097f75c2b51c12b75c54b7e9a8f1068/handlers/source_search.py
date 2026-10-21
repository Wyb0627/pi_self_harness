import json, os, re, sys

def main():
    try:
        request = json.load(sys.stdin)
    except Exception as exc:
        print(json.dumps({'content': 'Invalid JSON input.', 'details': {'error': str(exc)}}))
        return

    pattern = request.get('pattern', '')
    if not isinstance(pattern, str) or not pattern:
        print(json.dumps({'content': 'Missing pattern string.', 'details': {'error': 'pattern is required'}}))
        return

    try:
        flags = 0 if request.get('case_sensitive', False) else re.IGNORECASE
        regex = re.compile(pattern, flags)
    except re.error as exc:
        print(json.dumps({'content': 'Invalid regex.', 'details': {'error': str(exc)}}))
        return

    base = '/testbed'
    try:
        search_root = os.path.abspath(os.path.join(base, request.get('root', '.')))
        if os.path.commonpath([base, search_root]) != base:
            raise ValueError('root must be inside /testbed')
    except Exception as exc:
        print(json.dumps({'content': 'Invalid root.', 'details': {'error': str(exc)}}))
        return

    try:
        file_pattern = request.get('file_pattern', r'\.py$')
        file_regex = re.compile(file_pattern)
    except re.error as exc:
        print(json.dumps({'content': 'Invalid file_pattern.', 'details': {'error': str(exc)}}))
        return

    context = request.get('context_lines', 2)
    if not isinstance(context, int):
        context = 2
    context = max(0, min(10, context))

    max_results = request.get('max_results', 60)
    if not isinstance(max_results, int):
        max_results = 60
    max_results = max(1, min(200, max_results))

    skip_dirs = {'.git', '.hg', '.svn', '__pycache__', 'node_modules', '.tox', '.venv', 'venv'}
    matches = []

    for dirpath, dirnames, filenames in os.walk(search_root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        dirnames.sort()
        for filename in sorted(filenames):
            path = os.path.join(dirpath, filename)
            if not file_regex.search(path):
                continue
            try:
                with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                    lines = fh.readlines()
            except OSError:
                continue
            for lineno, line in enumerate(lines, 1):
                if regex.search(line):
                    start = max(0, lineno - 1 - context)
                    end = min(len(lines), lineno + context)
                    snippet_lines = lines[start:end]
                    if snippet_lines and not snippet_lines[-1].endswith('\n'):
                        snippet_lines[-1] += '\n'
                    snippet = ''.join(snippet_lines)
                    matches.append({
                        'path': os.path.relpath(path, base),
                        'line': lineno,
                        'snippet': snippet,
                    })
                    if len(matches) >= max_results:
                        break
            if len(matches) >= max_results:
                break
        if len(matches) >= max_results:
            break

    parts = []
    for idx, m in enumerate(matches, 1):
        parts.append(str(idx) + '. ' + m['path'] + ':' + str(m['line']))
        if context:
            parts.append(m['snippet'].rstrip('\n'))
    content = '\n'.join(parts)
    print(json.dumps({'content': content, 'details': {'count': len(matches), 'searched_root': os.path.relpath(search_root, base)}}))

if __name__ == '__main__':
    main()
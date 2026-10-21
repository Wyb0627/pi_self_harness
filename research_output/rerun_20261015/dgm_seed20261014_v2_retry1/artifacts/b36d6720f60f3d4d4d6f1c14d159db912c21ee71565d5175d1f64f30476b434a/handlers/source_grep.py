import json, os, re, fnmatch
import sys

def handler(params):
    query = params.get('query', '')
    root = params.get('root', '/testbed')
    glob_pattern = params.get('glob', '*.py')
    try:
        max_matches = int(params.get('max_matches', 30) or 30)
        context_lines = int(params.get('context_lines', 2) or 2)
    except ValueError:
        return {'content': 'max_matches and context_lines must be integers.', 'details': {}}
    if max_matches < 1:
        max_matches = 30
    if context_lines < 0:
        context_lines = 0
    if not query:
        return {'content': 'No query provided.', 'details': {}}
    root = os.path.abspath(root)
    testbed_root = os.path.abspath('/testbed')
    if os.path.normpath(root) != os.path.normpath(testbed_root) and not os.path.normpath(root).startswith(os.path.normpath(testbed_root) + os.sep):
        root = testbed_root
    if not os.path.isdir(root):
        return {'content': 'Root not found: ' + root, 'details': {}}
    try:
        q = re.compile(query, re.IGNORECASE | re.MULTILINE)
    except re.error as exc:
        return {'content': 'Invalid regular expression: ' + str(exc), 'details': {}}
    matches = []
    scanned = 0
    read_error = None
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for filename in filenames:
            if glob_pattern:
                rel = os.path.relpath(os.path.join(dirpath, filename), root)
                if not fnmatch.fnmatch(filename, glob_pattern) and not fnmatch.fnmatch(rel, glob_pattern):
                    continue
            scanned += 1
            path = os.path.join(dirpath, filename)
            try:
                with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                    lines = fh.read().splitlines()
            except Exception as exc:
                read_error = read_error or str(exc)
                continue
            for idx, line in enumerate(lines):
                if q.search(line):
                    start = max(0, idx - context_lines)
                    end = min(len(lines), idx + context_lines + 1)
                    snippet_lines = []
                    for i in range(start, end):
                        snippet_lines.append('{:5d}: {}'.format(i + 1, lines[i]))
                    snippet = chr(10).join(snippet_lines)
                    matches.append({'path': path, 'line': idx + 1, 'snippet': snippet})
                    if len(matches) >= max_matches:
                        break
            if len(matches) >= max_matches:
                break
        if len(matches) >= max_matches:
            break
    if not matches:
        content = 'No matches found.'
    else:
        blocks = []
        for m in matches:
            blocks.append('{}:{}'.format(m['path'], m['line']))
            blocks.append(m['snippet'])
        content = chr(10).join(blocks)
    details = {
        'match_count': len(matches),
        'files_scanned': scanned,
        'root': root,
        'query_pattern': query,
        'truncated': len(matches) >= max_matches,
    }
    if read_error:
        details['read_error'] = read_error
    return {'content': content, 'details': details}

if __name__ == '__main__':
    data = json.load(sys.stdin)
    if isinstance(data, dict) and isinstance(data.get('params'), dict):
        data = data['params']
    print(json.dumps(handler(data), ensure_ascii=False))
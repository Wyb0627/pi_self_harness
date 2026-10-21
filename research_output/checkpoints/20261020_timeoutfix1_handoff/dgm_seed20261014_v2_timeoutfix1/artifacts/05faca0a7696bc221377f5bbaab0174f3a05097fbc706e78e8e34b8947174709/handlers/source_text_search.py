import sys
import os
import json

def main():
    try:
        raw = sys.stdin.read()
        request = json.loads(raw)
    except Exception as exc:
        print(json.dumps({'content': 'Invalid JSON input.', 'details': {'error': str(exc)}}))
        return

    query = request.get('query')
    if not isinstance(query, str) or not query.strip():
        print(json.dumps({'content': 'Provide a non-empty string query.', 'details': {}}))
        return
    query = query.strip()

    root = '/testbed'
    requested_scope = request.get('scope')
    if requested_scope:
        scope = os.path.abspath(os.path.join(root, requested_scope.lstrip('/')))
        try:
            if os.path.commonpath([scope, root]) != root:
                scope = root
        except ValueError:
            scope = root
    else:
        scope = root

    if not os.path.isdir(scope):
        print(json.dumps({'content': 'Scope directory not found.', 'details': {'scope': scope}}))
        return

    try:
        max_results = int(request.get('max_results', 30))
    except (TypeError, ValueError):
        max_results = 30
    max_results = max(1, min(max_results, 200))

    results = []
    files_scanned = 0
    excluded_dirs = {'.git', '.hg', '.svn', '__pycache__', 'node_modules', '.tox', '.venv', 'venv'}
    needle = query.lower()

    for dirpath, dirnames, filenames in os.walk(scope):
        dirnames[:] = [d for d in dirnames if d not in excluded_dirs and not d.startswith('.')]
        for filename in filenames:
            if not (filename.endswith('.py') or filename.endswith('.html')):
                continue
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                    lines = f.readlines()
                files_scanned += 1
            except Exception:
                continue
            for idx, line in enumerate(lines):
                if needle in line.lower():
                    relpath = os.path.relpath(filepath, root)
                    start = max(0, idx - 1)
                    end = min(len(lines), idx + 2)
                    excerpt = ''.join(lines[start:end]).rstrip()
                    results.append(relpath + ':' + str(idx + 1) + '\n' + excerpt)
                    if len(results) >= max_results:
                        break
            if len(results) >= max_results:
                break
        if len(results) >= max_results:
            break

    if results:
        content = 'Found matches:\n\n' + '\n\n---\n\n'.join(results)
    else:
        content = 'No matches for ' + repr(query) + ' under ' + scope + '.'

    details = {
        'match_count': len(results),
        'files_scanned': files_scanned,
        'truncated': len(results) >= max_results,
        'scope': scope
    }
    print(json.dumps({'content': content, 'details': details}))

if __name__ == '__main__':
    main()

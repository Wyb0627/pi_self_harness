import json
import os
import re
import sys

SKIP_DIRS = {'.git', '.hg', '.svn', '__pycache__', '.tox', '.nox', '.venv', 'node_modules', '_build', 'build', 'dist'}
DEFAULT_EXTS = ('py', 'rst', 'txt', 'cfg', 'ini', 'html', 'js', 'css')

def emit_error(message):
    print(json.dumps({'content': message, 'details': {'match_count': 0}}))

def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
    except Exception as exc:
        emit_error('Could not read input JSON: ' + str(exc))
        return

    pattern = data.get('pattern')
    if not isinstance(pattern, str) or not pattern:
        emit_error('Parameter pattern is required.')
        return

    root = data.get('path')
    if not isinstance(root, str) or not root:
        root = '/testbed'

    ext_arg = data.get('extensions')
    if not isinstance(ext_arg, str) or not ext_arg.strip():
        ext_arg = ','.join(DEFAULT_EXTS)
    ext_set = set()
    for part in ext_arg.split(','):
        part = part.strip().lower()
        if part:
            if part.startswith('.'):
                part = part[1:]
            ext_set.add(part)

    try:
        context_lines = int(data.get('context_lines', 2))
    except Exception:
        context_lines = 2
    context_lines = max(0, min(context_lines, 10))

    try:
        max_results = int(data.get('max_results', 100))
    except Exception:
        max_results = 100
    max_results = max(1, min(max_results, 200))

    case_sensitive = data.get('case_sensitive', True)
    if not isinstance(case_sensitive, bool):
        case_sensitive = True
    flags = 0 if case_sensitive else re.IGNORECASE

    try:
        rx = re.compile(pattern, flags)
    except re.error as exc:
        emit_error('Invalid regular expression: ' + str(exc))
        return

    root = os.path.abspath(root)
    root = os.path.realpath(root)
    testbed = os.path.realpath('/testbed')
    if root != testbed and not root.startswith(testbed + os.sep):
        emit_error('Path must be inside /testbed.')
        return
    if not os.path.isdir(root):
        emit_error('Path is not a directory: ' + root)
        return

    matches = []
    scanned_files = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.'))
        for filename in sorted(filenames):
            if '.' not in filename:
                continue
            ext = filename.rsplit('.', 1)[1].lower()
            if ext not in ext_set:
                continue
            filepath = os.path.join(dirpath, filename)
            scanned_files += 1
            try:
                with open(filepath, 'r', encoding='utf-8', errors='replace') as handle:
                    lines = handle.readlines()
            except Exception:
                continue
            relpath = os.path.relpath(filepath, root)
            for lineno, line in enumerate(lines, start=1):
                if rx.search(line):
                    start = max(1, lineno - context_lines)
                    end = min(len(lines), lineno + context_lines)
                    context = []
                    for current in range(start, end + 1):
                        context.append({'line': current, 'text': lines[current - 1].rstrip()})
                    matches.append({
                        'path': relpath,
                        'line': lineno,
                        'text': line.rstrip(),
                        'context': context
                    })
                    if len(matches) >= max_results:
                        break
            if len(matches) >= max_results:
                break
        if len(matches) >= max_results:
            break

    content_lines = []
    content_lines.append('Searched ' + str(scanned_files) + ' files under ' + root + ' for pattern: ' + pattern)
    if matches:
        content_lines.append('Found ' + str(len(matches)) + ' matching line(s), showing up to ' + str(len(matches)) + '.')
        for match in matches:
            content_lines.append(match['path'] + ':' + str(match['line']) + ': ' + match['text'])
    else:
        content_lines.append('No matches found.')

    details = {
        'scanned_files': scanned_files,
        'match_count': len(matches),
        'matches': matches
    }
    print(json.dumps({'content': chr(10).join(content_lines), 'details': details}))

if __name__ == '__main__':
    main()
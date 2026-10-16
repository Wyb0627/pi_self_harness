import sys
import os
import json

def main():
    try:
        raw = sys.stdin.read()
        params = json.loads(raw) if raw.strip() else {}
    except Exception as exc:
        print(json.dumps({'content': 'Invalid JSON input: ' + str(exc)}))
        return

    root = '/testbed'
    if not os.path.isdir(root):
        print(json.dumps({'content': 'Source root /testbed not found.'}))
        return

    query = params.get('query', '')
    if not isinstance(query, str) or not query.strip():
        print(json.dumps({'content': 'Missing or empty query. Pass a symbol or file path fragment.'}))
        return
    query = query.strip()

    file_filter = params.get('file_filter', '')
    if not isinstance(file_filter, str):
        file_filter = ''
    file_filter = file_filter.strip()

    base = os.path.normpath(root)
    restrict = base
    if file_filter:
        candidate = os.path.normpath(os.path.join(base, file_filter))
        if candidate != base and not candidate.startswith(base + os.sep):
            print(json.dumps({'content': 'file_filter must stay inside /testbed.'}))
            return
        if not os.path.exists(candidate):
            print(json.dumps({'content': 'file_filter not found: ' + file_filter}))
            return
        restrict = candidate

    try:
        context_lines = int(params.get('context_lines', 4))
    except Exception:
        context_lines = 4
    context_lines = max(0, min(context_lines, 15))

    try:
        max_results = int(params.get('max_results', 15))
    except Exception:
        max_results = 15
    max_results = max(1, min(max_results, 50))

    find_refs = bool(params.get('find_references', False))

    def rel(path):
        try:
            return os.path.relpath(path, root)
        except Exception:
            return path

    def is_def_line(stripped, tail_name):
        for prefix in ('class ', 'def ', 'async def '):
            if stripped.startswith(prefix + tail_name):
                after = stripped[len(prefix + tail_name):]
                if after == '' or after[0] in (' ', '(', ':'):
                    return True
        return False

    def snippet(lines, idx, ctx):
        start = max(0, idx - ctx)
        end = min(len(lines), idx + ctx + 1)
        numbered = []
        for num in range(start, end):
            numbered.append(str(num + 1).rjust(5) + ': ' + lines[num].rstrip('\n'))
        return '\n'.join(numbered)

    line_param = params.get('line')
    if line_param is not None and os.path.isfile(restrict):
        try:
            line_no = int(line_param)
        except Exception:
            line_no = 0
        if line_no < 1:
            line_no = 1
        with open(restrict, 'r', errors='replace') as fh:
            all_lines = fh.readlines()
        if line_no > len(all_lines):
            print(json.dumps({'content': 'Line {0} is beyond end of {1} ({2} lines).'.format(line_no, rel(restrict), len(all_lines)), 'details': {'file': rel(restrict), 'line_count': len(all_lines)}}))
            return
        print(json.dumps({'content': 'File: ' + rel(restrict) + '\n' + snippet(all_lines, line_no - 1, context_lines), 'details': {'file': rel(restrict), 'line': line_no}}))
        return

    tail = query.split('.')[-1].strip()
    is_file_query = ('/' in query or '\\' in query or query.endswith('.py'))

    matches = []
    truncated = False
    scanned_files = 0

    def consider_file(path):
        nonlocal scanned_files, truncated
        if truncated:
            return
        if not path.endswith('.py'):
            return
        scanned_files += 1
        rpath = rel(path)
        if is_file_query and query.lower() in rpath.lower():
            matches.append({'type': 'file', 'file': rpath, 'line': None, 'snippet': ''})
            if len(matches) >= max_results:
                truncated = True
            return
        try:
            with open(path, 'r', errors='replace') as fh:
                content_lines = fh.readlines()
        except Exception:
            return
        for idx, line in enumerate(content_lines):
            stripped = line.lstrip()
            is_def = is_def_line(stripped, tail)
            if is_def or (find_refs and tail in line):
                if len(matches) >= max_results:
                    truncated = True
                    return
                matches.append({
                    'type': 'definition' if is_def else 'reference',
                    'file': rpath,
                    'line': idx + 1,
                    'snippet': snippet(content_lines, idx, context_lines)
                })
        if len(matches) >= max_results:
            truncated = True

    if os.path.isfile(restrict):
        consider_file(restrict)
    else:
        for dirpath, dirnames, filenames in os.walk(restrict):
            dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != '__pycache__']
            for filename in filenames:
                if filename.endswith('.py'):
                    consider_file(os.path.join(dirpath, filename))
                    if truncated:
                        break
            if truncated:
                break

    if not matches:
        if find_refs:
            content = 'No occurrences of {0} found under {1}.'.format(query, rel(restrict) if restrict != base else '/testbed')
        else:
            content = 'No definition of {0} found. Set find_references=true to search call sites and other occurrences.'.format(tail)
        print(json.dumps({'content': content, 'details': {'scanned_files': scanned_files}}))
        return

    lines_out = []
    for m in matches:
        if m['type'] == 'file':
            lines_out.append('FILE: ' + m['file'])
        else:
            lines_out.append('{0} {1}:{2}\n{3}'.format(m['type'].upper(), m['file'], m['line'], m['snippet']))
    content = '\n\n'.join(lines_out)
    if truncated:
        content += '\n\n[truncated after {0} matches]'.format(len(matches))
    print(json.dumps({'content': content, 'details': {'scanned_files': scanned_files, 'matched_count': len(matches), 'truncated': truncated}}))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'content': 'Unexpected tool error: ' + str(exc)}))
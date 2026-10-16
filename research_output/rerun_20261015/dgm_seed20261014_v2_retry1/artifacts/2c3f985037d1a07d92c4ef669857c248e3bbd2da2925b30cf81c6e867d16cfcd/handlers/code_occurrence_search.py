import sys, os, json, re, fnmatch

def main():
    try:
        payload = json.load(sys.stdin)
        pattern = str(payload.get('pattern', '')).strip()
        if not pattern:
            raise ValueError('pattern is required')
        file_glob = payload.get('file_glob', '*.py')
        max_matches = int(payload.get('max_matches', 50))
        if max_matches < 1:
            max_matches = 1
        if max_matches > 200:
            max_matches = 200
        context_lines = int(payload.get('context_lines', 2))
        if context_lines < 0:
            context_lines = 0
        if context_lines > 20:
            context_lines = 20
        case_sensitive = payload.get('case_sensitive', False)
        if isinstance(case_sensitive, str):
            case_sensitive = case_sensitive.lower() in ('1', 'true', 'yes')
        use_regex = payload.get('regex', True)
        if isinstance(use_regex, str):
            use_regex = use_regex.lower() not in ('0', 'false', 'no')
        flags = 0 if case_sensitive else re.IGNORECASE
        compiled = None
        if use_regex:
            try:
                compiled = re.compile(pattern, flags)
            except re.error as exc:
                raise ValueError('invalid regex: ' + str(exc))
        root = '/testbed'
        matches = []
        files_scanned = 0
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in ('.git', '__pycache__', '.tox', '.venv', 'venv', 'node_modules')]
            for fname in sorted(filenames):
                if not fnmatch.fnmatch(fname, file_glob):
                    continue
                path = os.path.join(dirpath, fname)
                files_scanned += 1
                try:
                    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                        lines = fh.readlines()
                except Exception:
                    continue
                for idx, line in enumerate(lines):
                    if use_regex:
                        hit = compiled.search(line)
                    else:
                        haystack = line if case_sensitive else line.lower()
                        needle = pattern if case_sensitive else pattern.lower()
                        hit = needle in haystack
                    if not hit:
                        continue
                    start = max(0, idx - context_lines)
                    end = min(len(lines), idx + context_lines + 1)
                    snippet = ''.join(lines[start:end])
                    matches.append({
                        'file': path,
                        'line': idx + 1,
                        'line_text': line.rstrip(chr(10)),
                        'snippet': snippet,
                    })
                    if len(matches) >= max_matches:
                        break
                if len(matches) >= max_matches:
                    break
            if len(matches) >= max_matches:
                break
        if matches:
            human_lines = ['Found %d match%s in %d files.' % (len(matches), '' if len(matches) == 1 else 'es', files_scanned)]
            for m in matches:
                human_lines.append('%s:%d' % (m['file'], m['line']))
                human_lines.append('  ' + m['line_text'])
            content = chr(10).join(human_lines)
        else:
            content = 'No matches found in %d files.' % files_scanned
        details = {
            'pattern': pattern,
            'matches': matches,
            'match_count': len(matches),
            'files_scanned': files_scanned,
            'truncated': len(matches) >= max_matches,
        }
        sys.stdout.write(json.dumps({'content': content, 'details': details}))
    except Exception as exc:
        sys.stdout.write(json.dumps({'content': 'Search failed: ' + str(exc)}))

if __name__ == '__main__':
    main()
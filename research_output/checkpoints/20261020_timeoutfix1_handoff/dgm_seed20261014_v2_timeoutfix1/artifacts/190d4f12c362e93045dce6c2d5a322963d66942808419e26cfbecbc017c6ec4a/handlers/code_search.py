import json
import os
import re
import sys

def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            raise ValueError('empty input')
        req = json.loads(raw)
        pattern = req.get('pattern')
        if not isinstance(pattern, str) or not pattern:
            raise ValueError('pattern must be a non-empty string')
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
            file_pattern = r'.*'
        try:
            regex = re.compile(pattern)
            file_re = re.compile(file_pattern)
            max_results = int(req.get('max_results', 50))
            context_lines = int(req.get('context_lines', 3))
        except Exception as exc:
            raise ValueError('invalid search options: ' + str(exc))
        if max_results < 1:
            max_results = 50
        if context_lines < 0:
            context_lines = 0
        matches = []
        files_with_matches = 0
        total_matches = 0
        for dirpath, dirnames, filenames in os.walk(search_root):
            dirnames[:] = [d for d in dirnames if d != '.git']
            dirnames.sort()
            for fname in sorted(filenames):
                if not file_re.search(fname):
                    continue
                path = os.path.join(dirpath, fname)
                real_path = os.path.realpath(path)
                if real_path != '/testbed' and not real_path.startswith('/testbed/'):
                    continue
                try:
                    st = os.stat(path)
                    if st.st_size > 2 * 1024 * 1024:
                        continue
                    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                        lines = fh.readlines()
                except Exception:
                    continue
                file_has_match = False
                for lineno, line in enumerate(lines, 1):
                    if regex.search(line):
                        total_matches += 1
                        file_has_match = True
                        if len(matches) < max_results:
                            start = max(0, lineno - 1 - context_lines)
                            end = min(len(lines), lineno + context_lines)
                            snippet_lines = []
                            for i in range(start, end):
                                marker = '>' if i + 1 == lineno else ' '
                                snippet_lines.append(marker + '%5d| ' % (i + 1) + lines[i].rstrip())
                            matches.append('### ' + path + ':' + str(lineno) + chr(10) + '```' + chr(10) + chr(10).join(snippet_lines) + chr(10) + '```')
                if file_has_match:
                    files_with_matches += 1
        if matches:
            content = 'Search results for ' + repr(pattern) + chr(10) + chr(10) + chr(10).join(matches)
        else:
            content = 'No matches found for pattern ' + repr(pattern) + ' under ' + search_root + ' with file pattern ' + repr(file_pattern) + '.'
        details = {
            'files_with_matches': files_with_matches,
            'matches_counted_up_to_limit': total_matches,
            'results_shown': len(matches),
            'truncated': total_matches > len(matches),
        }
        sys.stdout.write(json.dumps({'content': content, 'details': details}))
    except Exception as exc:
        sys.stdout.write(json.dumps({'content': 'code_search failed: ' + str(exc), 'details': {'error': str(exc)}}))

if __name__ == '__main__':
    main()
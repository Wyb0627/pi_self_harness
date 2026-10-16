import ast
import json
import os
import sys

SKIP_DIRS = {'.git', '.hg', '.svn', '__pycache__', '.tox', '.nox', '.venv', 'node_modules', '_build', 'build', 'dist'}

def emit_error(message):
    print(json.dumps({'content': message, 'details': {}}))

def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception as exc:
        emit_error('Could not read input JSON: ' + str(exc))
        return

    symbol = data.get('symbol')
    if not isinstance(symbol, str) or not symbol:
        emit_error('Parameter symbol is required.')
        return

    root = data.get('path')
    if not isinstance(root, str) or not root:
        root = '/testbed'
    root = os.path.realpath(root)
    testbed = os.path.realpath('/testbed')
    if root != testbed and not root.startswith(testbed + os.sep):
        emit_error('Path must be inside /testbed.')
        return
    if not os.path.isdir(root):
        emit_error('Path is not a directory: ' + root)
        return

    kind = data.get('kind')
    if not isinstance(kind, str):
        kind = 'all'
    kind = kind.strip().lower()
    if kind not in ('all', 'definitions', 'references'):
        emit_error('kind must be one of: all, definitions, references.')
        return

    try:
        max_results = int(data.get('max_results', 200))
    except Exception:
        max_results = 200
    max_results = max(1, min(max_results, 500))

    definitions = []
    references = []
    scanned_files = 0

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.'))
        for filename in sorted(filenames):
            if not filename.endswith('.py'):
                continue
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='replace') as handle:
                    source = handle.read()
            except Exception:
                continue
            scanned_files += 1
            try:
                tree = ast.parse(source, filename=filepath)
            except Exception:
                continue
            relpath = os.path.relpath(filepath, root)
            lines = source.splitlines()

            if kind in ('all', 'definitions'):
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        if node.name == symbol:
                            node_kind = 'class' if isinstance(node, ast.ClassDef) else 'function'
                            text = ''
                            if 1 <= node.lineno <= len(lines):
                                text = lines[node.lineno - 1].strip()
                            definitions.append({
                                'path': relpath,
                                'line': node.lineno,
                                'kind': node_kind,
                                'text': text
                            })
                            if len(definitions) >= max_results:
                                break
                if len(definitions) >= max_results:
                    break

            if kind in ('all', 'references'):
                for node in ast.walk(tree):
                    if isinstance(node, ast.Name) and node.id == symbol:
                        ref_kind = 'name'
                    elif isinstance(node, ast.Attribute) and node.attr == symbol:
                        ref_kind = 'attribute'
                    elif isinstance(node, (ast.Import, ast.ImportFrom)):
                        ref_kind = None
                        for alias in node.names:
                            if alias.asname == symbol or alias.name == symbol:
                                ref_kind = 'import'
                                break
                        if ref_kind is None:
                            continue
                    else:
                        continue
                    text = ''
                    if 1 <= node.lineno <= len(lines):
                        text = lines[node.lineno - 1].strip()
                    references.append({
                        'path': relpath,
                        'line': node.lineno,
                        'kind': ref_kind,
                        'text': text
                    })
                    if len(references) >= max_results:
                        break
                if len(references) >= max_results:
                    break
        if len(definitions) >= max_results or len(references) >= max_results:
            break

    result_defs = definitions[:max_results]
    result_refs = references[:max_results]
    content_lines = []
    content_lines.append('Scanned ' + str(scanned_files) + ' Python files under ' + root + ' for symbol: ' + symbol)
    if kind in ('all', 'definitions'):
        content_lines.append('Definitions (' + str(len(definitions)) + ' found, showing ' + str(len(result_defs)) + '):')
        for match in result_defs:
            content_lines.append(match['path'] + ':' + str(match['line']) + ' [' + match['kind'] + '] ' + match['text'])
    if kind in ('all', 'references'):
        content_lines.append('References (' + str(len(references)) + ' found, showing ' + str(len(result_refs)) + '):')
        for match in result_refs:
            content_lines.append(match['path'] + ':' + str(match['line']) + ' [' + match['kind'] + '] ' + match['text'])
    if not result_defs and not result_refs:
        content_lines.append('No definitions or references found.')

    details = {
        'scanned_files': scanned_files,
        'definition_count': len(definitions),
        'reference_count': len(references),
        'definitions': result_defs,
        'references': result_refs
    }
    print(json.dumps({'content': chr(10).join(content_lines), 'details': details}))

if __name__ == '__main__':
    main()

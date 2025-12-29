import os
import re
from pathlib import Path

WORKSPACE = "/home/imjd/Hong Kong University/Flask Website"
TEMPLATES = os.path.join(WORKSPACE, "templates")
OUT = os.path.join(WORKSPACE, "static_refs.txt")

PATTERNS = [
    re.compile(r"url_for\(\s*'static'\s*,\s*filename=\s*'([^']+)'\s*\)", re.IGNORECASE),
    re.compile(r"src=\"/static/([^\\\"]+)\"", re.IGNORECASE),
]


def extract_refs_from_file(path):
    refs = []
    try:
        text = Path(path).read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return refs
    for pat in PATTERNS:
        for m in pat.finditer(text):
            refs.append(m.group(1))
    return refs


def main():
    rows = []
    exts = {'.png', '.jpg', '.jpeg', '.svg', '.gif'}
    for root, dirs, files in os.walk(TEMPLATES):
        for f in files:
            if not f.lower().endswith(('.html', '.htm')):
                continue
            fp = os.path.join(root, f)
            refs = extract_refs_from_file(fp)
            for r in refs:
                _, ext = os.path.splitext(r)
                if ext.lower() in exts:
                    rows.append((os.path.relpath(fp, TEMPLATES), r))
    rows.sort()
    with open(OUT, 'w', encoding='utf-8') as fh:
        for page, ref in rows:
            fh.write(f"{page}\t{ref}\n")
    print(f"Wrote {len(rows)} refs to {OUT}")


if __name__ == "__main__":
    main()

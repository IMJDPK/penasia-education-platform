import os
from pathlib import Path

WORKSPACE = "/home/imjd/Hong Kong University/Flask Website"
MANIFEST = os.path.join(WORKSPACE, "images3_manifest.txt")
DOC = os.path.join(WORKSPACE, "IMAGE_USAGE_FLOWCHART.md")

PAGE_MAP = {
    "1. Home": ["index.html"],
    "2. About us": ["about.html"],
    "3. Programs": ["courses.html", "course_detail.html", "course_detail_premium.html"],
    "5. Student life": ["student_life.html"],
    "6. Facilities": ["facilities.html"],
    "Extras": ["(extras)"]
}


def parse_manifest(path):
    items = []
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            p = line.strip()
            if not p:
                continue
            items.append(p)
    return items


def group_by_top_folder(items):
    grouped = {}
    for p in items:
        parts = Path(p).parts
        # find the segment that equals like "images 3.0" and take next part as top folder
        try:
            idx = [i for i, s in enumerate(parts) if s.lower().startswith("images 3.0")][0]
            top = parts[idx+1] if idx + 1 < len(parts) else "(root)"
        except IndexError:
            top = parts[-2] if len(parts) >= 2 else "(unknown)"
        grouped.setdefault(top, []).append(p)
    return grouped


def safe_id(s):
    return ''.join(ch if ch.isalnum() else '_' for ch in s)[:60]


def build_mermaid(grouped):
    lines = ["graph LR"]
    # Page nodes
    for top, pages in PAGE_MAP.items():
        for page in pages:
            pid = safe_id(page)
            lines.append(f"    {pid}[{page}]")
    # Asset nodes and edges
    for top, assets in grouped.items():
        pages = PAGE_MAP.get(top, ["(unknown)"])
        for asset in assets:
            base = os.path.basename(asset)
            aid = safe_id(base + "_" + top)
            lines.append(f"    {aid}[{top}: {base}]")
            for page in pages:
                pid = safe_id(page)
                lines.append(f"    {pid} --> {aid}")
    return "\n".join(lines)


def build_markdown(grouped):
    out = []
    out.append("\n## Images 3.0 → Pages Mapping (Auto-generated)\n")
    out.append("```mermaid\n" + build_mermaid(grouped) + "\n``""\n")
    for top, assets in grouped.items():
        pages = ', '.join(PAGE_MAP.get(top, ["(unknown)"]))
        out.append(f"- {top} → {pages}")
        for asset in assets:
            out.append(f"  - {asset}")
    out.append("\n")
    return "\n".join(out)


def append_to_doc(doc_path, content):
    with open(doc_path, "a", encoding="utf-8") as fh:
        fh.write(content)


def main():
    items = parse_manifest(MANIFEST)
    grouped = group_by_top_folder(items)
    content = build_markdown(grouped)
    append_to_doc(DOC, content)
    print("Updated:", DOC)


if __name__ == "__main__":
    main()

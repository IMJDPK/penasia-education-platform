import os
from pathlib import Path

WORKSPACE = "/home/imjd/Hong Kong University/Flask Website"
PLAN = os.path.join(WORKSPACE, "IMAGES3_REPLACEMENT_PLAN.md")
DOC = os.path.join(WORKSPACE, "IMAGE_USAGE_FLOWCHART.md")


def parse_plan(path):
    proposed = []
    gaps = []
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        if line.startswith('- '):
            # format: - page: ref → best (confidence=X, status=Y)
            status = 'gap' if 'status=gap' in line else ('proposed' if 'status=proposed' in line else None)
            if status == 'proposed':
                proposed.append(line)
            elif status == 'gap':
                gaps.append(line)
    return proposed, gaps


def annotate(doc_path, proposed, gaps):
    lines = []
    lines.append("\n## Coverage Summary (Images 3.0)\n")
    lines.append(f"- Proposed replacements: {len(proposed)}")
    lines.append(f"- Gaps: {len(gaps)}")
    lines.append("- Details: see IMAGES3_REPLACEMENT_PLAN.md for per-image mapping\n")
    # add sample few lines for easy scan
    lines.append("### Sample Proposed (top 10)\n")
    for s in proposed[:10]:
        lines.append(f"- {s}")
    lines.append("\n### Sample Gaps (top 10)\n")
    for s in gaps[:10]:
        lines.append(f"- {s}")
    with open(doc_path, 'a', encoding='utf-8') as fh:
        fh.write("\n".join(lines) + "\n")


def main():
    proposed, gaps = parse_plan(PLAN)
    annotate(DOC, proposed, gaps)
    print("Annotated coverage in:", DOC)


if __name__ == "__main__":
    main()

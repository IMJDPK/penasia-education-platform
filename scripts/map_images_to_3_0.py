import os
import re
from pathlib import Path

WORKSPACE = "/home/imjd/Hong Kong University/Flask Website"
REFS = os.path.join(WORKSPACE, "static_refs.txt")
MANIFEST = os.path.join(WORKSPACE, "images3_manifest.txt")
OUT = os.path.join(WORKSPACE, "IMAGES3_REPLACEMENT_PLAN.md")

PAGE_TOP = {
    "index.html": "1. Home",
    "about.html": "2. About us",
    "courses.html": "3. Programs",
    "course_detail.html": "3. Programs",
    "course_detail_premium.html": "3. Programs",
    "student_life.html": "5. Student life",
    "facilities.html": "6. Facilities",
}

KEYWORD_TARGETS = {
    # file keyword -> preferred images 3.0 filename prefix
    "campus-exterior": "1.1 (Home page)",
    "about-us-hero": "2.1",
    "about_02": "2.2",
    "courses_01": "3.1",
    "courses_03": "3.2",
    "classroom": "6.4 (Smart class room)",
    "facility-01": "6.2 (Professional training kitchen)",
    "facility-03": "6.5 (Learning resource centre)",
    "student-life-01": "5.1",
    "student-life-02": "5.2",
    "student-life-03": "5.3",
    "testimonials": None,
    "penasia-logo": None,
    "Penasia-Logo": None,
}


def read_manifest(path):
    items = []
    with open(path, 'r', encoding='utf-8') as fh:
        for line in fh:
            p = line.strip()
            if p:
                items.append(p)
    return items


def parse_refs(path):
    rows = []
    with open(path, 'r', encoding='utf-8') as fh:
        for line in fh:
            if not line.strip():
                continue
            page, ref = line.strip().split('\t', 1)
            rows.append((page, ref))
    return rows


def best_candidate(page, ref, manifest):
    top = PAGE_TOP.get(page)
    base = os.path.basename(ref)
    name_no_ext = os.path.splitext(base)[0].lower()

    # choose items under the top folder
    if top:
        candidates = [p for p in manifest if f"/{top}/" in p]
    else:
        candidates = manifest[:]

    # keyword mapping
    target_prefix = None
    for kw, tgt in KEYWORD_TARGETS.items():
        if kw in name_no_ext:
            target_prefix = tgt
            break

    score_items = []
    for p in candidates:
        base3 = os.path.basename(p).lower()
        score = 0
        if target_prefix and target_prefix.lower() in base3:
            score += 5
        # fuzzy score by shared tokens
        tokens = re.split(r"[^a-z0-9]+", name_no_ext)
        for t in tokens:
            if t and t in base3:
                score += 1
        # extra boost for numeric matching like 5.1 vs 5_1 in filename
        nums = re.findall(r"\d+", name_no_ext)
        for n in nums:
            if n in base3:
                score += 1
        score_items.append((score, p))

    score_items.sort(reverse=True)
    best = score_items[0][1] if score_items else None
    confidence = score_items[0][0] if score_items else 0
    return best, confidence


def generate_plan():
    manifest = read_manifest(MANIFEST)
    refs = parse_refs(REFS)
    lines = []
    lines.append("# Images 3.0 Replacement Plan\n")
    lines.append("This plan proposes replacements from 'images 3.0' for currently used static images by page.\n")
    lines.append("- Status: 'proposed' means candidate found; 'gap' means none or low confidence.\n")
    lines.append("\n")
    for page, ref in refs:
        best, conf = best_candidate(page, ref, manifest)
        status = "proposed" if best and conf >= 3 else "gap"
        lines.append(f"- {page}: {ref} → {best if best else '(none)'} (confidence={conf}, status={status})")
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write("\n".join(lines) + "\n")
    print("Wrote plan:", OUT)


if __name__ == "__main__":
    generate_plan()

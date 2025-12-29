import os
import shutil
import re
from pathlib import Path

WORKSPACE = "/home/imjd/Hong Kong University/Flask Website"
STATIC = os.path.join(WORKSPACE, "static")
TEMPLATES = os.path.join(WORKSPACE, "templates")
MANIFEST = os.path.join(WORKSPACE, "images3_manifest.txt")
LOG = os.path.join(WORKSPACE, "IMAGES3_APPLIED_CHANGES.md")

# Explicit, high-confidence mappings (current static ref -> images 3.0 source path)
MAPPINGS = {
    # About
    "images/about/about-us-hero.png": "2. About us/2.1.PNG",
    "images/about/about_02.jpg": "2. About us/2.2.png",
    # Courses
    "images/courses/courses_01.jpg": "3. Programs/3.1.png",
    "images/courses/courses_03.jpg": "3. Programs/3.2.png",
    # Facilities (University)
    "images/university/facility-01.jpg": "6. Facilities/6.2 (Professional training kitchen).png",
    "images/university/facility-03.jpg": "6. Facilities/6.5 (Learning resource centre).png",
    # Facilities (cards)
    "images/facilities/facility-01.png": "6. Facilities/6.2 (Professional training kitchen).png",
    # Student Life
    "images/university/student-life-01.jpg": "5. Student life/5.1.png",
    "images/university/student-life-02.jpg": "5. Student life/5.2 (State of the art facilities).png",
    "images/university/student-life-03.jpg": "5. Student life/5.3 (Collaborative spaces).png",
}

IMAGES3_BASE = "/home/imjd/Hong Kong University/assets/images 3.0"


def resolve_source(rel):
    src = os.path.join(IMAGES3_BASE, rel)
    if not os.path.isfile(src):
        raise FileNotFoundError(src)
    return src


def ensure_dir(path):
    d = os.path.dirname(path)
    os.makedirs(d, exist_ok=True)


def update_templates_ref(old_ref, new_ref):
    # Replace occurrences of old_ref in templates with new_ref
    changed_files = []
    for root, dirs, files in os.walk(TEMPLATES):
        for f in files:
            if not f.lower().endswith(('.html', '.htm')):
                continue
            fp = os.path.join(root, f)
            text = Path(fp).read_text(encoding='utf-8', errors='ignore')
            if old_ref in text and old_ref != new_ref:
                updated = text.replace(old_ref, new_ref)
                Path(fp).write_text(updated, encoding='utf-8')
                changed_files.append(os.path.relpath(fp, WORKSPACE))
    return changed_files


def apply_mapping():
    lines = []
    lines.append("# Images 3.0 Applied Changes (High-confidence)\n")
    for dest_rel, src_rel in MAPPINGS.items():
        src = resolve_source(src_rel)
        dest_static = os.path.join(STATIC, dest_rel)
        # Decide destination filename extension
        src_ext = os.path.splitext(src)[1].lower()
        dest_ext = os.path.splitext(dest_static)[1].lower()
        new_dest_rel = dest_rel
        new_dest_static = dest_static
        changed_templates = []
        if src_ext != dest_ext:
            # Change reference in templates to .png if source is .png
            new_dest_rel = re.sub(r"\.(jpg|jpeg)$", ".png", dest_rel, flags=re.IGNORECASE)
            new_dest_static = os.path.join(STATIC, new_dest_rel)
            changed_templates = update_templates_ref(dest_rel, new_dest_rel)
        ensure_dir(new_dest_static)
        shutil.copyfile(src, new_dest_static)
        lines.append(f"- {dest_rel} ← {src_rel} → saved as {new_dest_rel}")
        if changed_templates:
            lines.append(f"  - Updated templates: {', '.join(changed_templates)}")
    Path(LOG).write_text("\n".join(lines) + "\n", encoding='utf-8')
    print("Wrote log:", LOG)


if __name__ == "__main__":
    apply_mapping()

import os
import sys

BASE = "/home/imjd/Hong Kong University/assets/images 3.0"
OUT = "/home/imjd/Hong Kong University/Flask Website/images3_manifest.txt"


def main():
    if not os.path.isdir(BASE):
        print(f"ERROR: Missing path: {BASE}")
        try:
            parent = os.path.dirname(BASE)
            print("Parent listing:")
            for name in os.listdir(parent):
                print(" -", name)
        except Exception as e:
            print("Could not list parent:", e)
        sys.exit(1)

    items = []
    exts = {".png", ".jpg", ".jpeg", ".svg", ".gif"}
    for root, dirs, files in os.walk(BASE):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in exts:
                items.append(os.path.join(root, f))

    items.sort()
    with open(OUT, "w", encoding="utf-8") as fh:
        for p in items:
            fh.write(p + "\n")
    print(f"Wrote {len(items)} entries to {OUT}")


if __name__ == "__main__":
    main()

import os
import csv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
OUTPUT_CSV = os.path.join(PROJECT_ROOT, "data", "manifest.csv")

CLASSES = ["acnee", "eczeme"]

def generate_manifest():
    rows = []
    total = 0

    for cls in CLASSES:
        cls_dir = os.path.join(DATA_DIR, cls)

        if not os.path.isdir(cls_dir):
            print(f"[WARN] Folder lipsă: {cls_dir}")
            continue

        for fname in os.listdir(cls_dir):
            if fname.lower().endswith((".jpg", ".jpeg", ".png")):
                rows.append([
                    os.path.join("data", "processed", cls, fname),
                    cls
                ])
                total += 1

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["image_path", "label"])
        writer.writerows(rows)

    print("\n--- MANIFEST GENERAT ---")
    print(f"Fișier: {OUTPUT_CSV}")
    print(f"Total rânduri: {total}")

if __name__ == "__main__":
    generate_manifest()

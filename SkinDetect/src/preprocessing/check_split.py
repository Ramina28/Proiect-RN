import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TRAIN_DIR = os.path.join(PROJECT_ROOT, "data", "train")

CLASSES = ["acnee", "eczeme"]

print("\n--- VERIFICARE RAPIDĂ DATASET ---")

total = 0
for cls in CLASSES:
    cls_dir = os.path.join(TRAIN_DIR, cls)
    if not os.path.isdir(cls_dir):
        print(f"[EROARE] Folder lipsă: {cls_dir}")
        continue

    files = [f for f in os.listdir(cls_dir) if f.lower().endswith((".jpg",".jpeg",".png"))]
    print(f"Train {cls}: {len(files)} imagini")
    total += len(files)

print(f"\nTotal imagini în train: {total}")

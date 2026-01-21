import os
import csv
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")

os.makedirs(DOCS_DIR, exist_ok=True)

CLASSES = ["acnee", "eczeme"]

rows = []

for cls in CLASSES:
    cls_dir = os.path.join(DATA_DIR, cls)
    files = [f for f in os.listdir(cls_dir) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
    rows.append({"class": cls, "num_images": len(files)})

csv_path = os.path.join(DOCS_DIR, "data_statistics.csv")
pd.DataFrame(rows).to_csv(csv_path, index=False)

plt.figure()
plt.bar([r["class"] for r in rows], [r["num_images"] for r in rows])
plt.title("Distribuția imaginilor pe clase (data/processed)")
plt.xlabel("Clasă")
plt.ylabel("Număr imagini")
png_path = os.path.join(DOCS_DIR, "data_statistics.png")
plt.savefig(png_path)
plt.close()

log_path = os.path.join(DOCS_DIR, "data_log.txt")
with open(log_path, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(f"Clasa {r['class']}: {r['num_images']} imagini\n")

print("\n--- DOVEZI GENERATE ---")
print(f"CSV: {csv_path}")
print(f"Grafic: {png_path}")
print(f"Log: {log_path}")

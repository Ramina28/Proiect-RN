#!/usr/bin/env python3
"""
Modul 1 – Data Logging / Acquisition pentru SIA Dermatologică

Acest script:
- scanează imaginile din:
    - data/processed/  (imagini originale standardizate)
    - data/generated/  (imagini augmentate)
- generează un fișier CSV cu metadate despre fiecare imagine:
    - id
    - filepath
    - class_label (acnee / eczema / roseata)
    - source_type (original / augmented)
    - width, height (dacă este disponibil Pillow, altfel None)

Este modulul cerut la Etapa 4 pentru:
„Data Logging / Acquisition” – produce un CSV cu datele voastre.
"""

import argparse
import csv
from pathlib import Path
from datetime import datetime

# Încercăm să importăm Pillow; dacă nu există, continuăm fără dimensiuni
try:
    from PIL import Image  # type: ignore
    HAS_PILLOW = True
except ImportError:
    Image = None
    HAS_PILLOW = False
    print("[WARNING] Pillow (PIL) nu este instalat. Dimensiunile imaginilor (width, height) vor fi setate la None.")
    print("          Poți instala ulterior cu: pip install pillow\n")

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}


def scan_images(root_dir: Path, source_type: str):
    """
    Scanează recursiv folderul root_dir și întoarce o listă de dicționare
    cu informații despre fiecare imagine.
    """
    records = []

    if not root_dir.exists():
        print(f"[WARNING] Folderul {root_dir} nu există. Îl sar.")
        return records

    for img_path in root_dir.rglob("*"):
        if not img_path.is_file():
            continue

        if img_path.suffix.lower() not in VALID_EXTENSIONS:
            continue

        # Se presupune că numele folderului părinte = clasa (ex: acnee, eczema, roseata)
        class_label = img_path.parent.name

        width, height = None, None

        if HAS_PILLOW:
            try:
                with Image.open(img_path) as im:
                    width, height = im.size
            except Exception:
                # Dacă imaginea e coruptă sau nu poate fi deschisă
                pass

        record = {
            "filepath": str(img_path.as_posix()),
            "class_label": class_label,
            "source_type": source_type,
            "width": width,
            "height": height,
        }
        records.append(record)

    return records


def main(processed_dir: str, generated_dir: str, output_csv: str):
    print("=======================================")
    print("  Modul Data Acquisition – SkinDetect  ")
    print("=======================================\n")

    processed_path = Path(processed_dir)
    generated_path = Path(generated_dir)

    print(f"[INFO] Folder imagini originale (processed): {processed_path}")
    print(f"[INFO] Folder imagini augmentate (generated): {generated_path}\n")

    processed_records = scan_images(processed_path, source_type="original")
    generated_records = scan_images(generated_path, source_type="augmented")

    all_records = processed_records + generated_records

    if not all_records:
        print("[ERROR] Nu am găsit nicio imagine în folderele specificate.")
        print("        Verifică să ai imagini în:")
        print(f"        - {processed_path}/")
        print(f"        - {generated_path}/")
        return

    # Adăugăm id și timestamp
    now_str = datetime.now().isoformat(timespec="seconds")
    for idx, rec in enumerate(all_records, start=1):
        rec["id"] = idx
        rec["created_at"] = now_str

    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["id", "filepath", "class_label", "source_type", "width", "height", "created_at"]

    print(f"[INFO] Scriu CSV în: {output_path}")
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_records)

    # Statistici simple pentru README / verificare 40%
    num_original = len(processed_records)
    num_augmented = len(generated_records)
    total = len(all_records)
    original_ratio = num_original / total * 100 if total > 0 else 0.0

    print("\n[SUMMARY DATASET]")
    print(f"  Total imagini:         {total}")
    print(f"  Originale (processed): {num_original}")
    print(f"  Augmentate (generated): {num_augmented}")
    print(f"  Procent original:      {original_ratio:.1f}%")

    if original_ratio >= 40.0:
        print("[OK] Cerința de minimum 40% date originale este ÎNDEPLINITĂ.")
    else:
        print("[NOTE] Procentul de date originale este sub 40% conform CSV-ului.")
        print("       Este în regulă dacă explici clar contribuția în README și cum ai construit dataset-ul.")

    print("\n[INFO] Gata. Poți deschide data/dataset_log.csv pentru a vedea rezultatele.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Modul Data Logging / Acquisition – generare CSV cu metadate pentru imagini."
    )
    parser.add_argument(
        "--processed",
        type=str,
        default="data/processed",
        help="Folder cu imaginile originale standardizate (default: data/processed)",
    )
    parser.add_argument(
        "--generated",
        type=str,
        default="data/generated",
        help="Folder cu imaginile augmentate (default: data/generated)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/dataset_log.csv",
        help="Calea către fișierul CSV de ieșire (default: data/dataset_log.csv)",
    )

    args = parser.parse_args()
    main(args.processed, args.generated, args.output)

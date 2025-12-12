import os
from PIL import Image
import glob

# --- CONFIGURARE ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

INPUT_CLASSES = ["acnee", "eczeme", "rosacee"]

INPUT_BASE_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw')
OUTPUT_BASE_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')

RESIZE_WIDTH = 200

def process_images_with_pillow():

    if not os.path.exists(OUTPUT_BASE_DIR):
        os.makedirs(OUTPUT_BASE_DIR)
        print(f"[CREAT] {OUTPUT_BASE_DIR}")

    total_processed = 0

    for class_name in INPUT_CLASSES:
        print(f"\n[CLASĂ] {class_name}")

        input_folder_path = os.path.join(INPUT_BASE_DIR, class_name)
        output_folder_path = os.path.join(OUTPUT_BASE_DIR, class_name)
        os.makedirs(output_folder_path, exist_ok=True)

        image_paths = glob.glob(os.path.join(input_folder_path, "*.*"))

        for image_path in image_paths:
            try:
                img = Image.open(image_path).convert("RGB")

                w, h = img.size
                new_h = int((RESIZE_WIDTH / w) * h)
                resized = img.resize((RESIZE_WIDTH, new_h), Image.Resampling.LANCZOS)

                output_path = os.path.join(output_folder_path, os.path.basename(image_path))
                resized.save(output_path)

                total_processed += 1
                print(f"  ✔ saved: {output_path}")

            except Exception as e:
                print(f"  [Eroare] {image_path} → {e}")

    print(f"\n--- FINALIZAT (RESIZE) ---")
    print(f"Total imagini resize: {total_processed}")


if __name__ == "__main__":
    process_images_with_pillow()

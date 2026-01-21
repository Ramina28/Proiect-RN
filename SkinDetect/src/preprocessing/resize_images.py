import os
import glob
import shutil
from PIL import Image

# --- CONFIGURARE ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

INPUT_CLASSES = ["acnee", "eczeme"]

INPUT_BASE_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
OUTPUT_BASE_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

TARGET_SIZE = 200  # output final: 200x200


def reset_output_folder():
    """Șterge complet data/processed ca să evităm duplicate la rulări repetate."""
    if os.path.exists(OUTPUT_BASE_DIR):
        shutil.rmtree(OUTPUT_BASE_DIR)
        print(f"[ȘTERS] {OUTPUT_BASE_DIR}")
    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
    print(f"[CREAT] {OUTPUT_BASE_DIR}")


def list_images(folder_path: str):
    exts = (".jpg", ".jpeg", ".png")
    return [p for p in glob.glob(os.path.join(folder_path, "*")) if p.lower().endswith(exts)]


def resize_with_padding(img: Image.Image, target: int = 200) -> Image.Image:
    """
    Redimensionează păstrând proporțiile + padding până la target x target.
    Nu deformează imaginea.
    """
    w, h = img.size
    scale = target / max(w, h)
    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))

    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", (target, target), (0, 0, 0))  # padding negru
    left = (target - new_w) // 2
    top = (target - new_h) // 2
    canvas.paste(resized, (left, top))

    return canvas


def process_images_with_pillow():
    reset_output_folder()

    total_processed = 0
    total_errors = 0

    for class_name in INPUT_CLASSES:
        print(f"\n[CLASĂ] {class_name}")

        input_folder_path = os.path.join(INPUT_BASE_DIR, class_name)
        output_folder_path = os.path.join(OUTPUT_BASE_DIR, class_name)
        os.makedirs(output_folder_path, exist_ok=True)

        image_paths = list_images(input_folder_path)
        print(f"  imagini găsite în raw: {len(image_paths)}")

        for image_path in image_paths:
            try:
                img = Image.open(image_path).convert("RGB")

                # 200x200 fără deformare
                resized = resize_with_padding(img, TARGET_SIZE)

                # nume unic stabil (după numărul curent procesat)
                base = os.path.splitext(os.path.basename(image_path))[0]
                output_name = f"{base}_{total_processed}.png"
                output_path = os.path.join(output_folder_path, output_name)

                resized.save(output_path)
                total_processed += 1

            except Exception as e:
                total_errors += 1
                print(f"  [Eroare] {image_path} → {e}")

        print(f"  salvate în processed/{class_name}: {len(list_images(output_folder_path))}")

    print("\n--- FINALIZAT (RESIZE -> 200x200) ---")
    print(f"Total imagini procesate: {total_processed}")
    print(f"Total erori: {total_errors}")
    print(f"Output: {OUTPUT_BASE_DIR}")


if __name__ == "__main__":
    process_images_with_pillow()

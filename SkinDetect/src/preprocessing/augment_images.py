import os, glob, random
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

# --- CONFIGURARE ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

INPUT_CLASSES = ["acnee", "eczeme", "rosacee"]

INPUT_BASE_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')
OUTPUT_BASE_DIR = os.path.join(PROJECT_ROOT, 'data', 'generated')

N_AUG = 2  # cate augmentari per imagine

def add_noise(img):
    arr = np.array(img).astype(np.float32)
    noise = np.random.normal(0, 6, arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def augment(img):
    aug = img.copy()

    if random.random()<0.8: aug = ImageEnhance.Brightness(aug).enhance(random.uniform(0.85,1.2))
    if random.random()<0.8: aug = ImageEnhance.Contrast(aug).enhance(random.uniform(0.8,1.3))
    if random.random()<0.7: aug = ImageEnhance.Color(aug).enhance(random.uniform(0.9,1.3))
    if random.random()<0.4: aug = add_noise(aug)
    if random.random()<0.3: aug = aug.filter(ImageFilter.GaussianBlur(random.uniform(0.3,1.2)))

    return aug


def generate():
    if not os.path.exists(OUTPUT_BASE_DIR):
        os.makedirs(OUTPUT_BASE_DIR)

    total = 0

    for cls in INPUT_CLASSES:
        print(f"\n[Augmentez] clasa → {cls}")

        in_path = os.path.join(INPUT_BASE_DIR, cls)
        out_path = os.path.join(OUTPUT_BASE_DIR, cls)
        os.makedirs(out_path, exist_ok=True)

        for img_path in glob.glob(os.path.join(in_path,"*.*")):
            img = Image.open(img_path).convert("RGB")
            name, ext = os.path.splitext(os.path.basename(img_path))

            for i in range(N_AUG):
                new_img = augment(img)
                filename = f"{name}_aug{i+1}{ext}"
                new_img.save(os.path.join(out_path, filename))
                total +=1

                print(f"  + {filename}")

    print(f"\n--- FINALIZAT (AUGMENTARE) ---")
    print(f"Total imagini generate: {total}")


if __name__ == "__main__":
    generate()

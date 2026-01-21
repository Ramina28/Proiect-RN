import os
import glob
import random
import shutil
from io import BytesIO

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

# --- CONFIG ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

CLASSES = ["acnee", "eczeme"]

INPUT_BASE_DIR = os.path.join(PROJECT_ROOT, "data", "train")
OUTPUT_BASE_DIR = os.path.join(PROJECT_ROOT, "data", "train_generated")

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# câte imagini sintetice generezi per imagine din train
N_AUG_PER_IMAGE = 1

# dacă vrei să nu augmentăm toate imaginile, setează la ex. 0.6 (60% augmentate)
AUGMENT_FRACTION = 1.0

# ---------------- AUGMENT FUNCTIONS ----------------

def add_gaussian_noise(img: Image.Image) -> Image.Image:
    arr = np.array(img).astype(np.float32)
    sigma = random.uniform(2.0, 10.0)  # zgomot mic, realist
    noise = np.random.normal(0, sigma, arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def jpeg_compress(img: Image.Image) -> Image.Image:
    # simulează compresie de upload/WhatsApp
    quality = random.randint(35, 95)
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    buf.seek(0)
    return Image.open(buf).convert("RGB")

def vignette(img: Image.Image) -> Image.Image:
    # umbrire ușoară spre margini (iluminare neuniformă)
    arr = np.array(img).astype(np.float32)
    h, w = arr.shape[:2]
    y = np.linspace(-1, 1, h)
    x = np.linspace(-1, 1, w)
    yy, xx = np.meshgrid(y, x, indexing="ij")
    r = np.sqrt(xx * xx + yy * yy)

    strength = random.uniform(0.0, 0.35)
    mask = 1.0 - strength * np.clip(r, 0, 1)
    arr = arr * mask[..., None]
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def slight_rotate(img: Image.Image) -> Image.Image:
    # rotație foarte mică, realistă
    angle = random.uniform(-6, 6)
    return img.rotate(angle, resample=Image.Resampling.BICUBIC, expand=False)

def slight_translate(img: Image.Image) -> Image.Image:
    # mică translație (simulează încadrări diferite)
    w, h = img.size
    max_dx = int(0.04 * w)
    max_dy = int(0.04 * h)
    dx = random.randint(-max_dx, max_dx)
    dy = random.randint(-max_dy, max_dy)
    return img.transform(
        (w, h),
        Image.Transform.AFFINE,
        (1, 0, dx, 0, 1, dy),
        resample=Image.Resampling.BICUBIC,
    )

def color_jitter(img: Image.Image) -> Image.Image:
    out = img
    if random.random() < 0.9:
        out = ImageEnhance.Brightness(out).enhance(random.uniform(0.85, 1.15))
    if random.random() < 0.9:
        out = ImageEnhance.Contrast(out).enhance(random.uniform(0.85, 1.2))
    if random.random() < 0.7:
        out = ImageEnhance.Color(out).enhance(random.uniform(0.9, 1.2))
    return out

def blur_or_defocus(img: Image.Image) -> Image.Image:
    if random.random() < 0.35:
        radius = random.uniform(0.3, 1.2)
        return img.filter(ImageFilter.GaussianBlur(radius))
    return img

def augment_one(img: Image.Image) -> Image.Image:
    aug = img.copy()

    # pipeline realist: încadrări -> culoare -> iluminare -> zgomot/blur -> compresie
    if random.random() < 0.4:
        aug = slight_translate(aug)
    if random.random() < 0.35:
        aug = slight_rotate(aug)

    aug = color_jitter(aug)

    if random.random() < 0.35:
        aug = vignette(aug)

    if random.random() < 0.4:
        aug = add_gaussian_noise(aug)

    aug = blur_or_defocus(aug)

    if random.random() < 0.6:
        aug = jpeg_compress(aug)

    return aug

# ---------------- PIPELINE ----------------

def reset_output():
    if os.path.exists(OUTPUT_BASE_DIR):
        shutil.rmtree(OUTPUT_BASE_DIR)
        print(f"[ȘTERS] {OUTPUT_BASE_DIR}")

def ensure_dirs():
    for cls in CLASSES:
        os.makedirs(os.path.join(OUTPUT_BASE_DIR, cls), exist_ok=True)

def list_images(folder):
    exts = (".jpg", ".jpeg", ".png")
    return [p for p in glob.glob(os.path.join(folder, "*")) if p.lower().endswith(exts)]

def generate():
    reset_output()
    ensure_dirs()

    total = 0
    kept = 0

    for cls in CLASSES:
        in_dir = os.path.join(INPUT_BASE_DIR, cls)
        out_dir = os.path.join(OUTPUT_BASE_DIR, cls)

        paths = list_images(in_dir)
        print(f"\n[CLASĂ] {cls} | train imagini: {len(paths)}")

        for img_path in paths:
            if random.random() > AUGMENT_FRACTION:
                continue

            try:
                img = Image.open(img_path).convert("RGB")
            except Exception as e:
                print(f"  [Eroare citire] {img_path} → {e}")
                continue

            base = os.path.splitext(os.path.basename(img_path))[0]

            for i in range(N_AUG_PER_IMAGE):
                aug = augment_one(img)
                out_name = f"{base}_syn{i+1}.png"
                out_path = os.path.join(out_dir, out_name)
                aug.save(out_path)
                total += 1

            kept += 1

        print(f"  augmentate din clasă: {kept} (cumulat)")

    print("\n--- FINALIZAT (AUGMENTARE TRAIN) ---")
    print(f"Total imagini generate: {total}")
    print(f"Output: {OUTPUT_BASE_DIR}")

if __name__ == "__main__":
    generate()

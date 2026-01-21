import os
import random
import shutil
from sklearn.model_selection import train_test_split

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

CLASSES = ["acnee", "eczeme"]

INPUT_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
OUTPUT_BASE = os.path.join(PROJECT_ROOT, "data")

TRAIN_DIR = os.path.join(OUTPUT_BASE, "train")
VAL_DIR   = os.path.join(OUTPUT_BASE, "validation")
TEST_DIR  = os.path.join(OUTPUT_BASE, "test")

SEED = 42
random.seed(SEED)

TRAIN_RATIO = 0.7
VAL_RATIO   = 0.15
TEST_RATIO  = 0.15

def prepare_folders():
    for base in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        os.makedirs(base, exist_ok=True)
        for cls in CLASSES:
            os.makedirs(os.path.join(base, cls), exist_ok=True)

def split_and_copy():
    prepare_folders()

    for cls in CLASSES:
        print(f"\n[CLASA] {cls}")
        cls_dir = os.path.join(INPUT_DIR, cls)
        images = [f for f in os.listdir(cls_dir) if f.lower().endswith(('.jpg','.jpeg','.png'))]

        train_files, temp_files = train_test_split(
            images,
            test_size=(1 - TRAIN_RATIO),
            random_state=SEED,
            shuffle=True
        )

        val_files, test_files = train_test_split(
            temp_files,
            test_size=TEST_RATIO / (VAL_RATIO + TEST_RATIO),
            random_state=SEED,
            shuffle=True
        )

        print(f"  train: {len(train_files)}")
        print(f"  val:   {len(val_files)}")
        print(f"  test:  {len(test_files)}")

        for fname in train_files:
            shutil.copy(os.path.join(cls_dir, fname), os.path.join(TRAIN_DIR, cls, fname))
        for fname in val_files:
            shutil.copy(os.path.join(cls_dir, fname), os.path.join(VAL_DIR, cls, fname))
        for fname in test_files:
            shutil.copy(os.path.join(cls_dir, fname), os.path.join(TEST_DIR, cls, fname))

    print("\n--- SPLIT FINALIZAT ---")

if __name__ == "__main__":
    split_and_copy()

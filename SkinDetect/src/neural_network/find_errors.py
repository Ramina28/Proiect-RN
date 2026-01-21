import os
import shutil
import numpy as np
import tensorflow as tf
from sklearn.metrics import confusion_matrix

# --- CONFIGURARE ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TEST_DIR = os.path.join(PROJECT_ROOT, "data", "test")
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "best_model.h5") # Sau trained_model.h5
OUTPUT_ERROR_DIR = os.path.join(PROJECT_ROOT, "docs", "error_examples")

IMG_SIZE = (200, 200)
BATCH_SIZE = 16
CLASS_NAMES = ["acnee", "eczeme"]

def main():
    if not os.path.exists(MODEL_PATH):
        print(f"[EROARE] Nu găsesc modelul: {MODEL_PATH}")
        return

    # Curățăm folderul de erori vechi
    if os.path.exists(OUTPUT_ERROR_DIR):
        shutil.rmtree(OUTPUT_ERROR_DIR)
    os.makedirs(OUTPUT_ERROR_DIR, exist_ok=True)

    print("--- Încărcare model și date ---")
    model = tf.keras.models.load_model(MODEL_PATH)

    # Încărcăm datele FĂRĂ shuffle ca să putem potrivi numele fișierelor cu predicțiile
    test_ds = tf.keras.utils.image_dataset_from_directory(
        TEST_DIR,
        labels="inferred",
        label_mode="int",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False 
    )

    # Obținem căile fișierelor (în ordinea încărcării)
    file_paths = test_ds.file_paths

    # Prezicem
    print("--- Generare predicții ---")
    # Normalizare manuală (dacă modelul nu are strat de rescale inclus, 
    # dar aici îl aplicăm ca în train.py)
    normalization_layer = tf.keras.layers.Rescaling(1./255)
    
    all_preds = []
    all_labels = []

    for images, labels in test_ds:
        images = normalization_layer(images) # Normalizăm
        probs = model.predict(images, verbose=0)
        preds = np.argmax(probs, axis=1)
        
        all_preds.extend(preds)
        all_labels.extend(labels.numpy())

    # Găsim erorile
    errors_found = 0
    print("\n--- ANALIZĂ ERORI ---")
    
    print(f"{'Fișier':<40} | {'Real':<10} | {'Predicție':<10}")
    print("-" * 70)

    for i in range(len(file_paths)):
        true_idx = all_labels[i]
        pred_idx = all_preds[i]

        if true_idx != pred_idx:
            errors_found += 1
            filename = os.path.basename(file_paths[i])
            src_path = file_paths[i]
            
            # Copiem imaginea greșită în docs pentru analiză
            # Numele va fi: pred_CLASA_real_CLASA_numeoriginal.jpg
            dst_name = f"pred_{CLASS_NAMES[pred_idx]}_real_{CLASS_NAMES[true_idx]}_{filename}"
            dst_path = os.path.join(OUTPUT_ERROR_DIR, dst_name)
            shutil.copy(src_path, dst_path)

            print(f"{filename:<40} | {CLASS_NAMES[true_idx]:<10} | {CLASS_NAMES[pred_idx]:<10}")

            if errors_found >= 5:
                break

    print(f"\n[OK] Am salvat primele 5 erori în folderul: {OUTPUT_ERROR_DIR}")
    print("Deschide imaginile din acel folder și descrie-le în README!")

if __name__ == "__main__":
    main()
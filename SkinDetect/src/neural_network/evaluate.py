import os
import json
import numpy as np
import tensorflow as tf
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
from sklearn.metrics import precision_score, recall_score
import matplotlib.pyplot as plt

# --- CONFIGURARE CĂI ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 1. Căutare Inteligentă a Datelor de Test
# Ordine preferință: processed/test -> raw/test -> processed/val (fallback)
paths_to_check = [
    os.path.join(PROJECT_ROOT, "data", "processed", "test"),
    os.path.join(PROJECT_ROOT, "data", "test"),
    os.path.join(PROJECT_ROOT, "data", "processed", "val"),
    os.path.join(PROJECT_ROOT, "data", "validation")
]

TEST_DIR = None
for p in paths_to_check:
    if os.path.exists(p):
        TEST_DIR = p
        break

if TEST_DIR is None:
    raise FileNotFoundError("Nu am găsit niciun folder de test sau validare (test/val/validation)!")

print(f"[INFO] Evaluarea se face pe datele din: {TEST_DIR}")

# 2. Modelul Optimizat
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "optimized_model.h5")

# 3. Output-uri pentru Documentație
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
DOCS_RES_DIR = os.path.join(PROJECT_ROOT, "docs", "results")

CONF_MAT_PATH = os.path.join(DOCS_RES_DIR, "confusion_matrix_optimized.png")
METRICS_PATH = os.path.join(RESULTS_DIR, "final_metrics.json")

# 4. Parametri (Trebuie să fie IDENTICI cu cei de la antrenare)
IMG_SIZE = (224, 224) 
BATCH_SIZE = 16
CLASS_NAMES = ["Acnee", "Eczeme"]

def main():
    # Creare foldere output
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(DOCS_RES_DIR, exist_ok=True)

    # Verificare Model
    if not os.path.exists(MODEL_PATH):
        # Fallback: Dacă nu există optimized, căutăm best_model
        fallback = os.path.join(PROJECT_ROOT, "models", "best_model.h5")
        if os.path.exists(fallback):
            print(f"[WARN] Nu am găsit optimized_model.h5. Folosesc {fallback}")
            MODEL_PATH_LOAD = fallback
        else:
            raise FileNotFoundError(f"Nu există modelul antrenat la: {MODEL_PATH}")
    else:
        MODEL_PATH_LOAD = MODEL_PATH

    print(f"[INFO] Se încarcă modelul: {MODEL_PATH_LOAD}")
    model = tf.keras.models.load_model(MODEL_PATH_LOAD)

    # Încărcare Dataset
    try:
        test_ds = tf.keras.utils.image_dataset_from_directory(
            TEST_DIR,
            labels="inferred",
            label_mode="int",
            image_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            shuffle=False, # IMPORTANT: Nu amesteca, pentru a putea compara cu etichetele reale
            interpolation='nearest' # Similar cu ImageDataGenerator
        )
    except Exception as e:
        print(f"[EROARE] Nu am putut încărca imaginile: {e}")
        return

    # Normalizare (trebuie să fie la fel ca la antrenare: 1/255)
    normalization_layer = tf.keras.layers.Rescaling(1./255)

    y_true = []
    y_pred = []
    prob_list = []

    print("[INFO] Se rulează predicțiile...")
    for batch_imgs, batch_labels in test_ds:
        # Aplicăm normalizarea manual
        batch_imgs_norm = normalization_layer(batch_imgs)
        
        probs = model.predict(batch_imgs_norm, verbose=0)
        preds = np.argmax(probs, axis=1)

        y_true.extend(batch_labels.numpy().tolist())
        y_pred.extend(preds.tolist())
        prob_list.extend(probs.tolist())

    # Calcul Metrici
    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average="macro")
    precision = precision_score(y_true, y_pred, average="macro")
    recall = recall_score(y_true, y_pred, average="macro")

    # Matricea de Confuzie
    cm = confusion_matrix(y_true, y_pred)

    # Plotare Matrice Confuzie (Professional Style)
    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(f"Confusion Matrix (Acc: {acc*100:.1f}%)", fontsize=14)
    plt.colorbar()
    
    # Etichete axe
    tick_marks = np.arange(len(CLASS_NAMES))
    plt.xticks(tick_marks, CLASS_NAMES, rotation=0, fontsize=12)
    plt.yticks(tick_marks, CLASS_NAMES, fontsize=12)

    # Text în căsuțe
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], 'd'),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black",
                     fontsize=14, fontweight='bold')

    plt.ylabel('Etichetă Reală (True)', fontsize=12)
    plt.xlabel('Predicție Model (Predicted)', fontsize=12)
    plt.tight_layout()
    plt.savefig(CONF_MAT_PATH, dpi=150)
    plt.close()

    # Raport Detaliat (pentru JSON)
    report_dict = classification_report(y_true, y_pred, target_names=CLASS_NAMES, output_dict=True)

    metrics_data = {
        "model_name": os.path.basename(MODEL_PATH_LOAD),
        "accuracy": float(acc),
        "f1_score": float(f1),
        "precision": float(precision),
        "recall": float(recall),
        "confusion_matrix": cm.tolist(),
        "classification_report": report_dict
    }

    # Salvare JSON Final
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, indent=4)

    # Output Consolă
    print("-" * 30)
    print("   REZULTATE EVALUARE FINALĂ   ")
    print("-" * 30)
    print(f"Model: {os.path.basename(MODEL_PATH_LOAD)}")
    print(f"Accuracy:  {acc*100:.2f}%")
    print(f"F1-Score:  {f1*100:.2f}%")
    print("-" * 30)
    print(f"[OK] Grafic salvat: {CONF_MAT_PATH}")
    print(f"[OK] Raport JSON:   {METRICS_PATH}")

if __name__ == "__main__":
    main()
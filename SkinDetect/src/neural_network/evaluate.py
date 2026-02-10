import os
import json
import argparse
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    confusion_matrix,
    classification_report,
)

# ============================================================
# evaluate.py — Evaluare model + confusion matrix + analiza erori
# ------------------------------------------------------------
# Default:
#   - evaluează models/optimized_model.h5
#   - caută automat un folder de test/val
#   - salvează:
#       docs/confusion_matrix_optimized.png
#       results/final_metrics.json
#       results/error_analysis.json (Top 5 erori)
#
# Opțional:
#   --model <path>     evaluează alt model (.h5/.keras)
#   --detailed         printează și classification_report în consolă
# ============================================================

# --- CONFIGURARE CĂI ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Căutare inteligentă a datelor de test/val
PATHS_TO_CHECK = [
    os.path.join(PROJECT_ROOT, "data", "processed", "test"),
    os.path.join(PROJECT_ROOT, "data", "test"),
    os.path.join(PROJECT_ROOT, "data", "processed", "val"),
    os.path.join(PROJECT_ROOT, "data", "validation"),
]
TEST_DIR = next((p for p in PATHS_TO_CHECK if os.path.exists(p)), None)
if TEST_DIR is None:
    raise FileNotFoundError("Nu am găsit niciun folder de test sau validare!")

# Output-uri (aliniate cu README-ul cerut)
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")

CONF_MAT_PATH = os.path.join(DOCS_DIR, "confusion_matrix_optimized.png")
METRICS_PATH = os.path.join(RESULTS_DIR, "final_metrics.json")
ERRORS_PATH = os.path.join(RESULTS_DIR, "error_analysis.json")

# Parametri (aceiași ca la antrenare)
IMG_SIZE = (200, 200)
BATCH_SIZE = 16


def _resolve_model_path(model_arg: str | None) -> str:
    """
    Returnează calea absolută către model.
    Dacă utilizatorul nu dă --model, folosim models/optimized_model.h5.
    """
    default_model = os.path.join(PROJECT_ROOT, "models", "optimized_model.h5")
    model_path = model_arg or default_model

    # acceptă atât absolut cât și relativ la root proiect
    if not os.path.isabs(model_path):
        model_path = os.path.join(PROJECT_ROOT, model_path)

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelul nu există: {model_path}")

    return model_path


def _plot_confusion_matrix(cm: np.ndarray, class_names: list[str], title: str, out_path: str) -> None:
    """Salvează confusion matrix ca imagine PNG."""
    plt.figure(figsize=(6, 5))
    plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.title(title)
    plt.colorbar()

    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=0)
    plt.yticks(tick_marks, class_names)

    thresh = cm.max() / 2.0 if cm.size else 0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(
                j, i, int(cm[i, j]),
                horizontalalignment="center",
                color="white" if cm[i, j] > thresh else "black",
                fontsize=12,
                fontweight="bold",
            )

    plt.ylabel("Etichetă reală")
    plt.xlabel("Predicție")
    plt.tight_layout()

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Evaluează un model CNN și salvează metrici + confusion matrix.")
    parser.add_argument("--model", type=str, default=None, help="Cale către model (.h5/.keras). Default: models/optimized_model.h5")
    parser.add_argument("--detailed", action="store_true", help="Afișează classification_report complet în consolă.")
    args = parser.parse_args()

    model_path = _resolve_model_path(args.model)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(DOCS_DIR, exist_ok=True)

    print(f"[INFO] Evaluarea se face pe: {TEST_DIR}")
    print(f"[INFO] Se încarcă modelul: {model_path}")

    # Încărcare model
    model = tf.keras.models.load_model(model_path)

    # Încărcare dataset FĂRĂ shuffle ca să păstrăm ordinea file_paths
    test_ds = tf.keras.utils.image_dataset_from_directory(
        TEST_DIR,
        labels="inferred",
        label_mode="int",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False,
    )

    # Obținem numele claselor din dataset (ordinea reală a folderelor)
    class_names = list(getattr(test_ds, "class_names", [])) or ["class_0", "class_1"]

    # Normalizare identică cu train/evaluate (dacă modelul nu include Rescaling)
    normalization_layer = tf.keras.layers.Rescaling(1.0 / 255)

    y_true: list[int] = []
    y_pred: list[int] = []
    confidences: list[float] = []
    probs_all: list[list[float]] = []

    print("[INFO] Rulez predicțiile...")

    for batch_imgs, batch_labels in test_ds:
        batch_imgs = normalization_layer(batch_imgs)
        probs = model.predict(batch_imgs, verbose=0)
        preds = np.argmax(probs, axis=1)
        conf = np.max(probs, axis=1)

        y_true.extend(batch_labels.numpy().tolist())
        y_pred.extend(preds.tolist())
        confidences.extend(conf.tolist())
        probs_all.extend(probs.tolist())

    # Metrici globale
    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average="macro")
    precision = precision_score(y_true, y_pred, average="macro")
    recall = recall_score(y_true, y_pred, average="macro")
    cm = confusion_matrix(y_true, y_pred)

    # Confusion matrix PNG
    _plot_confusion_matrix(
        cm=cm,
        class_names=[cn.capitalize() for cn in class_names],
        title=f"Confusion Matrix (Acc: {acc:.4f})",
        out_path=CONF_MAT_PATH,
    )

    # classification_report în JSON
    report_dict = classification_report(
        y_true,
        y_pred,
        target_names=[cn.capitalize() for cn in class_names],
        output_dict=True,
        zero_division=0,
    )

    metrics_data = {
        "model_name": os.path.basename(model_path),
        "test_dir": TEST_DIR,
        "img_size": list(IMG_SIZE),
        "batch_size": BATCH_SIZE,
        "accuracy": float(acc),
        "f1_score_macro": float(f1),
        "precision_macro": float(precision),
        "recall_macro": float(recall),
        "confusion_matrix": cm.tolist(),
        "classification_report": report_dict,
    }

    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, indent=4, ensure_ascii=False)

    # =========================================================
    # Analiza Top 5 erori (REALĂ) → results/error_analysis.json
    # =========================================================
    file_paths = getattr(test_ds, "file_paths", [])
    errors = []

    n = min(len(file_paths), len(y_true), len(y_pred), len(confidences), len(probs_all))
    for i in range(n):
        t = int(y_true[i])
        p = int(y_pred[i])
        if t != p:
            probs_vec = probs_all[i]
            probs_map = {class_names[j]: float(probs_vec[j]) for j in range(min(len(class_names), len(probs_vec)))}

            errors.append(
                {
                    "index": i,
                    "file_path": file_paths[i],
                    "file_name": os.path.basename(file_paths[i]),
                    "true_idx": t,
                    "true_label": class_names[t] if t < len(class_names) else str(t),
                    "pred_idx": p,
                    "pred_label": class_names[p] if p < len(class_names) else str(p),
                    "confidence": float(confidences[i]),
                    "probs": probs_map,
                }
            )

    errors_sorted = sorted(errors, key=lambda e: e.get("confidence", 0.0), reverse=True)
    top5 = errors_sorted[:5]

    error_payload = {
        "model_name": os.path.basename(model_path),
        "test_dir": TEST_DIR,
        "num_samples": int(n),
        "num_errors": int(len(errors)),
        "top_k": 5,
        "top_errors": top5,
    }

    with open(ERRORS_PATH, "w", encoding="utf-8") as f:
        json.dump(error_payload, f, indent=4, ensure_ascii=False)

    # Print output “în stil README”
    print("\n----- REZULTATE EVALUARE -----")
    print(f"Test Accuracy: {acc:.4f}")
    print(f"Test F1-score (macro): {f1:.4f}")

    print(f"✓ Confusion matrix saved to docs/confusion_matrix_optimized.png")
    print(f"✓ Metrics saved to results/final_metrics.json")
    print(f"✓ Top 5 errors analysis saved to results/error_analysis.json")

    if args.detailed:
        print("\n----- CLASSIFICATION REPORT -----")
        print(
            classification_report(
                y_true,
                y_pred,
                target_names=[cn.capitalize() for cn in class_names],
                zero_division=0,
            )
        )


if __name__ == "__main__":
    main()

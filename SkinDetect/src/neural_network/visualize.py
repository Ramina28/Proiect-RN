import os
import json
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# visualize.py — ACADEMIC CORECT (REAL, din JSON + CSV)
# Rulează:
#   python src/neural_network/visualize.py --all
#
# Generează (CERINȚA):
# - docs/results/metrics_evolution.png
# - docs/results/learning_curves_final.png
# - docs/optimization/accuracy_comparison.png
# - docs/optimization/f1_comparison.png
# ============================================================

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
DOCS_RESULTS_DIR = os.path.join(PROJECT_ROOT, "docs", "results")
DOCS_OPT_DIR = os.path.join(PROJECT_ROOT, "docs", "optimization")

os.makedirs(DOCS_RESULTS_DIR, exist_ok=True)
os.makedirs(DOCS_OPT_DIR, exist_ok=True)

# Fișiere reale (după cum ai acum în results/)
HISTORY_CSV = os.path.join(RESULTS_DIR, "optimization_history.csv")

METRICS_BASELINE = os.path.join(RESULTS_DIR, "final_metrics_baseline.json")
METRICS_OPTIMIZED = os.path.join(RESULTS_DIR, "final_metrics_optimized.json")

# Output cerut
OUT_METRICS_EVOLUTION = os.path.join(DOCS_RESULTS_DIR, "metrics_evolution.png")
OUT_LEARNING_CURVES = os.path.join(DOCS_RESULTS_DIR, "learning_curves_final.png")
OUT_ACC_COMP = os.path.join(DOCS_OPT_DIR, "accuracy_comparison.png")
OUT_F1_COMP = os.path.join(DOCS_OPT_DIR, "f1_comparison.png")


def load_metrics(path: str) -> dict:
    """
    În JSON-urile tale cheile sunt:
      accuracy, f1_score, precision, recall
    (care corespund macro avg din classification_report)
    """
    with open(path, "r", encoding="utf-8") as f:
        m = json.load(f)

    acc = float(m.get("accuracy", np.nan))
    f1 = float(m.get("f1_score", np.nan))
    prec = float(m.get("precision", np.nan))
    rec = float(m.get("recall", np.nan))

    return {
        "model_name": m.get("model_name", os.path.basename(path)),
        "accuracy": acc,
        "f1": f1,
        "precision": prec,
        "recall": rec,
    }


def assert_finite(name: str, value: float, path: str):
    if not np.isfinite(value):
        raise ValueError(
            f"[EROARE] {name} este NaN în {path}. "
            f"Verifică fișierul și cheile: accuracy, f1_score, precision, recall."
        )


def bar_plot(title: str, labels: list[str], values_percent: list[float], out_path: str, ylim=(0, 100)) -> None:
    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, values_percent)
    plt.title(title, fontsize=14)
    plt.ylabel("Procent (%)")
    plt.ylim(*ylim)
    plt.grid(axis="y", linestyle="--", alpha=0.3)

    for b in bars:
        h = b.get_height()
        plt.text(b.get_x() + b.get_width() / 2, h + 1, f"{h:.1f}%", ha="center", fontweight="bold")

    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"[OK] Generat: {out_path}")


def plot_metrics_evolution(metrics_opt_path: str, out_path: str) -> None:
    """
    metrics_evolution.png — 4 bare reale (Accuracy/F1/Precision/Recall)
    pentru modelul optimizat.
    """
    m = load_metrics(metrics_opt_path)

    assert_finite("accuracy", m["accuracy"], metrics_opt_path)
    assert_finite("f1_score", m["f1"], metrics_opt_path)
    assert_finite("precision", m["precision"], metrics_opt_path)
    assert_finite("recall", m["recall"], metrics_opt_path)

    names = ["Accuracy", "F1 (macro)", "Precision (macro)", "Recall (macro)"]
    vals = [
        m["accuracy"] * 100,
        m["f1"] * 100,
        m["precision"] * 100,
        m["recall"] * 100,
    ]

    plt.figure(figsize=(10, 5))
    bars = plt.bar(names, vals)
    plt.title("Metrici Finale - Model Optimizat", fontsize=14)
    plt.ylabel("Procent (%)")
    plt.ylim(0, 100)
    plt.grid(axis="y", linestyle="--", alpha=0.3)

    for b in bars:
        h = b.get_height()
        plt.text(b.get_x() + b.get_width() / 2, h + 1, f"{h:.1f}%", ha="center", fontweight="bold")

    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"[OK] Generat: {out_path}")


def plot_learning_curves(history_csv: str, out_path: str) -> None:
    """
    learning_curves_final.png — curbe reale din results/optimization_history.csv
    """
    df = pd.read_csv(history_csv)

    required = ["accuracy", "val_accuracy", "loss", "val_loss"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(
            f"Lipsesc coloane în {history_csv}: {missing}. "
            f"Coloane găsite: {list(df.columns)}"
        )

    epochs = np.arange(1, len(df) + 1)

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(epochs, df["accuracy"], label="Train Accuracy", linewidth=2)
    plt.plot(epochs, df["val_accuracy"], label="Val Accuracy", linewidth=2)
    plt.title("Acuratețe vs Epoci")
    plt.xlabel("Epoca")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.plot(epochs, df["loss"], label="Train Loss", linewidth=2)
    plt.plot(epochs, df["val_loss"], label="Val Loss", linewidth=2)
    plt.title("Loss vs Epoci")
    plt.xlabel("Epoca")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"[OK] Generat: {out_path}")


def plot_comparisons(baseline_path: str, optimized_path: str, out_acc: str, out_f1: str) -> None:
    """
    accuracy_comparison.png + f1_comparison.png — comparație REALĂ baseline vs optimized
    """
    b = load_metrics(baseline_path)
    o = load_metrics(optimized_path)

    assert_finite("baseline accuracy", b["accuracy"], baseline_path)
    assert_finite("optimized accuracy", o["accuracy"], optimized_path)
    assert_finite("baseline f1_score", b["f1"], baseline_path)
    assert_finite("optimized f1_score", o["f1"], optimized_path)

    labels = ["Baseline", "Optimized"]

    bar_plot(
        "Accuracy Comparison",
        labels,
        [b["accuracy"] * 100, o["accuracy"] * 100],
        out_acc,
    )

    bar_plot(
        "F1 (macro) Comparison",
        labels,
        [b["f1"] * 100, o["f1"] * 100],
        out_f1,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="Generează toate vizualizările")
    args = parser.parse_args()

    if not args.all:
        print("Rulează cu: python src/neural_network/visualize.py --all")
        return

    print("\n--- VISUALIZE (ACADEMIC, REAL) ---")
    print(f"[INFO] PROJECT_ROOT: {PROJECT_ROOT}")

    if not os.path.exists(METRICS_OPTIMIZED):
        raise FileNotFoundError(f"Lipsește: {METRICS_OPTIMIZED}")
    if not os.path.exists(METRICS_BASELINE):
        raise FileNotFoundError(f"Lipsește: {METRICS_BASELINE}")
    if not os.path.exists(HISTORY_CSV):
        raise FileNotFoundError(
            f"Lipsește: {HISTORY_CSV}\n"
            f"Rulează: python src/neural_network/train_optimized.py"
        )

    # 1) metrics_evolution.png
    plot_metrics_evolution(METRICS_OPTIMIZED, OUT_METRICS_EVOLUTION)

    # 2) learning_curves_final.png
    plot_learning_curves(HISTORY_CSV, OUT_LEARNING_CURVES)

    # 3) accuracy_comparison.png + f1_comparison.png
    plot_comparisons(METRICS_BASELINE, METRICS_OPTIMIZED, OUT_ACC_COMP, OUT_F1_COMP)

    print("\n--- GATA! ---")


if __name__ == "__main__":
    main()

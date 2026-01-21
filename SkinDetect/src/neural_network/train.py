import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from model import build_cnn, compile_model, ModelConfig

import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "validation")

MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")

TRAINED_MODEL_OUT = os.path.join(MODELS_DIR, "trained_model.h5")
BEST_MODEL_OUT = os.path.join(MODELS_DIR, "best_model.h5")

BATCH_SIZE = 16
EPOCHS = 30

def plot_loss_curve(history, out_path):
    plt.figure()
    plt.plot(history["loss"], label="loss")
    plt.plot(history["val_loss"], label="val_loss")
    plt.title("Loss vs Val Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def main():
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(DOCS_DIR, exist_ok=True)

    # --- Model ---
    config = ModelConfig(num_classes=2)
    model = compile_model(build_cnn(config), config)

    # --- Data Generators (Nivel 2: augmentare relevantă) ---
    train_gen = ImageDataGenerator(
        rescale=1./255,
        brightness_range=(0.8, 1.2),     # iluminare
        zoom_range=0.08,                # zoom mic
        width_shift_range=0.05,         # shift mic
        height_shift_range=0.05,        # shift mic
        shear_range=0.05,               # deformare mică (similar "perspective-ish")
        horizontal_flip=False           # pentru piele nu e obligatoriu; evităm flip agresiv
    )

    val_gen = ImageDataGenerator(rescale=1./255)

    train_data = train_gen.flow_from_directory(
        TRAIN_DIR,
        target_size=(200, 200),
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        shuffle=True
    )

    val_data = val_gen.flow_from_directory(
        VAL_DIR,
        target_size=(200, 200),
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        shuffle=False
    )

    # --- Callbacks (Nivel 2) ---
    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    )

    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=2,
        min_lr=1e-6,
        verbose=1
    )

    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        BEST_MODEL_OUT,
        monitor="val_loss",
        save_best_only=True,
        verbose=1
    )

    # --- Train ---
    history = model.fit(
        train_data,
        epochs=EPOCHS,
        validation_data=val_data,
        callbacks=[early_stop, reduce_lr, checkpoint]
    )

    # --- Save trained model (final) ---
    model.save(TRAINED_MODEL_OUT)
    print(f"\n[OK] Model antrenat salvat: {TRAINED_MODEL_OUT}")
    print(f"[OK] Best model (checkpoint) salvat: {BEST_MODEL_OUT}")

    # --- Save history CSV ---
    hist_path = os.path.join(RESULTS_DIR, "training_history.csv")
    pd.DataFrame(history.history).to_csv(hist_path, index=False)
    print(f"[OK] Training history salvat: {hist_path}")

    # --- Plot loss curve ---
    loss_curve_path = os.path.join(DOCS_DIR, "loss_curve.png")
    plot_loss_curve(history.history, loss_curve_path)
    print(f"[OK] Grafic loss/val_loss salvat: {loss_curve_path}")

if __name__ == "__main__":
    main()

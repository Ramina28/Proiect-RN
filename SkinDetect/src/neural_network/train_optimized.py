import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import pandas as pd
import matplotlib.pyplot as plt

# Importăm modelul optimizat
from optimize import build_optimized_model

# --- CONFIGURARE INTELIGENTĂ A CĂILOR ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 1. Căutăm unde sunt datele (în 'processed' sau direct în 'data')
path_processed = os.path.join(BASE_DIR, 'data', 'processed', 'train')
path_raw = os.path.join(BASE_DIR, 'data', 'train')

if os.path.exists(path_processed):
    DATA_ROOT = os.path.join(BASE_DIR, 'data', 'processed')
    print(f"[INFO] Am găsit datele în: data/processed")
elif os.path.exists(path_raw):
    DATA_ROOT = os.path.join(BASE_DIR, 'data')
    print(f"[INFO] Am găsit datele în: data (root)")
else:
    print(f"[EROARE CRITICĂ] Nu găsesc folderul 'train' nici în data/processed, nici în data!")
    exit()

TRAIN_DIR = os.path.join(DATA_ROOT, "train")

# 2. Căutăm folderul de validare ('val' sau 'validation')
if os.path.exists(os.path.join(DATA_ROOT, "val")):
    VAL_DIR = os.path.join(DATA_ROOT, "val")
    print("[INFO] Folder validare: val")
elif os.path.exists(os.path.join(DATA_ROOT, "validation")):
    VAL_DIR = os.path.join(DATA_ROOT, "validation")
    print("[INFO] Folder validare: validation")
else:
    # Dacă nu există, folosim tot train (doar ca să nu crape, deși nu e ideal)
    print("[ATENȚIE] Nu am găsit folder de validare! Voi folosi train pentru validare (temporar).")
    VAL_DIR = TRAIN_DIR

MODELS_DIR = os.path.join(BASE_DIR, "models")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
DOCS_DIR = os.path.join(BASE_DIR, "docs", "optimization")

# Asigurăm existența folderelor de output
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

OPTIMIZED_MODEL_OUT = os.path.join(MODELS_DIR, "optimized_model.h5")

# Parametri
BATCH_SIZE = 16
EPOCHS = 30
IMG_SIZE = (224, 224)

def plot_learning_curves(history, out_path):
    try:
        acc = history['accuracy']
        val_acc = history['val_accuracy']
        loss = history['loss']
        val_loss = history['val_loss']
        epochs_range = range(len(acc))

        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, acc, label='Training Accuracy')
        plt.plot(epochs_range, val_acc, label='Validation Accuracy')
        plt.legend(loc='lower right')
        plt.title('Accuracy')

        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, loss, label='Training Loss')
        plt.plot(epochs_range, val_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.title('Loss')
        
        plt.tight_layout()
        plt.savefig(out_path)
        plt.close()
    except Exception as e:
        print(f"[WARN] Nu s-a putut genera graficul: {e}")

def main():
    print("--- INCEPERE ANTRENARE MODEL OPTIMIZAT ---")

    # --- Augmentare ---
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        brightness_range=(0.8, 1.2),
        zoom_range=0.2,
        rotation_range=10,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    val_datagen = ImageDataGenerator(rescale=1./255)

    # --- Generatoare ---
    train_data = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="sparse",
        shuffle=True
    )

    val_data = val_datagen.flow_from_directory(
        VAL_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="sparse",
        shuffle=False
    )

    # --- Model ---
    num_classes = len(train_data.class_indices)
    print(f"Clase detectate: {train_data.class_indices}")
    
    model = build_optimized_model(input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3), num_classes=num_classes)

    # --- Antrenare ---
    checkpoint = ModelCheckpoint(OPTIMIZED_MODEL_OUT, monitor="val_accuracy", save_best_only=True, mode='max', verbose=1)
    early_stop = EarlyStopping(monitor="val_loss", patience=6, restore_best_weights=True, verbose=1)
    reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3, min_lr=1e-6, verbose=1)

    history = model.fit(
        train_data,
        epochs=EPOCHS,
        validation_data=val_data,
        callbacks=[early_stop, reduce_lr, checkpoint]
    )

    # --- Salvare finală ---
    pd.DataFrame(history.history).to_csv(os.path.join(RESULTS_DIR, "optimization_history.csv"), index=False)
    plot_learning_curves(history.history, os.path.join(DOCS_DIR, "learning_curves_best.png"))
    print(f"[SUCCES] Antrenare completa! Model salvat in: {OPTIMIZED_MODEL_OUT}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Modul 2 – Neural Network pentru SIA Dermatologică

În Etapa 4:
- definim un model CNN simplu pentru clasificarea în 3 clase (acnee, eczemă, roșeață)
- îl compilăm fără erori
- demonstrăm că poate fi salvat și reîncărcat

NU este necesar să fie antrenat cu acuratețe bună în acest stadiu.
"""

from pathlib import Path

print("=======================================")
print("  Modul 2 – Neural Network – SkinCNN  ")
print("=======================================\n")

print("[STEP] Import TensorFlow/Keras...")

try:
    import tensorflow as tf
    from tensorflow.keras import layers, models
except Exception as e:
    print("[ERROR] Nu am putut importa TensorFlow/Keras.")
    print("Mesaj de eroare:")
    print(e)
    print("\nSoluție probabilă: instalează TensorFlow cu:")
    print("    pip install tensorflow")
    raise SystemExit(1)

print("[OK] TensorFlow a fost importat cu succes.\n")

# Parametri de bază
IMG_HEIGHT = 200
IMG_WIDTH = 200
NUM_CHANNELS = 3
NUM_CLASSES = 3


def build_skin_cnn(
    input_shape=(IMG_HEIGHT, IMG_WIDTH, NUM_CHANNELS),
    num_classes=NUM_CLASSES,
) -> tf.keras.Model:
    """
    Construcția modelului CNN pentru clasificarea imaginilor de piele.

    Justificare rapidă:
    - straturi Conv2D + MaxPooling -> extragere caracteristici vizuale (texturi, margini, zone inflamate)
    - creșterea numărului de filtre (32 → 64 → 128) -> capturarea unor caracteristici din ce în ce mai complexe
    - GlobalAveragePooling2D -> reduce numărul de parametri, util pentru dataset relativ mic
    - Dense(64) + Dense(num_classes, softmax) -> clasificare finală pe cele 3 clase
    """

    inputs = layers.Input(shape=input_shape, name="input_image")

    # Normalizare [0, 1]
    x = layers.Rescaling(1.0 / 255.0, name="rescale_0_1")(inputs)

    # Bloc 1
    x = layers.Conv2D(32, (3, 3), activation="relu", padding="same", name="conv_1")(x)
    x = layers.MaxPooling2D(pool_size=(2, 2), name="pool_1")(x)

    # Bloc 2
    x = layers.Conv2D(64, (3, 3), activation="relu", padding="same", name="conv_2")(x)
    x = layers.MaxPooling2D(pool_size=(2, 2), name="pool_2")(x)

    # Bloc 3
    x = layers.Conv2D(128, (3, 3), activation="relu", padding="same", name="conv_3")(x)
    x = layers.MaxPooling2D(pool_size=(2, 2), name="pool_3")(x)

    # Clasificare
    x = layers.GlobalAveragePooling2D(name="gap")(x)
    x = layers.Dense(64, activation="relu", name="dense_1")(x)
    outputs = layers.Dense(num_classes, activation="softmax", name="predictions")(x)

    model = models.Model(inputs=inputs, outputs=outputs, name="skin_cnn_classifier")

    # Compilare – cerință Etapa 4
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model


def save_model(model: tf.keras.Model, path: str = "models/skin_cnn_untrained.keras") -> None:
    model_dir = Path(path).parent
    model_dir.mkdir(parents=True, exist_ok=True)

    print(f"[STEP] Salvez modelul în: {path}")
    model.save(path)
    print("[OK] Model salvat cu succes.\n")


def load_model(path: str = "models/skin_cnn_untrained.keras") -> tf.keras.Model:
    print(f"[STEP] Încarc modelul din: {path}")
    loaded_model = tf.keras.models.load_model(path)
    print("[OK] Model încărcat cu succes.\n")
    return loaded_model


if __name__ == "__main__":
    print("[STEP] Construiesc modelul...")
    model = build_skin_cnn()

    print("\n[STEP] Afișez summary-ul modelului:")
    model.summary()

    print("\n[STEP] Salvez modelul neantrenat...")
    save_model(model, path="models/skin_cnn_untrained.keras")

    print("[STEP] Reîncarc modelul pentru verificare...")
    _ = load_model(path="models/skin_cnn_untrained.keras")

    print("\n[INFO] Modul 2 (Neural Network) a rulat COMPLET fără erori.")

"""
Modul 2: Neural Network Module (Etapa 4) – SkinDetect (Acnee vs Eczeme)

Scop (Etapa 4):
- definirea unei arhitecturi CNN pentru clasificare imagini dermatologice
- compilarea modelului (fără antrenare serioasă)
- posibilitatea de a salva și reîncărca modelul (schelet funcțional end-to-end)

De ce această arhitectură:
- Problema este de clasificare imagini (2 clase), iar CNN-urile sunt potrivite deoarece învață filtre spațiale
  relevante (textură, contururi, pattern-uri) direct din pixeli.
- Arhitectura este moderat de mică (3 blocuri Conv) pentru a rula rapid și a fi ușor de integrat în pipeline/UI.
- Input fix: 200x200x3 (compatibil cu preprocesarea din `resize_images.py`).

IMPORTANT:
- În Etapa 4, modelul poate rămâne neantrenat (weights random). Se verifică doar că pipeline-ul rulează.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
import tensorflow as tf


@dataclass(frozen=True)
class ModelConfig:
    img_height: int = 200
    img_width: int = 200
    channels: int = 3
    num_classes: int = 2
    learning_rate: float = 1e-3


def build_cnn(config: ModelConfig) -> tf.keras.Model:
    """
    Construiește o rețea CNN simplă pentru clasificare binară (2 clase).

    Input: (200, 200, 3)
    Output: probabilități pe clase (softmax, 2 neuroni)
    """
    inputs = tf.keras.Input(shape=(config.img_height, config.img_width, config.channels), name="image")

    # Bloc 1
    x = tf.keras.layers.Conv2D(32, (3, 3), padding="same", activation="relu")(inputs)
    x = tf.keras.layers.MaxPooling2D((2, 2))(x)

    # Bloc 2
    x = tf.keras.layers.Conv2D(64, (3, 3), padding="same", activation="relu")(x)
    x = tf.keras.layers.MaxPooling2D((2, 2))(x)

    # Bloc 3
    x = tf.keras.layers.Conv2D(128, (3, 3), padding="same", activation="relu")(x)
    x = tf.keras.layers.MaxPooling2D((2, 2))(x)

    # Head
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(128, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.3)(x)

    outputs = tf.keras.layers.Dense(config.num_classes, activation="softmax", name="probs")(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="SkinDetect_CNN")
    return model


def compile_model(model: tf.keras.Model, config: ModelConfig) -> tf.keras.Model:
    """
    Compilează modelul pentru clasificare multi-class (2 clase).
    """
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=config.learning_rate),
        loss=tf.keras.losses.CategoricalCrossentropy(),
        metrics=["accuracy"],
    )
    return model


def save_model(model: tf.keras.Model, out_path: str) -> None:
    """
    Salvează modelul pe disc (format .keras recomandat).
    """
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    model.save(out_path)


def load_model(model_path: str) -> tf.keras.Model:
    """
    Reîncarcă modelul salvat.
    """
    return tf.keras.models.load_model(model_path)


def main():
    """
    Rulează o demonstrație minimă:
    - construiește modelul
    - îl compilează
    - îl salvează
    - îl reîncarcă
    - printează summary (dovadă că modulul funcționează)
    """
    config = ModelConfig()
    model = build_cnn(config)
    model = compile_model(model, config)

    print("\n--- MODEL SUMMARY (compiled) ---")
    model.summary()

    model_path = os.path.join("models", "untrained_model.keras")
    save_model(model, model_path)
    print(f"\n[OK] Model salvat: {model_path}")

    reloaded = load_model(model_path)
    print(f"[OK] Model reîncărcat: {model_path}")

    print("\n--- RELOADED MODEL SUMMARY ---")
    reloaded.summary()


if __name__ == "__main__":
    main()

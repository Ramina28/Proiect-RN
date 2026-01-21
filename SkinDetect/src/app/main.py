import os
import numpy as np
import gradio as gr
import tensorflow as tf
from PIL import Image

# ============================================================
# CONFIGURARE PROIECT & MODEL
# ============================================================
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Încărcăm modelul OPTIMIZAT
PATH_OPTIMIZED = os.path.join(PROJECT_ROOT, "models", "optimized_model.h5")
PATH_BEST = os.path.join(PROJECT_ROOT, "models", "best_model.h5")

# Logica de fallback (siguranță)
if os.path.exists(PATH_OPTIMIZED):
    MODEL_PATH = PATH_OPTIMIZED
    MODEL_NAME = "optimized_model.h5"
elif os.path.exists(PATH_BEST):
    MODEL_PATH = PATH_BEST
    MODEL_NAME = "best_model.h5 (Fallback)"
else:
    raise FileNotFoundError("Nu am găsit niciun model .h5 în folderul models/")

IMG_SIZE = (224, 224) 
CLASS_NAMES = ["Acnee", "Eczeme"]
CONF_THRESHOLD = 0.60 

print(f"[INFO] Se încarcă modelul: {MODEL_NAME}...")
MODEL = tf.keras.models.load_model(MODEL_PATH)

# ============================================================
# LOGICA DE PREDICȚIE
# ============================================================
def preprocess_image(pil_img: Image.Image) -> np.ndarray:
    img = pil_img.convert("RGB")
    img = img.resize(IMG_SIZE, Image.Resampling.LANCZOS)
    arr = np.asarray(img).astype(np.float32) / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr

def predict_skin_condition(pil_img: Image.Image):
    if pil_img is None:
        return "Te rog încarcă o imagine.", None

    try:
        processed_img = preprocess_image(pil_img)
        predictions = MODEL.predict(processed_img, verbose=0)[0]
        
        p_acnee = float(predictions[0])
        p_eczeme = float(predictions[1])
        
        class_probs = {"Acnee": p_acnee, "Eczeme": p_eczeme}
        confidence = max(p_acnee, p_eczeme)
        predicted_class = "Acnee" if p_acnee > p_eczeme else "Eczeme"

        # Logica de Siguranță (Etapa 6)
        if confidence < CONF_THRESHOLD:
            msg = (
                f"Rezultat: NESIGUR\n"
                f"Modelul nu este suficient de sigur ({confidence:.2f}).\n"
                f"Încearcă o imagine mai clară."
            )
            return msg, class_probs
        
        msg = (
            f"Predicție: **{predicted_class}**\n"
            f"Încredere: {confidence*100:.1f}%"
        )
        return msg, class_probs

    except Exception as e:
        return f"Eroare: {str(e)}", None

# ============================================================
# INTERFAȚA GRAFICĂ (SIMPLĂ - STILUL VECHI)
# ============================================================
with gr.Blocks(title="SkinDetect UI") as demo:
    gr.Markdown("# SkinDetect – UI")
    gr.Markdown(f"Model activ: `{MODEL_NAME}` | Prag: `{CONF_THRESHOLD}`")

    with gr.Row():
        inp = gr.Image(type="pil", label="Upload imagine")
        out_text = gr.Markdown(label="Rezultat Text")

    out_probs = gr.Label(num_top_classes=2, label="Probabilități")

    btn = gr.Button("Rulează inferența")
    btn.click(fn=predict_skin_condition, inputs=inp, outputs=[out_text, out_probs])

if __name__ == "__main__":
    demo.launch()
import os
import csv
import numpy as np
import gradio as gr
import tensorflow as tf
from PIL import Image

# ============================================================
# SkinDetect AI - main_app.py (UI Gradio)
# Etapa 6: Model optimizat + Confidence threshold + Recomandări din CSV
# ============================================================

# ============================================================
# 1) CONFIGURARE PROIECT & MODEL
# ============================================================

# PROJECT_ROOT = .../SkinDetect (două niveluri mai sus de acest fișier)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Căile către modele (NU redenumim nimic, păstrăm fallback)
PATH_OPTIMIZED = os.path.join(PROJECT_ROOT, "models", "optimized_model.h5")
PATH_BEST = os.path.join(PROJECT_ROOT, "models", "best_model.h5")

# Calea către CSV-ul cu recomandări (data/recommendations.csv)
RECS_PATH = os.path.join(PROJECT_ROOT, "data", "recommendations.csv")

# Logica de fallback (siguranță): preferăm optimized, apoi best
if os.path.exists(PATH_OPTIMIZED):
    MODEL_PATH = PATH_OPTIMIZED
    MODEL_NAME = "optimized_model.h5 (Final)"
elif os.path.exists(PATH_BEST):
    MODEL_PATH = PATH_BEST
    MODEL_NAME = "best_model.h5 (Fallback)"
else:
    raise FileNotFoundError("CRITIC: Nu am găsit niciun model .h5 în folderul models/!")

# Parametri folosiți la antrenare / inferență
IMG_SIZE = (200, 200)
CLASS_NAMES = ["Acnee", "Eczeme"]

# Prag de siguranță: dacă max(prob) < threshold -> UNCERTAIN
CONF_THRESHOLD = 0.60

# ============================================================
# 2) ÎNCĂRCARE MODEL (cu log-uri cerute)
# ============================================================

# Folosim aceeași “căutare inteligentă” ca în evaluate.py / train_optimized.py
PATHS_TO_CHECK = [
    os.path.join(PROJECT_ROOT, "data", "processed", "val"),
    os.path.join(PROJECT_ROOT, "data", "processed", "validation"),
    os.path.join(PROJECT_ROOT, "data", "val"),
    os.path.join(PROJECT_ROOT, "data", "validation"),
]
VAL_DIR = next((p for p in PATHS_TO_CHECK if os.path.exists(p)), None)

def _rel_from_root(p: str) -> str:
    try:
        return os.path.relpath(p, PROJECT_ROOT).replace("\\", "/")
    except Exception:
        return p.replace("\\", "/")

def _validation_accuracy(model) -> float:
    """
    Accuracy robust (NU depinde de model.compile/metrics):
    - încarcă imaginile din VAL_DIR (val/validation)
    - face predict
    - calculează accuracy pentru sigmoid(1) sau softmax(2+)
    Returnează NaN dacă nu poate evalua.
    """
    if VAL_DIR is None or not os.path.isdir(VAL_DIR):
        return float("nan")

    try:
        ds = tf.keras.utils.image_dataset_from_directory(
            VAL_DIR,
            labels="inferred",
            label_mode="int",         # IMPORTANT: etichete int (0/1/..)
            image_size=IMG_SIZE,
            batch_size=32,
            shuffle=False,
        )

        # Normalizare identică cu evaluate.py (dacă modelul nu include Rescaling)
        ds = ds.map(lambda x, y: (tf.cast(x, tf.float32) / 255.0, y))

        y_true_list = [y.numpy() for _, y in ds]
        if not y_true_list:
            return float("nan")
        y_true = np.concatenate(y_true_list, axis=0)

        y_pred = model.predict(ds, verbose=0)

        # binary sigmoid: (N,) sau (N,1)
        if isinstance(y_pred, np.ndarray) and (y_pred.ndim == 1 or (y_pred.ndim == 2 and y_pred.shape[1] == 1)):
            y_pred_cls = (y_pred.reshape(-1) >= 0.5).astype(int)
        else:
            # multiclass softmax: (N,C)
            y_pred_cls = np.argmax(y_pred, axis=1).astype(int)

        return float(np.mean(y_pred_cls == y_true))

    except Exception:
        return float("nan")


# Logica de fallback (siguranță): preferăm optimized, apoi best
if os.path.exists(PATH_OPTIMIZED):
    MODEL_PATH = PATH_OPTIMIZED
elif os.path.exists(PATH_BEST):
    MODEL_PATH = PATH_BEST
else:
    raise FileNotFoundError("CRITIC: Nu am găsit niciun model .h5 în folderul models/!")

# 1) Log EXACT cerut
print(f"Loading model: {_rel_from_root(MODEL_PATH)}")

# 2) Load
try:
    MODEL = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"CRITIC: Nu s-a putut încărca modelul: {e}")

# 3) Accuracy pe validation (val/validation)
acc = _validation_accuracy(MODEL)

# 4) Log EXACT cerut
print(f"Model loaded successfully. Accuracy on validation: {acc:.4f}")

# ============================================================
# 3) ÎNCĂRCARE RECOMANDĂRI DIN CSV
# ============================================================

def _sniff_delimiter(sample: str) -> str:
    """
    În Windows/Excel, CSV-ul poate fi separat prin ',' sau ';'.
    Încercăm să detectăm automat separatorul.
    """
    if sample.count(";") > sample.count(","):
        return ";"
    return ","


def load_recommendations(csv_path: str) -> dict:
    """
    Încarcă recommendations.csv într-un dict:
      recs[label] = {
        'solution_title': ...,
        'do': ...,
        'avoid': ...,
        'when_to_see_doctor': ...,
        'disclaimer': ...
      }

    Important:
    - folosim encoding 'utf-8-sig' ca să suportăm UTF-8 cu BOM (Excel/Notepad).
    - suportăm delimiter ',' sau ';'
    """
    if not os.path.exists(csv_path):
        print(f"[WARN] Nu există fișier de recomandări: {csv_path}")
        return {}

    try:
        # Citim întâi un mic sample pentru a detecta separatorul
        with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
            sample = f.read(2048)
            delim = _sniff_delimiter(sample)

        # Re-citim fișierul complet
        recs = {}
        with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f, delimiter=delim)
            for row in reader:
                label = (row.get("label") or "").strip()
                if not label:
                    continue

                recs[label] = {
                    "solution_title": (row.get("solution_title") or "").strip(),
                    "do": (row.get("do") or "").strip(),
                    "avoid": (row.get("avoid") or "").strip(),
                    "when_to_see_doctor": (row.get("when_to_see_doctor") or "").strip(),
                    "disclaimer": (row.get("disclaimer") or "").strip(),
                }

        print(f"[INFO] Recomandări încărcate din CSV: {len(recs)} intrări (labels: {list(recs.keys())})")
        return recs

    except Exception as e:
        print(f"[WARN] Nu am putut încărca recommendations.csv: {e}")
        return {}


RECOMMENDATIONS = load_recommendations(RECS_PATH)

# ============================================================
# 4) PREPROCESARE IMAGINE
# ============================================================

def preprocess_image(pil_img: Image.Image) -> np.ndarray:
    """
    Transformă imaginea PIL în tensor gata pentru model:
    - RGB
    - resize la IMG_SIZE
    - normalizare 1./255
    - batch dimension (1, H, W, 3)
    """
    img = pil_img.convert("RGB")
    img = img.resize(IMG_SIZE, Image.Resampling.LANCZOS)
    arr = np.asarray(img).astype(np.float32) / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr

# ============================================================
# 5) UI HELPERS (STATUS + RECOMANDĂRI)
# ============================================================

def _build_status_box(predicted_class: str, confidence: float) -> str:
    """
    Box tip "traffic light" + bară de confidence.
    - roșu: < CONF_THRESHOLD => UNCERTAIN
    - portocaliu: între threshold și 0.80
    - verde: >= 0.80
    """

    def bar(color_hex: str) -> str:
        return f"""
        <div style="height:10px;background:rgba(0,0,0,0.10);border-radius:8px;overflow:hidden;margin-top:10px;">
          <div style="height:10px;width:{confidence*100:.0f}%;background:{color_hex};"></div>
        </div>
        <p style="margin:8px 0 0 0;font-size:12px;opacity:0.85;color:#111 !important;">
            Confidence: <b style="color:#111 !important;">{confidence:.1%}</b>
        </p>
        """

    # 1) Roșu: INCERT
    if confidence < CONF_THRESHOLD:
        return f"""
        <div style="background-color:#ffebee;border:2px solid #ef5350;border-radius:10px;padding:20px;text-align:center;color:#111 !important;">
            <h2 style="color:#c62828;margin:0;">⚠️ REZULTAT INCERT</h2>
            <p style="font-size:16px;margin-top:10px;color:#111 !important;">
                Modelul nu este sigur.<br>
                Prag minim: <b style="color:#111 !important;">{CONF_THRESHOLD*100:.0f}%</b>
            </p>
            {bar("#ef5350")}
            <p style="font-size:12px;opacity:0.80;margin-top:10px;color:#111 !important;">
                Sugestie: reîncercați cu lumină mai bună și focalizare clară.
            </p>
        </div>
        """

    # 2) Portocaliu: MEDIU
    if confidence < 0.80:
        return f"""
        <div style="background-color:#fff3e0;border:2px solid #ffb74d;border-radius:10px;padding:20px;text-align:center;color:#111 !important;">
            <h2 style="color:#ef6c00;margin:0;">🔍 Posibil: {predicted_class}</h2>
            <p style="font-size:16px;margin-top:10px;color:#111 !important;">
                Nivel de încredere mediu.<br>
                Rezultatul este probabil, dar necesită verificare.
            </p>
            {bar("#ffb74d")}
        </div>
        """

    # 3) Verde: SIGUR
    return f"""
    <div style="background-color:#e8f5e9;border:2px solid #66bb6a;border-radius:10px;padding:20px;text-align:center;color:#111 !important;">
        <h2 style="color:#2e7d32;margin:0;">✅ Rezultat: {predicted_class}</h2>
        <p style="font-size:16px;margin-top:10px;color:#111 !important;">
            Nivel de încredere ridicat.<br>
            Modelul a identificat clar caracteristicile specifice.
        </p>
        {bar("#66bb6a")}
    </div>
    """


def _build_recommendation_box(label_for_recs: str) -> str:
    """
    Afișează recomandările pentru:
    - Acnee / Eczeme (dacă confidence >= threshold)
    - UNCERTAIN (dacă confidence < threshold)
    """
    rec = RECOMMENDATIONS.get(label_for_recs)

    if not rec:
        return f"""
        <div style="background:#f5f5f5;border:1px solid #ddd;border-radius:10px;padding:16px;">
          <h3 style="margin:0 0 8px 0;color:#111 !important;">📌 Recomandări</h3>
          <p style="margin:0;color:#111 !important;">
            Nu am găsit recomandări pentru <b style="color:#111 !important;">{label_for_recs}</b>.
          </p>
        </div>
        """

    title = rec.get("solution_title", "").strip()
    do_txt = rec.get("do", "").strip()
    avoid_txt = rec.get("avoid", "").strip()
    doctor_txt = rec.get("when_to_see_doctor", "").strip()
    disclaimer_txt = rec.get("disclaimer", "").strip()

    return f"""
    <div style="
        background: #eef6ff;
        border: 1px solid #cfe3ff;
        border-radius: 12px;
        padding: 16px;
        color: #111 !important;
        opacity: 1 !important;
        line-height: 1.5;
    ">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
            <span style="font-size:18px;">🧾</span>
            <h3 style="margin:0;color:#0d47a1 !important;">Recomandări</h3>
        </div>

        <p style="margin:0 0 10px 0;color:#111 !important;">
            <b style="color:#111 !important;">{title}</b>
        </p>

        <p style="margin:0 0 10px 0;color:#111 !important;">
            <b style="color:#111 !important;">Ce să faci:</b><br>
            {do_txt}
        </p>

        <p style="margin:0 0 10px 0;color:#111 !important;">
            <b style="color:#111 !important;">Ce să eviți:</b><br>
            {avoid_txt}
        </p>

        <p style="margin:0 0 10px 0;color:#111 !important;">
            <b style="color:#111 !important;">Când să mergi la medic:</b><br>
            {doctor_txt}
        </p>

        <p style="margin:0;color:#333 !important;font-size:12px;">
            {disclaimer_txt}
        </p>
    </div>
    """


# ============================================================
# 6) PREDICȚIE (MODEL + UI)
# ============================================================

def predict_skin_condition(pil_img: Image.Image):
    """
    Funcția apelată de butonul UI.
    Returnează:
    1) probs_output -> dict cu probabilități (gr.Label)
    2) status_output -> HTML traffic light + bară confidence
    3) recs_output -> HTML recomandări (din CSV)
    """
    if pil_img is None:
        return (
            None,
            "<div style='color:red;'>⚠️ Te rog încarcă o imagine mai întâi.</div>",
            ""
        )

    try:
        processed_img = preprocess_image(pil_img)

        # Predicție: vector [p_acnee, p_eczeme]
        preds = MODEL.predict(processed_img, verbose=0)[0]
        p_acnee = float(preds[0])
        p_eczeme = float(preds[1])

        # Probabilități pentru componenta gr.Label
        class_probs = {"Acnee": p_acnee, "Eczeme": p_eczeme}

        # Clasa + confidence
        confidence = max(p_acnee, p_eczeme)
        predicted_class = "Acnee" if p_acnee > p_eczeme else "Eczeme"

        # Dacă nu suntem siguri, folosim label-ul special UNCERTAIN pentru recomandări
        label_for_recs = predicted_class if confidence >= CONF_THRESHOLD else "UNCERTAIN"

        html_status = _build_status_box(predicted_class, confidence)
        html_recs = _build_recommendation_box(label_for_recs)

        return class_probs, html_status, html_recs

    except Exception as e:
        return (
            None,
            f"<div style='color:red;'>Eroare internă: {str(e)}</div>",
            ""
        )

# ============================================================
# 7) UI GRADIO (MODERN)
# ============================================================

theme = gr.themes.Soft(
    primary_hue="teal",
    secondary_hue="slate",
    radius_size="md"
)

css_style = """

/* Import font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

/* Aplică fontul peste tot */
body, .gradio-container {
    font-family: 'Inter', sans-serif !important;
}

.container { max-width: 980px; margin: auto; }
footer { visibility: hidden; }

/* Card look (premium) */
.card {
  border-radius: 14px;
  padding: 16px;
  border: 1px solid rgba(255,255,255,0.10);
  box-shadow: 0 8px 22px rgba(0,0,0,0.20);
  background: rgba(255,255,255,0.03);
}

/* Titluri secțiuni */
.section-title {
  font-size: 15px;
  opacity: 0.85;
  margin-bottom: 10px;
}

.small-note { font-size: 12px; opacity: 0.75; line-height: 1.4; }
"""


with gr.Blocks(theme=theme, css=css_style, title="SkinDetect AI v6") as demo:

    # --- HEADER ---
    gr.Markdown("""
    <div style="text-align: center;">
        <h1>🏥 SkinDetect AI</h1>
        <h3>Sistem Asistat de Inteligență Artificială pentru Analiza Afecțiunilor Dermatologice</h3>
    </div>
    """)

    # --- ZONA PRINCIPALĂ (2 COLOANE) ---
    with gr.Row():

        # Coloana Stânga: INPUT (card)
        with gr.Column(scale=1, elem_classes=["card"]):
            gr.Markdown("<div class='section-title'>1) Încărcare Imagine</div>")

            input_image = gr.Image(
                type="pil",
                label="Încărcați fotografia leziunii",
                height=300
            )

            gr.Markdown("""
            <div class="small-note">
              <b>Tips pentru o imagine bună:</b><br>
              • lumină naturală • fără filtre • focalizare bună • cadru apropiat
            </div>
            """)

            run_btn = gr.Button("🔍 Analizează Imaginea", variant="primary", size="lg")

            with gr.Accordion("ℹ️ Detalii Tehnice & Configurare", open=False):
                gr.Markdown(f"""
                - **Model Activ:** `{MODEL_NAME}`
                - **Dimensiune Input:** `{IMG_SIZE}`
                - **Prag Siguranță:** `{CONF_THRESHOLD*100:.0f}%`
                - **Recomandări CSV:** `data/recommendations.csv` ({'OK' if os.path.exists(RECS_PATH) else 'LIPSEȘTE'})
                - **Framework:** TensorFlow/Keras + Gradio
                """)

        # Coloana Dreapta: OUTPUT (card)
        with gr.Column(scale=1, elem_classes=["card"]):
            gr.Markdown("<div class='section-title'>2) Rezultate Analiză</div>")

            status_output = gr.HTML(label="Status Diagnostic")
            probs_output = gr.Label(num_top_classes=2, label="Probabilități Detaliate")
            recs_output = gr.HTML(label="Recomandări")

    # --- DISCLAIMER ---
    gr.Markdown("""
    ---
    <div style="font-size: 12px; color: gray; text-align: center;">
        ⚠️ <b>Disclaimer Medical:</b> Această aplicație este un proiect universitar (Etapa 6 - Optimizare).
        Rezultatele generate de AI nu reprezintă un diagnostic medical certificat.
        Pentru probleme reale de sănătate, adresați-vă unui medic dermatolog.
    </div>
    """)

    # --- LEGĂTURI FUNCȚIONALE ---
    run_btn.click(
        fn=predict_skin_condition,
        inputs=input_image,
        outputs=[probs_output, status_output, recs_output]
    )

# ============================================================
# 8) RULARE APLICAȚIE
# ============================================================
if __name__ == "__main__":
    demo.launch()

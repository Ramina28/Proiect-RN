# Modul 3: Web Service / UI (Etapa 4) – SkinDetect

Acest modul oferă o interfață minimă (Gradio) care demonstrează că pipeline-ul end-to-end funcționează:

**Input user → Preprocess (200×200) → Model CNN → Output (clasă + probabilități)**

În Etapa 4, modelul este definit și compilat, dar poate fi neantrenat (predicții posibil incorecte).

---

## Fișiere

- `app.py` – aplicația UI Gradio.

---

## Precondiție

Modelul trebuie să existe în:

`models/untrained_model.keras`

Se generează rulând:

```bash
python src/neural_network/model.py

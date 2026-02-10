# 🧠 Modulul Neural Network

Acest director conține „creierul” proiectului **SkinDetect**: arhitectura CNN, antrenarea și evaluarea performanței.

Modulul este împărțit în două etape:
- **Baseline (Etapa 4–5)** – model + antrenare inițială
- **Optimizat (Etapa 6)** – pipeline îmbunătățit + evaluare finală

---

## 📂 Descrierea fișierelor (ce face + ce produce)

### 1) `model.py` — Arhitectura baseline (scheletul CNN)
**Ce face:**
- Definește o rețea CNN simplă cu 3 blocuri convoluționale (Conv2D + MaxPool).
- Compilează modelul cu:
  - **Adam**
  - **CategoricalCrossentropy** (etichete one-hot)
  - metrică: **accuracy**
- Include funcții de salvare/încărcare model.

**Ce produce (output):**
- La rulare directă (`python model.py`), creează și salvează un model neantrenat:
  - `models/untrained_model.keras`
- Afișează și `model.summary()` în consolă.

---

### 2) `train.py` — Antrenarea baseline
**Ce face:**
- Construiește modelul din `model.py`.
- Încarcă datele din:
  - `data/train`
  - `data/validation`
- Normalizează imaginile (`rescale=1./255`) și aplică augmentări moderate (brightness/zoom/shift etc).
- Antrenează cu callbacks:
  - `EarlyStopping` (monitorizează `val_loss`)
  - `ReduceLROnPlateau` (monitorizează `val_loss`)
  - `ModelCheckpoint` (salvează cel mai bun model după `val_loss`)

**Ce produce (output):**
- Modele:
  - `models/trained_model.h5` (modelul final după antrenare)
  - `models/best_model.h5` (cel mai bun model pe `val_loss`)
- Istoric antrenare:
  - `results/training_history.csv`
- Grafic loss:
  - `docs/loss_curve.png`

---

### 3) `optimize.py` — Arhitectura “optimizată” (compatibilă cu sparse labels)
**Ce face:**
- Definește un model CNN similar ca structură, dar compilat cu:
  - loss: **sparse_categorical_crossentropy**
  - metrică: **accuracy**
- Asta înseamnă că etichetele sunt **integer** (0/1), nu one-hot.

**Ce produce (output):**
- Nu salvează fișiere implicit.
- La rulare directă (`python optimize.py`), afișează `model.summary()` în consolă (test rapid al arhitecturii).

---

### 4) `train_optimized.py` — Antrenarea optimizată (Etapa 6)
**Ce face:**
- Găsește automat datele astfel:
  - preferă `data/processed/train`, altfel `data/train`
- Val/validation:
  - caută `val` sau `validation`
  - dacă nu există, folosește train și ca validation (fallback ca să nu crape)
- Folosește augmentare mai puternică:
  - brightness, zoom, rotation, horizontal_flip
- Creează generator cu:
  - `class_mode="sparse"` (etichetă integer)
- Callbacks:
  - `ModelCheckpoint` monitorizează **val_accuracy**
  - `EarlyStopping` monitorizează **val_loss**
  - `ReduceLROnPlateau` monitorizează **val_loss**

**Ce produce (output):**
- Model final:
  - `models/optimized_model.h5`
- Istoric optimizare:
  - `results/optimization_history.csv`
- Grafice de antrenare (accuracy + loss):
  - `docs/optimization/learning_curves_best.png`

---

### 5) `evaluate.py` — Evaluarea finală + metrici + confusion matrix + analiză erori

**Ce face:**
- Încarcă modelul specificat prin argument:
  - implicit: `models/optimized_model.h5`
  - opțional: alt model folosind `--model <cale>`
- Caută automat setul de evaluare în următoarea ordine:
  1. `data/processed/test`
  2. `data/test`
  3. `data/processed/val`
  4. `data/validation`
- Încarcă imaginile folosind `image_dataset_from_directory`, cu:
  - `shuffle=False` (păstrează ordinea fișierelor pentru analiza erorilor)
  - `label_mode="int"`
- Normalizează imaginile cu:
  - `Rescaling(1./255)`
- Rulează predicțiile pe întreg setul și calculează:
  - Accuracy
  - Precision (macro)
  - Recall (macro)
  - F1-score (macro)
  - Confusion Matrix
  - Classification report (pe clase)

**Analiza erorilor:**
- Identifică toate predicțiile greșite.
- Selectează **Top 5 erori** (după nivelul de încredere al modelului).
- Pentru fiecare eroare salvează:
  - numele fișierului
  - eticheta reală
  - eticheta prezisă
  - nivelul de încredere
  - probabilitățile pe clase

**Ce produce (output):**
- Metrici finale salvate în:
  - `results/final_metrics.json`
- Confusion matrix salvată ca imagine:
  - `docs/confusion_matrix_optimized.png`
- Analiza Top 5 erori:
  - `results/error_analysis.json`

**Output în consolă:**
- Test Accuracy
- Test F1-score (macro)
- Confirmarea fișierelor salvate

### 6) `find_errors.py` — Găsirea exemplelor greșite (Error Inspection / Debug)
**Ce face:**
- Încarcă un model deja antrenat (implicit **`models/best_model.h5`**, poate fi schimbat manual și pe `trained_model.h5`).
- Încarcă setul de test din **`data/test`** folosind `image_dataset_from_directory`.
- Rulează predicții pe imagini și compară **eticheta reală** cu **predicția modelului**.
- Identifică imaginile clasificate greșit și le copiază într-un folder separat pentru analiză vizuală.
- Se oprește după **primele 5 erori** găsite (ca să fie rapid și ușor de inspectat).

**Cum funcționează intern (pe scurt):**
- Folosește `shuffle=False` la încărcarea dataset-ului ca să păstreze aceeași ordine între:
  - `test_ds.file_paths` (numele/ordinea fișierelor)
  - predicțiile modelului
- Normalizează imaginile manual cu `Rescaling(1./255)` înainte de `model.predict()`.
- Predicția finală este `argmax` peste probabilitățile softmax (deci clasa cu scorul cel mai mare).

**Ce produce (output):**
1. **Folder cu imagini greșite copiate pentru analiză:**
   - `docs/error_examples/`
   - Folderul este curățat la fiecare rulare (șterge erorile vechi și le regenerează).
2. **Primele 5 imagini greșite sunt copiate și redenumite astfel:**
   - `pred_<clasaPrezisa>_real_<clasaReala>_<numeOriginal>`
   - Exemplu: `pred_eczeme_real_acnee_IMG123.jpg`
3. **Afișează în consolă un tabel cu:**
   - nume fișier
   - clasa reală
   - clasa prezisă

**Unde citește datele și modelul:**
- Model: `models/best_model.h5` (setat în `MODEL_PATH`)
- Test set: `data/test` (setat în `TEST_DIR`)
- Clase (hardcodate): `["acnee", "eczeme"]`  
  > Atenție: ordinea trebuie să corespundă cu ordinea folderelor/claselor din `data/test`.
  

> Notă: clasele sunt considerate în ordinea `["Acnee", "Eczeme"]`. Această ordine trebuie să corespundă și cu ordinea folderelor/claselor din dataset.

---
### 7) `visualize.py` — Generare vizualizări finale (academic, din metrici reale)

**Ce face:**
- Încarcă automat fișierele de rezultate generate de `evaluate.py` și `train_optimized.py`:
  - Metrici baseline: `results/final_metrics_baseline.json`
  - Metrici optimized: `results/final_metrics_optimized.json`
  - Istoric antrenare: `results/optimization_history.csv`
- Generează grafice **doar din valori reale** (fără hardcodări):
  - Metrici finale pentru modelul optimizat (Accuracy, F1, Precision, Recall)
  - Curbe de învățare reale (Train/Val Accuracy + Train/Val Loss)
  - Comparație baseline vs optimized:
    - Accuracy Comparison
    - F1 (macro) Comparison
- Rulează în mod “all” folosind:
  - `--all` (generează toate vizualizările cerute)

**Ce produce (output):**
- În `docs/results/`:
  - `docs/results/metrics_evolution.png`  
    (bare: Accuracy / F1 (macro) / Precision (macro) / Recall (macro) pentru modelul optimizat)
  - `docs/results/learning_curves_final.png`  
    (curbe reale: Train vs Val pentru Accuracy și Loss, din `optimization_history.csv`)
- În `docs/optimization/`:
  - `docs/optimization/accuracy_comparison.png`  
    (Baseline vs Optimized, din JSON-uri reale)
  - `docs/optimization/f1_comparison.png`  
    (Baseline vs Optimized, din JSON-uri reale)

**Dependențe / condiții:**
- Pentru graficele de comparație este necesar să existe **ambele** fișiere:
  - `results/final_metrics_baseline.json`
  - `results/final_metrics_optimized.json`
- Pentru curbele de învățare este necesar:
  - `results/optimization_history.csv`

---
## 🚀 Cum se rulează

### Antrenare (model final, optimizat)
```bash
cd src/neural_network
python train_optimized.py
python evaluate.py
python find_errors.py
python src/neural_network/visualize.py --all

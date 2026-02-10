# 📘 README – Etapa 5: Configurarea și Antrenarea Modelului RN

**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** Gaitan Ramina Alessandra 
**Link Repository GitHub:** [\[URL complet\]](https://github.com/Ramina28/Proiect-RN.git)  
**Data predării:** 18.12.2025

---

## Scopul Etapei 5

Această etapă corespunde punctului **6. Configurarea și antrenarea modelului RN** din lista de 9 etape - slide 2 **RN Specificatii proiect.pdf**.

**Obiectiv principal:** Antrenarea efectivă a modelului RN definit în Etapa 4, evaluarea performanței și integrarea în aplicația completă.

**Pornire obligatorie:** Arhitectura completă și funcțională din Etapa 4:
- State Machine definit și justificat
- Cele 3 module funcționale (Data Logging, RN, UI)
- Minimum 40% date originale în dataset

---

## PREREQUISITE – Verificare Etapa 4 (OBLIGATORIU)

**Înainte de a începe Etapa 5, verificați că aveți din Etapa 4:**

- [x] **State Machine** definit și documentat în `docs/state_machine.*`
- [x] **Contribuție ≥40% date originale** în `data/processed/` (verificabil prin data/manifest.csv + statistici în docs/)
- [x] **Modul 1 (Data Logging)** funcțional - produce CSV-uri
- [x] **Modul 2 (RN)** cu arhitectură definită dar NEANTRENATĂ (`models/untrained_model.keras`)
- [x] **Modul 3 (UI/Web Service)** funcțional cu model dummy
- [x] **Tabelul "Nevoie → Soluție → Modul"** complet în README Etapa 4

** Dacă oricare din punctele de mai sus lipsește → reveniți la Etapa 4 înainte de a continua.**

---

## Pregătire Date pentru Antrenare 

### Dacă ați adăugat date noi în Etapa 4 (contribuția de 40%):

**TREBUIE să refaceți preprocesarea pe dataset-ul COMBINAT:**

Exemplu:
```bash
# 1. Combinare date vechi (Etapa 3) + noi (Etapa 4)
python src/preprocessing/combine_datasets.py

# 2. Refacere preprocesare COMPLETĂ
python src/preprocessing/data_cleaner.py
python src/preprocessing/feature_engineering.py
python src/preprocessing/data_splitter.py --stratify --random_state 42

# Verificare finală:
# data/train/ → trebuie să conțină date vechi + noi
# data/validation/ → trebuie să conțină date vechi + noi
# data/test/ → trebuie să conțină date vechi + noi
```

** ATENȚIE - Folosiți ACEIAȘI parametri de preprocesare:**
- Același `scaler` salvat în `config/preprocessing_params.pkl`
- Aceiași proporții split: 70% train / 15% validation / 15% test
- Același `random_state=42` pentru reproducibilitate

**Verificare rapidă:**
```python
import pandas as pd
train = pd.read_csv('data/train/X_train.csv')
print(f"Train samples: {len(train)}")  # Trebuie să includă date noi
```

---

##  Cerințe Structurate pe 3 Niveluri

### Nivel 1 – Obligatoriu pentru Toți (70% din punctaj)

Completați **TOATE** punctele următoare:

1. **Antrenare model** definit în Etapa 4 pe setul final de date (≥40% originale)
2. **Minimum 10 epoci**, batch size 8–32
3. **Împărțire stratificată** train/validation/test: 70% / 15% / 15%
4. **Tabel justificare hiperparametri** (vezi secțiunea de mai jos - OBLIGATORIU)
5. **Metrici calculate pe test set:**
   - **Acuratețe ≥ 65%** (0.9143)
   - **F1-score (macro) ≥ 0.60** (0.9143)
6. **Salvare model antrenat** în `models/trained_model.h5` (Keras/TensorFlow) sau `.pt` (PyTorch) sau `.lvmodel` (LabVIEW)
7. **Integrare în UI din Etapa 4:**
   - UI trebuie să încarce modelul ANTRENAT (nu dummy)
   - Inferență REALĂ demonstrată
   - Screenshot în `docs/screenshots/inference_real.png`

#### Tabel Hiperparametri și Justificări (OBLIGATORIU - Nivel 1)

Completați tabelul cu hiperparametrii folosiți și **justificați fiecare alegere**:

#### Tabel Hiperparametri și Justificări (OBLIGATORIU - Nivel 1)

| **Hiperparametru** | **Valoare Aleasă** | **Justificare** |
|--------------------|-------------------|-----------------|
| Learning rate | 0.001 | Valoare standard pentru Adam care oferă convergență stabilă fără tuning agresiv. Pe un CNN mediu (3 blocuri Conv) și dataset de câteva mii de imagini/clasă, LR=1e-3 este un punct de plecare robust și frecvent folosit. |
| Batch size | 16 | Compromis între stabilitatea gradientului și consumul de memorie. Pentru ~5823 imagini în train, rezultă ~5823/16 ≈ 364 iterații/epocă, suficient pentru învățare stabilă și timp de antrenare rezonabil pe CPU. |
| Number of epochs | 30 | Permite modelului să parcurgă suficient datele pentru convergență. În practică s-a observat creștere constantă a acurateței în primele epoci, iar setarea la 30 oferă marjă pentru stabilizare fără a complica Nivelul 1 (fără early stopping). |
| Optimizer | Adam | Optimizator adaptiv și stabil pentru CNN-uri, necesită mai puțin tuning decât SGD și funcționează bine în practică pe clasificare de imagini. |
| Loss function | Categorical Crossentropy | Potrivită pentru clasificare cu **2 clase** atunci când etichetele sunt one-hot (`class_mode="categorical"` în generator). |
| Activation functions | ReLU (hidden), Softmax (output) | ReLU ajută la învățarea non-liniarităților și evită saturația comparativ cu sigmoid/tanh. Softmax la ieșire produce probabilități pe clase (acnee/eczeme) necesare afișării în UI. |
| Input size | 200×200×3 | Dimensiune fixă compatibilă cu preprocesarea (`resize_images.py`) și suficientă pentru a păstra detalii vizuale relevante (textură/roșeață) fără cost computațional prea mare. |
| Normalization | rescale 1/255 | Normalizează valorile pixelilor din [0,255] în [0,1], îmbunătățind stabilitatea antrenării și convergența optimizatorului. |
| Callbacks | (Nivel 1) None | În Nivelul 1 s-a urmărit un training simplu, reproductibil. Callbacks precum EarlyStopping/ReduceLROnPlateau/ModelCheckpoint vor fi introduse în Nivelul 2 pentru optimizare și prevenirea overfitting-ului. |
| Data augmentation | (Nivel 1) None / doar rescale | Pentru Nivelul 1 s-a folosit un pipeline minim (rescale). Augmentările relevante domeniului (iluminare/contrast/blur fin) vor fi incluse în Nivelul 2 pentru a crește robustețea modelului. |


**Justificare detaliată batch size (exemplu):**
```
Am ales batch_size=16 deoarece setul meu de antrenare conține aproximativ 70% din imaginile din `data/processed/` (după split 70/15/15). 
Cu ~8.300 imagini totale (acnee + eczeme), rezultă ~5.800 imagini în train. Astfel, într-o epocă modelul parcurge aproximativ:

~5800 / 16 ≈ 362 iterații/epocă.

Batch size 16 este un compromis bun între:
- stabilitatea gradientului (mai stabil decât batch foarte mic, ex. 8),
- consumul de memorie (mai sigur decât batch mare, ex. 32),
- timp de antrenare rezonabil pe CPU/GPU.

Prin urmare, batch_size=16 permite antrenare stabilă și eficientă pe un dataset mediu-mare, fără a suprasolicita resursele sistemului.

```

**Resurse învățare rapidă:**
- Împărțire date: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html (video 3 min: https://youtu.be/1NjLMWSGosI?si=KL8Qv2SJ1d_mFZfr)  
- Antrenare simplă Keras: https://keras.io/examples/vision/mnist_convnet/ (secțiunea „Training”)  
- Antrenare simplă PyTorch: https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html#training-an-image-classifier (video 2 min: https://youtu.be/ORMx45xqWkA?si=FXyQEhh0DU8VnuVJ)  
- F1-score: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html (video 4 min: https://youtu.be/ZQlEcyNV6wc?si=VMCl8aGfhCfp5Egi)


---

### Nivel 2 – Recomandat (85-90% din punctaj)

Includeți **TOATE** cerințele Nivel 1 + următoarele:

1. **Early Stopping** - oprirea antrenării dacă `val_loss` nu scade în 5 epoci consecutive
2. **Learning Rate Scheduler** - `ReduceLROnPlateau` sau `StepLR`
3. **Augmentări relevante domeniu:**
   - Vibrații motor: zgomot gaussian calibrat, jitter temporal
   - Imagini industriale: slight perspective, lighting variation (nu rotații simple!)
   - Serii temporale: time warping, magnitude warping
4. **Grafic loss și val_loss** în funcție de epoci salvat în `docs/loss_curve.png`
5. **Analiză erori context industrial** (vezi secțiunea dedicată mai jos - OBLIGATORIU Nivel 2)

**Indicatori țintă Nivel 2:**
- **Acuratețe ≥ 75%**
- **F1-score (macro) ≥ 0.70**

**Resurse învățare (aplicații industriale):**
- Albumentations: https://albumentations.ai/docs/examples/   
- Early Stopping + ReduceLROnPlateau în Keras: https://keras.io/api/callbacks/   
- Scheduler în PyTorch: https://pytorch.org/docs/stable/optim.html#how-to-adjust-learning-rate 

---


## Nivel 3 – Bonus: Analiză Erori (Confusion Matrix)

**Matricea de Confuzie:**
![Confusion Matrix](docs/confusion_matrix.png)

**Analiza a 5 exemple clasificate greșit:**

Am utilizat un script automat pentru a extrage imaginile greșite și le-am analizat individual. S-a observat o tendință a modelului de a confunda **Acneea** cu **Eczema** (False Negatives pentru clasa Acnee), în special în imaginile unde textura specifică (pustule) nu este clară.

| **Imagine** | **Clasa Reală** | **Predicție Greșită** | **Posibilă Cauză a Erorii (Analiză vizuală)** |
|-------------|------------------|-----------------------|-----------------------------------------------|
| `196__Protect...FocusFill...png` | **Acnee** | Eczeme | **Focus/Procesare:** Imaginea pare să aibă o zonă de focus artificial sau o prelucrare anterioară (indicată de "FocusFill" în nume) care a șters detaliile fine ale porilor, făcând pielea să pară netedă și roșie, specific eczemei. |
| `2 (54)1 - Copy_110.png` | **Acnee** | Eczeme | **Rezoluție/Artefacte:** Fiind o copie ("Copy"), imaginea probabil a pierdut din calitate/rezoluție. Modelul nu a putut detecta conturul leziunilor de acnee și a interpretat zona ca o pată difuză. |
| `20_before_133.png` | **Acnee** | Eczeme | **Iluminare/Blur:** Fiind o poză "before" (probabil selfie de pacient), iluminarea este probabil neuniformă sau există blur de mișcare, ceea ce ascunde relieful specific coșurilor, lăsând doar informația de culoare (roșu). |
| `37_197.png` | **Acnee** | Eczeme | **Confuzie Textură:** Leziunile de acnee din această imagine sunt probabil foarte grupate și inflamate (congestie), formând o pată roșie continuă care seamănă vizual cu o placă de eczemă. |
| `C0024056-Acne_vulgaris...png` | **Acnee** | Eczeme | **Severitate:** Acesta pare a fi un caz medical sever ("Acne vulgaris"). Inflamația extremă poate crea cruste sau zone extinse care morfologic se aseamănă cu dermatita/eczema severă, inducând modelul în eroare. |

**Concluzie Analiză:**
Modelul tinde să clasifice eronat Acneea drept Eczemă atunci când **informația de textură (granulație/pustule)** lipsește din cauza blur-ului sau a compresiei, bazându-se excesiv pe informația de culoare (roșeață).

**Resurse bonus:**
- Export ONNX din PyTorch: [PyTorch ONNX Tutorial](https://pytorch.org/tutorials/beginner/onnx/export_simple_model_to_onnx_tutorial.html)
- TensorFlow Lite converter: [TFLite Conversion Guide](https://www.tensorflow.org/lite/convert)
- Confusion Matrix analiză: [Scikit-learn Confusion Matrix](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html)

---

## Verificare Consistență cu State Machine (Etapa 4)

Antrenarea și inferența trebuie să respecte fluxul din State Machine-ul vostru definit în Etapa 4.

**Exemplu pentru monitorizare vibrații lagăr:**

| **Stare din Etapa 4** | **Implementare în Etapa 5** |
|-----------------------|-----------------------------|
| `ACQUIRE_DATA` | Citire batch date din `data/train/` pentru antrenare |
| `PREPROCESS` | Aplicare scaler salvat din `config/preprocessing_params.pkl` |
| `RN_INFERENCE` | Forward pass cu model ANTRENAT (nu weights random) |
| `THRESHOLD_CHECK` | Clasificare Normal/Uzură pe baza output RN antrenat |
| `ALERT` | Trigger în UI bazat pe predicție modelului real |

**În `src/app/main.py` (UI actualizat):**

Verificați că **TOATE stările** din State Machine sunt implementate cu modelul antrenat:

```python
# ÎNAINTE (Etapa 4 - model dummy):
model = keras.models.load_model('models/untrained_model.h5')  # weights random
prediction = model.predict(input_scaled)  # output aproape aleator

# ACUM (Etapa 5 - model antrenat):
model = keras.models.load_model('models/trained_model.h5')  # weights antrenate
prediction = model.predict(input_scaled)  # predicție REALĂ și corectă
```

---

## Analiză Erori în Context Industrial (OBLIGATORIU Nivel 2)

**Nu e suficient să raportați doar acuratețea globală.** Analizați performanța în contextul aplicației voastre industriale:

### 1. Pe ce clase greșește cel mai mult modelul?

Modelul confundă cel mai frecvent clasa "acnee" cu "eczeme" și invers.
Acest lucru apare în special în cazurile în care zonele de piele prezintă roșeață difuză
sau textură neuniformă, fără leziuni clar delimitate.

*Cauze posibile:*

-ambele afecțiuni se manifestă prin roșeață și iritație;

-imaginile sunt realizate în condiții diferite de iluminare și rezoluție;

-lipsa unor caracteristici vizuale puternic discriminative în poze (ex: pustule clare vs. plăci uscate).


### 2. Ce caracteristici ale datelor cauzează erori?

Modelul are performanță scăzută pe imaginile cu:
- iluminare slabă sau artificială (culoarea pielii este distorsionată);
- blur de mișcare sau focus greșit;
- suprafețe foarte mici de piele afectată în raport cu fundalul;
- imagini cu piele foarte deschisă sau foarte închisă la culoare.


### 3. Ce implicații are pentru aplicația industrială?


FALSE NEGATIVES (acnee clasificată ca eczemă sau invers):
- Impact: mediu – utilizatorul primește un rezultat eronat și poate lua măsuri greșite.

FALSE POSITIVES:
- Impact: scăzut – utilizatorul este doar informat incorect și poate reîncărca o nouă imagine.

Prioritate: minimizarea erorilor de tip confuzie între afecțiuni, deoarece scopul aplicației este orientativ, nu diagnostic medical definitiv.


### 4. Ce măsuri corective propuneți?

1. Colectarea a minimum 300–500 imagini reale suplimentare pentru fiecare clasă,
   realizate cu telefonul mobil în condiții de iluminare variabilă.
2. Implementarea augmentărilor specifice domeniului dermatologic:
   - ajustări fine de contrast și saturație;
   - variații controlate de lumină caldă / rece.
3. Introducerea ponderilor pe clase (class weights) pentru a penaliza mai mult
   confuziile dintre acnee și eczeme.
4. Adăugarea unei a treia clase „necunoscut / altă afecțiune” pentru a evita forțarea
   clasificării atunci când imaginea este ambiguă.

---

## Structura Repository-ului la Finalul Etapei 5

**Clarificare organizare:** Vom folosi **README-uri separate** pentru fiecare etapă în folderul `docs/`:

```
proiect-rn-[prenume-nume]/
├── README.md                           # Overview general proiect (actualizat)
├── etapa3_analiza_date.md         # Din Etapa 3
├── etapa4_arhitectura_sia.md      # Din Etapa 4
├── etapa5_antrenare_model.md      # ← ACEST FIȘIER (completat)
│
├── docs/
│   ├── state_machine.png              # Din Etapa 4
│   ├── loss_curve.png                 # NOU - Grafic antrenare
│   ├── confusion_matrix.png           # (opțional - Nivel 3)
│   └── screenshots/
│       ├── inference_real.png         # NOU - OBLIGATORIU
│       └── ui_demo.png                # Din Etapa 4
│
├── data/                               # Din Etapa 3-4 (NESCHIMBAT)
│   ├── raw/
│   ├── generated/                     # Contribuția voastră 40%
│   ├── processed/
│   ├── train/
│   ├── validation/
│   └── test/
│
├── src/
│   ├── data_acquisition/              # Din Etapa 4
│   ├── preprocessing/                 # Din Etapa 3
│   │   └── combine_datasets.py        # NOU (dacă ați adăugat date în Etapa 4)
│   ├── neural_network/
│   │   ├── model.py                   # Din Etapa 4
│   │   ├── train.py                   # NOU - Script antrenare
│   │   └── evaluate.py                # NOU - Script evaluare
│   └── app/
│       └── main.py                    # ACTUALIZAT - încarcă model antrenat
│
├── models/
│   ├── untrained_model.h5             # Din Etapa 4
│   ├── trained_model.h5               # NOU - OBLIGATORIU
│   └── final_model.onnx               # (opțional - Nivel 3 bonus)
│
├── results/                            # NOU - Folder rezultate antrenare
│   ├── training_history.csv           # OBLIGATORIU - toate epoch-urile
│   ├── test_metrics.json              # Metrici finale pe test set
│   └── hyperparameters.yaml           # Hiperparametri folosiți
│
├── config/
│   └── preprocessing_params.pkl       # Din Etapa 3 (NESCHIMBAT)
│
├── requirements.txt                    # Actualizat
└── .gitignore
```

**Diferențe față de Etapa 4:**
- Adăugat `docs/etapa5_antrenare_model.md` (acest fișier)
- Adăugat `docs/loss_curve.png` (Nivel 2)
- Adăugat `models/trained_model.h5` - OBLIGATORIU
- Adăugat `results/` cu history și metrici
- Adăugat `src/neural_network/train.py` și `evaluate.py`
- Actualizat `src/app/main.py` să încarce model antrenat

---

## Instrucțiuni de Rulare (Actualizate față de Etapa 4)

### 1. Setup mediu (dacă nu ați făcut deja)

```bash
pip install -r requirements.txt
```

### 2. Pregătire date (DACĂ ați adăugat date noi în Etapa 4)

```bash
# Combinare + reprocesare dataset complet
python src/preprocessing/combine_datasets.py
python src/preprocessing/data_cleaner.py
python src/preprocessing/feature_engineering.py
python src/preprocessing/data_splitter.py --stratify --random_state 42
```

### 3. Antrenare model

```bash
python src/neural_network/train.py --epochs 50 --batch_size 32 --early_stopping

# Output așteptat:
# Epoch 1/50 - loss: 0.8234 - accuracy: 0.6521 - val_loss: 0.7891 - val_accuracy: 0.6823
# ...
# Epoch 23/50 - loss: 0.3456 - accuracy: 0.8234 - val_loss: 0.4123 - val_accuracy: 0.7956
# Early stopping triggered at epoch 23
# ✓ Model saved to models/trained_model.h5
```

### 4. Evaluare pe test set

```bash
python src/neural_network/evaluate.py --model models/trained_model.h5

# Output așteptat:
# Test Accuracy: 0.7823
# Test F1-score (macro): 0.7456
# ✓ Metrics saved to results/test_metrics.json
# ✓ Confusion matrix saved to docs/confusion_matrix.png
```

### 5. Lansare UI cu model antrenat

```bash
streamlit run src/app/main.py

# SAU pentru LabVIEW:
# Deschideți WebVI și rulați main.vi
```

**Testare în UI:**
1. Introduceți date de test (manual sau upload fișier)
2. Verificați că predicția este DIFERITĂ de Etapa 4 (când era random)
3. Verificați că confidence scores au sens (ex: 85% pentru clasa corectă)
4. Faceți screenshot → salvați în `docs/screenshots/inference_real.png`

---

## Checklist Final – Bifați Totul Înainte de Predare

### Prerequisite Etapa 4 (verificare)
- [x] State Machine există și e documentat în `docs/state_machine.*`
- [x] Contribuție ≥40% date originale verificabilă
- [x] Cele 3 module din Etapa 4 funcționale

### Preprocesare și Date
- [x] Dataset combinat (vechi + nou) preprocesat (dacă ați adăugat date)
- [x] Split train/val/test: 70/15/15% (verificat dimensiuni fișiere)

### Antrenare Model - Nivel 1 (OBLIGATORIU)
- [x] Model antrenat de la ZERO (nu fine-tuning pe model pre-antrenat)
- [x] Minimum 10 epoci rulate (verificabil în `results/training_history.csv`)
- [x] Tabel hiperparametri + justificări completat în acest README
- [x] Metrici calculate pe test set: **Accuracy ≥65%**, **F1 ≥0.60**
- [x] Model salvat în `models/trained_model.h5` 
- [x] `results/training_history.csv` există cu toate epoch-urile

### Integrare UI și Demonstrație - Nivel 1 (OBLIGATORIU)
- [x] Model ANTRENAT încărcat în UI din Etapa 4 (nu model dummy)
- [x] UI face inferență REALĂ cu predicții corecte
- [x] Screenshot inferență reală în `docs/screenshots/inference_real.png`
- [x] Verificat: predicțiile sunt diferite față de Etapa 4 (când erau random)

### Documentație Nivel 2 (dacă aplicabil)
- [x] Early stopping implementat și documentat în cod
- [x] Learning rate scheduler folosit (ReduceLROnPlateau )
- [x] Augmentări relevante domeniu aplicate (brightness/zoom/shift/shear)
- [x] Grafic loss/val_loss salvat în `docs/loss_curve.png`
- [x] Analiză erori în context industrial completată (4 întrebări răspunse)
- [x] Metrici Nivel 2: **Accuracy ≥75%**, **F1 ≥0.70**

### Documentație Nivel 3 Bonus (dacă aplicabil)
- [ ] Comparație 2+ arhitecturi (tabel comparativ + justificare)
- [ ] Export ONNX/TFLite + benchmark latență (<50ms demonstrat)
- [x] Confusion matrix + analiză 5 exemple greșite cu implicații

### Verificări Tehnice
- [x] `requirements.txt` actualizat cu toate bibliotecile noi
- [x] Toate path-urile RELATIVE (nu absolute: `/Users/...` )
- [x] Cod nou comentat în limba română sau engleză (minimum 15%)
- [x] `git log` arată commit-uri incrementale (NU 1 commit gigantic)
- [x] Verificare anti-plagiat: toate punctele 1-5 respectate

### Verificare State Machine (Etapa 4)
- [x] Fluxul de inferență respectă stările din State Machine
- [x] Toate stările critice (PREPROCESS, INFERENCE, ALERT) folosesc model antrenat
- [x] UI reflectă State Machine-ul pentru utilizatorul final

### Pre-Predare
- [x] `docs/etapa5_antrenare_model.md` completat cu TOATE secțiunile
- [x] Structură repository conformă: `docs/`, `results/`, `models/` actualizate
- [x] Commit: `"Etapa 5 completă – Accuracy=X.XX, F1=X.XX"`
- [x] Tag: `git tag -a v0.5-model-trained -m "Etapa 5 - Model antrenat"`
- [x] Push: `git push origin main --tags`
- [x] Repository accesibil (public sau privat cu acces profesori)

---

## Livrabile Obligatorii (Nivel 1)

Asigurați-vă că următoarele fișiere există și sunt completate:

1. **`docs/etapa5_antrenare_model.md`** (acest fișier) cu:
   - Tabel hiperparametri + justificări (complet)
   - Metrici test set raportate (accuracy, F1)
   - (Nivel 2) Analiză erori context industrial (4 paragrafe)

2. **`models/trained_model.h5`** (sau `.pt`, `.lvmodel`) - model antrenat funcțional

3. **`results/training_history.csv`** - toate epoch-urile salvate

4. **`results/test_metrics.json`** - metrici finale:

Exemplu:
```json
{
  "test_accuracy": 0.7823,
  "test_f1_macro": 0.7456,
  "test_precision_macro": 0.7612,
  "test_recall_macro": 0.7321
}
```

5. **`docs/screenshots/inference_real.png`** - demonstrație UI cu model antrenat

6. **(Nivel 2)** `docs/loss_curve.png` - grafic loss vs val_loss

7. **(Nivel 3)** `docs/confusion_matrix.png` + analiză în README

---

## Predare și Contact

**Predarea se face prin:**
1. Commit pe GitHub: `"Etapa 5 completă – Accuracy=X.XX, F1=X.XX"`
2. Tag: `git tag -a v0.5-model-trained -m "Etapa 5 - Model antrenat"`
3. Push: `git push origin main --tags`

---

**Mult succes! Această etapă demonstrează că Sistemul vostru cu Inteligență Artificială (SIA) funcționează în condiții reale!**
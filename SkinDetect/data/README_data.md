# Dataset – SkinDetect

Acest director conține toate datele utilizate în proiectul **SkinDetect**, inclusiv date brute, date preprocesate și seturile împărțite pentru antrenare, validare și testare.

---

## Structura directorului

data/
│
├── raw/ # Imagini originale (date brute)
├── processed/ # Imagini redimensionate și curățate
├── train/ # Set de antrenare (~70%)
├── validation/ # Set de validare (~15%)
├── test/ # Set de test (~15%)
├── train_generated/ # Imagini generate suplimentar (augmentare offline)
│
├── dataset_log.csv # Evidența imaginilor și operațiilor efectuate
├── recommendations.csv # Recomandări generate de aplicație (dacă există)
└── README_data.md # Documentație detaliată dataset


---

## Descriere foldere

### `raw/`
Conține imaginile originale colectate din surse externe (Kaggle, DermNet etc.).  
Aceste date nu sunt modificate și reprezintă punctul de plecare al pipeline-ului.

---

### `processed/`
Imagini preprocesate:
- redimensionate la dimensiunea utilizată de model (200x200)
- curățate (eliminare fișiere corupte sau nevalide)
- organizate pe clase

Aceste date sunt folosite pentru împărțirea în train/validation/test.

---

### `train/`
Set utilizat pentru antrenarea modelului.


---

### `validation/`
Set utilizat pentru:
- monitorizarea performanței în timpul antrenării
- EarlyStopping
- ajustarea hiperparametrilor

---

### `test/`
Set utilizat exclusiv pentru evaluarea finală a modelului.

Acest set nu este folosit în procesul de antrenare.

---

### `train_generated/`
Conține imagini suplimentare obținute prin augmentare offline (rotații, zoom, variații de iluminare etc.).

Notă: În versiunea finală a proiectului, augmentarea este aplicată dinamic în timpul antrenării, astfel încât acest folder este utilizat doar pentru experimente anterioare.

---

## Fișiere suplimentare

### `dataset_log.csv`
Conține informații despre:
- numărul de imagini pe clasă
- sursa datelor
- operații de preprocesare efectuate

---

### `recommendations.csv`
Fișier generat de aplicație pentru salvarea recomandărilor sau rezultatelor inferenței (dacă funcționalitatea este activată).

---

## Distribuția datelor

Împărțirea dataset-ului:
- Train: ~70%
- Validation: ~15%
- Test: ~15%

Împărțirea a fost realizată folosind un split stratificat pentru a păstra distribuția claselor.

---

## Clase

Proiectul clasifică două tipuri de afecțiuni dermatologice:
- **Acnee**
- **Eczeme**

---

## Surse date

- Kaggle – Skin Disease Datasets  
- DermNet NZ – Dermatology Image Library  

---



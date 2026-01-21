# Preprocessing Pipeline (Etapa 3–4)

Acest folder conține scripturile care pregătesc imaginile dermatologice pentru antrenarea unei rețele neuronale de clasificare (acnee vs eczeme).

Pipeline-ul corect este:

1) `raw → processed` (standardizare imagini)
2) `processed → train/validation/test` (split corect, fără data leakage)
3) `train → train_generated` (augmentare DOAR pe train)

---


## 1. resize_images.py — RAW → PROCESSED

**Scop:** standardizarea imaginilor brute pentru a putea fi utilizate ca intrare în modelul RN și în LabVIEW.

**Funcționalități:**
- citește imaginile din `data/raw/acnee` și `data/raw/eczeme`;
- convertește fiecare imagine în format RGB;
- redimensionează imaginile la dimensiune fixă **200×200 px**, păstrând proporțiile prin padding;
- șterge automat conținutul anterior din `data/processed/` pentru a evita duplicatele;
- salvează rezultatul în `data/processed/<clasă>/`.

Acest pas elimină variațiile de rezoluție și asigură o intrare uniformă pentru rețeaua neuronală.

---

## 2. split_dataset.py — PROCESSED → TRAIN/VALIDATION/TEST

**Scop:** separarea corectă a datasetului pentru antrenare și evaluare.

**Funcționalități:**
- citește imaginile din `data/processed/<clasă>/`;
- împarte datele în:
  - 70% `train`
  - 15% `validation`
  - 15% `test`
- șterge automat seturile generate anterior pentru a preveni acumularea de fișiere;
- salvează imaginile în:
  - `data/train/<clasă>/`
  - `data/validation/<clasă>/`
  - `data/test/<clasă>/`.

Split-ul se realizează **înainte de augmentare** pentru a preveni apariția de data leakage.

---

## 3. augment_train.py — TRAIN → TRAIN_GENERATED

**Scop:** creșterea diversității datelor de antrenare fără a altera seturile de validare și test.

**Funcționalități:**
- citește imaginile exclusiv din `data/train/<clasă>/`;
- aplică transformări realiste care simulează condiții reale de captură:
  - variații de luminozitate, contrast și saturație;
  - zgomot gaussian (simulare ISO);
  - blur ușor (defocus / mișcare);
  - compresie JPEG (simulare upload web / WhatsApp);
  - vignette și mici rotații/translații;
- salvează imaginile augmentate în `data/train_generated/<clasă>/`;
- șterge automat conținutul anterior din `data/train_generated/`.

Augmentarea se aplică **doar pe setul de train**, pentru a evita contaminarea seturilor de validare și test cu variații ale acelorași imagini.

**De ce augmentarea se aplică doar pe o fracțiune a imaginilor din train**

Setul de date utilizat în acest proiect conține deja un număr mare de imagini reale (peste 8000 observații). În aceste condiții, augmentarea nu mai este necesară pentru fiecare imagine, deoarece beneficiul asupra performanței modelului scade semnificativ după un anumit volum de date.

Pentru a păstra un echilibru între diversitatea datelor și costul computațional, augmentarea este aplicată doar pe o fracțiune a setului de antrenare (de exemplu 50%). Această abordare:
- previne creșterea inutilă a dimensiunii datasetului;
- reduce timpul de antrenare;
- păstrează totodată avantajele augmentării, forțând modelul să învețe caracteristici robuste la variații de iluminare, zgomot și poziționare.

Această strategie este frecvent utilizată în aplicații reale cu volume mari de date.

---

## Dependențe

- Pillow
- numpy
- scikit-learn

Instalare: pip install pillow numpy scikit-learn


---

## Ordine recomandată de rulare (IMPORTANT)

1. Resize: python src/preprocessing/resize_images.py
2. Split: python src/preprocessing/split_dataset.py
3. Augment train: python src/preprocessing/augment_train.py


După acești pași, proiectul are datele pregătite pentru definirea și compilarea modelului RN și pentru conectarea la UI/Web Service.


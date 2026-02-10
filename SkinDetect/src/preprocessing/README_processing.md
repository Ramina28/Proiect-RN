---

## 🧰 Preprocesare date (resize / split / augmentare offline)

---

### 1) `resize_images.py` — Preprocesare: resize la 200x200 cu padding (din raw → processed)
**Ce face:**
- Ia imaginile brute din:
  - `data/raw/acnee`
  - `data/raw/eczeme`
- Le redimensionează la **200x200** păstrând proporțiile (fără deformare), folosind **padding negru**.
- Salvează imaginile procesate în `data/processed/<clasă>/...`.
- La fiecare rulare, **șterge complet folderul `data/processed`** ca să nu rămână duplicate din rulări anterioare.

**De unde citește (input):**
- `data/raw/` (hard setat ca `INPUT_BASE_DIR`)

**Ce produce (output):**
- Folder: `data/processed/`
  - `data/processed/acnee/*.png`
  - `data/processed/eczeme/*.png`

**Detalii importante:**
- Numele fișierelor de output devin: `originalName_<index>.png` (index global cumulativ în timpul procesării).
- Scriptul raportează câte imagini a procesat și câte erori au apărut.
:contentReference[oaicite:0]{index=0}

---

### 2) `split_dataset.py` — Split dataset: processed → train/validation/test
**Ce face:**
- Ia imaginile din `data/processed/<clasă>/`.
- Împarte imaginile pe clase în:
  - **train = 70%**
  - **validation = 15%**
  - **test = 15%**
- Copiază fișierele în:
  - `data/train/<clasă>/`
  - `data/validation/<clasă>/`
  - `data/test/<clasă>/`

**De unde citește (input):**
- `data/processed/`

**Ce produce (output):**
- `data/train/`
- `data/validation/`
- `data/test/`

**Detalii importante:**
- Folosește `train_test_split` (sklearn) cu `SEED=42` → split **reproductibil**.

---
### 3) `check_split.py` — Verificare rapidă a dataset-ului
**Ce face:**
Script de verificare (sanity check) pentru setul de antrenare.

- Verifică existența folderelor:
  - `data/train/acnee`
  - `data/train/eczeme`
- Numără imaginile din fiecare clasă.
- Afișează în consolă distribuția și totalul imaginilor din train.

**De unde citește:**
- `data/train/`

**Ce produce:**
- Nu creează fișiere.
- Afișează doar informații în terminal.

**Scop:**
Util pentru a verifica rapid dacă:
- split-ul a fost realizat corect
- nu lipsesc foldere
- distribuția claselor este corectă.

---

### 4) `augment_train.py` — Augmentare offline: generează imagini sintetice (train → train_generated)
**Ce face:**
- Creează imagini **augmentate offline** pornind de la `data/train/<clasă>/`.
- Pentru fiecare imagine din train, poate genera `N_AUG_PER_IMAGE` imagini sintetice folosind un pipeline realist:
  - translație ușoară
  - rotație mică
  - brightness/contrast/color jitter
  - vignette (iluminare neuniformă)
  - gaussian noise
  - blur ușor (defocus)
  - simulare compresie JPEG (WhatsApp/upload)
- Salvează imaginile augmentate într-un folder separat: `data/train_generated/<clasă>/`.
- La fiecare rulare, **șterge complet `data/train_generated/`** și regenerează tot.

**De unde citește (input):**
- `data/train/`

**Ce produce (output):**
- `data/train_generated/`
  - `data/train_generated/acnee/*_syn1.png`
  - `data/train_generated/eczeme/*_syn1.png`

**Parametri importanți (config):**
- `N_AUG_PER_IMAGE = 1` → câte imagini sintetice per imagine originală
- `AUGMENT_FRACTION = 1.0` → procentul de imagini din train care vor fi augmentate (1.0 = toate)
- `SEED = 42` → augmentare mai reproductibilă (random + numpy seed)

**Notă:**
- Scriptul generează doar imaginile sintetice (nu copiază și imaginile originale în `train_generated`).  
  Dacă vrei `train_generated` să conțină și originale + augmentate, trebuie adăugat un pas de copy.
:contentReference[oaicite:2]{index=2}

## 🔁 De ce am trecut de la augmentare offline (`train_generated/`) la augmentare direct în training?

Inițial am experimentat cu **augmentare offline**, adică generam imagini sintetice în plus cu `augment_train.py` și le salvam într-un folder separat (`data/train_generated/`). Scopul era să măresc setul de antrenare și să reduc overfitting-ul.

Ulterior am trecut la varianta recomandată în practică: **augmentare direct în timpul antrenării** (online augmentation), folosind `ImageDataGenerator` în `train.py` / `train_optimized.py`.

###  De ce augmentarea direct în training este mai bună
- **Nu dublează/umflă dataset-ul pe disc:** nu mai salvez mii de imagini noi; setul rămâne curat și mic.
- **Generează variații diferite la fiecare epocă:** modelul vede “alte versiuni” ale aceleiași imagini de fiecare dată, ceea ce crește generalizarea mai mult decât un set fix de augmentări offline.
- **Pipeline mai simplu și mai reproductibil:** nu mai există folder intermediar (`train_generated`) care poate rămâne vechi sau inconsistent; antrenarea pornește direct din `data/train`.
- **Mai puțin risc de erori (duplicate / leak / mix train-test):** când creezi seturi noi offline, crește riscul să copiezi greșit imagini sau să apară duplicate între foldere; augmentarea online păstrează split-ul original intact.

### Concluzie
`augment_train.py` a fost util pentru explorare și testare. În varianta finală a proiectului, augmentarea este făcută **direct în etapa de training**, iar folderul `train_generated/` nu mai este folosit.


---

**Cum se rulează:**
```bash
python preprocessing/resize_imges.py
python preprocessing/split_dataset.py
python preprocessing/check_split.py
python preprocessing/augment_train.py
# 📘 README – Etapa 3: Analiza și Pregătirea Setului de Date pentru Rețele Neuronale

**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** Găitan Ramina Alessandra 
**Data:** 26.11.2025  

---

## Introducere

Acest document descrie activitățile realizate în **Etapa 3**, în care se analizează și se preprocesează setul de date necesar proiectului „Rețele Neuronale". Scopul etapei este pregătirea corectă a datelor pentru instruirea modelului RN, respectând bunele practici privind calitatea, consistența și reproductibilitatea datelor.

---

##  1. Structura Repository-ului Github (versiunea Etapei 3)

```
project-name/
├── README.md
├── docs/
│   └── datasets/          # descriere seturi de date, surse, diagrame
├── data/
│   ├── raw/               # date brute
│   ├── processed/         # date curățate și transformate
│   ├── train/             # set de instruire
│   ├── validation/        # set de validare
│   └── test/              # set de testare
├── src/
│   ├── preprocessing/     # funcții pentru preprocesare
│   ├── data_acquisition/  # generare / achiziție date (dacă există)
│   └── neural_network/    # implementarea RN (în etapa următoare)
├── config/                # fișiere de configurare
└── requirements.txt       # dependențe Python (dacă aplicabil)
```

---

##  2. Descrierea Setului de Date

### 2.1 Sursa datelor

* **Origine:** imagini dermatologice preluate dintr-o bază de date publică online
* **Modul de achiziție:** ☑ Fișier extern - Imaginile au fost descărcate individual și filtrate vizual înainte de includerea în dataset.
* **Perioada / condițiile colectării:**  Noiembrie–Decembrie 2025  ,  Colectarea s-a realizat manual prin selecție vizuală, urmărindu-se claritatea leziunii, focalizarea corectă și relevanța dermatologică.

### 2.2 Caracteristicile dataset-ului

* **Număr total de observații:** 423 (141 originale + 282 augmentate)
* **Număr de caracteristici (features):** 3
* **Tipuri de date:** ☑ Imagini
* **Format fișiere:** ☑ PNG   ☑ JPG / JPEG

### 2.3 Descrierea fiecărei caracteristici

| **Caracteristică** | **Tip** | **Unitate** | **Descriere** | **Domeniu valori** |
|-------------------|---------|-------------|---------------|--------------------|
| Canal R        | numeric | intensitate pixel | Componenta roșie pentru fiecare pixel | 0–255 |
| Canal G        | numeric | intensitate pixel | Componenta verde | 0–255 |
| Canal B        | numeric | intensitate pixel | Componenta albastră | 0–255 |
| Width          | numeric | px | Lățime imagine, standardizată prin resize | 200 |
| Height         | numeric | px | Înălțime variabilă proporțional | ~200–400 |
| Label (clasă)  | categorial | - | Categoria dermatologică asociată imaginii | {acnee, eczemă, roșeață} |

**Fișier recomandat:**  `data/README.md`

---

##  3. Analiza Exploratorie a Datelor (EDA) – Sintetic

### 3.1 Statistici descriptive aplicate

În cazul dataset-ului bazat pe imagini dermatologice, analiza statistică se referă la dimensiuni și distribuții vizuale:

* **Medie, mediană, deviație standard** pentru intensitatea pixelilor pe canale RGB
→ nu au fost identificate deviații extreme sau modificări nenaturale ale culorii.
* **Min–max și quartile**
→ valorile pixelilor se află constant în intervalul 0–255 (normal pentru imagini RGB).
* **Distribuții pe caracteristici** (histograme)
→ histogramă RGB arată variații de iluminare între imagini (motivul pentru care augmentarea era necesară).
* **Identificarea outlierilor** (IQR / percentile)
→ au fost detectate câteva imagini neclare sau irelevante, eliminate înainte de preprocesare.

### 3.2 Analiza calității datelor

* **Detectarea valorilor lipsă** 
→ nu există imagini corupte sau incomplete (0% valori lipsă).
* **Detectarea valorilor inconsistente sau eronate**
→ unele imagini au iluminare foarte diferită; rezolvat prin augmentare (luminozitate, contrast, color shift)
* **Identificarea caracteristicilor redundante sau puternic corelate**
→ nu se aplică ca indicator numeric, însă imaginile din aceeași clasă pot fi vizual similare → augmentarea mărește diversitatea.

### 3.3 Probleme identificate

* Dezechilibru între clase (class imbalance):

Acnee = 53 imagini

Eczemă = 63 imagini

Roșeață = 25 imagini (semnificativ mai puține)
➤ Corectat prin generarea a 2 augmentări per imagine.

* Iluminare și contrast neuniform între surse
➤ soluție: augmentare cu modificări lumină/contrast + noise mic + blur controlat.

* Rezoluții inițiale diferite
➤ soluție: resize standard 200px și conversie uniformă RGB.

##  4. Preprocesarea Datelor

### 4.1 Curățarea datelor
Întrucât datasetul conține imagini, nu tabele numerice, etapa de curățare s-a realizat vizual și structural, nu prin imputare numerică.
* **Eliminare duplicatelor**
 → au fost eliminate imagini foarte asemănătoare sau duplicate descărcate din aceeași sursă
* **Tratarea valorilor lipsă:**
  → nu există imagini corupte sau incomplete; 0% lipsă
(nu este necesară imputare statistică în cazul imaginilor)
* **Tratarea outlierilor:** s
→ imagini neclare / incomplet cadrate / necentrate au fost eliminate manual
→ rezoluțiile diferite au fost uniformizate ulterior prin resize

### 4.2 Transformarea caracteristicilor

* **Normalizare:** implicită prin transformare RGB 0–255 → transmisibil ulterior ca 0–1 pentru model
* **Encoding pentru variabile categoriale**
* **Ajustarea dezechilibrului de clasă** 
→ clasa roșeață având mai puține imagini, datasetul a fost extins prin 2 augmentări per imagine

### 4.3 Structurarea seturilor de date

**Împărțire recomandată:**
* 70–80% – train
* 10–15% – validation
* 10–15% – test

**Principii respectate:**
* Stratificare pentru clasificare
* Fără scurgere de informație (data leakage)
* Statistici calculate DOAR pe train și aplicate pe celelalte seturi

### 4.4 Salvarea rezultatelor preprocesării

* Date preprocesate în `data/processed/`
* Seturi train/val/test în foldere dedicate
* Parametrii de preprocesare în `config/preprocessing_config.*` (opțional)

---

##  5. Fișiere Generate în Această Etapă

* `data/raw/` – date brute
* `data/processed/` – date curățate & transformate
* `data/train/`, `data/validation/`, `data/test/` – seturi finale
* `src/preprocessing/` – codul de preprocesare
* `data/README.md` – descrierea dataset-ului

---

##  6. Stare Etapă (de completat de student)

- [x] Structură repository configurată
- [x] Dataset analizat (EDA realizată)
- [x] Date preprocesate
- [ ] Seturi train/val/test generate
- [x] Documentație actualizată în README + `data/README.md`

---

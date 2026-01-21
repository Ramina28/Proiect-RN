# 🧠 Modulul Neural Network

Acest director conține "creierul" proiectului SkinDetect. Aici se află scripturile care definesc arhitectura Rețelei Neurale (CNN), logica de antrenare și scripturile de evaluare a performanței.

Modulul este împărțit în două etape de dezvoltare: **Baseline (Etapa 4-5)** și **Optimizat (Etapa 6)**.

---

## 📂 Descrierea Fișierelor

### 1. Arhitectura Modelului (Scheletul)
* **`model.py` (Versiunea Veche - Baseline):**
    * Definește o rețea CNN simplă (Sequential) cu 3 blocuri convoluționale.
    * A fost folosită în primele etape pentru a valida că pipeline-ul funcționează.
    * *Limitare:* Tindea să facă overfitting (memora pozele) și nu avea mecanisme de regularizare.

* **`optimize.py` (Versiunea Nouă - Optimizată):**
    * Este evoluția lui `model.py`.
    * Definește arhitectura finală, îmbunătățită pentru a rezolva problemele observate (confuzia Acnee/Eczeme).
    * **Ce aduce în plus:**
        * **Strat de Dropout (0.3):** Oprește 30% din neuroni aleatoriu la fiecare pas de antrenare. Asta forțează rețeaua să învețe trăsături robuste, nu să memoreze zgomotul.
        * **Filtre ajustate:** Numărul de filtre a fost calibrat pentru complexitatea datelor dermatologice.

### 2. Antrenarea (Motorul)
* **`train.py` (Versiunea Veche):**
    * Scriptul de bază care antrenează modelul definit în `model.py`.
    * Folosea augmentări minime și salva modelul ca `trained_model.h5`.

* **`train_optimized.py` (Versiunea Nouă):**
    * Scriptul avansat care antrenează modelul definit în `optimize.py`.
    * **Îmbunătățiri majore:**
        * **Augmentare Avansată:** Introduce variații de luminozitate (`brightness_range`), zoom și rotație pentru a simula condiții reale de fotografiere (poze întunecate, neclare).
        * **Gestionare Căi:** Detectează automat dacă datele sunt în `data/processed` sau `data/raw`.
        * **Callbacks:** Folosește `EarlyStopping` (oprește antrenarea dacă nu mai învață) și `ReduceLROnPlateau` (micșorează pasul de învățare pentru finețe).
        * Salvează rezultatul final ca **`models/optimized_model.h5`**.

### 3. Evaluarea (Testarea)
* **`evaluate.py`:**
    * Acest script este "examinatorul". Este agnostic la model (nu îi pasă cum a fost antrenat).
    * Încarcă un model `.h5` și un set de date de test.
    * Generează metricile finale: Acuratețe, Matricea de Confuzie și Raportul de Clasificare.

---

## 🚀 Ce am adus în plus la Optimizare (Etapa 6)?

Trecerea de la `model.py` + `train.py` la `optimize.py` + `train_optimized.py` a rezolvat problema overfitting-ului și a crescut acuratețea (de la ~65% la ~87%).

| Componentă | Varianta Baseline | Varianta Optimizată | Beneficiu |
| :--- | :--- | :--- | :--- |
| **Arhitectură** | CNN Simplu | **CNN + Dropout** | Previne memorarea fundalului imaginilor. |
| **Date** | Augmentare simplă | **Augmentare Fotometrică** | Modelul recunoaște boala și în lumină slabă/puternică. |
| **Loss Function** | Categorical Crossentropy | **Sparse Categorical** | Mai eficient pentru etichete integer. |
| **Monitoring** | Loss | **Accuracy** | Monitorizăm direct metrica ce ne interesează. |

---

## 💻 Cum se rulează

**Pentru a antrena modelul final (Optimizat):**
```bash
cd src/neural_network
python train_optimized.py
# 🖥️ main.py — SkinDetect AI (Interfață Gradio)

`main.py` este aplicația principală (UI) a proiectului **SkinDetect**. Scriptul pornește o interfață web (Gradio) în care utilizatorul încarcă o fotografie a unei leziuni, iar sistemul:
1) face preprocesarea imaginii (resize + normalizare),
2) rulează modelul CNN antrenat (preferă modelul optimizat),
3) afișează probabilitățile pe clase (Acnee/Eczeme),
4) aplică un prag de încredere (confidence threshold) pentru cazurile incerte,
5) afișează recomandări (dintr-un fișier CSV) în funcție de clasă.

---

## 1) Scop și rol în proiect

- `main.py` este **punctul de intrare pentru demo**: nu antrenează modelul, ci doar îl folosește pentru inferență.
- Este gândit ca o aplicație “end-user friendly”:
  - încărcare imagine
  - buton de analiză
  - rezultate vizuale (bară de confidence / mesaj “traffic light”)
  - recomandări și disclaimere pentru utilizator

---

## 2) Resurse necesare (fișiere fără de care nu merge)

### 2.1 Modele
Aplicația caută automat modelul în folderul `models/`:
- preferă: `models/optimized_model.h5` (modelul final)
- fallback: `models/best_model.h5` (dacă optimized lipsește)

Dacă nu găsește niciun `.h5`, aplicația se oprește cu eroare critică. :

### 2.2 Fișier recomandări (CSV)
Aplicația citește recomandările din:
- `data/recommendations.csv`

Acest fișier este folosit ca “bază de cunoștințe” pentru:
- ce să faci (DO)
- ce să eviți (AVOID)
- când să mergi la medic (WHEN_TO_SEE_DOCTOR)
- disclaimer

CSV-ul poate fi exportat din Excel și uneori folosește separator `;` în loc de `,`, iar aplicația încearcă să detecteze automat delimiter-ul. 

---

## 3) Configurare & parametri importanți

### 3.1 Căi proiect
`PROJECT_ROOT` este setat relativ la locația fișierului `main.py`, astfel încât scriptul să poată fi rulat din proiect fără hardcodări de gen `C:\...`. 

### 3.2 Dimensiune input imagine
- `IMG_SIZE = (200, 200)`
Aceasta trebuie să coincidă cu ce ai folosit la antrenare/evaluare. 

### 3.3 Clase
- `CLASS_NAMES = ["Acnee", "Eczeme"]`
Aplicația presupune că modelul produce un vector de probabilități în ordinea:
- index 0 → Acnee
- index 1 → Eczeme 

### 3.4 Prag de încredere (confidence threshold)
- `CONF_THRESHOLD = 0.60`
Dacă modelul are o probabilitate maximă sub acest prag, aplicația consideră cazul “UNCERTAIN” pentru partea de recomandări (adică nu dă recomandări specifice unei boli, ci o variantă neutră/precaută). 

---

## 4) Încărcarea modelului (inferință)

La pornire:
- se alege modelul (optimized → best fallback),
- se încarcă cu `tf.keras.models.load_model(...)`,
- dacă încărcarea eșuează, UI nu pornește (aplicația ar ridica o eroare). 

---

## 5) Încărcarea recomandărilor din CSV

Există o funcție care:
- detectează separatorul (`;` vs `,`) printr-o “sniffing logic”
- citește fișierul cu encoding compatibil cu Excel (UTF-8 cu BOM)
- construiește un dicționar de forma:
  - `recs[label] = { solution_title, do, avoid, when_to_see_doctor, disclaimer }`

În aplicație, recomandările sunt afișate ca HTML formatat (card/box). 

---

## 6) Pipeline-ul de predicție (ce se întâmplă după ce încarci o imagine)

### 6.1 Preprocesare imagine
Când utilizatorul încarcă o imagine (PIL), scriptul:
- o aduce la dimensiunea `IMG_SIZE` (200x200),
- o transformă într-un tensor batch (shape tipic: `(1, 200, 200, 3)`),
- normalizează pixelii (0..1).

(*În cod există o funcție dedicată pentru preprocesare; UI-ul apelează această preprocesare înainte de predict.*) 

### 6.2 Predicție
Modelul returnează probabilități, iar scriptul interpretează:
- `p_acnee = preds[0]`
- `p_eczeme = preds[1]`

Apoi:
- `predicted_class` = clasa cu probabilitate mai mare
- `confidence` = probabilitatea maximă 

### 6.3 Pragul de siguranță
Dacă `confidence < CONF_THRESHOLD`:
- aplicația folosește label special `"UNCERTAIN"` pentru recomandări
- dar poate afișa în continuare probabilitățile (ca utilizatorul să înțeleagă “nesiguranța”) 

### 6.4 Output UI (3 tipuri de output)
Funcția de inferență întoarce 3 lucruri:
1) **Probabilități** (pentru componenta `gr.Label`) — ex: `{"Acnee": 0.72, "Eczeme": 0.28}`
2) **Status HTML** — un box cu mesaj + indicator de încredere (traffic light / bar)
3) **Recomandări HTML** — card cu “DO / AVOID / când mergi la medic / disclaimer” 

---

## 7) Interfața Gradio (UI)

UI-ul folosește `gr.Blocks` cu temă modernă și CSS custom:
- font Inter
- aspect tip “card”
- layout pe 2 coloane:
  - stânga: încărcare imagine + buton “Analizează”
  - dreapta: status + probabilități + recomandări

În plus, există o secțiune tip accordion “Detalii Tehnice” unde se afișează:
- ce model este activ
- dimensiunea input
- threshold
- dacă există recommendations.csv 

---

## 8) Fișiere generate de `main.py`
`main.py` este în principal un UI de inferență și:
- **nu antrenează**
- **nu salvează modele**
- în mod normal **nu produce fișiere noi** (doar afișează rezultate în interfață)

(Excepție: dacă în cod ai adăugat manual loguri/exports ulterior, dar în varianta curentă focusul e pe UI.) 

---

# ▶️ Cum se rulează

## 1) Cerințe
Ai nevoie de:
- Python 3.9+ (recomandat)
- TensorFlow
- Gradio
- NumPy
- Pillow

Instalare (varianta simplă):
```bash

pip install -r requirements.txt
python src/main.py



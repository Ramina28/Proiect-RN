# 📘 README – Etapa 4: Arhitectura Completă a Aplicației SIA bazată pe Rețele Neuronale

**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** Gaitan Ramina Alessandra  
**Link Repository GitHub** https://github.com/Ramina28/Proiect-RN.git
**Data:** 4.12.2025  
---

## Scopul Etapei 4

Această etapă corespunde punctului **5. Dezvoltarea arhitecturii aplicației software bazată pe RN** din lista de 9 etape - slide 2 **RN Specificatii proiect.pdf**.

**Trebuie să livrați un SCHELET COMPLET și FUNCȚIONAL al întregului Sistem cu Inteligență Artificială (SIA). In acest stadiu modelul RN este doar definit și compilat (fără antrenare serioasă).**

### IMPORTANT - Ce înseamnă "schelet funcțional":

 **CE TREBUIE SĂ FUNCȚIONEZE:**
- Toate modulele pornesc fără erori
- Pipeline-ul complet rulează end-to-end (de la date → până la output UI)
- Modelul RN este definit și compilat (arhitectura există)
- Web Service/UI primește input și returnează output

 **CE NU E NECESAR ÎN ETAPA 4:**
- Model RN antrenat cu performanță bună
- Hiperparametri optimizați
- Acuratețe mare pe test set
- Web Service/UI cu funcționalități avansate

**Scopul anti-plagiat:** Nu puteți copia un notebook + model pre-antrenat de pe internet, pentru că modelul vostru este NEANTRENAT în această etapă. Demonstrați că înțelegeți arhitectura și că ați construit sistemul de la zero.

---

##  Livrabile Obligatorii


### 1. Tabelul Nevoie Reală → Soluție SIA → Modul Software  

| **Nevoie reală concretă** | **Cum o rezolvă SIA-ul vostru** | **Modul software responsabil** |
|---------------------------|--------------------------------|--------------------------------|
| Identificarea rapidă a tipului de afecțiune cutanată (acnee vs eczeme) dintr-o imagine | Modelul clasifică imaginea încărcată și returnează rezultatul în **< 3 secunde** (pe PC local) | Preprocessing + RN Inference + UI |
| Reducerea autodiagnosticării greșite prin rezultat “alb/negru” | Sistemul returnează **probabilități pe clase (%)** și eticheta finală (ex: acnee 82%, eczeme 18%) | RN Inference + UI Results |
| Asigurarea funcționării end-to-end fără intervenție manuală | Flux complet: **Upload → Preprocess (200×200) → Inferență → Afișare rezultat**, fără pași manuali | Preprocessing + RN + UI |
| Posibilitatea extinderii viitoare (ex: încă 1 clasă sau severitate) | Arhitectură modulară: adăugarea unei clase și reantrenare pe dataset extins cu modificări minime în cod/UI | Data Pipeline + RN Architecture |


### 2. Contribuția Voastră Originală la Setul de Date – MINIM 40% din Totalul Observațiilor Finale

**Total observații finale:** 8320  
**Observații originale:** 8320 (100%)

**Tipul contribuției:**
[ ] Date generate prin simulare fizică  
[ ] Date achiziționate cu senzori proprii  
[X] Etichetare/adnotare manuală  
[ ] Date sintetice prin metode avansate  

**Descriere detaliată:**

Setul de date utilizat în proiect este alcătuit din 8320 imagini dermatologice colectate manual din surse publice. Fiecare imagine a fost inspectată vizual și etichetată manual într-una din cele două clase: **acnee** sau **eczeme**. În procesul de selecție au fost eliminate imaginile neclare, duplicatele, colajele și cazurile ambigue, asigurând astfel un dataset curat și corect etichetat.

Această activitate de selecție și adnotare manuală reprezintă o contribuție originală substanțială, întrucât datele brute din surse publice nu sunt structurate inițial pentru această problemă de clasificare binară. Datasetul final este rezultatul unui proces propriu de curățare, organizare și validare vizuală, adaptat special scopului acestui proiect.

Preprocesarea s-a realizat prin scriptul `resize_images.py`, care convertește imaginile în format RGB și le redimensionează la o lățime si inaltime standard de 200px, menținând proporțiile. Datele standardizate sunt salvate în `data/processed/`.

**Locația codului:**  
`src/preprocessing/resize_images.py`

**Locația datelor:**  
`data/raw/` – imagini brute colectate și etichetate manual  
`data/processed/` – imagini standardizate

**Notă:** Augmentările aplicate pe setul de antrenare (train) sunt folosite pentru creșterea robusteții modelului, dar nu sunt contabilizate ca “contribuție originală” (conform cerințelor proiectului).

**Dovezi:**
- Structura folderelor `data/raw/acnee` și `data/raw/eczeme`  
- Număr mare de fișiere per clasă (peste 4000 imagini / clasă)


**Dovezi:**
- Grafic comparativ: `docs/generated_vs_real.png`
- Setup experimental: `docs/acquisition_setup.jpg` (dacă aplicabil)
- Tabel statistici: `docs/data_statistics.csv`

---

#### Exemple pentru "contribuție originală":
-Simulări fizice realiste cu ecuații și parametri justificați  
-Date reale achiziționate cu senzori proprii (setup documentat)  
-Augmentări avansate cu justificare fizică (ex: simulare perspective camera industrială)  

---

### 3. Diagrama State Machine a Întregului Sistem (OBLIGATORIE)

**Cerințe:**
- **Minimum 4-6 stări clare** cu tranziții între ele
- **Formate acceptate:** PNG/SVG, pptx, draw.io 
- **Locație:** `docs/state_machine.*` (orice extensie)
- **Legendă obligatorie:** "De ce ați ales acest State Machine pentru nevoia voastră?"
State Machine-ul a fost definit astfel încât să urmeze exact pașii prin care trece un utilizator real care vrea să își verifice o problemă ușoară a pielii: așteptare (IDLE), încărcare imagine (ACQUIRE_IMAGE), verificare validitate (VALIDATE_IMAGE), preprocesare (PREPROCESS), clasificare prin rețeaua neuronală (INFERENCE_RN) și afișarea rezultatului în interfață (DISPLAY_RESULT). Aceste stări separate reflectă direct pipeline-ul end-to-end implementat în cod (preprocesare + RN + UI), permițând atât testarea fiecărei componente, cât și înțelegerea clară a fluxului complet.

Am introdus explicit starea de **VALIDATE_IMAGE** și ramura **ERROR_INVALID_INPUT** deoarece, în cazul imaginilor dermatologice, calitatea și relevanța pozei sunt critice (blur, cadru greșit, format nepotrivit). Acest lucru permite sistemului să gestioneze elegant situațiile în care inputul nu este adecvat, fără a bloca aplicația sau a produce rezultate înșelătoare. Structura este modulară: dacă în viitor adăugăm și alte clase sau un modul de „severitate leziune”, acestea se vor integra natural după starea de PREPROCESS sau INFERENCE_RN, fără a schimba logica principală a State Machine-ului.


    IDLE → ACQUIRE_IMAGE (user upload) → VALIDATE_IMAGE (format, dimensiune, integritate) →
  ├─ [Valid] → PREPROCESS (RGB + resize 200×200 cu padding + normalizare) → INFERENCE_RN (CNN acnee/eczeme) → DISPLAY_RESULT (clasă + probabilități) → IDLE
  └─ [Invalid] → ERROR_INVALID_INPUT (mesaj în UI) → IDLE



**Legendă obligatorie (scrieți în README):**

### Justificarea State Machine-ului ales:

Am ales arhitectura de **clasificare la cerere (user upload → clasificare imagine → afișare rezultat)** pentru că proiectul nostru rezolvă nevoia de **diagnostic vizual rapid al problemelor ușoare ale pielii** (acnee, eczemă, roșeață) fără consult medical imediat. Utilizatorul interacționează punctual cu sistemul: încarcă o poză, primește clasă + probabilități, după care poate încărca o nouă imagine sau închide aplicația.

Stările principale sunt:
1. **IDLE**: aplicația este deschisă, dar nu prelucrează nimic; UI așteaptă ca utilizatorul să încarce o imagine cu zona de piele afectată.  
2. **ACQUIRE_IMAGE**: utilizatorul selectează sau face upload unei imagini din galerie/cameră; fișierul este preluat de aplicație și trimis spre verificare.  
3. **VALIDATE_IMAGE**: se verifică dacă fișierul este o imagine validă (format acceptat, dimensiune minimă, nu este complet neagră / albă, nu este goală); dacă nu trece validarea, se intră în starea de eroare.  
4. **PREPROCESS**: imaginea este preprocesată (resize la 200x200px , conversie în RGB, normalizare), astfel încât să fie compatibilă cu input-ul rețelei neuronale convoluționale.  
5. **INFERENCE_RN**: imaginea preprocesată este trimisă către modelul CNN, care calculează scoruri de probabilitate pentru fiecare clasă: acnee / eczemă / roșeață.  
6. **DISPLAY_RESULT**: UI afișează utilizatorului rezultatul clasificării (clasa cu probabilitatea maximă + eventual probabilitățile pe fiecare categorie) și oferă opțiunea de a încărca o nouă imagine sau de a închide aplicația.  
7. **ERROR_INVALID_INPUT**: dacă imaginea este coruptă, prea mică, blurată sau nu are format suportat, sistemul afișează un mesaj de eroare și revine în starea IDLE, permițând utilizatorului să încerce din nou.

Tranzițiile critice sunt:
- **IDLE → ACQUIRE_IMAGE**: are loc atunci când utilizatorul apasă butonul de „Upload” și selectează o poză.  
- **ACQUIRE_IMAGE → VALIDATE_IMAGE**: imediat după ce fișierul a fost încărcat în aplicație, înainte de orice preprocesare.  
- **VALIDATE_IMAGE → PREPROCESS**: se întâmplă doar dacă imaginea trece toate verificările de bază (format, dimensiune, nu e goală).  
- **PREPROCESS → INFERENCE_RN**: atunci când imaginea a fost redimensionată și convertită corect, fiind gata pentru model.  
- **INFERENCE_RN → DISPLAY_RESULT**: când modelul a generat cu succes probabilitățile pentru cele trei clase.  
- **VALIDATE_IMAGE → ERROR_INVALID_INPUT**: când fișierul este invalid (ex: nu este imagine, e prea mic, complet blurat).  
- **ERROR_INVALID_INPUT → IDLE**: după ce utilizatorul închide mesajul de eroare sau apasă „Încearcă din nou”.  
- **DISPLAY_RESULT → IDLE**: când utilizatorul decide să analizeze o nouă imagine sau reinițializează aplicația.

Starea **ERROR_INVALID_INPUT** este esențială pentru că, în contextul aplicației dermatologice, utilizatorul poate încărca poze nerelevante (ex: selfie complet, fundal, obiecte, sau o zonă de piele complet blurată). În lipsa acestei stări, sistemul ar încerca să clasifice imagini necorespunzătoare, generând rezultate înșelătoare. Prin tratarea explicită a erorilor de input, aplicația devine mai robustă și mai sigură pentru utilizator, ghidându-l să folosească poze clare și utile pentru model.

Bucla de feedback funcționează astfel: după **DISPLAY_RESULT**, utilizatorul poate alege să reîncarce o nouă imagine, revenind în starea **IDLE**. În versiunile viitoare ale sistemului, rezultatele inferenței și imaginile încărcate ar putea fi stocate (cu acordul utilizatorului) pentru a extinde datasetul și a reantrena modelul, îmbunătățind astfel continuu acuratețea și robustețea SIA-ului.

---

### 4. Scheletul Complet al celor 3 Module Cerute la Curs (slide 7)

Toate cele 3 module trebuie să **pornească și să ruleze fără erori** la predare. Nu trebuie să fie perfecte, dar trebuie să demonstreze că înțelegeți arhitectura.

| **Modul** | **Python (exemple tehnologii)** | **LabVIEW** | **Cerință minimă funcțională (la predare)** |
|-----------|----------------------------------|-------------|----------------------------------------------|
| **1. Data Logging / Acquisition** | `src/data_acquisition/` | LLB cu VI-uri de generare/achiziție | **MUST:** Produce CSV cu datele voastre (inclusiv cele 40% originale). Cod rulează fără erori și generează minimum 100 samples demonstrative. |
| **2. Neural Network Module** | `src/neural_network/model.py` sau folder dedicat | LLB cu VI-uri RN | **MUST:** Modelul RN definit, compilat, poate fi încărcat. **NOT required:** Model antrenat cu performanță bună (poate avea weights random/inițializați). |
| **3. Web Service / UI** | Streamlit, Gradio, FastAPI, Flask, Dash | WebVI sau Web Publishing Tool | **MUST:** Primește input de la user și afișează un output. **NOT required:** UI frumos, funcționalități avansate. |

#### Detalii per modul:

#### **Modul 1: Data Logging / Acquisition**

**Funcționalități obligatorii:**
- [x] Cod rulează fără erori: `python src/data_acquisition/generate.py` sau echivalent LabVIEW
- [x] Generează CSV în format compatibil cu preprocesarea din Etapa 3
- [x] Include minimum 40% date originale în dataset-ul final
- [x] Documentație în cod: ce date generează, cu ce parametri

#### **Modul 2: Neural Network Module**

**Funcționalități obligatorii:**
- [x] Arhitectură RN definită și compilată fără erori
- [x] Model poate fi salvat și reîncărcat
- [x] Include justificare pentru arhitectura aleasă (în docstring sau README)
- [x] **NU trebuie antrenat** cu performanță bună (weights pot fi random)


#### **Modul 3: Web Service / UI**

**Funcționalități MINIME obligatorii:**
- [x] Propunere Interfață ce primește input de la user (formular, file upload, sau API endpoint)
- [x] Includeți un screenshot demonstrativ în `docs/screenshots/`

**Ce NU e necesar în Etapa 4:**
- UI frumos/profesionist cu grafică avansată
- Funcționalități multiple (istorice, comparații, statistici)
- Predicții corecte (modelul e neantrenat, e normal să fie incorect)
- Deployment în cloud sau server de producție

**Scop:** Prima demonstrație că pipeline-ul end-to-end funcționează: input user → preprocess → model → output.


## Structura Repository-ului la Finalul Etapei 4 (OBLIGATORIE)

**Verificare consistență cu Etapa 3:**

```
proiect-rn-[nume-prenume]/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── generated/  # Date originale
│   ├── train/
│   ├── validation/
│   └── test/
├── src/
│   ├── data_acquisition/
│   ├── preprocessing/  # Din Etapa 3
│   ├── neural_network/
│   └── app/  # UI schelet
├── docs/
│   ├── state_machine.*           #(state_machine.png sau state_machine.pptx sau state_machine.drawio)
│   └── [alte dovezi]
├── models/  # Untrained model
├── config/
├── README.md
├── README_Etapa3.md              # (deja existent)
├── README_Etapa4_Arhitectura_SIA.md              # ← acest fișier completat (în rădăcină)
└── requirements.txt  # Sau .lvproj
```

**Diferențe față de Etapa 3:**
- Adăugat `data/generated/` pentru contribuția dvs originală
- Adăugat `src/data_acquisition/` - MODUL 1
- Adăugat `src/neural_network/` - MODUL 2
- Adăugat `src/app/` - MODUL 3
- Adăugat `models/` pentru model neantrenat
- Adăugat `docs/state_machine.png` - OBLIGATORIU
- Adăugat `docs/screenshots/` pentru demonstrație UI

---

## Checklist Final – Bifați Totul Înainte de Predare

### Documentație și Structură
- [x] Tabelul Nevoie → Soluție → Modul complet (minimum 2 rânduri cu exemple concrete completate in README_Etapa4_Arhitectura_SIA.md)
- [x] Declarație contribuție 40% date originale completată în README_Etapa4_Arhitectura_SIA.md
- [x] Cod generare/achiziție date funcțional și documentat
- [x] Dovezi contribuție originală: grafice + log + statistici în `docs/`
- [x] Diagrama State Machine creată și salvată în `docs/state_machine.*`
- [x] Legendă State Machine scrisă în README_Etapa4_Arhitectura_SIA.md (minimum 1-2 paragrafe cu justificare)
- [x] Repository structurat conform modelului de mai sus (verificat consistență cu Etapa 3)

### Modul 1: Data Logging / Acquisition
- [x] Cod rulează fără erori (`python src/data_acquisition/...` sau echivalent LabVIEW)
- [x] Produce minimum 40% date originale din dataset-ul final
- [x] CSV generat în format compatibil cu preprocesarea din Etapa 3
- [x] Documentație în `src/data_acquisition/README.md` cu:
  - [x] Metodă de generare/achiziție explicată
  - [x] Justificare relevanță date pentru problema voastră
- [x] Fișiere în `data/generated/` conform structurii

### Modul 2: Neural Network
- [x] Arhitectură RN definită și documentată în cod (docstring detaliat) - versiunea inițială 
- [x] README în `src/neural_network/` cu detalii arhitectură curentă

### Modul 3: Web Service / UI
- [x] Propunere Interfață ce pornește fără erori (comanda de lansare testată)
- [x] Screenshot demonstrativ în `docs/screenshots/ui_demo.png`
- [x] README în `src/app/` cu instrucțiuni lansare (comenzi exacte)

---

**Predarea se face prin commit pe GitHub cu mesajul:**  
`"Etapa 4 completă - Arhitectură SIA funcțională"`

**Tag obligatoriu:**  
`git tag -a v0.4-architecture -m "Etapa 4 - Skeleton complet SIA"`



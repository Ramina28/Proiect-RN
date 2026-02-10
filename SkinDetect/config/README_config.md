## Folderul `config/` — justificare (neutilizat )

În structura inițială a proiectului a fost prevăzut un folder `config/`, care ar fi putut conține:
- `preprocessing_params.pkl` – parametri salvați pentru preprocesare (ex: scalere, encodere)
- `optimized_config.yaml` – fișier de configurare pentru hiperparametri (learning rate, batch size, epoci etc.)

### De ce nu este necesar în această implementare

În versiunea actuală a proiectului, toate componentele sunt proiectate să funcționeze **independent de fișiere de configurare externe**, deoarece:

1. **Parametrii modelului sunt definiți direct în cod**
   - `train_optimized.py` conține explicit:
     - arhitectura modelului
     - hiperparametrii (learning rate, batch size, epoci)
   - Nu există citire din fișiere `.yaml`.

2. **Preprocesarea este standard și deterministă**
   - Imaginile sunt:
     - redimensionate la `(200, 200)`
     - normalizate cu `Rescaling(1./255)`
   - Nu sunt utilizați scaleri, encodere sau transformări care să necesite salvarea parametrilor în `.pkl`.

3. **Scripturile nu depind de `config/`**
   Următoarele componente funcționează complet autonom:
   - `train_optimized.py`
   - `evaluate.py`
   - `visualize.py`
   - `main.py` (UI)
   
   Niciun script nu încarcă:
   - fișiere `.yaml`
   - fișiere `.pkl`
   - sau orice altă configurație externă.

4. **Portabilitate și simplitate**
   Eliminarea dependenței de `config/`:
   - reduce complexitatea proiectului
   - evită erori de path/config lipsă
   - permite rularea directă a scripturilor fără configurare suplimentară

### Când ar fi necesar un folder `config/`

Un folder de configurare ar fi util dacă proiectul ar include:
- experimente multiple cu hiperparametri diferiți
- pipeline de preprocesare complex (StandardScaler, LabelEncoder etc.)
- medii de producție unde configurația trebuie separată de cod

### Concluzie

Folderul `config/` nu este inclus în această versiune deoarece:
- nu este utilizat de niciun script
- toate setările sunt gestionate direct în cod
- proiectul este complet funcțional și reproductibil fără configurații externe

# Modul Data Logging / Acquisition – manifest.csv

Acest modul are rolul de a documenta setul de date utilizat în proiect prin generarea unui fișier
`manifest.csv`, care conține metadate despre fiecare imagine procesată.

Fișierul CSV nu este folosit direct de rețeaua neuronală, ci reprezintă un **jurnal al datasetului**,
necesar pentru trasabilitate, audit al datelor și respectarea cerințelor de la Etapa 4.

---

## Ce este `manifest.csv`

`manifest.csv` este un fișier tabelar care conține un rând pentru fiecare imagine din
`data/processed/`.

Structura tipică:

| Coloana     | Descriere |
|-------------|-----------|
| `image_path`| Calea relativă către fișierul imaginii |
| `label`     | Eticheta clasei (ex: acnee, eczeme) |
| *(opțional)* `width`, `height` | Dimensiunile imaginii (dacă Pillow este instalat) |
| *(opțional)* `created_at` | Data și ora generării înregistrării |

---

## Ce face scriptul `generate_manifest.py`

Scriptul:

- scanează automat folderele `data/processed/acnee` și `data/processed/eczeme`;
- extrage eticheta clasei din numele folderului părinte;
- construiește o intrare CSV pentru fiecare imagine găsită;
- salvează rezultatul în fișierul `data/manifest.csv`.

---

## De ce este necesar acest fișier

`manifest.csv` servește ca:

- dovadă a existenței și structurii datasetului;
- suport pentru analiza distribuției pe clase;
- document de audit pentru respectarea regulii de minimum 40% date originale.

Acest fișier nu influențează direct performanța modelului, ci are rol strict de **documentare și trasabilitate a datelor**.

---
## Metoda de generare / achiziție a datelor

Imaginile utilizate în proiect au fost colectate manual din surse publice online (baze de date deschise și site-uri educaționale dermatologice). Fiecare imagine a fost inspectată vizual și etichetată manual într-una dintre cele două clase finale: **acnee** și **eczeme**.

În procesul de colectare au fost eliminate imagini:
- neclare sau foarte blurate;
- duplicate sau aproape duplicate;
- colaje sau imagini cu watermark mare;
- imagini care nu conțin o zonă clară de piele.

Această etapă de selecție și etichetare manuală reprezintă contribuția originală principală asupra setului de date și asigură relevanța și calitatea observațiilor utilizate ulterior în modelul RN.

---

## Cum se generează

Din rădăcina proiectului:

```bash
python src/data_acquisition/generate_manifest.py

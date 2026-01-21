# Dovezi Contribuție Originală – data_statistics.py

Acest modul generează dovezile necesare pentru a demonstra contribuția originală asupra setului de date utilizat în proiectul de clasificare a imaginilor dermatologice (acnee vs eczeme).

Scriptul analizează imaginile finale standardizate din `data/processed/` și produce statistici, grafice și fișiere de log salvate în folderul `docs/`.

---

## Ce face `data_statistics.py`

La rulare, scriptul parcurge fiecare clasă din `data/processed/` și:

1. Numără câte imagini există pentru fiecare clasă (ex: `acnee`, `eczeme`);
2. Creează un fișier CSV cu distribuția pe clase;
3. Generează un grafic tip bar chart care vizualizează distribuția datasetului;
4. Creează un fișier de log textual cu aceleași informații.

---

## Fișiere generate

După rulare apar automat:

| Fișier | Conținut |
|--------|----------|
| `docs/data_statistics.csv` | Tabel cu două coloane: `class`, `num_images` |
| `docs/data_statistics.png` | Grafic bar care arată distribuția imaginilor pe clase |
| `docs/data_log.txt` | Jurnal text cu numărul de imagini pentru fiecare clasă |

---

## De ce sunt necesare aceste fișiere

Aceste fișiere constituie **dovezile oficiale** ale contribuției originale la setul de date:

- demonstrează existența unui volum mare de imagini reale;
- arată distribuția pe clase;
- permit verificarea obiectivă a respectării cerinței de minimum 40% date originale.

---

## Cum se rulează

Din rădăcina proiectului:

```bash
python src/data_acquisition/data_statistics.py

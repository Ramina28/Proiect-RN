---

## 📊 Scripturi auxiliare (statistici + manifest + vizualizări)

---

### 1) `data_statistics.py` — Statistici despre dataset (data/processed)
**Ce face:**
- Numără imaginile din dataset-ul procesat, pe clase:
  - `data/processed/acnee`
  - `data/processed/eczeme`
- Creează un mic raport (CSV + grafic + log text) cu distribuția imaginilor pe clase.

**De unde citește:**
- `data/processed/` (hard setat în `DATA_DIR`)
- clase așteptate: `["acnee", "eczeme"]`

**Ce produce (output):**
- CSV cu numărul de imagini/clasă:
  - `docs/data_statistics.csv`
- Grafic bar chart (distribuția imaginilor):
  - `docs/data_statistics.png`
- Log text (ușor de citit rapid):
  - `docs/data_log.txt`

---

### 2) `generate_manifest.py` — Creează manifest CSV (listă de imagini + label)
**Ce face:**
- Parcurge imaginile din `data/processed/acnee` și `data/processed/eczeme`.
- Generează un fișier `manifest.csv` cu două coloane:
  - `image_path` (cale relativă către imagine)
  - `label` (clasa: acnee/eczeme)

**De unde citește:**
- `data/processed/`
- clase așteptate: `["acnee", "eczeme"]`

**Ce produce (output):**
- Manifest CSV:
  - `data/manifest.csv`

**Comportament special:**
- Dacă un folder de clasă lipsește, afișează warning:
  - `[WARN] Folder lipsă: ...`
  și continuă fără să crape.

---





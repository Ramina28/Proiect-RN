# Modul 1 – Data Logging / Acquisition (scurt)

Acest modul are rolul de a documenta și structura datasetul utilizat în aplicația SIA. Scriptul generate_dataset_csv.py scanează folderele cu imagini originale (data/processed/) și augmentate (data/generated/) și generează fișierul data/dataset_log.csv, care conține metadate despre fiecare imagine: clasă, tipul sursei (original/augmented), dimensiuni și calea completă a fișierului.

## Metodă de generare / achiziție

Se parcurg automat toate imaginile din processed/ și generated/.

Clasa imaginii este dedusă din numele folderului (acnee / eczema / roseata).

Se extrag și salvează dimensiunile imaginii (width, height).

Toate informațiile sunt centralizate într-un CSV pentru utilizare ulterioară în pipeline.

## Parametrii utilizați

Pentru imaginile originale (processed/):

Redimensionare: 200px lățime, menținând proporțiile

Conversie: RGB

Eliminare imagini neclare / nerelevante

Pentru imaginile augmentate (generated/):

Ajustări luminozitate

Ajustări contrast

Modificări saturație

Gaussian noise (zgomot controlat)

Blur redus

Acești parametri simulează variabilitatea reală a fotografiilor dermatologice și contribuie la diversificarea datasetului (+200% imagini suplimentare).
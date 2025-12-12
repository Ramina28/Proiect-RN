### Modul 2: Neural Network Module

Modulul de rețea neuronală este implementat în:

`src/neural_network/model.py`

Acest modul definește un model CNN pentru clasificarea imaginilor dermatologice în 3 clase: **acnee, eczemă, roșeață**. Arhitectura folosește trei blocuri `Conv2D + MaxPooling`, urmate de un strat `GlobalAveragePooling2D` și două straturi dense (`Dense(64)` + `Dense(3, softmax)`), ceea ce permite extragerea graduală de caracteristici vizuale (texturi, margini, zone inflamate) și o clasificare finală pe cele trei clase.

Modelul este:
- **definit și compilat** cu optimizer *Adam* și loss `categorical_crossentropy`;
- **salvat** ca model neantrenat în `models/skin_cnn_untrained.keras`;
- **reîncărcat** prin funcția `load_model(...)` pentru verificarea integrității.

În Etapa 4 modelul NU este antrenat cu performanță bună; weights sunt random. Scopul acestei etape este demonstrarea faptului că arhitectura RN este corect definită, compilată și integrată în pipeline (poate fi salvată și reîncărcată fără erori).

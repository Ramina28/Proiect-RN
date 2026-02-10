import tensorflow as tf
from tensorflow.keras import layers, models, optimizers

def build_optimized_model(input_shape=(200, 200, 3), num_classes=2):
    """
    Construieste arhitectura optimizata pentru Etapa 6.
    Include strat de Dropout pentru regularizare si input_shape corect.
    """
    model = models.Sequential([
        # Bloc 1
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        
        # Bloc 2
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Bloc 3
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Clasificator
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        # OPTIMIZARE CHEIE: Dropout 30% pentru a preveni overfitting-ul
        layers.Dropout(0.3), 
        layers.Dense(num_classes, activation='softmax')
    ])
    
    # Compilare cu Learning Rate specific (mai mic pentru finete)
    optimizer = optimizers.Adam(learning_rate=0.001)
    
    model.compile(optimizer=optimizer,
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

if __name__ == "__main__":
    # Test rapid
    model = build_optimized_model()
    model.summary()
    print("Arhitectura optimizata a fost definita corect.")
import os
from PIL import Image
import glob

# --- CONFIGURARE ---
# 1. Calculul Căii Rădăcină a Proiectului (Salt de două nivele înapoi)
# Din src/preprocessing/ sarim inapoi de 2 ori pentru a ajunge la SkinDetect/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) 


# 2. DEFINIREA CĂILOR DE INTRARE ȘI IEȘIRE (Folosind calea rădăcină fixă)
INPUT_CLASSES = ["acnee", "eczeme", "rosacee"]

# Căi de Intrare/Ieșire care pleacă de la [SkinDetect]/
INPUT_BASE_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw')
OUTPUT_BASE_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')

# Dimensiunea dorită
RESIZE_WIDTH = 200

def process_images_with_pillow():
  # 1. Creează folderul de ieșire dacă nu există
    if not os.path.exists(OUTPUT_BASE_DIR):
        os.makedirs(OUTPUT_BASE_DIR)
        print(f"Am creat folderul de ieșire: {OUTPUT_BASE_DIR}")
        
    total_processed = 0

    # 2. Parcurge fiecare folder sursă
    for class_name in INPUT_CLASSES:
        print(f"\nProcesez clasa: {class_name}")

        input_folder_path = os.path.join(INPUT_BASE_DIR, class_name)
        output_folder_path = os.path.join(OUTPUT_BASE_DIR, class_name)
        
        # Asigură-te că folderul de clasă există în processed
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        # Caută imaginile în INPUT_BASE_DIR/clasa
        image_paths = (
            glob.glob(os.path.join(input_folder_path, "*.jpg")) +
            glob.glob(os.path.join(input_folder_path, "*.jpeg")) +
            glob.glob(os.path.join(input_folder_path, "*.png"))
        )

        for image_path in image_paths:
            # ... (Restul logicii de citire, redimensionare și salvare rămâne)
            try:
                # 3. Încarcă imaginea
                img = Image.open(image_path)
                
                # 4. Calculează noile dimensiuni (păstrând proporțiile)
                original_width, original_height = img.size
                aspect_ratio = original_width / original_height
                new_width = RESIZE_WIDTH
                new_height = int(new_width / aspect_ratio)
                
                # 5. Redimensionează imaginea
                # Image.Resampling.LANCZOS este un filtru de înaltă calitate
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

              # 6. Salvează imaginea în folderul corect de ieșire
                filename = os.path.basename(image_path)
                output_path = os.path.join(output_folder_path, filename)
                resized_img.save(output_path)
                
                print(f"  -> Procesat: {filename}")
                total_processed += 1
                
            except Exception as e:
                print(f"  [ATENȚIE] Eroare la procesare {image_path}: {e}")
                continue

    print("\n--- FINALIZAT ---")
    print(f"Total imagini procesate: {total_processed}")

if __name__ == "__main__":
    process_images_with_pillow()
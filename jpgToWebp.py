import os
from PIL import Image

def convert_images_to_jpg_and_webp(input_folder, output_folder_webp):
    """
    Parcourt un dossier pour convertir toutes les images en JPG et en WebP.
    
    :param input_folder: Chemin du dossier contenant les images d'origine.
    :param output_folder_jpg: Chemin où enregistrer les fichiers JPG.
    :param output_folder_webp: Chemin où enregistrer les fichiers WebP.
    """
    # Création des dossiers de sortie s'ils n'existent pas
    os.makedirs(output_folder_webp, exist_ok=True)

    # Parcours des fichiers dans le dossier d'entrée
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        # Vérifie que le fichier est une image
        if os.path.isfile(input_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            try:
                # Ouvre l'image
                with Image.open(input_path) as img:
                    # Convertir en mode RGB (pour éviter les problèmes avec les images en mode palette ou avec transparence)
                    #img = img.convert('RGB')

                    # Conversion en JPG
                    base_filename = os.path.splitext(filename)[0]

                    # Conversion en WebP
                    webp_output_path = os.path.join(output_folder_webp, f"{base_filename}.webp")
                    img.save(webp_output_path, format='WEBP', quality=90)

                    print(f"Converti: {filename} -> {base_filename}.jpg, {base_filename}.webp")
            except Exception as e:
                print(f"Erreur lors du traitement de {filename}: {e}")

# Chemins des dossiers
input_folder = "_photos/photos/max"
output_folder_webp = "_photos/photos/max"

convert_images_to_jpg_and_webp(input_folder, output_folder_webp)
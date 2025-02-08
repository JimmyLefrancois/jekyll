import os
from PIL import Image

def convert_images_to_jpg_and_webp(input_folder, output_folder_webp):
    """
    Parcourt un dossier pour convertir toutes les images en WebP et supprimer les originaux.
    
    :param input_folder: Chemin du dossier contenant les images d'origine.
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
                    # Conversion en WebP
                    base_filename = os.path.splitext(filename)[0]
                    webp_output_path = os.path.join(output_folder_webp, f"{base_filename}.webp")
                    img.save(webp_output_path, format='WEBP', quality=90)

                    # Suppression du fichier original après conversion réussie
                    os.remove(input_path)
                    print(f"Converti et supprimé: {filename} -> {base_filename}.webp")
            except Exception as e:
                print(f"Erreur lors du traitement de {filename}: {e}")

def convert_md_to_webp(file_path):
    """
    Lit le fichier markdown et remplace toutes les extensions .jpg par .webp
    
    :param file_path: Chemin du fichier markdown à modifier
    """
    try:
        # Lecture du fichier
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Remplacement des extensions .jpg par .webp
        modified_content = content.replace('.jpg', '.webp')

        # Écriture du contenu modifié dans le fichier
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)

        print(f"Conversion terminée avec succès pour {file_path}")

    except Exception as e:
        print(f"Erreur lors du traitement du fichier: {e}")

# Exécution de la conversion
photos_md_path = "_photos/photos.md"

# Chemins des dossiers
input_folder_max = "_photos/photos/max"
output_folder_max_webp = "_photos/photos/max"

input_folder_min = "_photos/photos/min"
output_folder_min_webp = "_photos/photos/min"

convert_images_to_jpg_and_webp(input_folder_max, output_folder_max_webp)
convert_images_to_jpg_and_webp(input_folder_min, output_folder_min_webp)
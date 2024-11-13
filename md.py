import os
import shutil
from datetime import datetime
from ruamel.yaml import YAML
from io import StringIO
from PIL import Image

def compress_images(directory):
    """
    Compresse toutes les images du répertoire source sans perte de qualité.

    :param directory: Répertoire contenant les images à compresser.
    """
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            source_path = os.path.join(directory, filename)

            with Image.open(source_path) as img:
                # Déterminer le format de l'image
                format = img.format

                # Compresser selon le format
                if format == 'JPEG':
                    img.save(source_path, format='JPEG', optimize=True)
                    print(f"Image {filename} compressée (JPEG).")
                elif format == 'PNG':
                    img.save(source_path, format='PNG', compress_level=6)  # Compression sans perte pour PNG
                    print(f"Image {filename} compressée (PNG).")

def update_markdown(directory, markdown_file, max_directory, min_directory, target_width=800):
    """
    Met à jour un fichier Markdown avec des photos d'un répertoire, déplace les photos dans 'max',
    et redimensionne les photos pour les enregistrer dans 'min'.

    :param directory: Répertoire contenant les photos à traiter.
    :param markdown_file: Fichier Markdown à mettre à jour.
    :param max_directory: Répertoire où déplacer les photos source.
    :param min_directory: Répertoire où enregistrer les photos redimensionnées.
    :param target_width: Largeur cible des photos redimensionnées (en pixels).
    """
    # Compresser les images dans le répertoire source
    compress_images(directory)

    # Initialiser YAML
    yaml = YAML()
    yaml.preserve_quotes = True

    # Charger le fichier Markdown
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Repérer les délimiteurs YAML "---" et extraire les données
    yaml_content = content.split('---\n')[1]
    data = yaml.load(yaml_content)

    # Récupérer les chemins des photos déjà dans le fichier
    existing_paths = {photo['path'] for photo in data.get('photos', [])}

    # Scanner les photos dans le répertoire
    new_photos = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Ajuster les extensions si nécessaire
            photo_path = os.path.basename(filename)
            if photo_path not in existing_paths:
                # Ajouter la photo au fichier Markdown
                new_photos.append({
                    'path': photo_path,
                    'alt': 'Texte à remplacer',
                    'description': '',
                    'tag1': '',
                    'tag2': ''
                })

                # Déplacer la photo vers le répertoire 'max'
                source_path = os.path.join(directory, filename)
                max_path = os.path.join(max_directory, filename)
                shutil.move(source_path, max_path)

                # Redimensionner et enregistrer dans le répertoire 'min'
                min_path = os.path.join(min_directory, filename)
                resize_image(max_path, min_path, target_width)

    # Ajouter les nouvelles photos au fichier Markdown
    if new_photos:
        data['photos'].extend(new_photos)

        # Mettre à jour la date avec la date et l'heure actuelles
        data['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' +0200'

        # Utiliser StringIO pour capturer le YAML en chaîne
        yaml_stream = StringIO()
        yaml.dump(data, yaml_stream)
        updated_yaml_content = yaml_stream.getvalue()

        # Recomposer le contenu YAML en ajoutant les délimiteurs "---" pour sauvegarder
        updated_content = f"---\n{updated_yaml_content}---\n"
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print(f"{len(new_photos)} nouvelles photos ajoutées, déplacées et redimensionnées.")
    else:
        print("Aucune nouvelle photo trouvée.")

def resize_image(source_path, destination_path, target_width):
    """
    Redimensionne une image en respectant le ratio et l'enregistre dans un fichier.

    :param source_path: Chemin de l'image source.
    :param destination_path: Chemin où enregistrer l'image redimensionnée.
    :param target_width: Largeur cible des images redimensionnées.
    """
    with Image.open(source_path) as img:
        # Calculer la hauteur tout en respectant le ratio
        width_percent = target_width / float(img.width)
        target_height = int(img.height * width_percent)

        # Redimensionner l'image
        resized_img = img.resize((target_width, target_height))

        # Enregistrer l'image redimensionnée
        resized_img.save(destination_path)
        print(f"Image redimensionnée et enregistrée dans {destination_path}")

# Utilisation
update_markdown(
    'C:/Users/Jiphie/Desktop/jekyll/_photos/photos/waitingRoom',
    'C:/Users/Jiphie/Desktop/jekyll/_photos/photos.md',
    'C:/Users/Jiphie/Desktop/jekyll/_photos/photos/max',
    'C:/Users/Jiphie/Desktop/jekyll/_photos/photos/min',
    target_width=800  # Largeur cible en pixels
)
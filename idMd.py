import os
import requests
from lxml import html
import time
import shutil
from datetime import datetime
import pandas as pd
from ruamel.yaml import YAML
from io import StringIO
from PIL import Image
from slugify import slugify
import uuid
from ultralytics import YOLO

# Fonction pour envoyer la première requête et extraire l'image
def send_first_request(url, image_path):
    with open(image_path, "rb") as img_file:
        data = {
            "Name_img": "",
            "level": "",
            "X1": "",
            "Y1": "",
            "X2": "",
            "Y2": "",
            "TX": "",
            "TY": "",
            "minTX": "",
            "minTY": "",
            "maxTX": "",
            "maxTY": "",
        }
        files = {
            "NOM_DE_FICHIER": img_file
        }

        response_from_first_request = requests.post(url, headers={}, data=data, files=files)

        tree1 = html.fromstring(response_from_first_request.text)
        image_name_from_server = tree1.xpath('//input[@id="Name_img"]/@value')[0]

        return image_name_from_server

# Fonction pour envoyer la deuxième requête et récupérer les résultats
def send_second_request(url, image_name):
    data = {
        "Name_img": image_name,
        "level": "2",
        "X1": "5",
        "Y1": "5",
        "X2": "588",
        "Y2": "588",
        "TX": "583",
        "TY": "583",
        "minTX": "55",
        "minTY": "55",
        "maxTX": "599",
        "maxTY": "600",
        "validez": "Suivant",
    }

    time.sleep(1)

    response_from_second_request = requests.post(url, headers={}, data=data)
    tree2 = html.fromstring(response_from_second_request.text)
    bird_name = tree2.xpath('//a[@class="fiche"]/text()')[0]
    probability_string = tree2.xpath('//div[@class="pour100esp"]/text()')[1]
    probability_float = float(probability_string.replace(' %', ''))

    return bird_name, probability_string, probability_float

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
                image_format = img.format

                # Compresser selon le format
                if image_format == 'JPEG':
                    img.save(source_path, format='JPEG', optimize=True)
                    print(f"Image {filename} compressée (JPEG).")
                elif image_format == 'PNG':
                    img.save(source_path, format='PNG', compress_level=6)  # Compression sans perte pour PNG
                    print(f"Image {filename} compressée (PNG).")

def update_markdown(directory, markdown_file, max_directory, min_directory, bird_names, target_width=800):
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
    for index, filename in enumerate(os.listdir(directory), start=0):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Ajuster les extensions si nécessaire
            photo_path = os.path.basename(filename)
            if photo_path not in existing_paths:
                # Ajouter la photo au fichier Markdown
                new_photos.append({
                    'path': photo_path,
                    # 'alt': '',
                    # 'description': '',
                    'alt': bird_names[index],
                    'description': bird_names[index],
                    'tag1': 'Animaux',
                    'tag2': 'Oiseaux',
                    'tag3': 'Nature'
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

# Fonction pour traiter les images et enregistrer celles avec une probabilité < 90%
def process_images_in_folder(folder_path, url, excel_file):
    df = pd.DataFrame(columns=["Nom du fichier", "Nom de l'oiseau", "Probabilité"])
    bird_names = []
    for image_filename in os.listdir(folder_path):
        if image_filename.lower().endswith(('.jpg', '.jpeg')):

            image_path = os.path.join(folder_path, image_filename)
            cords, image_to_crop = bird_coords(image_path)
            x_max_new, x_min_new, y_max_new, y_min_new = transform_coords_to_square(cords, image_to_crop)
            cropped_image = image_to_crop.crop((x_min_new, y_min_new, x_max_new, y_max_new))

            cropped_image_path = "./_photos/photos/"+ image_filename.replace('.jpg', '') +"_cropped_image.jpg"
            cropped_image.save(cropped_image_path)

            image_name = send_first_request(url, cropped_image_path)
            bird_name, probability_string, probability_float = send_second_request(url, image_name)
            print(f'Il s\'agit à {probability_string} d\'un {bird_name} pour l\'image {image_filename}')
            #os.remove('./_photos/photos/cropped_image.jpg')

            if probability_float < 80:
                # Déplace l'image dans 'manualActions'
                manual_actions_folder = './_photos/photos/manualActions'
                shutil.move(image_path, os.path.join(manual_actions_folder, image_filename))
                shutil.move(cropped_image_path, os.path.join(manual_actions_folder, image_filename +"cropped_image.jpg"))
                new_row = pd.DataFrame([{"Nom du fichier": image_filename, "Nom de l'oiseau": bird_name, "Probabilité": probability_float}])
                df = pd.concat([df, new_row], ignore_index=True)
                print(f"Images déplacées vers 'manualActions' : {image_filename}")
            else:
                bird_names.append(bird_name.replace("'", "\'"))
                rename_photo(bird_name, folder_path, image_path)

    df.to_excel(excel_file, index=False)
    return bird_names

def rename_photo(bird_name, folder_path, image_path):
    bird_slug = slugify(bird_name)
    unique_id = str(uuid.uuid4())  # Génère un ID unique
    new_name = f"{bird_slug}-{unique_id}.jpg"  # Combine le slug et l'ID unique
    new_path = os.path.join(folder_path, new_name)
    os.rename(image_path, new_path)

def transform_coords_to_square(cords, image):
    # Calculer la largeur et la hauteur actuelles
    x_min, y_min, x_max, y_max = cords
    width = x_max - x_min
    height = y_max - y_min
    max_side = max(width, height)
    # Calculer les nouveaux coins pour le carré
    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    x_min_new = int(x_center - max_side / 2)
    x_max_new = int(x_center + max_side / 2)
    y_min_new = int(y_center - max_side / 2)
    y_max_new = int(y_center + max_side / 2)
    # Assurer que les coordonnées restent dans les limites de l'image
    x_min_new = max(0, x_min_new)
    y_min_new = max(0, y_min_new)
    x_max_new = min(image.width, x_max_new)
    y_max_new = min(image.height, y_max_new)
    return x_max_new, x_min_new, y_max_new, y_min_new

def bird_coords(image_path):
    model = YOLO("yolov8m.pt")
    results = model.predict(image_path)
    image = Image.open(image_path)
    result = results[0]
    box = result.boxes
    cords = box.xyxy[0].tolist()
    return cords, image

def main():
    url = "https://www.ornitho.com/"
    folder_path = "./_photos/photos/waitingRoom"  # Remplace par ton chemin de dossier
    excel_file = "resultats_oiseaux.xlsx"

    bird_names = process_images_in_folder(folder_path, url, excel_file)

    # Utilisation
    update_markdown(
        './_photos/photos/waitingRoom',
        './_photos/photos.md',
        './_photos/photos/max',
        './_photos/photos/min',
        bird_names,
        target_width=400  # Largeur cible en pixels
    )

# Exécution du script
if __name__ == "__main__":
    main()
import os
import requests
import pandas as pd
from lxml import html
import time

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

#         print(f'Envoi requête n°1 pour {image_path}')
        response1 = requests.post(url, headers={}, data=data, files=files)

        tree1 = html.fromstring(response1.text)
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

#     print('1s sleep')
    time.sleep(1)
#     print('Envoi requête n°2')

    response2 = requests.post(url, headers={}, data=data)

    tree2 = html.fromstring(response2.text)
    bird_name = tree2.xpath('//a[@class="fiche"]/text()')[0]
    probabilityString = tree2.xpath('//div[@class="pour100esp"]/text()')[1]
    probabilityFloat = float(probabilityString.replace(' %', ''))

    return bird_name, probabilityString, probabilityFloat

# Fonction pour traiter les images et enregistrer celles avec une probabilité < 90% dans un fichier Excel
def process_images_in_folder(folder_path, url, excel_file):
    # Créer un DataFrame vide pour les photos à ajouter
    df = pd.DataFrame(columns=["Nom du fichier", "Nom de l'oiseau", "Probabilité"])

    for image_filename in os.listdir(folder_path):
        if image_filename.lower().endswith(('.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, image_filename)

            image_name = send_first_request(url, image_path)
            bird_name, probabilityString, probabilityFloat = send_second_request(url, image_name)
            print(f'Il s\'agit à {probabilityString} d\'un {bird_name} pour l\'image {image_filename}')

            # Si la probabilité est inférieure à 90%, ajouter l'image aux résultats
#             if probabilityFloat < 90:
            new_row = pd.DataFrame([{"Nom du fichier": image_filename, "Nom de l'oiseau": bird_name, "Probabilité": probabilityFloat}])
            df = pd.concat([df, new_row], ignore_index=True)

    # Sauvegarder les résultats dans un fichier Excel
    df.to_excel(excel_file, index=False)
    print(f"Les résultats ont été enregistrés dans {excel_file}")

# Fonction principale
def main():
    url = "https://www.ornitho.com/"
    folder_path = "C:/Users/Jiphie/Desktop/Photos/script"  # Remplace par ton chemin de dossier
    excel_file = "resultats_oiseaux.xlsx"  # Nom du fichier Excel de sortie

    process_images_in_folder(folder_path, url, excel_file)

# Exécution du script
if __name__ == "__main__":
    main()





# todo trouver max % avant doute, si doute -> fichier de logs avec nom fichier + guessName + guess%
# Si c'est > au % de doute, on ajoute la photo au fichier photos.md en se servant du nom de l'oiseau pour la description
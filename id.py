import requests
from datetime import datetime
import secrets
from lxml import html
import time

# Fonction pour envoyer la première requête et extraire l'image
def send_first_request(url, image_path):
    """
    Envoie la première requête POST avec l'image, récupère la réponse et extrait la valeur de 'Name_img'.

    :param url: URL du site.
    :param image_path: Chemin du fichier image à envoyer.
    :return: La valeur de 'Name_img' récupérée du serveur.
    """
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

        # Envoi de la première requête
        print('Envoi requête n°1')
        response1 = requests.post(url, headers={}, data=data, files=files)

        # Extraire le nom de l'image retourné par le serveur
        tree1 = html.fromstring(response1.text)
        image_name_from_server = tree1.xpath('//input[@id="Name_img"]/@value')[0]

        return image_name_from_server

# Fonction pour envoyer la deuxième requête avec les données extraites
def send_second_request(url, image_name):
    """
    Envoie la deuxième requête POST avec les paramètres requis.

    :param url: URL du site.
    :param image_name: Le nom de l'image récupéré lors de la première requête.
    :return: Les informations extraites du serveur après la deuxième requête.
    """
    # Données de la deuxième requête
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

    # Attente de 3 secondes avant d'envoyer la deuxième requête
    print('3s sleep')
    time.sleep(3)
    print('Envoi requête n°2')

    # Envoi de la deuxième requête
    response2 = requests.post(url, headers={}, data=data)

    # Extraire le nom de l'oiseau et la probabilité
    tree2 = html.fromstring(response2.text)
    bird_name = tree2.xpath('//a[@class="fiche"]/text()')[0]
    probability = tree2.xpath('//div[@class="pour100esp"]/text()')[1]

    return bird_name, probability

# Fonction principale pour exécuter le processus complet
def main():
    """
    Exécute le processus complet des deux requêtes et affiche les résultats de la deuxième requête.
    """
    url = "https://www.ornitho.com/"

    # Envoi de la première requête et récupération du nom de l'image
    image_name = send_first_request(url, "_L5A4729-Modifier.jpg")

    # Envoi de la deuxième requête et récupération des informations sur l'oiseau
    bird_name, probability = send_second_request(url, image_name)

    # Afficher le résultat final
    print(f'Il s\'agit à {probability} d\'un {bird_name}')

# Exécution de la fonction principale
if __name__ == "__main__":
    main()

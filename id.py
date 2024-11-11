import requests
from datetime import datetime
import secrets
from lxml import html
import time

def printResponse(response1):
    # Afficher le code de statut
    print("Status Code:", response1.status_code)

    # Afficher les en-têtes de la réponse
    print("\nHeaders:", response1.headers)

    # Afficher le contenu de la réponse en texte (si lisible en texte)
    print("\nText Content:", response1.text)

    # Afficher le contenu de la réponse en JSON (si applicable)
    try:
        print("\nJSON Content:", response1.json())
    except ValueError:
        print("\nLa réponse n'est pas au format JSON.")

    # Afficher le contenu brut de la réponse
    print("\nRaw Content:", response1.content)

# URL de la première requête
url = "https://www.ornitho.com/"

headers_first_request = {

}

# Charger l'image
with open("_L5A4729-Modifier.jpg", "rb") as img_file:
    data_first_request = {
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
    files_first_request = {
        "NOM_DE_FICHIER": img_file
    }

    # Envoyer la première requête
    print('Envoi requête n°1')
    response1 = requests.post(url, headers={}, data=data_first_request, files=files_first_request)
    tree1 = html.fromstring(response1.text)
    imageNameFromServer = tree1.xpath('//input[@id="Name_img"]/@value')[0]

    data_second_request = {
        "Name_img": imageNameFromServer,
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

    time.sleep(3)
    response2 = requests.post(url, headers={}, data=data_second_request)
#     printResponse(response2)
    tree = html.fromstring(response2.text)
    birdName = tree.xpath('//a[@class="fiche"]/text()')[0]
    probabilite = tree.xpath('//div[@class="pour100esp"]/text()')[1]
    print('Il s\'agit à ' + probabilite + ' d\'un ' + birdName)



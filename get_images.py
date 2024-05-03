import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def allImages(dossier, class_name):
    for filename in os.listdir(dossier):
        html_content =[]
        fined_divs = []
        if filename.endswith(".html"):  # Filtrer les fichiers texte
            full_path = os.path.join(dossier, filename)
            with open(full_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                html_content = BeautifulSoup(html_content, 'html.parser')
                fined_divs = html_content.find_all('div', class_=class_name)
                for div in fined_divs:
                    getImages(str(div))

def getImages(code):

    # Parse HTML
    soup = BeautifulSoup(code, 'html.parser')

    # Find the <a> tag inside the <p> tag
    p_tag = soup.find('p')
    a_tag = p_tag.find('a')

    # Get the URL of the image from the href attribute of the <a> tag
    image_url = a_tag['href']

    # Create the output directory if it doesn't exist
    output_dir = 'output_images'
    os.makedirs(output_dir, exist_ok=True)

    # Download the image
    response = requests.get(image_url)

    # Parse the URL to get the filename
    filename = urlparse(image_url).path.split('/')[-1]

    # Save the image to the output directory
    output_path = os.path.join(output_dir, filename)
    with open(output_path, 'wb') as f:
        f.write(response.content)
        print(f"Image {filename} téléchargée avec succès dans le dossier {output_dir}.")

dossier_parent = os.path.dirname(os.path.abspath(__file__))  # Obtient le chemin du fichier en cours

# Chemin du sous-dossier
sous_dossier = "html_files"  # Remplacez par le nom de votre sous-dossier

# Chemin complet du dossier à traiter
dossier = os.path.join(dossier_parent, sous_dossier)
# La classe html a extraire
class_name = "wpProQuiz_question"
allImages(dossier, class_name)
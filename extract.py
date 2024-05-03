import requests
from bs4 import BeautifulSoup
import json

# URL du site à scraper
url = "https://login.formation-tcfcanada.com/comprehension-ecrite-test-14/"

# Faire une requête GET pour obtenir le contenu HTML de la page
response = requests.get(url)
html_content = response.text

# Analyser le contenu HTML avec BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Fonction pour extraire les ressources textuelles, sonores et images
def extract_resources(soup):
    resources = {
        'text': [],
        'audio': [],
        'image': []
    }

    # Extraire les textes
    for text_element in soup.find_all('p'):
        text = text_element.get_text(strip=True)
        if text:
            resources['text'].append(text)

    # Extraire les fichiers audio
    for audio_element in soup.find_all('audio'):
        audio_src = audio_element.get('src')
        if audio_src:
            resources['audio'].append(audio_src)

    # Extraire les images
    for img_element in soup.find_all('img'):
        img_src = img_element.get('src')
        if img_src:
            resources['image'].append(img_src)

    return resources

# Extraire les ressources du site
site_resources = extract_resources(soup)

# Enregistrer les ressources extraites dans un fichier JSON
output_file = 'site_resources.json'
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(site_resources, json_file, indent=4)

print(f"Ressources extraites enregistrées dans le fichier : {output_file}")

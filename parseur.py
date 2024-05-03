from bs4 import BeautifulSoup
import json

# Fonction pour extraire les div avec une certaine classe et leurs enfants
def extract_divs_with_class(html_content, class_name):
    soup = BeautifulSoup(html_content, 'html.parser')
    divs_with_class = []
    
    # Trouver tous les divs avec la classe spécifiée
    div_tags = soup.find_all('div', class_=class_name)
    
    for div_tag in div_tags:
        div_with_class = {}
        div_with_class['class'] = class_name
        div_with_class['children'] = []
        
        # Parcourir les enfants du div
        for child in div_tag.children:
            if child.name:  # Vérifier si l'enfant est un élément HTML
                child_data = {
                    'tag': child.name,
                    'attributes': dict(child.attrs),
                    'text': child.get_text(strip=True)
                }
                div_with_class['children'].append(child_data)
        
        divs_with_class.append(div_with_class)
    
    return divs_with_class

def extract(html_file_path, class_name_to_extract, json_file_path):
    

    # Ouvrir le fichier HTML et extraire son contenu
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Extraire les divs avec la classe spécifiée
    extracted_data = extract_divs_with_class(html_content, class_name_to_extract)

    # Convertir les résultats en JSON et les écrire dans un fichier
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(extracted_data, json_file, indent=4)

    print(f"Données extraites enregistrées dans le fichier : {json_file_path}")
# Nom du fichier HTML à ouvrir
html_file_path = 'index.html'
class_name_to_extract = "wpProQuiz_question"
# Nom du fichier JSON de sortie
json_file_path = 'extracted_data.json'
extract(html_file_path, class_name_to_extract, json_file_path)


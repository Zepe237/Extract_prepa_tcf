import json
import re
from bs4 import BeautifulSoup
import os

# fonction pour extraire les points
def getPoint(i_file, class_name):
    spans_with_class =[]
    with open(i_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    span_with_class = []
    # Trouver tous les span avec la classe spécifiée
    span_tags = soup.find_all('div', class_=class_name)
    for span_tag in span_tags:
        span_with_class = {}
        span_with_class['class'] = class_name
        span_with_class['children'] = []
        span_with_class['point'] = 0
        for child in span_tag.children:
            if child.name:  # Vérifier si l'enfant est un élément HTML
                child_data = {
                    'tag': child.name,
                    'attributes': dict(child.attrs),
                    'text': child.get_text(strip=True)
                }
                #print(child_data['text'])
                span_with_class['children'].append(child_data)
                span_with_class['point'] = child_data['text']
            #print(child)
        #print(span_with_class)
        if span_tag.text:
            point = span_tag.get_text(strip=True)
        
            span_with_class['point']= point
            #print(span_with_class)
        spans_with_class.append(span_with_class)
    print(span_with_class['children'][0]['text'])
    #print('bonjour')
    return spans_with_class 

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
        div_with_class['points'] = 0
        
        
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

def getQuestion(dossier, class_name_to_extract, json_file, questions_file):
    cpt = 1
    for filename in os.listdir(dossier):
        if filename.endswith(".html"):  # Filtrer les fichiers texte
            full_path = os.path.join(dossier, filename)
            extract(full_path, class_name_to_extract, json_file)
            pattern = r"[A-Z]\d{2}"
            replacement = r"  "
            with open(json_file, 'r', encoding='utf-8') as file:
                json_content = json.load(file)
                text = ""
            with open(questions_file+str(cpt)+'.json', 'w', encoding='utf-8') as final_file:
                final_file.write('[')
                j = 0
                for elt in json_content:
                    data =''
                    if elt['children'][2]['attributes']['class'][0]=="wpProQuiz_questionList":
                        text =  re.sub(pattern, replacement, elt['children'][2]['text'])
                        i=0
                        for token in text.split('  '):
                            globals()['p_'+ str(i)] = token 
                            i+=1
                        data ={
                            "id": j,
                            "title": "",
                            "proposition": {
                                "p1": globals()['p_'+ str(1)],
                                "p2": globals()['p_'+ str(2)],
                                "p3": globals()['p_'+ str(3)],
                                "p4": globals()['p_'+ str(4)]

                            },
                            "point":"",
                            "niveau" : "",
                            "reponse" :"",
                        }
                        
                        json.dump(data, final_file, indent=4)
                        if (j<len(json_content)-1):
                            final_file.write(',')
                    j+=1
                final_file.write(']')
            cpt+=1
# Nom du fichier HTML à ouvrir
# Obtenir le chemin du dossier parent (le projet)
dossier_parent = os.path.dirname(os.path.abspath(__file__))  # Obtient le chemin du fichier en cours

# Chemin du sous-dossier
sous_dossier = "html_files"  # Remplacez par le nom de votre sous-dossier

# Chemin complet du dossier à traiter
dossier = os.path.join(dossier_parent, sous_dossier)
# La classe html a extraire
class_name_to_extract = "wpProQuiz_question"
#Le fichier json extrait de l'html
json_file = 'extracted_data.json'
#le fichier json contenant les qustions extraites
questions_file ='serie_'
#getQuestion(dossier, class_name_to_extract,  json_file, questions_file)
getPoint('html_files/index.html', 'lqc-available-points')
                    

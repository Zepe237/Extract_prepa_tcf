import pytesseract
from PIL import Image

# Charger l'image
image = Image.open("Compréhension-Ecrite-Test-1Q1-avec-Q.png")

# Utiliser Tesseract OCR pour extraire le texte de l'image
text = pytesseract.image_to_string(image)

# Afficher le texte extrait
print(text)

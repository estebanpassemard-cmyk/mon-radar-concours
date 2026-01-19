import requests
from bs4 import BeautifulSoup
import os

def chercher():
    # Liste de sites de marques et plateformes directes
    urls = [
        "https://www.touslesconcours.fr/nouveaux.php",
        "https://www.vivez-plus-fort.fr/concours/",
        "https://www.ledemondujeu.com/concours-du-jour.html"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    tous_les_liens = []

    for url in urls:
        try:
            print(f"Analyse de : {url}")
            r = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            for a in soup.find_all('a', href=True):
                titre = a.text.strip()
                lien = a['href']
                
                # FILTRE GROS LOTS UNIQUEMENT
                mots_cles = ["auto", "voiture", "voyage", "iphone", "pc", "tv", "€", "argent"]
                if any(m in titre.lower() for m in mots_cles) and len(titre) > 10:
                    if not lien.startswith('http'):
                        from urllib.parse import urljoin
                        lien = urljoin(url, lien)
                    tous_les_liens.append((titre, lien))
        except Exception as e:
            print(f"Erreur sur {url} ignorée.")
            continue

    # CREATION DU FICHIER HTML SANS BALISES COMPLEXES
    html_content = """<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; background: #1a1a1a; color: white; padding: 20px; }
        .box { background: #333; margin-bottom: 15px; padding: 15px; border-radius: 10px; border-left: 5px solid gold; }
        a { color: #00ff00; text-decoration: none; font-weight: bold; font-size: 1.2em; }
    </style></head><body><h1>🚀 MON RADAR DIRECT</h1>"""

    for t, l in tous_les_liens[:30]:
        html_content += f'<div class="box"><b>{t}</b><br><br><a href="{l}" target="_blank">CLIQUE ICI POUR JOUER</a></div>'

    html_content += "</body></html>"
    
    with open("concours.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    chercher()

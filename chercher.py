import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urljoin

def recuperer_concours_site(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    concours_trouves = []
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        source_nom = url.split("//")[1].split("/")[0].replace("www.", "")
        
        for l in soup.find_all('a', href=True):
            titre = l.text.strip()
            if "concours" in titre.lower() or "gagner" in titre.lower():
                if len(titre) > 12:
                    lien_propre = urljoin(url, l['href'])
                    concours_trouves.append({"titre": titre, "lien": lien_propre, "source": source_nom})
        return concours_trouves
    except:
        return []

def generer_page_complete(liste_concours):
    random.shuffle(liste_concours)
    
    # On prépare le début du HTML
    html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Mon Radar Cadeaux</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: auto; padding: 20px; background-color: #f4f4f9; }
        h1 { text-align: center; color: #2c3e50; }
        .card { background: white; padding: 15px; margin-bottom: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .source { color: #888; font-size: 0.8em; }
        .btn { display: inline-block; margin-top: 10px; color: #28a745; font-weight: bold; text-decoration: none; }
    </style>
</head>
<body>
    <h1>🎯 Mes Concours du Jour</h1>
    """

    vu = set()
    compteur = 0
    for c in liste_concours:
        if c['lien'] not in vu and compteur < 50:
            html += f'''
    <div class="card">
        <strong>🎁 {c['titre']}</strong><br>
        <span class="source">Source : {c['source']}</span><br>
        <a href="{c['lien']}" target="_blank" class="btn">Participer →</a>
    </div>'''
            vu.add(c['lien'])
            compteur += 1

    # On ferme le HTML
    html += """
    </body>
</html>"""

    # ON ECRASE TOUT LE FICHIER AVEC LE NOUVEAU CONTENU
    with open("concours.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Fichier concours.html entièrement recréé avec succès !")

if __name__ == "__main__":
    urls = [
        "https://www.toutgagner.com/nouveaux-concours.html",
        "https://www.ledemondujeu.com/concours-du-jour.html",
        "https://www.concours-du-net.com/nouveaux-concours.php",
        "https://www.jeu-concours.biz/",
        "https://www.infoconcours.com/"
    ]
    
    tous = []
    for u in urls:
        print(f"Recherche sur : {u}")
        tous.extend(recuperer_concours_site(u))
    
    if tous:
        generer_page_complete(tous)

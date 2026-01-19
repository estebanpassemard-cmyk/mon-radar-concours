import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urljoin

def recuperer_details_concours(url_referencement):
    """Va sur la page du site de concours pour trouver le vrai lien et la description"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        resp = requests.get(url_referencement, headers=headers, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # On cherche un résumé (souvent dans les balises <p> ou les meta descriptions)
        description = "Cliquez pour découvrir le lot..."
        p_tags = soup.find_all('p')
        for p in p_tags:
            texte = p.text.strip()
            if len(texte) > 30 and len(texte) < 200:
                description = texte
                break
        
        return description
    except:
        return "Pas de description disponible."

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
                if len(titre) > 15:
                    lien_propre = urljoin(url, l['href'])
                    # On ne récupère le résumé que pour les 10 premiers de chaque site pour ne pas être trop lent
                    desc = "Chargement du résumé..."
                    concours_trouves.append({
                        "titre": titre, 
                        "lien": lien_propre, 
                        "source": source_nom,
                        "desc": desc
                    })
        return concours_trouves
    except:
        return []

def generer_page_complete(liste_concours):
    random.shuffle(liste_concours)
    
    html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mon Radar Cadeaux Pro</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; max-width: 800px; margin: auto; padding: 20px; background-color: #f0f2f5; }
        h1 { text-align: center; color: #1a73e8; }
        .card { background: white; padding: 20px; margin-bottom: 15px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #1a73e8; }
        .titre { font-size: 1.2em; color: #333; display: block; margin-bottom: 8px; font-weight: bold; }
        .description { color: #555; font-size: 0.95em; margin-bottom: 15px; font-style: italic; background: #f9f9f9; padding: 10px; border-radius: 5px; }
        .source { color: #999; font-size: 0.8em; }
        .btn { display: block; text-align: center; background: #28a745; color: white; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; transition: background 0.3s; }
        .btn:hover { background: #218838; }
    </style>
</head>
<body>
    <h1>🎯 Radar à Concours Pro</h1>"""

    vu = set()
    compteur = 0
    for c in liste_concours:
        if c['lien'] not in vu and compteur < 40:
            # Pour chaque concours, on essaie d'aller chercher le résumé
            description_reelle = recuperer_details_concours(c['lien'])
            
            html += f'''
    <div class="card">
        <span class="titre">🎁 {c['titre']}</span>
        <div class="description">"{description_reelle}"</div>
        <span class="source">Source : {c['source']}</span><br><br>
        <a href="{c['lien']}" target="_blank" class="btn">PARTICIPER DIRECTEMENT</a>
    </div>'''
            vu.add(c['lien'])
            compteur += 1

    html += "</body></html>"

    with open("concours.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    urls = [
        "https://www.toutgagner.com/nouveaux-concours.html",
        "https://www.ledemondujeu.com/concours-du-jour.html",
        "https://www.concours-du-net.com/nouveaux-concours.php"
    ]
    
    tous = []
    for u in urls:
        print(f"Extraction : {u}")
        tous.extend(recuperer_concours_site(u))
    
    if tous:
        generer_page_complete(tous)

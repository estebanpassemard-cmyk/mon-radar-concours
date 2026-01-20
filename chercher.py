import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, unquote
import re

def extraire_vrai_lien(url):
    """Saute les redirections pour aller sur le site de la marque"""
    patterns = [r'url=([^&]+)', r'dest=([^&]+)', r'link=([^&]+)']
    for p in patterns:
        match = re.search(p, url)
        if match:
            clean = unquote(match.group(1))
            if clean.startswith('http'): return clean
    return url

def chercher():
    urls = [
        "https://www.toutgagner.com/nouveaux-concours.html",
        "https://www.ledemondujeu.com/concours-du-jour.html",
        "https://www.concours-du-net.com/nouveaux-concours.php",
        "https://www.jeu-concours.biz/",
        "https://www.touslesconcours.fr/nouveaux.php"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
    tous_les_liens = []
    vu = set()

    # Liste de mots-clés "Gros Lots" élargie
    mots_cles = [
        "auto", "voiture", "voyage", "séjour", "week-end", "iphone", "samsung", 
        "macbook", "pc", "ordinateur", "tv", "télévision", "€", "euro", 
        "argent", "chèque", "virement", "ps5", "console", "cuisine", "vélo"
    ]

    for url in urls:
        try:
            print(f"Scan de {url}...")
            r = requests.get(url, headers=headers, timeout=12)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            for a in soup.find_all('a', href=True):
                titre = a.text.strip()
                lien_brut = a['href']
                
                # On vérifie si c'est un gros lot
                t_lower = titre.lower()
                if any(m in t_lower for m in mots_cles) and len(titre) > 12:
                    lien_final = extraire_vrai_lien(urljoin(url, lien_brut))
                    
                    if lien_final not in vu:
                        source = url.split("//")[1].split("/")[0].replace("www.", "")
                        tous_les_liens.append({"titre": titre, "lien": lien_final, "source": source})
                        vu.add(lien_final)
        except:
            continue

    # Génération HTML robuste
    html = """<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #f8fafc; padding: 15px; margin: 0; }
        .container { max-width: 800px; margin: auto; }
        h1 { text-align: center; color: #38bdf8; font-size: 1.5rem; }
        .card { background: #1e293b; border-radius: 12px; padding: 15px; margin-bottom: 15px; border-left: 5px solid #f1c40f; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
        .source { color: #94a3b8; font-size: 0.75rem; font-weight: bold; text-transform: uppercase; }
        .title { display: block; margin: 8px 0; font-size: 1.1rem; font-weight: bold; line-height: 1.3; }
        .btn { display: block; background: #22c55e; color: white; text-align: center; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; margin-top: 10px; }
    </style></head><body><div class="container"><h1>💎 MON RADAR HAUTE VALEUR</h1>"""

    if not tous_les_liens:
        html += "<p style='text-align:center;'>Recherche en cours ou aucun nouveau gros lot trouvé...</p>"
    else:
        for c in tous_les_liens[:50]: # On affiche jusqu'à 50 résultats
            html += f'''<div class="card">
                <span class="source">{c['source']}</span>
                <span class="title">🎁 {c['titre']}</span>
                <a href="{c['lien']}" target="_blank" class="btn">PARTICIPER DIRECTEMENT</a>
            </div>'''

    html += "</div></body></html>"
    with open("concours.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    chercher()

import requests
from bs4 import BeautifulSoup
import re
import random

def recuperer_concours_directs():
    """Cherche sur des plateformes de concours directs (sans compte obligatoire)"""
    # Plateformes utilisées par les marques pour leurs jeux directs
    sources = [
        "https://gleam.io/competitions",
        "https://www.vivez-plus-fort.fr/concours/",
        "https://www.touslesconcours.fr/nouveaux.php"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
    resultats = []

    for url in sources:
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(resp.text, 'html.parser')
            domaine = url.split("//")[1].split("/")[0]
            
            for l in soup.find_all('a', href=True):
                titre = l.text.strip()
                lien = l['href']
                
                # FILTRE : On ne garde que les gros lots (Auto, Voyage, Tech)
                t_low = titre.lower()
                gros_mots = ["auto", "voiture", "voyage", "séjour", "iphone", "macbook", "pc", "tv", "€", "euro", "virement"]
                
                if any(m in t_low for m in gros_mots) and len(titre) > 10:
                    if not lien.startswith('http'):
                        from urllib.parse import urljoin
                        lien = urljoin(url, lien)
                    
                    resultats.append({
                        "titre": titre,
                        "lien": lien,
                        "source": domaine
                    })
        except:
            continue
    return resultats

def generer_page_radar(liste):
    html = """<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: white; padding: 20px; }
        .card { background: #1e293b; border-radius: 12px; padding: 20px; margin-bottom: 15px; border-left: 6px solid #fbbf24; }
        .source { color: #38bdf8; font-size: 0.8rem; font-weight: bold; }
        .title { display: block; margin: 10px 0; font-size: 1.2rem; font-weight: bold; }
        .btn { display: block; background: #22c55e; color: white; text-align: center; padding: 15px; border-radius: 8px; text-decoration: none; font-weight: bold; }
    </style></head><body>
    <h1 style="text-align:center;">🚀 RADAR DIRECT MARQUES</h1>"""

    for c in liste[:30]:
        html += f'''<div class="card">
            <span class="source">🌐 SOURCE : {c['source']}</span>
            <span class="title">🎁 {c['titre']}</span>
            <a href="{c['lien']}" target="_blank" class="btn">PARTICIPER DIRECTEMENT</a>
        </div>'''

    html += "</body></html>"
    with open("concours.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    print("🚀 Démarrage du robot...")
    data = recuperer_concours_directs()
    if data:
        generer_page_radar(data)
        print(f"✅ Terminé : {len(data)} concours trouvés.")
    else:
        print("⚠️ Aucun concours trouvé, vérifiez les filtres.")

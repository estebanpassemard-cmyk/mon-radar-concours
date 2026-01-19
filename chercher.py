import requests
from bs4 import BeautifulSoup
import random
import re
import time
from urllib.parse import urljoin, unquote

# --- CONFIGURATION IA & FILTRES ---
MOTS_PRESTIGE = ["auto", "voiture", "argent", "chèque", "virement", "€", "euro", "voyage", "séjour", "croisière"]
MOTS_TECH = ["iphone", "macbook", "pc", "ordinateur", "tv", "télévision", "ps5", "xbox", "cuisine", "robot", " Dyson"]

def extraire_direct_link(url):
    """Tente de sauter l'intermédiaire pour arriver sur le formulaire final"""
    patterns = [r'url=([^&]+)', r'dest=([^&]+)', r'link=([^&]+)', r'target=([^&]+)']
    for p in patterns:
        match = re.search(p, url)
        if match:
            url_claire = unquote(match.group(1))
            if url_claire.startswith('http'): return url_claire
    return url

def classer_concours(titre):
    t = titre.lower()
    if any(m in t for m in MOTS_PRESTIGE): return "PRESTIGE"
    if any(m in t for m in MOTS_TECH): return "TECH"
    return "GROS_LOTS"

def est_valide(titre):
    t = titre.lower()
    poubelle = ["cinéma", "place", "dvd", "livre", "goodies", "échantillon", "entrée", "mug", "remise", "poster"]
    if any(p in t for p in poubelle): return False
    return any(v in t for v in (MOTS_PRESTIGE + MOTS_TECH + ["gagner", "concours", "jouer"]))

def scraper_site(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
    results = []
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        source = url.split("//")[1].split("/")[0].replace("www.", "")
        for l in soup.find_all('a', href=True):
            titre = l.text.strip()
            if len(titre) > 15 and est_valide(titre):
                results.append({
                    "titre": titre,
                    "lien": extraire_direct_link(urljoin(url, l['href'])),
                    "source": source,
                    "cat": classer_concours(titre)
                })
        return results
    except: return []

if __name__ == "__main__":
    # LISTE ÉLARGIE DES SITES
    sites = [
        "https://www.toutgagner.com/nouveaux-concours.html",
        "https://www.ledemondujeu.com/concours-du-jour.html",
        "https://www.concours-du-net.com/nouveaux-concours.php",
        "https://www.jeu-concours.biz/",
        "https://www.infoconcours.com/",
        "https://www.e-concours.net/",
        "https://www.plusdebonsplans.com/concours"
    ]
    
    tous = []
    for s in sites:
        print(f"Scan : {s}")
        tous.extend(scraper_site(s))
        time.sleep(1)

    # STRUCTURE HTML AVEC GRID
    html = """<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #f1f5f9; margin: 0; padding: 10px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; }
        .column { background: #1e293b; border-radius: 12px; padding: 15px; border: 1px solid #334155; }
        h2 { border-bottom: 2px solid #38bdf8; padding-bottom: 5px; color: #38bdf8; font-size: 1.2rem; }
        .card { background: #0f172a; border-radius: 8px; padding: 12px; margin-bottom: 12px; border-left: 4px solid #38bdf8; }
        .card.prestige { border-left-color: #f1c40f; }
        .source { font-size: 0.7rem; color: #94a3b8; }
        .btn { display: block; background: #22c55e; color: white; text-align: center; padding: 10px; border-radius: 6px; text-decoration: none; font-weight: bold; margin-top: 10px; }
    </style></head><body>
    <h1 style="text-align:center; color:#38bdf8;">💎 DASHBOARD CONCOURS PRO</h1>
    <div class="grid">"""

    for cat, nom, color in [("PRESTIGE", "🏆 PRESTIGE", "prestige"), ("TECH", "💻 TECH & MAISON", "tech"), ("GROS_LOTS", "🎁 AUTRES GROS LOTS", "autres")]:
        html += f'<div class="column"><h2>{nom}</h2>'
        vu = set()
        for c in [x for x in tous if x['cat'] == cat]:
            if c['titre'].lower() not in vu and len(vu) < 20:
                html += f'''<div class="card {color}">
                    <span class="source">{c['source']}</span><br>
                    <strong>{c['titre']}</strong>
                    <a href="{c['lien']}" target="_blank" class="btn">PARTICIPER</a>
                </div>'''
                vu.add(c['titre'].lower())
        html += "</div>"

    html += "</div></body></html>"
    with open("concours.html", "w", encoding="utf-8") as f: f.write(html)

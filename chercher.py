import requests
from bs4 import BeautifulSoup
import random
import re
import time
from urllib.parse import urljoin, unquote

def extraire_reponse_ia(url_page):
    """Essaye de trouver la réponse au concours"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
    try:
        resp = requests.get(url_page, headers=headers, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        texte = soup.get_text()
        match = re.search(r'(?:Rép|Réponse|R1|Réponses)\s*[:\-]\s*([^\n\.]+)', texte, re.IGNORECASE)
        return match.group(1).strip() if match else "À chercher sur la page"
    except:
        return "Non détectée"

def est_un_gros_lot(titre):
    t = titre.lower()
    # On définit ce qui a de la valeur
    valeur = ["tv", "télévision", "auto", "voiture", "voyage", "séjour", "iphone", "macbook", "pc", "argent", "chèque", "€", "euro", "virement", "ps5", "moto", "vélo", "cuisine"]
    # On définit ce qu'on veut ignorer
    poubelle = ["cinéma", "place", "dvd", "livre", "goodies", "échantillon", "entrée", "mug", "porte-clés"]
    
    if any(p in t for p in poubelle) and not any(v in t for v in valeur):
        return False
    return any(v in t for v in valeur)

def recuperer_de_site(url):
    """Récupère les liens filtrés pour un site donné"""
    # Identité aléatoire pour éviter les blocages
    agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    headers = {'User-Agent': random.choice(agents)}
    resultats = []
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        source_nom = url.split("//")[1].split("/")[0].replace("www.", "")
        
        for l in soup.find_all('a', href=True):
            titre = l.text.strip()
            if len(titre) > 15 and est_un_gros_lot(titre):
                lien_brut = urljoin(url, l['href'])
                # On nettoie les redirections
                match = re.search(r'(?:url|dest|link)=([^&]+)', lien_brut)
                lien_final = unquote(match.group(1)) if match else lien_brut
                resultats.append({"titre": titre, "lien": lien_final, "source": source_nom})
        
        # On ne garde que les 15 premiers de CHAQUE site pour laisser de la place aux autres
        return resultats[:15]
    except Exception as e:
        print(f"Erreur sur {url} : {e}")
        return []

if __name__ == "__main__":
    sites = [
        "https://www.toutgagner.com/nouveaux-concours.html",
        "https://www.ledemondujeu.com/concours-du-jour.html",
        "https://www.concours-du-net.com/nouveaux-concours.php",
        "https://www.jeu-concours.biz/",
        "https://www.infoconcours.com/"
    ]
    
    global_concours = []
    for s in sites:
        print(f"📡 Scan de {s}...")
        liste_site = recuperer_de_site(s)
        global_concours.extend(liste_site)
        time.sleep(2) # Petite pause pour être discret

    # Création de la page HTML
    random.shuffle(global_concours)
    html = """<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Arial', sans-serif; background: #0f172a; color: #f8fafc; padding: 15px; }
        h1 { color: #38bdf8; text-align: center; font-size: 1.5rem; }
        .card { background: #1e293b; border-radius: 12px; padding: 18px; margin-bottom: 20px; border: 1px solid #334155; }
        .tag { background: #0369a1; color: #bae6fd; font-size: 0.7rem; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; }
        .titre { font-size: 1.1rem; font-weight: bold; margin: 10px 0; color: #f1f5f9; display: block; }
        .reponse { background: #064e3b; border-left: 4px solid #10b981; padding: 10px; margin: 12px 0; font-size: 0.9rem; color: #d1fae5; }
        .btn { display: block; background: #0284c7; color: white; text-align: center; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; }
    </style></head><body><h1>💎 RADAR GROS LOTS (MULTI-SITES)</h1>"""

    vu = set()
    for c in global_concours[:40]:
        if c['titre'].lower() not in vu:
            rep = extraire_reponse_ia(c['lien'])
            html += f'''<div class="card">
                <span class="tag">{c['source']}</span>
                <span class="titre">💰 {c['titre']}</span>
                <div class="reponse"><b>💡 RÉPONSE IA :</b> {rep}</div>
                <a href="{c['lien']}" target="_blank" class="btn">PARTICIPER MAINTENANT</a>
            </div>'''
            vu.add(c['titre'].lower())

    html += "</body></html>"
    with open("concours.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Mise à jour terminée.")

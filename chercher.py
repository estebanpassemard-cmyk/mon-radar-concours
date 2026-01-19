import requests
from bs4 import BeautifulSoup
import random
import re
from urllib.parse import urljoin, unquote

def extraire_reponse_et_lots(url_page):
    """Analyse la page source pour trouver la réponse et les lots"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        resp = requests.get(url_page, headers=headers, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        texte_complet = soup.get_text()
        
        # IA Simplifiée : Recherche de la réponse
        reponse = "Pas de question détectée"
        match = re.search(r'(?:Rép|Réponse|R1)\s*[:\-]\s*([^\n\.]+)', texte_complet, re.IGNORECASE)
        if match:
            reponse = match.group(1).strip()
            
        return reponse
    except:
        return "Non trouvée"

def est_un_gros_lot(titre):
    """Filtre de valeur pour ne garder que le premium"""
    t = titre.lower()
    gros_lots = ["tv", "télévision", "auto", "voiture", "voyage", "séjour", "iphone", "macbook", "ordinateur", "pc", "argent", "chèque", "€", "euro", "virement", "cuisine", "ps5", "xbox"]
    petits_lots = ["cinéma", "place", "dvd", "livre", "goodies", "échantillon", "entrée", "lot de"]
    
    # Si un petit mot est présent, on jette (sauf si un gros mot est aussi là)
    if any(p in t for p in petits_lots) and not any(g in t for g in gros_lots):
        return False
    # On garde si un gros mot est présent
    return any(g in t for g in gros_lots)

def recuperer_concours_site(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    concours_trouves = []
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for l in soup.find_all('a', href=True):
            titre = l.text.strip()
            if est_un_gros_lot(titre):
                lien_brut = urljoin(url, l['href'])
                # Extraction du lien direct si possible
                match = re.search(r'(?:url|dest|link)=([^&]+)', lien_brut)
                lien_final = unquote(match.group(1)) if match else lien_brut
                
                concours_trouves.append({"titre": titre, "lien": lien_final, "source": url.split("//")[1][:15]})
        return concours_trouves
    except: return []

def generer_page(liste):
    random.shuffle(liste)
    html = """<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background: #121212; color: white; padding: 15px; }
        .card { background: #1e1e1e; border-radius: 12px; padding: 15px; margin-bottom: 15px; border: 1px solid #333; }
        .titre { color: #f1c40f; font-size: 1.1em; font-weight: bold; }
        .reponse { background: #2c3e50; padding: 8px; border-radius: 5px; margin: 10px 0; color: #ff4757; font-weight: bold; border-left: 4px solid #ff4757; }
        .btn { display: block; background: #27ae60; color: white; text-align: center; padding: 12px; border-radius: 8px; text-decoration: none; }
    </style></head><body><h1>💎 Radar Gros Lots & IA</h1>"""

    for c in liste[:30]:
        rep = extraire_reponse_et_lots(c['lien'])
        html += f'''<div class="card">
            <div class="titre">💰 {c['titre']}</div>
            <div class="reponse">💡 IA - Réponse probable : {rep}</div>
            <small>Source : {c['source']}</small><br><br>
            <a href="{c['lien']}" target="_blank" class="btn">PARTICIPER MAINTENANT</a>
        </div>'''
    
    html += "</body></html>"
    with open("concours.html", "w", encoding="utf-8") as f: f.write(html)

if __name__ == "__main__":
    sites = ["https://www.toutgagner.com/nouveaux-concours.html", "https://www.ledemondujeu.com/concours-du-jour.html", "https://www.concours-du-net.com/nouveaux-concours.php"]
    tous = []
    for s in sites: tous.extend(recuperer_concours_site(s))
    if tous: generer_page(tous)

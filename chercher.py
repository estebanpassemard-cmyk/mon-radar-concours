import requests
from bs4 import BeautifulSoup
import re
import random
from urllib.parse import unquote

def recherche_ia_marques():
    """Cherche des formulaires directs sur le web sans passer par les sites de concours"""
    # Requêtes ciblées pour trouver des formulaires de marques (.fr ou .com)
    # On cherche des structures d'URL que les agrégateurs n'ont pas
    queries = [
        'site:.fr "jeu concours" "règlement" 2026 -toutgagner -ledemondujeu',
        'site:.fr "gagner" (voiture | voyage | iphone) "formulaire"',
        'intitle:"jeu concours" "dotation" 2026',
        'inurl:concours "inscription"'
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
    direct_results = []
    
    # On utilise un moteur qui autorise l'extraction (ici DuckDuckGo version HTML)
    for q in queries:
        url = f"https://html.duckduckgo.com/html/?q={q}"
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            for item in soup.find_all('a', class_='result__a', href=True):
                link = item['href']
                title = item.text.strip()
                
                # NETTOYAGE : On ignore les sites de référencement connus
                blacklist = ["toutgagner", "ledemondujeu", "concours-du-net", "jeu-concours", "infoconcours", "vendeur", "comparateur"]
                if not any(b in link.lower() for b in blacklist):
                    # On essaie de deviner la marque via l'URL
                    domain = link.split("//")[-1].split("/")[0].replace("www.", "")
                    
                    direct_results.append({
                        "titre": title,
                        "lien": link,
                        "source": domain,
                        "prio": 1 if any(word in title.lower() for word in ["voiture", "auto", "voyage", "argent", "€"]) else 0
                    })
        except:
            continue
    return direct_results

def generer_radar_pro(liste):
    # Tri par priorité (Gros lots d'abord)
    liste.sort(key=lambda x: x['prio'], reverse=True)
    
    html = """<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">
    <meta name="viewport"

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def recherche_marques_directe():
    """Simule une recherche IA pour trouver des concours sur des sites de marques"""
    # On cible des mots-clés de marques et de gros lots
    requetes = [
        "site:.fr inurl:concours voiture 2026",
        "site:.com gagner iphone 16 règlement",
        "site:.fr \"jeu concours\" (voyage | séjour | virement)",
        "inurl:formulaire-concours luxe"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
    direct_links = []

    # Note: Dans une version pro, on utiliserait l'API Google Search ici.
    # Pour GitHub, on va utiliser un moteur de recherche qui ne bloque pas les robots (comme DuckDuckGo)
    for q in requetes:
        url = f"https://html.duckduckgo.com/html/?q={q}"
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            for a in soup.find_all('a', class_='result__a', href=True):
                titre = a.text.strip()
                lien = a['href']
                
                # On filtre pour exclure les sites de référencement classiques
                exclusions = ["toutgagner", "ledemondujeu", "concours-du-net", "jeu-concours.biz"]
                if not any(ex in lien for ex in exclusions):
                    direct_links.append({
                        "titre": titre,
                        "lien": lien,
                        "source": "Détection Directe Marque",
                        "cat": "PRESTIGE" if "voiture" in titre.lower() or "voyage" in titre.lower() else "TECH"
                    })
        except:
            continue
    return direct_links

# ... (reste du code de génération HTML identique à la version précédente)

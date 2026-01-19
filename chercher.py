import requests
from bs4 import BeautifulSoup
import os
import random

def recuperer_concours_site(url):
    """Cherche les liens de concours de manière intelligente sur n'importe quel site"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    concours_trouves = []
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # On cherche tous les liens qui contiennent le mot 'concours' dans leur texte ou URL
        for l in soup.find_all('a', href=True):
            titre = l.text.strip()
            lien = l['href']
            
            # Nettoyage et filtrage
            if "concours" in titre.lower() or "gagner" in titre.lower():
                if len(titre) > 15: # Évite les liens trop courts type 'Nos concours'
                    if not lien.startswith('http'):
                        from urllib.parse import urljoin
                        lien = urljoin(url, lien)
                    
                    source = url.split("//")[1].split("/")[0].replace("www.", "")
                    concours_trouves.append({
                        "titre": titre,
                        "lien": lien,
                        "source": source
                    })
        return concours_trouves
    except:
        return []

def mettre_a_jour_fichier(liste_concours):
    if not os.path.exists("concours.html"): return
    
    # On mélange les résultats pour ne pas avoir tous les concours du même site en haut
    random.shuffle(liste_concours)
    
    html_final = ""
    for c in liste_concours[:40]: # On garde les 40 meilleurs résultats
        html_final += f'''
        <div style="border-bottom: 1px solid #eee; padding: 15px; margin-bottom: 10px; background: #fff;">
            <strong style="font-size: 16px; color: #333;">🎁 {c['titre']}</strong><br>
            <small style="color: #888;">Source : {c['source']}</small><br>
            <a href="{c['lien']}" target="_blank" style="color: #28a745; font-weight: bold; text-decoration: none; display: inline-block; margin-top: 5px;">Voir le concours →</a>
        </div>'''

    with open("concours.html", "r", encoding="utf-8") as f:
        page = f.read()

    D, F = "", ""
    if D in page and F in page:
        nouvelle_page = page.split(D)[0] + D + html_final + F + page.split(F)[1]
        with open("concours.html", "w", encoding="utf-8") as f:
            f.write(nouvelle_page)

if __name__ == "__main__":
    # Voici une liste de sites populaires de concours
    liste_urls = [
        "https://www.toutgagner.com/nouveaux-concours.html",
        "https://www.ledemondujeu.com/concours-du-jour.html",
        "https://www.concours-du-net.com/nouveaux-concours.php",
        "https://www.jeu-concours.biz/",
        "https://www.infoconcours.com/"
    ]
    
    tous_les_concours = []
    for url in liste_urls:
        print(f"Extraction sur : {url}")
        tous_les_concours.extend(recuperer_concours_site(url))
    
    if tous_les_concours:
        mettre_a_jour_fichier(tous_les_concours)
        print(f"Terminé ! {len(tous_les_concours)} concours trouvés.")

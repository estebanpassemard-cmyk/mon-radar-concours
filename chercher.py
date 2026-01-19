import requests
from bs4 import BeautifulSoup
import os

def recuperer_concours():
    url = "https://www.toutgagner.com/nouveaux-concours.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        html_genere = ""
        liens = soup.find_all('a', href=True)
        compteur = 0
        for l in liens:
            titre = l.text.strip()
            if "concours" in titre.lower() and len(titre) > 10 and compteur < 15:
                lien_reel = l['href']
                if not lien_reel.startswith('http'): 
                    lien_reel = "https://www.toutgagner.com" + lien_reel
                html_genere += f'<div style="border-bottom:1px solid #eee;padding:10px;"><strong>🎁 {titre}</strong><br><a href="{lien_reel}" target="_blank">Participer</a></div>'
                compteur = compteur + 1
        return html_genere
    except:
        return "Erreur de recherche"

def mettre_a_jour_fichier(contenu_neuf):
    # Sécurité absolue : on définit les balises ici
    D = ""
    F = ""
    
    if not os.path.exists("concours.html"):
        print("Fichier concours.html absent")
        return

    with open("concours.html", "r", encoding="utf-8") as f:
        page_complete = f.read()

    if D not in page_complete or F not in page_complete:
        print("BALISES ABSENTES DU HTML")
        return

    # Découpage par étape
    index_debut = page_complete.find(D) + len(D)
    index_fin = page_complete.find(F)
    
    partie_haute = page_complete[:index_debut]
    partie_basse = page_complete[index_fin:]
    
    nouvelle_page = partie_haute + "\n" + contenu_neuf + "\n" + partie_basse

    with open("concours.html", "w", encoding="utf-8") as f:
        f.write(nouvelle_page)
    print("REUSSITE")

if __name__ == "__main__":
    resultats = recuperer_concours()
    mettre_a_jour_fichier(resultats)

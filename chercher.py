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
                compteur += 1
        return html_genere
    except:
        return "<p>Erreur de recherche</p>"

def mettre_a_jour_fichier(contenu_neuf):
    # On vérifie si le fichier existe
    if not os.path.exists("concours.html"):
        print("Fichier concours.html introuvable")
        return

    with open("concours.html", "r", encoding="utf-8") as f:
        page = f.read()

    # Si les balises ne sont pas là, on les affiche pour comprendre pourquoi
    if "" not in page:
        print("BALISE DEBUT MANQUANTE DANS LE HTML")
        return

    # RECONSTRUCTION SIMPLE
    debut_site = page.split("")[0]
    fin_site = page.split("")[1]

    page_finale = debut_site + "" + contenu_neuf + "" + fin_site

    with open("concours.html", "w", encoding="utf-8") as f:
        f.write(page_finale)
    print("Succès !")

if __name__ == "__main__":
    resultats = recuperer_concours()
    mettre_a_jour_fichier(resultats)

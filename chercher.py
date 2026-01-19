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
    nom_fichier = "concours.html"
    # ICI : On définit bien les séparateurs
    marqueur_debut = ""
    marqueur_fin = ""

    if not os.path.exists(nom_fichier):
        print("Fichier introuvable")
        return

    with open(nom_fichier, "r", encoding="utf-8") as f:
        page = f.read()

    if marqueur_debut not in page:
        print("Le marqueur DEBUT est introuvable dans le HTML")
        return

    # DECOUPAGE
    # On coupe au marqueur de début
    parties = page.split(marqueur_debut)
    debut_site = parties[0]
    
    # On coupe le reste au marqueur de fin
    suite = parties[1].split(marqueur_fin)
    fin_site = suite[1]

    # RECONSTRUCTION
    page_finale = debut_site + marqueur_debut + contenu_neuf + marqueur_fin + fin_site

    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(page_finale)
    print("Mise à jour réussie !")

if __name__ == "__main__":
    resultats = recuperer_concours()
    mettre_a_jour_fichier(resultats)

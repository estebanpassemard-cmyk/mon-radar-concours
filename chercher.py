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
        vu = set()
        compteur = 0
        for l in liens:
            titre = l.text.strip()
            if "concours" in titre.lower() and len(titre) > 10 and compteur < 15:
                lien_reel = l['href']
                if not lien_reel.startswith('http'): 
                    lien_reel = "https://www.toutgagner.com" + lien_reel
                if lien_reel not in vu:
                    html_genere += f"""
                    <div style="border-bottom: 1px solid #eee; padding: 15px; margin-bottom: 10px;">
                        <strong style="font-size: 18px;">🎁 {titre}</strong><br>
                        <a href="{lien_reel}" target="_blank" style="color: #28a745; font-weight: bold; text-decoration: none;">Participer maintenant</a>
                    </div>"""
                    vu.add(lien_reel)
                    compteur += 1
        return html_genere
    except Exception as e:
        return f"<p>Erreur de recherche : {e}</p>"

def mettre_a_jour_fichier(contenu_neuf):
    # On définit les balises en dur pour éviter l'erreur "empty separator"
    balise_debut = ""
    balise_fin = ""
    
    if not os.path.exists("concours.html"):
        print("Erreur : Le fichier concours.html est introuvable !")
        return

    with open("concours.html", "r", encoding="utf-8") as f:
        page = f.read()

    if balise_debut not in page or balise_fin not in page:
        print("Erreur : Les balises sont absentes de concours.html")
        return

    # Découpage propre
    parties = page.split(balise_debut)
    debut_du_site = parties[0]
    reste = parties[1].split(balise_fin)
    fin_du_site = reste[1]

    # Reconstruction
    page_finale = debut_du_site + balise_debut + contenu_neuf + balise_fin + fin_du_site

    with open("concours.html", "w", encoding="utf-8") as f:
        f.write(page_finale)
    print("Mise à jour réussie !")

if __name__ == "__main__":
    resultats = recuperer_concours()
    mettre_a_jour_fichier(resultats)

import requests
from bs4 import BeautifulSoup

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
                        <strong>🎁 {titre}</strong><br>
                        <a href="{lien_reel}" target="_blank" style="color: #28a745; font-weight: bold;">Participer</a>
                    </div>"""
                    vu.add(lien_reel)
                    compteur += 1
        return html_genere
    except Exception as e:
        return f"<p>Erreur lors de la récupération : {e}</p>"

def mettre_a_jour_fichier(contenu_neuf):
    # Balises exactes à chercher
    DEBUT = ""
    FIN = ""
    
    with open("concours.html", "r", encoding="utf-8") as f:
        page = f.read()

    # Vérification de sécurité : si les balises sont absentes, on ne fait rien
    if DEBUT not in page or FIN not in page:
        print("Erreur : Les balises DEBUT_LISTE ou FIN_LISTE sont manquantes dans concours.html")
        return

    # On reconstruit la page proprement
    partie_haute = page.split(DEBUT)[0]
    partie_basse = page.split(FIN)[1]
    
    nouvelle_page = partie_haute + DEBUT + contenu_neuf + FIN + partie_basse
    
    with open("concours.html", "w", encoding="utf-8") as f:
        f.write(nouvelle_page)

if __name__ == "__main__":
    resultats = recuperer_concours()
    mettre_a_jour_fichier(resultats)

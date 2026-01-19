import requests
from bs4 import BeautifulSoup

def recuperer_concours():
    # Site de regroupement source
    url = "https://www.toutgagner.com/nouveaux-concours.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    nouveaux_items_html = ""
    liens = soup.find_all('a', href=True)
    vu = set() # Pour éviter les doublons
    
    compteur = 0
    for l in liens:
        titre = l.text.strip()
        # On filtre les liens qui semblent être des jeux
        if "concours" in titre.lower() and len(titre) > 10 and compteur < 15:
            lien_reel = l['href']
            if not lien_reel.startswith('http'): 
                lien_reel = "https://www.toutgagner.com" + lien_reel
            
            if lien_reel not in vu:
                nouveaux_items_html += f"""
                <div class="item">
                    <strong>🎁 {titre}</strong><br>
                    <a href="{lien_reel}" target="_blank" class="btn">Participer</a>
                </div>"""
                vu.add(lien_reel)
                compteur += 1
                
    return nouveaux_items_html

def mettre_a_jour_fichier(contenu_neuf):
    # On ouvre concours.html pour y injecter les résultats
    with open("concours.html", "r", encoding="utf-8") as f:
        ancienne_page = f.read()

    balise_debut = ""
    balise_fin = ""
    
    # On découpe la page et on remplace le milieu
    debut_page = ancienne_page.split(balise_debut)[0]
    fin_page = ancienne_page.split(balise_fin)[1]
    
    page_finale = debut_page + balise_debut + contenu_neuf + balise_fin + fin_page
    
    with open("concours.html", "w", encoding="utf-8") as f:
        f.write(page_finale)

if __name__ == "__main__":
    resultats = recuperer_concours()
    mettre_a_jour_fichier(resultats)

import requests
from bs4 import BeautifulSoup
import os

def extraire_concours(url, selecteur_lien):
    """Fonction générique pour chercher sur un site"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    html_cumule = ""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        liens = soup.select(selecteur_lien) # On cherche les liens spécifiques
        
        compteur = 0
        vu = set()
        
        for l in liens:
            titre = l.text.strip()
            lien_reel = l['href']
            
            # Nettoyage du lien
            if lien_reel.startswith('/'):
                from urllib.parse import urljoin
                lien_reel = urljoin(url, lien_reel)
                
            if "concours" in titre.lower() and lien_reel not in vu and compteur < 10:
                html_cumule += f'''
                <div style="border-bottom:1px solid #eee;padding:15px;">
                    <strong style="color:#333;">🎁 {titre[:100]}</strong><br>
                    <small style="color:#999;">Source: {url.split("//")[1].split("/")[0]}</small><br>
                    <a href="{lien_reel}" target="_blank" style="color:#28a745;text-decoration:none;font-weight:bold;">Participer →</a>
                </div>'''
                vu.add(lien_reel)
                compteur += 1
        return html_cumule
    except Exception as e:
        print(f"Erreur sur {url}: {e}")
        return ""

def mettre_a_jour_fichier(contenu_total):
    if not os.path.exists("concours.html"): return
    
    with open("concours.html", "r", encoding="utf-8") as f:
        page = f.read()

    D, F = "", ""
    if D not in page or F not in page: return

    index_debut = page.find(D) + len(D)
    index_fin = page.find(F)
    
    nouvelle_page = page[:index_debut] + "\n" + contenu_total + "\n" + page[index_fin:]

    with open("concours.html", "w", encoding="utf-8") as f:
        f.write(nouvelle_page)

if __name__ == "__main__":
    # LISTE DES SITES A SURVEILLER
    sites = [
        {"url": "https://www.toutgagner.com/nouveaux-concours.html", "selecteur": "a"},
        {"url": "https://www.ledemondujeu.com/concours-du-jour.html", "selecteur": ".liste-concours a"}
    ]
    
    resultat_final = ""
    for s in sites:
        print(f"Analyse de {s['url']}...")
        resultat_final += extraire_concours(s['url'], s['selecteur'])
    
    mettre_a_jour_fichier(resultat_final)
    print("Terminé !")

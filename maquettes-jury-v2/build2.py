"""Construit miroir.html, tipi.html et belvedere.html (lancer geometrie2.py avant)."""
import json, os
from contenu import TANGRAM
from contenu2 import MAQUETTES
ici = os.path.dirname(os.path.abspath(__file__))
G = json.load(open(os.path.join(ici, "maquettes2.json"), encoding="utf-8"))
gab = open(os.path.join(ici, "gabarit.html"), encoding="utf-8").read()
for nom, m in MAQUETTES.items():
    assert set(e["piece"] for e in m["etapes"]) == set(G[nom]["pieces"])
    data = dict(m, pieces=G[nom]["pieces"], chemin=G[nom]["chemin"], tangram=TANGRAM)
    html = gab.replace("{{DATA}}", json.dumps(data, ensure_ascii=False)).replace("{{TITRE}}", m["titre"])
    open(os.path.join(ici, nom + ".html"), "w", encoding="utf-8").write(html)
    print(nom + ".html", len(html))

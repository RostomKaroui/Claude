"""Construit papillon.html, sheds.html et kiosque.html (lancer geometrie.py avant)."""
import json, os
from contenu import MAQUETTES, TANGRAM
ici = os.path.dirname(os.path.abspath(__file__))
G = json.load(open(os.path.join(ici, "maquettes.json"), encoding="utf-8"))
gab = open(os.path.join(ici, "gabarit.html"), encoding="utf-8").read()
for nom, m in MAQUETTES.items():
    data = dict(m, pieces=G[nom]["pieces"], chemin=G[nom]["chemin"], tangram=TANGRAM)
    assert [e["piece"] for e in m["etapes"]] and set(e["piece"] for e in m["etapes"]) == set(G[nom]["pieces"])
    html = gab.replace("{{DATA}}", json.dumps(data, ensure_ascii=False)).replace("{{TITRE}}", m["titre"])
    assert "{{" not in html
    open(os.path.join(ici, nom + ".html"), "w", encoding="utf-8").write(html)
    print(nom + ".html", len(html), "octets")

"""Construit montage.html (lancer mouvements.py avant)."""
import json, os
ici = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(ici, "mouvements.json"), encoding="utf-8"))
gab = open(os.path.join(ici, "gabarit.html"), encoding="utf-8").read()
html = gab.replace("{{DATA}}", json.dumps(data, ensure_ascii=False))
open(os.path.join(ici, "montage.html"), "w", encoding="utf-8").write(html)
print("montage.html", len(html))

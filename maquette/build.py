"""Construit maquette/index.html (lancer geometrie.py avant)."""
import json, os
ici = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(ici, "pieces.json")))
html = open(os.path.join(ici, "gabarit.html"), encoding="utf-8").read()
html = html.replace("{{PIECES}}", json.dumps(P, ensure_ascii=False))
assert "{{" not in html
open(os.path.join(ici, "index.html"), "w", encoding="utf-8").write(html)
print("index.html", len(html), "octets")

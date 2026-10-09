"""Version épurée du montage : on garde l'animation, les boutons (vues, soleil, couleurs, promenade) et la fiche
de chaque étape ; on enlève le texte autour (titre du haut, les 4 arguments, pied de page, aide de la 3D).
Part de gabarit.html. Lancer : python3 fabriquer_epure.py  ->  montage-epure.html
(mouvements.py puis build.py avant, si la géométrie change)"""
import json, os, re

ici = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(ici, "gabarit.html"), encoding="utf-8").read()
data = json.load(open(os.path.join(ici, "mouvements.json"), encoding="utf-8"))


def retirer(motif):
    global s
    s, n = re.subn(motif, "", s, count=1, flags=re.S)
    assert n == 1, motif


def remplacer(ancien, nouveau):
    global s
    assert s.count(ancien) == 1, f"{s.count(ancien)} occurrence(s) : {ancien[:70]!r}"
    s = s.replace(ancien, nouveau)


# le texte autour
retirer(r'\s*<header class="cartouche">.*?</header>')            # titre, phrase d'intro, les 3 règles
retirer(r'\s*<section class="lecture".*?</section>')              # « Nos quatre arguments »
retirer(r'\s*<footer>.*?</footer>')                               # pied de page
retirer(r'\s*<div class="aide">.*?</div>')                        # « glisser : tourner · molette… »

# téléphone : la caméra recule un peu quand l'écran est plus étroit que large (sans rien changer sur ordinateur)
remplacer("return { p: T([C.c[0] + C.d[0], C.c[1] + C.d[1], C.c[2] + C.d[2]]), c: T(C.c) };",
          "const k = Math.pow(Math.max(1, 1.25 / camera.aspect), 0.9);\n    return { p: T([C.c[0] + C.d[0] * k, C.c[1] + C.d[1] * k, C.c[2] + C.d[2] * k]), c: T(C.c) };")
remplacer("  window.allerEtape(0, true);\n  boucle();", "  taille();\n  window.allerEtape(0, true);\n  boucle();")

remplacer("<title>Montage de la maquette</title>", "<title>Montage épuré</title>")
assert "{{DATA}}" in s
s = s.replace("{{DATA}}", json.dumps(data, ensure_ascii=False))
open(os.path.join(ici, "montage-epure.html"), "w", encoding="utf-8").write(s)
print("montage-epure.html", len(s))

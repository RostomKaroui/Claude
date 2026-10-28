"""Versions épurées du montage (avec et sans couleurs) : on garde l'animation, les boutons (vues, soleil, couleurs, promenade) et la fiche
de chaque étape ; on enlève le texte autour (titre du haut, les 4 arguments, pied de page, aide de la 3D).
Part de gabarit.html. Lancer : python3 fabriquer_epure.py  ->  montage-epure.html et montage-epure-sans-couleurs.html
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

GABARIT_TITRE = "<title>Montage de la maquette</title>"


def ecrire(nom, titre, d):
    page = s.replace(GABARIT_TITRE, f"<title>{titre}</title>")
    assert "{{DATA}}" in page
    page = page.replace("{{DATA}}", json.dumps(d, ensure_ascii=False))
    open(os.path.join(ici, nom), "w", encoding="utf-8").write(page)
    print(nom, len(page))


# 1 · version épurée, avec les couleurs et leur bouton
ecrire("montage-epure.html", "Montage épuré", data)

# 2 · variante sans couleurs : toutes les pièces en carton, plus de bouton « Couleurs », plus de noms de couleurs
remplacer('        <button id="couleurs" type="button" aria-pressed="true">Couleurs</button>\n', "")
remplacer('  const btnCoul = document.getElementById("couleurs");\n'
          '  btnCoul.addEventListener("click", () => { enCouleurs = !enCouleurs; btnCoul.setAttribute("aria-pressed", enCouleurs); majCouleurs(); });\n',
          "  // pas de bouton « Couleurs » dans cette version : toutes les pièces gardent la couleur du carton\n")

CARTON = "#b8ab97"
NOMS = {"G1": "Grand triangle", "G2": "Grand triangle", "M": "Triangle moyen", "C": "Carré",
        "P1": "Petit triangle sud", "P2": "Petit triangle nord", "Pa": "Parallélogramme"}
REMPLACEMENTS = [("Le petit triangle vert", "Le petit triangle du nord"), ("Le petit triangle bleu clair", "Le petit triangle du sud")]


def sans_couleurs(v):
    if isinstance(v, str):
        for a, b in REMPLACEMENTS:
            v = v.replace(a, b)
        return v
    if isinstance(v, list):
        return [sans_couleurs(x) for x in v]
    if isinstance(v, dict):
        return {k: sans_couleurs(x) for k, x in v.items()}
    return v


d2 = sans_couleurs(json.loads(json.dumps(data)))
for k, piece in d2["pieces"].items():
    piece["nom"], piece["couleur"] = NOMS[k], CARTON
reste = re.findall(r"\b(?:vert|bleu|bleue|orange|turquoise|jaune|rouge)\b", json.dumps(d2, ensure_ascii=False), flags=re.I)
assert not reste, reste
ecrire("montage-epure-sans-couleurs.html", "Montage sans couleurs", d2)

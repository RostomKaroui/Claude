"""Version sans texte du montage : seulement l'animation 3D, les flèches et les cases d'étapes (0 à 7).
Part de gabarit.html (même animation, mêmes mouvements) et en retire tout ce qui est écrit.
Lancer : python3 fabriquer_epure.py  ->  montage-sans-texte.html   (mouvements.py puis build.py avant, si la géométrie change)"""
import json, os, re

ici = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(ici, "gabarit.html"), encoding="utf-8").read()
data = json.load(open(os.path.join(ici, "mouvements.json"), encoding="utf-8"))


def remplacer(ancien, nouveau, n=1):
    global s
    assert s.count(ancien) == n, f"{s.count(ancien)} occurrence(s) au lieu de {n} : {ancien[:70]!r}"
    s = s.replace(ancien, nouveau)


# 1 · la page : l'animation, les flèches, les cases d'étapes. Rien d'autre.
page = '''<main class="epure">
  <div class="cadre3d"><canvas id="scene" aria-label="Maquette 3D animée"></canvas></div>
  <div class="commandes">
    <button id="prec" type="button" aria-label="Étape précédente">←</button>
    <button id="suiv" type="button" aria-label="Étape suivante">→</button>
    <ol class="etapes" id="liste"></ol>
    <button id="rejouer" type="button" aria-label="Rejouer l'étape">↺</button>
    <button id="tout" type="button" aria-label="Tout le montage">▶</button>
  </div>
</main>'''
s, n = re.subn(r'<main class="planche">.*?</main>', lambda m: page, s, count=1, flags=re.S)
assert n == 1

# 2 · la mise en page de cette version
remplacer("</style>", """
/* Version sans texte : la 3D prend la place, les commandes dessous. */
body { padding-block: 14px 18px; }
.epure { max-width: 1240px; margin-inline: auto; display: grid; gap: 12px; }
.epure .cadre3d { border: 1.5px solid var(--encre); background: var(--feuille); }
.epure #scene { min-height: 0; aspect-ratio: 16 / 10; max-height: 80vh; }
.commandes { display: flex; flex-wrap: wrap; gap: 8px 12px; align-items: center; justify-content: center; }
.commandes > button { min-width: 46px; min-height: 42px; font-size: 1.1rem; padding: 4px 12px; }
.commandes ol.etapes { gap: 6px; justify-content: center; }
.commandes ol.etapes button { min-width: 3em; min-height: 42px; font-size: .95rem; padding: 4px 9px; gap: 6px; }
@media (max-width: 860px) { .epure #scene { min-height: 0; aspect-ratio: 4 / 5; max-height: 72vh; } }
</style>""")

# 3 · le code : les éléments retirés de la page n'existent plus, on les remplace par des coquilles vides
remplacer('const az = document.getElementById("azimut"), ht = document.getElementById("hauteur");',
          'const az = { value: 25, addEventListener() {} }, ht = { value: 38, addEventListener() {} };   // soleil fixe')
remplacer(" nord.add(lettre);", "")
remplacer("  scene.add(disque);\n", "")      # le disque du soleil n'a plus de commandes      # la lettre N de la flèche du nord est du texte
remplacer("document.getElementById(", "$(", n=s.count("document.getElementById("))
remplacer("<script>\nconst DATA = ", """<script>
// Commandes retirées de cette version (soleil, vues, promenade, légende) : le code qui les cherche ne casse pas.
const FANTOME = () => ({ value: 0, disabled: false, addEventListener() {}, setAttribute() {} });
const $ = id => document.getElementById(id) || FANTOME();
const DATA = """)
remplacer("""  b.title = E.titre;""", """  b.setAttribute("aria-label", "Étape " + i);""")

# 3 bis · écran étroit (téléphone) : la caméra recule pour garder toute la maquette dans le cadre
remplacer("return { p: T([C.c[0] + C.d[0], C.c[1] + C.d[1], C.c[2] + C.d[2]]), c: T(C.c) };",
          "const k = Math.pow(Math.max(1, 1.6 / camera.aspect), 0.85);\n    return { p: T([C.c[0] + C.d[0] * k, C.c[1] + C.d[1] * k, C.c[2] + C.d[2] * k]), c: T(C.c) };")
remplacer("  window.allerEtape(0, true);\n  boucle();", "  taille();\n  window.allerEtape(0, true);\n  boucle();")

# 4 · la fiche ne raconte plus rien : elle marque seulement la case en cours
s, n = re.subn(r"function afficherFiche\(\) \{.*?\n\}\nconst liste", """function afficherFiche() {
  document.querySelectorAll("#liste button").forEach((b, i) => b.setAttribute("aria-pressed", i === etape));
  $("prec").disabled = etape === 0;
  $("suiv").disabled = etape === FIN;
  $("rejouer").disabled = etape === 0 || etape === FIN;
}
const liste""", s, count=1, flags=re.S)
assert n == 1
remplacer('textContent: "La vue 3D n\'a pas pu démarrer (" + e.message + "). Les étapes du montage restent lisibles à droite." }',
          'textContent: "La vue 3D n\'a pas pu démarrer (" + e.message + ")." }')
remplacer("<title>Montage de la maquette</title>", "<title>Montage sans texte</title>")

# 5 · la géométrie vient de mouvements.json, comme dans montage.html
assert "{{DATA}}" in s
s = s.replace("{{DATA}}", json.dumps(data, ensure_ascii=False))
open(os.path.join(ici, "montage-sans-texte.html"), "w", encoding="utf-8").write(s)
print("montage-sans-texte.html", len(s))

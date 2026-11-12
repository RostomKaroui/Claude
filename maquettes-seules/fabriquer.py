"""Versions « seules » des 4 maquettes : la 3D, les flèches d'étapes et le soleil, sans aucun texte.
Géométrie, animation et éclairage identiques aux pages complètes. three.js est intégré au fichier
pour que la page marche une fois téléchargée.  Usage : python3 fabriquer.py <dossier three.js>"""
import os, re, sys
ici = os.path.dirname(os.path.abspath(__file__)); racine = os.path.dirname(ici)
three_dir = sys.argv[1]
THREE = open(os.path.join(three_dir, "build/three.min.js"), encoding="utf-8").read()
ORBIT = open(os.path.join(three_dir, "examples/js/controls/OrbitControls.js"), encoding="utf-8").read()
PAGES = {"le-pli": ("maquette", "Le Pli"), "shahed": ("maquette-shahed", "Maquette de Shahed"),
         "yassmine": ("maquette-yassmine", "Maquette de Yassmine"), "commune": ("maquette-commune", "Maquette commune"),
         "jury": ("maquette-jury", "Maquette du jury")}
CSS = """
body { padding: 0; margin: 0; overflow: hidden; }
#app { height: 100vh; height: 100dvh; display: grid; grid-template-rows: 1fr auto; background: var(--scene); }
#scene { width: 100%; height: 100%; min-height: 0; max-height: none; aspect-ratio: auto; }
.ctrl { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 10px; padding: 10px 16px; background: var(--feuille); border-top: 1.5px solid var(--encre); }
.ctrl .sep { flex: 1; }
.ctrl button { font-size: 1rem; min-width: 2.6em; }
.ctrl input[type=range] { width: 140px; accent-color: var(--trait); }
ol.etapes { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: 5px; }
"""
for nom, (dossier, titre) in PAGES.items():
    html = open(os.path.join(racine, dossier, "index.html"), encoding="utf-8").read()
    az = re.search(r'id="azimut"[^>]*value="(\d+)"', html).group(1)
    ht = re.search(r'id="hauteur"[^>]*value="(\d+)"', html).group(1)
    main = html[html.index('<main class="planche">'):html.index("</main>") + 7]
    # tous les identifiants utilisés par le script restent présents, mais cachés et vides
    ids = [i for i in re.findall(r'id="([^"]+)"', main) if i not in ("scene", "prec", "suiv", "liste", "azimut", "hauteur", "tourner", "promenade")]
    caches = "".join(f'<input id="{i}" value="15">' if i == "cote" else f'<span id="{i}"></span>' for i in ids)
    promenade = '\n    <button id="promenade" type="button" aria-pressed="false" aria-label="Promenade du personnage">🚶</button>' if 'id="promenade"' in main else ""
    corps = f"""<div id="app">
  <canvas id="scene" aria-label="{titre}"></canvas>
  <div class="ctrl">
    <button id="prec" type="button" aria-label="Étape précédente">←</button>
    <ol class="etapes" id="liste"></ol>
    <button id="suiv" type="button" aria-label="Étape suivante">→</button>
    <span class="sep"></span>
    <input id="azimut" type="range" min="0" max="360" value="{az}" aria-label="Direction du soleil">
    <input id="hauteur" type="range" min="5" max="88" value="{ht}" aria-label="Hauteur du soleil">
    <button id="tourner" type="button" aria-pressed="false" aria-label="Faire tourner le soleil">☀</button>{promenade}
  </div>
</div>
<div hidden>{caches}</div>"""
    html = html.replace(main, corps)
    html = html.replace("</style>", CSS + "</style>", 1)
    html = html.replace('<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>', "<script>" + THREE + "</script>")
    html = html.replace('<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>', "<script>" + ORBIT + "</script>")
    html = html.replace("  b.title = E.titre;\n", "")
    assert "cdn.jsdelivr" not in html and "b.title" not in html
    open(os.path.join(ici, nom + ".html"), "w", encoding="utf-8").write(html)
    print(nom, len(html) // 1024, "Ko")

"""Construit montage.html : la page 3D étape par étape (three.js intégré : aucun accès internet nécessaire).
Lancer geometrie.py et patrons.py avant, puis : python3 build.py
"""
import json, math, os
import geometrie as g

ICI = os.path.dirname(os.path.abspath(__file__))
# three.js r128 (npm) : si le dossier n'existe pas encore, « npm pack three@0.128.0 » puis décompresser dans ./three-r128/
THREE = os.environ.get("THREE_DIR", os.path.join(ICI, "three-r128", "package"))
if not os.path.isdir(THREE):
    import subprocess, tarfile, tempfile
    tmp = tempfile.mkdtemp()
    subprocess.run(["npm", "pack", "three@0.128.0"], cwd=tmp, check=True, capture_output=True)
    tarfile.open(os.path.join(tmp, "three-0.128.0.tgz")).extractall(os.path.join(ICI, "three-r128"))
A, B, H, L = g.A, g.B, g.H, g.L


def fr(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


data = json.load(open(os.path.join(ICI, "pieces.json"), encoding="utf-8"))
svg = json.load(open(os.path.join(ICI, "svg-fiche.json"), encoding="utf-8"))
ymin = min(y for _, y in data["languette"]["decalee"])
larg_v, haut_v = 2 * (L + g.LANGUETTE_PILIER), A + B - ymin
pil = data["patron_pilier"]
arete = data["verifications"]["longueur_arete_cm"]
diag = 2 * A * math.sqrt(2)

CAM = dict(
    general=dict(pos=[24, -33, 22], tgt=[0, 0, 5.5]),
    socle=dict(pos=[17, -23, 24], tgt=[0, 0, 0.3]),
    piliers=dict(pos=[22, -30, 19], tgt=[0, 0, 4]),
    montage=dict(pos=[22, -30, 26], tgt=[0, 0, 11]),
    pose=dict(pos=[24, -33, 22], tgt=[0, 0, 7]),
    final=dict(pos=[21, -35, 18], tgt=[0, 0, 5.8]),
)
LIFT = 5.5

STEPS = [
    dict(kicker="comprendre", titre="La voûte croisée en bref", camera=CAM["general"], nouveaux=[], actifs=[], lift=0,
         labels=["clef", "arete", "voutain", "arc", "pilier", "socle"],
         texte=["Une <b>voûte croisée</b> (ou voûte d'arêtes) naît du croisement de <b>deux voûtes en berceau</b> — deux demi-cylindres de même rayon — à angle droit. "
                "Le croisement crée <b>4 voûtains</b> (les 4 triangles courbes) séparés par <b>2 arêtes</b> diagonales qui se rejoignent à la <b>clef</b>, le point le plus haut.",
                "Sur le croquis du prof : les 4 arcs en demi-cercle au bord, les 4 piliers d'angle et la clef au centre. Ici : <b>rayon 4,5 cm</b>, donc 9 cm de portée libre entre deux piliers, "
                "et une maquette presque cubique (12,7 cm de haut pour 12 cm de côté)."],
         mesures=[["Rayon des arcs (demi-cercles)", "4,5 cm"], ["Portée libre entre deux piliers", "9,0 cm"], ["Emprise (pilier à pilier, dehors)", "12,0 × 12,0 cm"],
                  ["Hauteur totale (socle compris)", "12,7 cm"]]),
    dict(kicker="le socle", titre="Le socle : carton gris 2 mm", camera=CAM["socle"], nouveaux=["socle"], lift=0, patron="socle",
         texte=["Découpe un carré de <b>carton gris de 2 mm, 14,0 × 14,0 cm</b>. Trace au crayon les 4 carrés de <b>1,5 × 1,5 cm</b> des piliers, à <b>1,0 cm</b> des bords. "
                "Entre deux carrés d'un même côté il reste <b>9,0 cm</b> : c'est la portée libre des arcs.",
                "<b>Contrôle :</b> la diagonale entre deux coins intérieurs opposés mesure <b>12,73 cm</b> (9 × √2)."],
         mesures=[["Socle", "14,0 × 14,0 cm, ép. 0,2 cm"], ["Carrés des piliers", "1,5 × 1,5 cm, à 1,0 cm des bords"], ["Entre deux piliers (face à face)", "9,0 cm"],
                  ["Diagonale entre coins intérieurs", "12,73 cm"]]),
    dict(kicker="les 4 piliers", titre="Les 4 piliers : tubes carrés de 8 cm", camera=CAM["piliers"], nouveaux=[f"pil{i}" for i in range(4)], lift=0, patron="pilier",
         texte=["Découpe et plie les 4 patrons de pilier (bristol). Chaque pilier est un <b>tube carré 1,5 × 1,5 cm, haut de 8,0 cm</b> : plie les 4 faces, colle la languette de 0,6 cm, "
                "puis rabats le fond et le dessus. <i>Option :</i> glisse un rouleau de papier serré à l'intérieur avant de fermer le dessus pour le rendre plein.",
                "Mesure-les côte à côte : les 4 piliers doivent avoir <b>exactement la même hauteur</b>. Colle-les sur les carrés tracés (colle blanche). "
                "La tête des piliers est à <b>8,2 cm</b> de la table (8,0 + 0,2 de socle) : c'est la naissance des arcs."],
         mesures=[["Section d'un pilier", "1,5 × 1,5 cm"], ["Hauteur d'un pilier", "8,0 cm"], [f"Patron d'un pilier", f"{fr(pil['largeur'])} × {fr(pil['hauteur'])} cm"],
                  ["Languette de recouvrement", "0,6 cm"], ["Naissance des arcs au-dessus de la table", "8,2 cm"]]),
]
for k, (nom, pos) in enumerate([("1", "à plat, puis courbé"), ("2", "colle-le à droite du voûtain 1"), ("3", "même chose"), ("4", "il ferme l'anneau")]):
    pass

STEPS += [
    dict(kicker="voûtain 1", titre="Le voûtain 1 : un morceau de cylindre", camera=CAM["montage"], nouveaux=["web0"], lift=LIFT, patron="voutain", numeros=True,
         texte=["Le voûtain se <b>déplie à plat</b> sans se déformer : un seul patron, avec la bande de l'arc (1,5 cm). Découpe-le en gardant les languettes. "
                "Plie la languette d'arête (tirets bleus) <b>vers soi</b>, puis <b>courbe doucement</b> le voûtain en demi-cercle de rayon 4,5 cm (glisse le gabarit de contrôle dessous).",
                "Le bord haut devient l'arc ; ses deux bouts reposeront sur deux piliers (languettes rouges, pliées <b>en s'éloignant</b>). "
                "Fais glisser le curseur sous la scène pour voir le patron se courber.",
                "<i>La voûte est montée à part, au-dessus des piliers : tu la poseras à l'étape 7.</i>"],
         mesures=[["Longueur de l'arc (bord haut)", f"{fr(math.pi * A, 2)} cm (π × 4,5)"], ["Hauteur du patron (clef → bord de l'arc)", f"{fr(A + B)} cm"],
                  ["Bande de l'arc", "1,5 cm"], ["Languette d'arête", "0,5 cm de large"], ["Languettes sur les piliers", "1,0 × 1,5 cm (×2)"],
                  ["Patron entier, languettes comprises", f"{fr(larg_v, 2)} × {fr(haut_v, 2)} cm"]]),
    dict(kicker="voûtain 2", titre="Le voûtain 2 : on colle la première arête", camera=CAM["montage"], nouveaux=["web1"], lift=LIFT, numeros=True,
         texte=["Prépare le voûtain 2 comme le 1. Place-le <b>à droite du voûtain 1</b>, en tournant dans le sens des aiguilles d'une montre vu d'en haut. "
                "Colle la <b>languette d'arête du voûtain 1 sous le bord gauche du voûtain 2</b> (côté intérieur) : les deux bords se superposent exactement, les deux clefs se touchent.",
                f"Les deux arêtes ont la <b>même longueur : {fr(arete, 2)} cm</b> (mesurée le long de la courbe). Presse avec des pinces à linge 10 minutes."],
         mesures=[["Longueur d'une arête (courbe)", f"{fr(arete, 2)} cm"], ["Angle entre les deux voûtains à la clef", "plat (180°) : les 4 patrons font 4 × 90° = 360° autour de la clef"]]),
    dict(kicker="voûtain 3", titre="Le voûtain 3", camera=CAM["montage"], nouveaux=["web2"], lift=LIFT, numeros=True,
         texte=["Même geste : la languette d'arête du <b>voûtain 2</b> se colle sous le bord gauche du <b>voûtain 3</b>.",
                "Les clefs des trois voûtains se rejoignent en un seul point, au centre. Garde l'ensemble <b>courbé en demi-cercles</b> : s'il se tord, remets le gabarit de contrôle sous l'arc."],
         mesures=[["Distance entre les deux pointes d'un arc", "9,0 cm (= portée libre)"]]),
    dict(kicker="voûtain 4", titre="Le voûtain 4 ferme l'anneau", camera=CAM["montage"], nouveaux=["web3"], lift=LIFT, numeros=True,
         texte=["Le <b>voûtain 4</b> se colle à celui de gauche (languette du voûtain 3) <b>et</b> sa propre languette se colle sous le voûtain 1 : l'anneau est fermé, les 4 clefs forment un seul point.",
                f"<b>Contrôle avant de continuer :</b> les 8 pointes des arcs forment un carré de <b>9,0 cm de côté</b> (diagonale <b>{fr(diag, 2)} cm</b>). Si ce n'est pas le cas, une arête n'a pas la bonne longueur ({fr(arete, 2)} cm)."],
         mesures=[["Côté du carré formé par les pointes", "9,0 cm"], ["Diagonale", f"{fr(diag, 2)} cm"]]),
    dict(kicker="pose de la voûte", titre="On pose la voûte sur les 4 piliers", camera=CAM["pose"], nouveaux=[], actifs=["web0", "web1", "web2", "web3"], lift=0,
         texte=["Descends la voûte sur les piliers : chaque <b>pointe d'arc</b> tombe sur l'angle intérieur de la tête d'un pilier, et la face intérieure de l'arc prolonge la face du pilier.",
                "Rabats les <b>8 languettes de 1,0 cm</b> sur la tête des piliers (2 par pilier, elles se superposent) et colle-les. Les arcs partent bien de la hauteur de <b>8,2 cm</b>."],
         mesures=[["Languettes sur les piliers", "8 de 1,0 × 1,5 cm"], ["Naissance des arcs", "8,2 cm"], ["Flèche des arcs (naissance → clef)", "4,5 cm"]]),
    dict(kicker="contrôle final", titre="Les contrôles de la maquette finie", camera=CAM["final"], nouveaux=[], actifs=["socle", "pil0", "pil1", "pil2", "pil3", "web0", "web1", "web2", "web3"], lift=0, cotes=True,
         texte=["Vérifie ces mesures à la règle :",
                "• hauteur totale de la table à la clef : <b>12,7 cm</b> ; • emprise des piliers (dehors) : <b>12,0 × 12,0 cm</b> ; • portée libre entre deux piliers : <b>9,0 cm</b> ; "
                "• la clef est à <b>6,0 cm</b> de chaque bord extérieur ; • chaque arc est un <b>demi-cercle</b> parfait de 4,5 cm de rayon.",
                "Si tu veux une maquette de 13 cm, ajoute 0,3 cm à la hauteur des piliers (8,3 cm) et change juste cette mesure : le reste des patrons ne change pas."],
         mesures=[["Hauteur totale", "12,7 cm"], ["Emprise", "12,0 × 12,0 cm"], ["Portée libre", "9,0 cm"], ["Clef : distance au bord extérieur", "6,0 cm"], ["Arcs", "demi-cercles, R = 4,5 cm"]]),
]
for i, s in enumerate(STEPS):
    s["n"] = i
    s.setdefault("actifs", s["nouveaux"])
    s.setdefault("mesures", [])
    s.setdefault("labels", [])
    s.setdefault("patron", None)
    s.setdefault("numeros", False)
    s.setdefault("cotes", False)
STEPS[2]["camera"] = CAM["piliers"]

# ---- tableaux
lignes = [
    ("Socle", "1", "carton gris 2 mm", "14,0 × 14,0 cm (épaisseur 0,2 cm)", "carrés des piliers de 1,5 cm à 1,0 cm des bords"),
    ("Pilier", "4", "bristol 200 g", f"patron {fr(pil['largeur'])} × {fr(pil['hauteur'])} cm : 4 faces de 1,5 × 8,0 + languette 0,6 + dessus et fond 1,5 × 1,5", "tube carré 1,5 × 1,5 × 8,0 cm"),
    ("Voûtain", "4", "bristol 200 g", f"patron {fr(larg_v, 2)} × {fr(haut_v, 2)} cm : arc {fr(math.pi * A, 2)} cm, hauteur 6,0 cm dont bande de l'arc 1,5 cm ; languettes 0,5 et 1,0 × 1,5 cm",
     f"arête courbe w = 4,5 sin(s ÷ 4,5), longueur {fr(arete, 2)} cm"),
    ("Gabarit de contrôle", "1", "carton gris 2 mm", "demi-disque de rayon 4,5 cm (9,0 × 4,5 cm)", "facultatif : à glisser sous un arc"),
]
tab = "<table><tr><th>Pièce</th><th>Qté</th><th>Matière</th><th>Dimensions exactes</th><th>Remarque</th></tr>" + "".join(
    f"<tr><td><b>{a}</b></td><td class='v'>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a, b, c, d, e in lignes) + "</table>"
pts = data["points_arete"]
tabp = "<table><tr><th>s (cm depuis la clef)</th>" + "".join(f"<th>{fr(s, 0) if s == int(s) else fr(s, 2)}</th>" for s, _ in pts) + "</tr>" \
       "<tr><td><b>w (cm)</b></td>" + "".join(f"<td class='v'>{fr(w, 2)}</td>" for _, w in pts) + "</tr></table>"

D = dict(A=A, B=B, H=H, EP=g.EP_SOCLE, SOCLE=g.SOCLE, L=L, HAUT=g.HAUT_TOTAL, piliers=g.PILIERS, steps=STEPS)
gab = open(os.path.join(ICI, "gabarit.html"), encoding="utf-8").read()
three = open(os.path.join(THREE, "build", "three.min.js"), encoding="utf-8").read()
orbit = open(os.path.join(THREE, "examples", "js", "controls", "OrbitControls.js"), encoding="utf-8").read()
assert "</script" not in three.lower() and "</script" not in orbit.lower()
html = (gab.replace("{{TABLEAU}}", tab).replace("{{POINTS}}", tabp).replace("{{DATA}}", json.dumps(D, ensure_ascii=False))
        .replace("{{SVG}}", json.dumps(svg, ensure_ascii=False)).replace("{{THREE}}", "").replace("{{ORBIT}}", ""))
# three.js est inséré à part pour éviter que ses « $ » ne soient pris pour des motifs
html = html.replace("<script></script>\n<script></script>", f"<script>{three}</script>\n<script>{orbit}</script>", 1)
open(os.path.join(ICI, "montage.html"), "w", encoding="utf-8").write(html)
print("montage.html", len(html) // 1024, "Ko")

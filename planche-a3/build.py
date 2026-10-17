"""Planche A3 du jury : « Un seul pli ».
Lancer : python3 build.py  ->  planche.html (puis render.js en fait le PDF A3)
Tout le texte est ici, en « nous » ; les 3 photos sont dans photos/."""
import html, re

NOMS = "Rostom · Yassmine · Shahed · Souad"

DEMARCHE = [
    "Nous sommes partis d'un tangram de 15 cm, doublé et collé pour que chaque pièce soit rigide. Notre première proposition était trop fermée : la lumière et la vue n'y entraient pas. Nous avons donc cherché un abri plus ouvert, que l'on traverse.",
    "Nous nous sommes donné trois règles. Nous utilisons les sept pièces. Aucune ne reste posée à plat sur le sol. Et chacune arrive à sa place par un seul des mouvements du tangram : translation, rotation ou pliage.",
]

POINTS = [
    ("Un seul pli",
     "Nous avons plié les deux grands triangles de 30° autour de leur côté commun. Ce pli monte à 5,3 cm, la hauteur du carré : toutes les pièces debout viennent se glisser dessous. Il devient l'axe de symétrie de l'abri, et l'axe de la vue."),
    ("Le cadrage de la vue",
     "L'abri s'ouvre d'est en ouest : nous entrons par l'est et nous sortons face au coucher du soleil. À l'ouest, la paroi du milieu partage l'ouverture en deux cadrages. Le soir, la lumière rasante entre jusqu'au fond ; à midi en été, les pentes mettent le parcours à l'ombre."),
    ("Le climat",
     "Les deux pentes écartent la pluie et la neige de chaque côté du passage, qui reste au sec. Aucune paroi droite ne fait face au vent : il glisse sur le dos des pentes. L'abri est ouvert aux deux bouts, donc l'air le traverse."),
    ("Le personnage de 3 cm",
     "Il entre par l'est sous le petit toit, passe un moment à ciel ouvert, puis se glisse sous le pli et sous la paroi penchée, et ressort face à la vue. Il garde au moins 4 cm au-dessus de la tête : il est protégé sans être enfermé."),
]

CONCLUSION = ("Nous avons voulu un abri poreux, où l'on passe du dehors au dedans petit à petit. Les limites sont tantôt "
              "<b>continues</b> (les pentes), <b>discontinues</b> (les petits triangles), <b>linéaires</b> (le pli) "
              "ou <b>ponctuelles</b> (les pointes posées au sol).")

PHOTOS = [
    ("photos/1-pli.jpg", "Le pli", "Deux pentes à 30° et le petit toit de l'entrée."),
    ("photos/2-entree.jpg", "L'entrée", "Vue de l'est : le personnage de 3 cm est à l'abri sous le petit toit."),
    ("photos/3-plan.jpg", "Le plan", "Vu de dessus : le pli, axe de symétrie, entre les deux pentes."),
]

# le tangram (carré de 4), pièces en position de départ ; les deux grands triangles sont ceux du pli
TANGRAM = {
    "G1": [(0, 4), (4, 4), (2, 2)], "G2": [(2, 2), (0, 4), (0, 0)], "M": [(2, 0), (4, 2), (4, 0)],
    "C": [(2, 2), (3, 3), (4, 2), (3, 1)], "P1": [(4, 4), (4, 2), (3, 3)], "P2": [(2, 2), (3, 1), (1, 1)],
    "Pa": [(2, 0), (0, 0), (1, 1), (3, 1)],
}


def typo(s):
    """Typographie française : apostrophes courbes, espaces insécables avant : ; ! ? et autour des guillemets."""
    s = s.replace("'", "\u2019")
    s = re.sub(r" ([:;!?])", lambda m: ("\u00a0" if m.group(1) == ":" else "\u202f") + m.group(1), s)
    s = re.sub(r"(\d) (cm|°)", "\\1\u00a0\\2", s)
    return s


def tangram_svg():
    out = []
    for k, pts in TANGRAM.items():
        d = " ".join(f"{x},{4 - y}" for x, y in pts)
        cls = "pli" if k in ("G1", "G2") else "autre"
        out.append(f'<polygon class="{cls}" points="{d}"/>')
    return '<svg viewBox="-0.15 -0.15 4.3 4.3" aria-label="Le tangram">' + "".join(out) + "</svg>"


def page():
    demarche = "".join(f"<p>{typo(p)}</p>" for p in DEMARCHE)
    points = "".join(
        f'<section class="pt"><div class="n">{i + 1}</div><h3>{typo(t)}</h3><p>{typo(p)}</p></section>'
        for i, (t, p) in enumerate(POINTS))
    photos = "".join(
        f'<figure><div class="cadre"><img src="{src}" alt="{html.escape(typo(t))}"><span class="num">{i + 1}</span></div>'
        f'<figcaption><b>{typo(t)}</b> {typo(c)}</figcaption></figure>'
        for i, (src, t, c) in enumerate(PHOTOS))
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<title>Un seul pli — planche A3</title>
<link rel="stylesheet" href="fonts/fonts.css">
<style>
@page {{ size: 297mm 420mm; margin: 0; }}
:root {{ --encre: #1d2220; --gris: #5b625e; --trait: #2346a8; --ligne: #cfd2cc; --carton: #d9cfbd; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #fff; }}
body {{ width: 297mm; height: 420mm; color: var(--encre); font-family: "Source Serif 4", Georgia, serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ width: 297mm; height: 420mm; padding: 15mm 14mm 11mm; display: grid; grid-template-rows: auto auto auto 1fr auto auto; row-gap: 0; overflow: hidden; }}
.mono {{ font-family: "IBM Plex Mono", ui-monospace, monospace; }}

header {{ display: grid; grid-template-columns: 1fr 48mm; column-gap: 12mm; align-items: end; padding-bottom: 7mm; border-bottom: 0.5mm solid var(--encre); }}
.surtitre {{ font-family: "IBM Plex Mono", monospace; font-size: 8.5pt; letter-spacing: .08em; text-transform: uppercase; color: var(--gris); }}
h1 {{ font-family: "Archivo", sans-serif; font-stretch: 125%; font-weight: 800; font-size: 74pt; line-height: .92; letter-spacing: -.01em; margin: 4mm 0 4mm -1mm; }}
.sous {{ font-size: 15pt; line-height: 1.35; max-width: 185mm; }}
.noms {{ font-family: "IBM Plex Mono", monospace; font-size: 10pt; letter-spacing: .04em; margin-top: 4mm; color: var(--trait); font-weight: 500; }}
.depart svg {{ width: 48mm; height: 48mm; display: block; }}
.depart polygon {{ stroke: #fff; stroke-width: .045; stroke-linejoin: round; }}
.depart .autre {{ fill: var(--carton); }}
.depart .pli {{ fill: var(--trait); }}
.depart figcaption {{ font-family: "IBM Plex Mono", monospace; font-size: 7pt; line-height: 1.35; color: var(--gris); margin-top: 2mm; }}

.photos {{ display: grid; grid-template-columns: repeat(3, 1fr); column-gap: 6mm; padding-top: 7mm; }}
.cadre {{ position: relative; aspect-ratio: 3 / 4; overflow: hidden; background: var(--carton); }}
.cadre img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.num {{ position: absolute; left: 0; top: 0; width: 9mm; height: 9mm; background: var(--trait); color: #fff; font-family: "Archivo", sans-serif; font-weight: 700; font-size: 14pt; display: grid; place-items: center; }}
figcaption {{ font-size: 10pt; line-height: 1.35; margin-top: 2.5mm; max-width: 80mm; }}
figcaption b {{ font-family: "Archivo", sans-serif; font-weight: 700; margin-right: 1mm; }}

.texte {{ display: grid; grid-template-columns: repeat(3, 1fr); column-gap: 6mm; padding-top: 8mm; align-content: start; }}
.demarche {{ grid-row: 1 / span 2; }}
h2 {{ font-family: "Archivo", sans-serif; font-stretch: 112%; font-weight: 700; font-size: 18pt; line-height: 1.1; padding-top: 2.5mm; border-top: 0.5mm solid var(--encre); margin-bottom: 4mm; }}
.demarche p, .pt p {{ font-size: 13.5pt; line-height: 1.5; hyphens: manual; }}
.demarche p + p {{ margin-top: 3.5mm; }}
.pt {{ padding-bottom: 7mm; }}
.pt .n {{ font-family: "Archivo", sans-serif; font-stretch: 62%; font-weight: 800; font-size: 26pt; line-height: .8; color: var(--trait); position: absolute; }}
.pt {{ position: relative; border-top: 0.5mm solid var(--encre); padding-top: 2.5mm; }}
.pt h3 {{ font-family: "Archivo", sans-serif; font-stretch: 112%; font-weight: 700; font-size: 15pt; line-height: 1.15; margin: 0 0 3mm 9mm; }}
.pt .n {{ left: 0; top: 3mm; }}
.pt p {{ margin-left: 0; }}

.conclusion {{ border-top: 0.5mm solid var(--encre); padding-top: 3.5mm; font-size: 13.5pt; line-height: 1.5; }}
.conclusion b {{ font-family: "Archivo", sans-serif; font-weight: 700; color: var(--trait); }}
footer {{ margin-top: 5mm; font-family: "IBM Plex Mono", monospace; font-size: 7.5pt; letter-spacing: .05em; color: var(--gris); display: flex; justify-content: space-between; }}
</style></head>
<body><div class="page">
<header>
  <div>
    <div class="surtitre">Atelier · Séance 4 · Jury — {typo("La structure cachée : expérimentation de la notion d'abri")}</div>
    <h1>Un seul pli</h1>
    <div class="sous">{typo("Un abri pour un personnage de 3 cm, né d'un tangram de 15 cm.")}</div>
    <div class="noms">{NOMS}</div>
  </div>
  <figure class="depart">{tangram_svg()}<figcaption>{typo("Notre point de départ. En bleu, les deux grands triangles : ils forment le pli.")}</figcaption></figure>
</header>
<div class="photos">{photos}</div>
<div></div>
<div class="texte">
  <div class="demarche"><h2>Notre démarche</h2>{demarche}</div>
  {points}
</div>
<div class="conclusion">{typo(CONCLUSION)}</div>
<footer><span>{typo("Tangram de 15 cm en double épaisseur · personnage de 3 cm")}</span><span>{NOMS}</span></footer>
</div></body></html>"""


open("planche.html", "w", encoding="utf-8").write(page())
print("planche.html écrit")

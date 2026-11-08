"""Croquis A3 portrait (+ 2 x A4 paysage) de la porte jaune REDRESSÉE : filtre crayon + LH, LT, PF.

Entrée : photo_redressee.jpg (voir redresse.py : verticales verticales, horizon horizontal) et redresse.json.
La photo n'est pas retouchée autrement : même contenu, même cadrage, seul le filtre crayon est appliqué.
Repère de mesure : la photo redressée réduite à 1358 x 2064 px (« petite image »).
  - LH (horizon) : y = 1392,9 (calculée avec la focale EXIF 24 mm éq. 35 mm et le point de fuite des verticales)
  - PF : sur la LH, x = 697 (point principal 691 + 6 px : la façade est presque exactement de face)
  - LT : bas de la photo (y = 2064), parallèle à la LH
"""
import cv2, numpy as np, json, os

ICI = os.path.dirname(os.path.abspath(__file__))
mes = json.load(open(os.path.join(ICI, "pf_mesure.json")))

# -------- 1. le filtre crayon, à la résolution d'impression (largeur 2200 px)
im = cv2.imread(os.path.join(ICI, "photo_redressee.jpg"))
Wp = 2200
Hp = round(im.shape[0] * Wp / im.shape[1])
im = cv2.resize(im, (Wp, Hp), interpolation=cv2.INTER_AREA)
g = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8)).apply(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
flou = cv2.GaussianBlur(255 - g, (0, 0), 9 * Wp / 1500)
d = np.clip(cv2.divide(g, 255 - flou, scale=256).astype(np.float32), 0, 255)
t = np.clip(((d / 255.0) ** 1.35 - 0.06) / 0.94, 0, 1)
papier, crayon = np.array([248, 252, 253], np.float32), np.array([48, 48, 52], np.float32)
res = papier * t[..., None] + crayon * (1 - t[..., None])
cv2.imwrite(os.path.join(ICI, "croquis_redresse.png"), np.clip(res, 0, 255).astype(np.uint8))

# -------- 2. mise en page A3 portrait (mm)
PW, PH = 297, 420
SW, SH = 1358.0, 2064.0                    # petite image de mesure
FY0, FY1 = 46.0, 382.0
S = (FY1 - FY0) / SH                       # mm par px de la petite image
IW = SW * S
FX0 = (PW - IW) / 2
FX1 = FX0 + IW


def P(x, y):
    return (FX0 + x * S, FY0 + y * S)


YH = mes["yh"]
PFX = mes["cx"] + mes["dx_pf"]
PF = P(PFX, YH)
LHY = PF[1]
LTY = FY1
BLEU = "#2f62b0"
FOND = "#fdfcf8"
print(f"image {IW:.1f} x {FY1 - FY0:.0f} mm ; PF = ({PF[0]:.1f}; {PF[1]:.1f}) mm ; LH y={LHY:.1f} ; LT y={LTY:.1f} ; yeux = {(LTY - LHY):.1f} mm")

# arêtes réelles de profondeur (retrait de la fenêtre du haut) et coins de la façade, mesurés dans l'image redressée
RETRAITS = [((335.7, 7.2), (364.1, 92.9)), ((1046.2, 2.4), (1026.0, 90.2))]
ANCRES = [(335.7, 7.2), (1046.2, 2.4), (337.4, 343.3), (1016.9, 353.6), (141.5, 383.4), (1239.4, 377.9),
          (412.9, 1792.8), (954.7, 1804.3)]

o = []
font = "font-family=\"'Architects Daughter', 'Caveat', cursive\""


def txt(x, y, s, size=4.2, anchor="start", col=BLEU, rot=0, halo=True):
    tr = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot else ""
    h = f' stroke="{FOND}" stroke-width="1.1" paint-order="stroke" stroke-linejoin="round"' if halo else ""
    return f'<text x="{x:.2f}" y="{y:.2f}" {font} font-size="{size}" fill="{col}" text-anchor="{anchor}"{tr}{h}>{s}</text>'


o.append(f'<rect width="{PW}" height="{PH}" fill="{FOND}"/>')
o.append(f'<image href="croquis_redresse.png" x="{FX0:.2f}" y="{FY0}" width="{IW:.2f}" height="{FY1 - FY0}"/>')
o.append(f'<clipPath id="cadre"><rect x="{FX0:.2f}" y="{FY0}" width="{IW:.2f}" height="{FY1 - FY0}"/></clipPath><g clip-path="url(#cadre)">')
for (x, y) in ANCRES:                       # fuyantes : du PF vers chaque coin, prolongées jusqu'au bord
    a = P(x, y)
    dx, dy = a[0] - PF[0], a[1] - PF[1]
    tt = 3.0
    o.append(f'<line x1="{PF[0]:.2f}" y1="{PF[1]:.2f}" x2="{PF[0] + dx * tt:.2f}" y2="{PF[1] + dy * tt:.2f}" '
             f'stroke="{BLEU}" stroke-width="0.32" stroke-dasharray="2.2 1.4" stroke-opacity="0.9"/>')
o.append('</g>')
for (x, y) in ANCRES:
    a = P(x, y)
    o.append(f'<circle cx="{a[0]:.2f}" cy="{a[1]:.2f}" r="1.2" fill="none" stroke="{BLEU}" stroke-width="0.35"/>')
for (p, q) in RETRAITS:                     # les vraies arêtes de profondeur
    a, b = P(*p), P(*q)
    o.append(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="{BLEU}" stroke-width="0.7"/>')
o.append(f'<rect x="{FX0:.2f}" y="{FY0}" width="{IW:.2f}" height="{FY1 - FY0}" fill="none" stroke="#1c1c1c" stroke-width="0.5"/>')
o.append(f'<line x1="0" y1="{LHY:.2f}" x2="{PW}" y2="{LHY:.2f}" stroke="{BLEU}" stroke-width="0.6" stroke-dasharray="4 1.2 0.8 1.2"/>')
o.append(f'<line x1="0" y1="{LTY:.2f}" x2="{PW}" y2="{LTY:.2f}" stroke="{BLEU}" stroke-width="0.6" stroke-dasharray="2.2 1.4"/>')
o.append(txt(4, LHY - 2, "LH", 5))
o.append(txt(PW - 4, LHY - 2, "LH", 5, "end"))
o.append(txt(4, LTY - 2, "LT", 4.6))
o.append(txt(PW - 4, LTY - 2, "LT", 4.6, "end"))
o.append(f'<circle cx="{PF[0]:.2f}" cy="{PF[1]:.2f}" r="3" fill="none" stroke="{BLEU}" stroke-width="0.6"/>'
         f'<circle cx="{PF[0]:.2f}" cy="{PF[1]:.2f}" r="0.7" fill="{BLEU}"/>')
o.append(txt(PF[0] + 4.5, PF[1] + 8.5, "PF", 6.2))
xc = FX1 + 9                                # cote : hauteur des yeux
o.append(f'<line x1="{xc}" y1="{LHY:.2f}" x2="{xc}" y2="{LTY}" stroke="{BLEU}" stroke-width="0.5"/>')
for yy, sg in ((LHY, 1), (LTY, -1)):
    o.append(f'<line x1="{xc - 1.4}" y1="{yy:.2f}" x2="{xc + 1.4}" y2="{yy:.2f}" stroke="{BLEU}" stroke-width="0.5"/>')
    o.append(f'<line x1="{xc}" y1="{yy:.2f}" x2="{xc - 0.9}" y2="{yy + sg * 2.4:.2f}" stroke="{BLEU}" stroke-width="0.5"/>')
    o.append(f'<line x1="{xc}" y1="{yy:.2f}" x2="{xc + 0.9}" y2="{yy + sg * 2.4:.2f}" stroke="{BLEU}" stroke-width="0.5"/>')
o.append(txt(xc + 5, (LHY + LTY) / 2, "hauteur des yeux (LH → LT)", 3.6, "middle", rot=-90))
# en-tête et notes
o.append(txt(FX0, 13, "La porte jaune · photo redressée au crayon", 6.6, col="#1f1f1f", halo=False))
o.append(txt(FX0, 20.5, "la photo était un peu penchée : verticales remises verticales, horizon remis horizontal", 3.4, col="#555", halo=False))
notes = ["LH : à hauteur des yeux (calculée avec la focale EXIF 24 mm et la convergence des verticales)",
         "PF : sur la LH, au milieu de la porte · PF2 : à l'infini (façade de face : ses horizontales restent parallèles)",
         "segments épais bleus = vraies arêtes de profondeur du retrait de la fenêtre : elles pointent vers le PF",
         "cercles bleus = coins de la façade, reliés au PF (fuyantes de construction) · imprimer à 100 %"]
for i, n in enumerate(notes):
    o.append(txt(FX0, 391 + i * 5, n, 3.0, col="#666", halo=False))
corps = "".join(o)


def svg(vb, extra=""):
    return f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg">{corps}{extra}</svg>'


def page(pages, w, h, titre):
    divs = "".join(f'<div class="p">{p}</div>' for p in pages)
    return (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{titre}</title>'
            f'<link rel="stylesheet" href="polices-local.css">'
            f'<style>@page {{ size: {w}mm {h}mm; margin: 0; }} html, body {{ margin: 0; background: #fff; }}'
            f'.p {{ width: {w}mm; height: {h}mm; page-break-after: always; break-after: page; overflow: hidden; background: {FOND}; }}'
            f'.p:last-child {{ page-break-after: auto; break-after: auto; }} svg {{ width: 100%; height: 100%; display: block; }}'
            f'</style></head><body>{divs}</body></html>')


J = PH / 2
e1 = txt(6, J / 2, "feuille 1/2 · moitié HAUTE de l'A3 · la jonction est en bas ↓", 3.0, "middle", "#a0302a", rot=-90, halo=False)
e2 = txt(6, J * 1.5, "↑ la jonction est en haut · feuille 2/2 · moitié BASSE de l'A3", 3.0, "middle", "#a0302a", rot=-90, halo=False)
open(os.path.join(ICI, "a3.html"), "w", encoding="utf-8").write(page([svg(f"0 0 {PW} {PH}")], 297, 420, "Porte jaune A3"))
open(os.path.join(ICI, "a4x2.html"), "w", encoding="utf-8").write(
    page([svg(f"0 0 {PW} {J:g}", e1), svg(f"0 {J:g} {PW} {J:g}", e2)], 297, 210, "Porte jaune 2 x A4"))
print("a3.html et a4x2.html écrits")

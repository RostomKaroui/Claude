"""Croquis A3 paysage (+ 2 x A4 portrait) de la place Ramadhan Bey REDRESSÉE : filtre crayon + LH, LT, PF1, PF2.

Entrées : photo_redressee.jpg (voir redresse.py : verticales verticales), redresse.json.
La photo n'est pas retouchée autrement : même contenu, même cadrage (un peu réduit par le redressement), seul le filtre crayon est appliqué.
Mesures dans l'image redressée (1871 x 1466 px) :
  - LH (horizon) : y = 1022 (focale supposée 24 mm éq. 35 mm = 1386 px : cette photo n'a pas d'EXIF)
  - PF1 (la ruelle sous la voûte) : (464 ; 1022). Mesuré sur la base du mur droit de la ruelle et le haut de son soubassement : ± 150 px.
  - PF2 (les façades de la place) : très loin à droite, vers x ≈ 22 000 px (entre 17 000 et 29 000) : hors feuille.
  - LT : bas de la photo.
"""
import cv2, numpy as np, json, os

ICI = os.path.dirname(os.path.abspath(__file__))
info = json.load(open(os.path.join(ICI, "redresse.json")))

# -------- 1. le filtre crayon, à la résolution d'impression
im = cv2.imread(os.path.join(ICI, "photo_redressee.jpg"))
SH_, SW_ = im.shape[:2]
Wp = 2600
Hp = round(SH_ * Wp / SW_)
im = cv2.resize(im, (Wp, Hp), interpolation=cv2.INTER_CUBIC)
g = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8)).apply(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
flou = cv2.GaussianBlur(255 - g, (0, 0), 9 * Wp / 1500)
d = np.clip(cv2.divide(g, 255 - flou, scale=256).astype(np.float32), 0, 255)
t = np.clip(((d / 255.0) ** 1.35 - 0.06) / 0.94, 0, 1)
papier, crayon = np.array([248, 252, 253], np.float32), np.array([48, 48, 52], np.float32)
res = papier * t[..., None] + crayon * (1 - t[..., None])
cv2.imwrite(os.path.join(ICI, "croquis_redresse.png"), np.clip(res, 0, 255).astype(np.uint8))

# -------- 2. mise en page A3 paysage (mm)
PW, PH = 420, 297
SW, SH = float(SW_), float(SH_)
IW = 316.0
S = IW / SW                                # mm par px de l'image redressée
IH = SH * S
FX0 = (PW - IW) / 2
FX1 = FX0 + IW
FY0 = 22.0
FY1 = FY0 + IH


def P(x, y):
    return (FX0 + x * S, FY0 + y * S)


YH = info["horizon_y"]
PF1 = P(464.0, YH)
LHY = P(0, YH)[1]
LTY = FY1
BLEU = "#2f62b0"
FOND = "#fdfcf8"
print(f"image {IW:.0f} x {IH:.1f} mm ; PF1 = ({PF1[0]:.1f}; {PF1[1]:.1f}) mm ; LH y={LHY:.1f} ; LT y={LTY:.1f} ; yeux = {(LTY - LHY):.1f} mm ; jonction x=210")

# arêtes réelles de la ruelle (mesurées sur la photo, puis passées dans l'image redressée)
H = np.array(info["H_travail"])
xs0, ys0 = info["rect"][0], info["rect"][1]


def T(p):
    q = H @ np.array([p[0], p[1], 1.0])
    return (q[0] / q[2] - xs0, q[1] / q[2] - ys0)


ALLEE = [(T((741, 1097)), T((902, 1203))),      # base du mur droit de la ruelle
         (T((783, 985)), T((854, 991)))]        # haut de son soubassement gris
# arêtes réelles de la façade (vont vers PF2) : toit, auvent de la fenêtre, linteau
FACADE = [((986, 150), (540, 131)), ((1597, 359), (1102, 347)), ((1112, 448), (1311, 455)), ((1146, 520), (1282, 524))]

o = []
font = "font-family=\"'Architects Daughter', 'Caveat', cursive\""


def txt(x, y, s, size=4.2, anchor="start", col=BLEU, rot=0, halo=True):
    tr = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot else ""
    h = f' stroke="{FOND}" stroke-width="1.1" paint-order="stroke" stroke-linejoin="round"' if halo else ""
    return f'<text x="{x:.2f}" y="{y:.2f}" {font} font-size="{size}" fill="{col}" text-anchor="{anchor}"{tr}{h}>{s}</text>'


def prolonge(a, b, x_lo, x_hi):
    """la droite (a, b) en mm, prolongée sur toute la largeur de l'image"""
    (ax, ay), (bx, by) = a, b
    k = (by - ay) / (bx - ax)
    return (x_lo, ay + k * (x_lo - ax)), (x_hi, ay + k * (x_hi - ax))


o.append(f'<rect width="{PW}" height="{PH}" fill="{FOND}"/>')
o.append(f'<image href="croquis_redresse.png" x="{FX0:.2f}" y="{FY0}" width="{IW:.2f}" height="{IH:.2f}"/>')
o.append(f'<clipPath id="cadre"><rect x="{FX0:.2f}" y="{FY0}" width="{IW:.2f}" height="{IH:.2f}"/></clipPath><g clip-path="url(#cadre)">')
for a, b in ALLEE:                          # fuyantes vers PF1 : de PF1 à l'arête, puis au-delà
    pa, pb = P(*a), P(*b)
    for q in (pa, pb):
        dx, dy = q[0] - PF1[0], q[1] - PF1[1]
        o.append(f'<line x1="{PF1[0]:.2f}" y1="{PF1[1]:.2f}" x2="{PF1[0] + dx * 3:.2f}" y2="{PF1[1] + dy * 3:.2f}" '
                 f'stroke="{BLEU}" stroke-width="0.32" stroke-dasharray="2.2 1.4" stroke-opacity="0.9"/>')
for a, b in FACADE:                         # fuyantes vers PF2 : l'arête prolongée sur toute la largeur
    p, q = prolonge(P(*a), P(*b), FX0, FX1)
    o.append(f'<line x1="{p[0]:.2f}" y1="{p[1]:.2f}" x2="{q[0]:.2f}" y2="{q[1]:.2f}" stroke="{BLEU}" stroke-width="0.32" '
             f'stroke-dasharray="2.2 1.4" stroke-opacity="0.9"/>')
o.append('</g>')
for a, b in ALLEE:                          # les vraies arêtes, épaisses
    pa, pb = P(*a), P(*b)
    o.append(f'<line x1="{pa[0]:.2f}" y1="{pa[1]:.2f}" x2="{pb[0]:.2f}" y2="{pb[1]:.2f}" stroke="{BLEU}" stroke-width="0.8"/>')
for a, b in FACADE:
    pa, pb = P(*a), P(*b)
    o.append(f'<line x1="{pa[0]:.2f}" y1="{pa[1]:.2f}" x2="{pb[0]:.2f}" y2="{pb[1]:.2f}" stroke="{BLEU}" stroke-width="0.8"/>')
o.append(f'<rect x="{FX0:.2f}" y="{FY0}" width="{IW:.2f}" height="{IH:.2f}" fill="none" stroke="#1c1c1c" stroke-width="0.5"/>')
o.append(f'<line x1="0" y1="{LHY:.2f}" x2="{PW}" y2="{LHY:.2f}" stroke="{BLEU}" stroke-width="0.6" stroke-dasharray="4 1.2 0.8 1.2"/>')
o.append(f'<line x1="0" y1="{LTY:.2f}" x2="{PW}" y2="{LTY:.2f}" stroke="{BLEU}" stroke-width="0.6" stroke-dasharray="2.2 1.4"/>')
o.append(txt(3, LHY - 2, "LH", 5))
o.append(txt(PW - 3, LHY - 2, "LH", 5, "end"))
o.append(txt(3, LTY - 2, "LT", 4.6))
o.append(txt(PW - 3, LTY - 2, "LT", 4.6, "end"))
o.append(f'<circle cx="{PF1[0]:.2f}" cy="{PF1[1]:.2f}" r="3" fill="none" stroke="{BLEU}" stroke-width="0.6"/>'
         f'<circle cx="{PF1[0]:.2f}" cy="{PF1[1]:.2f}" r="0.7" fill="{BLEU}"/>')
o.append(txt(PF1[0] - 4, PF1[1] - 5, "PF1", 6.2, "end"))
# PF2 : flèche sur la LH, dans la marge de droite (hors feuille)
ax = FX1 + 3
o.append(f'<line x1="{ax}" y1="{LHY + 6:.2f}" x2="{ax + 38}" y2="{LHY + 6:.2f}" stroke="{BLEU}" stroke-width="0.6"/>')
o.append(f'<line x1="{ax + 38}" y1="{LHY + 6:.2f}" x2="{ax + 34.8}" y2="{LHY + 4.4:.2f}" stroke="{BLEU}" stroke-width="0.6"/>')
o.append(f'<line x1="{ax + 38}" y1="{LHY + 6:.2f}" x2="{ax + 34.8}" y2="{LHY + 7.6:.2f}" stroke="{BLEU}" stroke-width="0.6"/>')
o.append(txt(ax, LHY + 12, "PF2 : très loin à droite", 3.4, "start"))
o.append(txt(ax, LHY + 16, "(≈ 4 m hors feuille)", 3.0, "start"))
xc = FX0 - 12                               # cote : hauteur des yeux (à gauche)
o.append(f'<line x1="{xc}" y1="{LHY:.2f}" x2="{xc}" y2="{LTY:.2f}" stroke="{BLEU}" stroke-width="0.5"/>')
for yy, sg in ((LHY, 1), (LTY, -1)):
    o.append(f'<line x1="{xc - 1.4}" y1="{yy:.2f}" x2="{xc + 1.4}" y2="{yy:.2f}" stroke="{BLEU}" stroke-width="0.5"/>')
    o.append(f'<line x1="{xc}" y1="{yy:.2f}" x2="{xc - 0.9}" y2="{yy + sg * 2.4:.2f}" stroke="{BLEU}" stroke-width="0.5"/>')
    o.append(f'<line x1="{xc}" y1="{yy:.2f}" x2="{xc + 0.9}" y2="{yy + sg * 2.4:.2f}" stroke="{BLEU}" stroke-width="0.5"/>')
o.append(txt(xc - 3, (LHY + LTY) / 2, "hauteur des yeux (LH → LT)", 3.4, "middle", rot=-90))
# en-tête et notes
o.append(txt(FX0, 9.5, "La place Ramadhan Bey · photo redressée au crayon", 6.2, col="#1f1f1f", halo=False))
o.append(txt(FX0, 15.5, "perspective à 2 points de fuite : la ruelle sous la voûte (PF1) et les façades de la place (PF2) · verticales verticales", 3.2, col="#555", halo=False))
notes = ["LH : à hauteur des yeux (elle passe par les yeux de l'homme debout) · PF1 mesuré à ± 4 cm sur la feuille · PF2 estimé (façades presque de face)",
         "segments épais bleus = vraies arêtes (mur et soubassement de la ruelle → PF1 ; toit, auvent, linteau → PF2) · photo sans données d'appareil : focale supposée · imprimer à 100 %"]
for i, n in enumerate(notes):
    o.append(txt(FX0, FY1 + 7 + i * 4.4, n, 2.8, col="#666", halo=False))
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


J = PW / 2
e1 = txt(J / 2, 293, "feuille 1/2 · moitié GAUCHE de l'A3 · la jonction est à droite →", 3.0, "middle", "#a0302a", halo=False)
e2 = txt(J * 1.5, 293, "← la jonction est à gauche · feuille 2/2 · moitié DROITE de l'A3", 3.0, "middle", "#a0302a", halo=False)
open(os.path.join(ICI, "a3.html"), "w", encoding="utf-8").write(page([svg(f"0 0 {PW} {PH}")], 420, 297, "Place Ramadhan Bey A3"))
open(os.path.join(ICI, "a4x2.html"), "w", encoding="utf-8").write(
    page([svg(f"0 0 {J:g} {PH}", e1), svg(f"{J:g} 0 {J:g} {PH}", e2)], 210, 297, "Place Ramadhan Bey 2 x A4"))
print("a3.html et a4x2.html écrits")

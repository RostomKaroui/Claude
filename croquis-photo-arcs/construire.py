"""Pose la construction (LH, LT, points de fuite, fuyantes) sur la photo passée au filtre crayon.

La photo n'est pas modifiée : mêmes pixels, même cadrage (croquis.png fait 1500 x 2000 comme photo.jpg).
On ajoute seulement des marges blanches pour que les points de fuite et les étiquettes tiennent sur la feuille.

Mesures faites sur la photo (px, origine en haut à gauche de la photo) :
- LH (ligne d'horizon) : y = 1430. C'est la hauteur des yeux : elle passe par la tête du passant au fond de la
  ruelle (tête ~ 1404-1416, pieds 1548) et à mi-hauteur des portes bleues de la ruelle.
- LT (ligne de terre) : bas du tableau, y = 2000 (le sol le plus proche, au pied du pilier de gauche).
- PF1 : là où convergent les lignes qui partent vers le fond (pied du mur de la ruelle, plinthes, bandeaux de la
  porte jaune, haut et bas des portes bleues) : x ~ 1650, hors de la photo (à droite).
- PF2 : l'autre direction (perpendiculaire à la ruelle) fuit vers la GAUCHE, du côté opposé à PF1 par rapport au
  centre de la photo. Avec une focale d'au moins ~1500 px (la photo n'a pas de données EXIF), il est à plus de
  1750 px à gauche du bord de la photo : hors de la feuille. On ne le place donc pas ; on l'indique par une flèche.
"""
import os, sys, math
ICI = os.path.dirname(os.path.abspath(__file__))
W, H = 1500, 2000
LH, LT = 1430, 2000
PF1 = (1650, LH)
CX = W / 2

# points relevés sur de vraies arêtes de la famille « vers le fond » : (x, y, étiquette)
ANCRES = [
    (880, 1585, "pied du mur de la ruelle"),
    (590, 1758, "pied du pilier"),
    (255, 1895, "pied du pilier de gauche"),
    (300, 1118, "traverse de la porte jaune"),
    (1025, 1321, "haut de la porte bleue"),
    (1025, 1569, "bas de la porte bleue"),
]

BLEU = "#2f62b0"


def fuyante(p, q, long=4000):
    """droite de p vers q, prolongée vers p-gauche jusqu'à x = -long"""
    return p, q


def svg(vue, marges, titre=True):
    ml, mt, mr, mb = marges
    cw, ch = W + ml + mr, H + mt + mb
    X = lambda x: ml + x
    Y = lambda y: mt + y
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {cw} {ch}" width="{cw}" height="{ch}">']
    o.append(f'<rect width="{cw}" height="{ch}" fill="#fdfcf8"/>')
    o.append(f'<image href="croquis.png" x="{X(0)}" y="{Y(0)}" width="{W}" height="{H}"/>')
    o.append(f'<rect x="{X(0)}" y="{Y(0)}" width="{W}" height="{H}" fill="none" stroke="#1c1c1c" stroke-width="3"/>')
    # fuyantes vers PF1
    for (x, y, nom) in ANCRES:
        dx, dy = x - PF1[0], y - PF1[1]
        xa = -ml + 10 if vue == "photo" else -ml
        t = (xa - PF1[0]) / dx
        o.append(f'<line x1="{X(xa)}" y1="{Y(PF1[1] + t * dy)}" x2="{X(PF1[0])}" y2="{Y(PF1[1])}" stroke="{BLEU}" '
                 f'stroke-width="2.4" stroke-dasharray="14 9" stroke-opacity="0.9"/>')
        o.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="7" fill="none" stroke="{BLEU}" stroke-width="2.4"/>')
    # LH et LT
    o.append(f'<line x1="0" y1="{Y(LH)}" x2="{cw}" y2="{Y(LH)}" stroke="{BLEU}" stroke-width="4" stroke-dasharray="26 8 5 8"/>')
    o.append(f'<line x1="0" y1="{Y(LT)}" x2="{cw}" y2="{Y(LT)}" stroke="{BLEU}" stroke-width="4" stroke-dasharray="10 8"/>')
    fs = 46
    lab = lambda x, y, t, a="start", s=fs: f'<text x="{x}" y="{y}" font-family="\'Architects Daughter\', \'Caveat\', cursive" font-size="{s}" fill="{BLEU}" text-anchor="{a}" stroke="#fdfcf8" stroke-width="7" paint-order="stroke" stroke-linejoin="round">{t}</text>'
    o.append(lab(X(-ml) + 14, Y(LH) - 14, "LH"))
    o.append(lab(X(W) + 300, Y(LH) - 14, "LH"))
    o.append(lab(X(-ml) + 14, Y(LT) - 14, "LT"))
    o.append(lab(X(W) + 300, Y(LT) - 14, "LT"))
    # PF1
    px, py = X(PF1[0]), Y(PF1[1])
    o.append(f'<circle cx="{px}" cy="{py}" r="22" fill="none" stroke="{BLEU}" stroke-width="4"/><circle cx="{px}" cy="{py}" r="5" fill="{BLEU}"/>')
    o.append(lab(px, py - 36, "PF1", "middle", 50))
    # PF2 : très loin à gauche, hors feuille -> flèche sur la LH
    ax = X(-ml) + 14
    o.append(f'<line x1="{ax + 150}" y1="{Y(LH) + 34}" x2="{ax}" y2="{Y(LH) + 34}" stroke="{BLEU}" stroke-width="4"/>')
    o.append(f'<line x1="{ax}" y1="{Y(LH) + 34}" x2="{ax + 24}" y2="{Y(LH) + 20}" stroke="{BLEU}" stroke-width="4"/>')
    o.append(f'<line x1="{ax}" y1="{Y(LH) + 34}" x2="{ax + 24}" y2="{Y(LH) + 48}" stroke="{BLEU}" stroke-width="4"/>')
    o.append(f'<text x="{ax}" y="{Y(LH) + 88}" font-family="\'Architects Daughter\', \'Caveat\', cursive" font-size="34" fill="{BLEU}" stroke="#fdfcf8" stroke-width="6" paint-order="stroke">PF2 : très loin à gauche,</text>')
    o.append(f'<text x="{ax}" y="{Y(LH) + 126}" font-family="\'Architects Daughter\', \'Caveat\', cursive" font-size="34" fill="{BLEU}" stroke="#fdfcf8" stroke-width="6" paint-order="stroke">hors de la feuille</text>')
    # cote : hauteur des yeux, dans la marge droite
    xc = X(W) + 70
    o.append(f'<line x1="{xc}" y1="{Y(LH)}" x2="{xc}" y2="{Y(LT)}" stroke="{BLEU}" stroke-width="3.5"/>')
    for yy, s in ((Y(LH), 1), (Y(LT), -1)):
        o.append(f'<line x1="{xc - 14}" y1="{yy}" x2="{xc + 14}" y2="{yy}" stroke="{BLEU}" stroke-width="3.5"/>')
        o.append(f'<line x1="{xc}" y1="{yy}" x2="{xc - 9}" y2="{yy + s * 22}" stroke="{BLEU}" stroke-width="3.5"/>')
        o.append(f'<line x1="{xc}" y1="{yy}" x2="{xc + 9}" y2="{yy + s * 22}" stroke="{BLEU}" stroke-width="3.5"/>')
    o.append(f'<text x="{xc + 52}" y="{(Y(LH) + Y(LT)) / 2}" font-family="\'Architects Daughter\', \'Caveat\', cursive" font-size="36" fill="{BLEU}" '
             f'text-anchor="middle" transform="rotate(-90 {xc + 52} {(Y(LH) + Y(LT)) / 2})">hauteur des yeux (LH → LT)</text>')
    if titre:
        o.append(lab(X(0), Y(0) - 22, "Photo au crayon · LH, LT et points de fuite", "start", 40))
    o.append("</svg>")
    return "\n".join(o), cw, ch


def page(corps, cw, ch, titre):
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{titre}</title>
<link rel="stylesheet" href="polices-local.css"><style>html,body{{margin:0;background:#fdfcf8}}svg{{display:block}}</style></head>
<body>{corps}</body></html>"""


if __name__ == "__main__":
    s1, w1, h1 = svg("photo", (150, 70, 380, 60))
    open(os.path.join(ICI, "construction.html"), "w", encoding="utf-8").write(page(s1, w1, h1, "Photo au crayon"))
    print(f"PF1 = {PF1}  LH = {LH}  LT = {LT}  canevas {w1}x{h1}")

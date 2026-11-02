"""Pose la construction (LH, LT, PF, fuyantes) sur la photo de la porte jaune passée au filtre crayon.

La photo n'est pas modifiée (mêmes pixels, orientation EXIF appliquée, réduite à 1500 x 2000). Marges blanches ajoutées.

Mesures (px sur la photo 1500 x 2000) :
- Focale : EXIF = 24 mm équivalent 35 mm -> f ~ 1390-1410 px (Samsung SM-A525F).
- Verticales : les 107 droites quasi verticales convergent vers un point de fuite vertical VV = (650, -7279).
  => l'appareil regarde vers le haut de ~9,5 deg, et la LH est à  y = 1000 + f^2 / (1000 + 7279) ~ 1237 au centre.
- Façade de face : ses horizontales (54 longues droites) sont parallèles entre elles (PF2 à l'infini) et penchent de
  -0,0185 (1 deg : la photo est un peu penchée) -> la LH est parallèle à elles.
- PF (fuite de la profondeur) : x ~ 790 : les arêtes des retraits de la fenêtre du haut (côté gauche -> x 857, côté
  droit -> x 787), les joints du sol et la géométrie (x 753 + 22) donnent 700-860 ; on prend 790.
"""
import os, math
ICI = os.path.dirname(os.path.abspath(__file__))
W, H = 1500, 2000
PENTE = -0.0185                    # pente de la LH (parallèle aux horizontales de la façade)
PF = (790.0, 1237.0)


def lh(x): return PF[1] + PENTE * (x - PF[0])


def lt(x): return 2000 + PENTE * (x - 1500)         # parallèle à la LH, passant par le coin bas-droite de la photo


# arêtes de profondeur (vraies ou prolongées) : coins du retrait de la fenêtre, de l'encadrement et de la porte
ANCRES = [
    (427, 20), (1044, 8),            # fenêtre du haut : coins extérieurs de son retrait (haut)
    (421, 283), (1033, 283),         # fenêtre du haut : coins extérieurs (bas)
    (243, 318), (1235, 300),         # encadrement de pierre : coins du haut
    (462, 1673), (1040, 1678),       # porte : coins du bas
]
# arêtes réellement visibles sur la photo qui montrent la profondeur : (coin extérieur, coin intérieur) de la fenêtre
RETRAITS = [((427, 20), (450, 85)), ((1044, 8), (1030, 75))]
BLEU = "#2f62b0"


def svg(marges):
    ml, mt, mr, mb = marges
    cw, ch = W + ml + mr, H + mt + mb
    X = lambda x: ml + x
    Y = lambda y: mt + y
    font = "font-family=\"'Architects Daughter', 'Caveat', cursive\""
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cw} {ch}" width="{cw}" height="{ch}">']
    o.append(f'<rect width="{cw}" height="{ch}" fill="#fdfcf8"/>')
    o.append(f'<image href="croquis.png" x="{X(0)}" y="{Y(0)}" width="{W}" height="{H}"/>')
    o.append(f'<rect x="{X(0)}" y="{Y(0)}" width="{W}" height="{H}" fill="none" stroke="#1c1c1c" stroke-width="3"/>')
    def bout(x, y):
        """point où la droite PF -> (x, y), prolongée au-delà de l'arête, sort de la photo (+ petite marge)"""
        dx, dy = x - PF[0], y - PF[1]
        ts = []
        for v, i, lo, hi in ((0, 0, 0, H), (W, 0, 0, H), (0, 1, 0, W), (H, 1, 0, W)):
            d = (dx, dy)[i]
            if abs(d) < 1e-9: continue
            t = (v - PF[i]) / d
            q = PF[1 - i] + t * (dy, dx)[i] if False else (PF[1 - i] + t * (dy if i == 0 else dx))
            if t > 1 and lo <= q <= hi: ts.append(t)
        t = min(ts)
        return PF[0] + t * dx, PF[1] + t * dy

    for (x, y) in ANCRES:                                     # fuyantes : du PF vers l'arête, prolongées jusqu'au bord de la photo
        bx, by = bout(x, y)
        o.append(f'<line x1="{X(bx)}" y1="{Y(by)}" x2="{X(PF[0])}" y2="{Y(PF[1])}" stroke="{BLEU}" stroke-width="2.4" stroke-dasharray="14 9" stroke-opacity="0.9"/>')
        o.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="8" fill="none" stroke="{BLEU}" stroke-width="2.6"/>')
    for (p, q) in RETRAITS:                                   # vraies arêtes de profondeur, pour la vérification
        o.append(f'<line x1="{X(p[0])}" y1="{Y(p[1])}" x2="{X(q[0])}" y2="{Y(q[1])}" stroke="{BLEU}" stroke-width="3.2"/>')
    x0, x1 = -ml, W + mr
    o.append(f'<line x1="{X(x0)}" y1="{Y(lh(x0))}" x2="{X(x1)}" y2="{Y(lh(x1))}" stroke="{BLEU}" stroke-width="4" stroke-dasharray="26 8 5 8"/>')
    o.append(f'<line x1="{X(x0)}" y1="{Y(lt(x0))}" x2="{X(x1)}" y2="{Y(lt(x1))}" stroke="{BLEU}" stroke-width="4" stroke-dasharray="10 8"/>')
    lab = lambda x, y, t, a="start", s=46: (f'<text x="{x}" y="{y}" {font} font-size="{s}" fill="{BLEU}" text-anchor="{a}" '
                                             f'stroke="#fdfcf8" stroke-width="7" paint-order="stroke" stroke-linejoin="round">{t}</text>')
    o.append(lab(X(x0) + 14, Y(lh(x0)) - 14, "LH"))
    o.append(lab(X(x1) - 14, Y(lh(x1)) - 14, "LH", "end"))
    o.append(lab(X(x0) + 14, Y(lt(x0)) - 14, "LT"))
    o.append(lab(X(x1) - 14, Y(lt(x1)) - 14, "LT", "end"))
    px, py = X(PF[0]), Y(PF[1])
    o.append(f'<circle cx="{px}" cy="{py}" r="24" fill="none" stroke="{BLEU}" stroke-width="4.5"/><circle cx="{px}" cy="{py}" r="5.5" fill="{BLEU}"/>')
    o.append(lab(px + 36, py + 56, "PF", "start", 52))
    xc = X(W) + 70                                            # cote : hauteur des yeux
    yh, yt = Y(lh(W + 70)), Y(lt(W + 70))
    o.append(f'<line x1="{xc}" y1="{yh}" x2="{xc}" y2="{yt}" stroke="{BLEU}" stroke-width="3.5"/>')
    for yy, s in ((yh, 1), (yt, -1)):
        o.append(f'<line x1="{xc - 14}" y1="{yy}" x2="{xc + 14}" y2="{yy}" stroke="{BLEU}" stroke-width="3.5"/>')
        o.append(f'<line x1="{xc}" y1="{yy}" x2="{xc - 9}" y2="{yy + s * 22}" stroke="{BLEU}" stroke-width="3.5"/>')
        o.append(f'<line x1="{xc}" y1="{yy}" x2="{xc + 9}" y2="{yy + s * 22}" stroke="{BLEU}" stroke-width="3.5"/>')
    ym = (yh + yt) / 2
    o.append(f'<text x="{xc + 52}" y="{ym}" {font} font-size="34" fill="{BLEU}" text-anchor="middle" transform="rotate(-90 {xc + 52} {ym})">hauteur des yeux (LH → LT)</text>')
    # notes
    o.append(lab(X(0), Y(0) - 22, "Photo au crayon · LH, LT et point de fuite", "start", 40))
    o.append(f'<text x="{X(0)}" y="{Y(H) + 78}" {font} font-size="30" fill="{BLEU}">PF : sur la LH, au milieu de la porte · PF2 : à l\'infini (façade de face, ses horizontales restent parallèles)</text>')
    o.append(f'<text x="{X(0)}" y="{Y(H) + 118}" {font} font-size="30" fill="{BLEU}">les segments épais bleus = vraies arêtes de profondeur de la fenêtre du haut ; elles pointent vers le PF</text>')
    o.append("</svg>")
    return "\n".join(o), cw, ch


if __name__ == "__main__":
    s, w, h = svg((150, 70, 380, 150))
    open(os.path.join(ICI, "construction.html"), "w", encoding="utf-8").write(
        f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Porte jaune au crayon</title>'
        f'<link rel="stylesheet" href="polices-local.css"><style>html,body{{margin:0;background:#fdfcf8}}svg{{display:block}}</style></head><body>{s}</body></html>')
    print(f"PF = {PF}  LH(0)={lh(0):.0f} LH(1500)={lh(1500):.0f}  LT(0)={lt(0):.0f} LT(1500)={lt(1500):.0f}  canevas {w}x{h}")

"""Croquis 3 : la cour (auvent, climatiseur, fenêtres à grille, chaises), méthode du cadrage à l'acétate.

Remarques de la prof appliquées :
  - pas de hachures ;
  - trois qualités de trait : contours forts et foncés, détails moyens, joints du sol fins ;
  - la construction (grille, horizon, AB, A'B', C, D, fuyantes) reste visible mais très très légère.

Entrée : redresse.png (vue dans la fenêtre de l'acétate, 40 px = 1 cm). Sortie : croquis-3.html (A4).
Perspective presque frontale : le mur du fond est de face, le mur aux fenêtres et les joints du sol
fuient vers un seul point de fuite PF, juste à gauche du cadre.
"""
import math, random, sys
import numpy as np

ICI = sys.argv[1] if len(sys.argv) > 1 else "."
S = 40; MM = 10 / S
W, H = 680, 1040
X0, Y0 = -0.5, -1.0
PAGE_W, PAGE_H = 210, 297
OX, OY = 20, 25

YH = 470                 # ligne d'horizon (px)
PF = (-40, YH)           # point de fuite du mur aux fenêtres et des joints du sol


def sur(x0, y0, x):
    """y à l'abscisse x sur la fuyante qui passe par (x0, y0)"""
    return y0 + (x - x0) * (PF[1] - y0) / (PF[0] - x0)


def P(x, y):
    return (OX + x * MM, OY + y * MM)


# ---------------------------------------------------------------- crayon
class Crayon:
    TRAITS = {  # épaisseur (mm), opacité, couleur
        "fort": (0.50, 0.95, "#1b1b1b"),
        "moyen": (0.30, 0.85, "#2e2e2e"),
        "fin": (0.18, 0.62, "#404040"),
        "leger": (0.14, 0.45, "#505050"),
        "construction": (0.12, 0.30, "#7d8fa6"),
    }

    def __init__(self, graine):
        self.r = random.Random(graine); self.out = []

    def trait(self, p, q, sorte="moyen", depasse=None, double=False, tirets=None):
        lw, op, col = self.TRAITS[sorte]
        if depasse is None: depasse = sorte in ("fort", "moyen")
        self.out.append(self._ligne(p, q, lw, col, op, depasse, 0, tirets))
        if double: self.out.append(self._ligne(p, q, lw * 0.7, col, op * 0.45, depasse, 1, tirets))

    def _ligne(self, p, q, lw, col, op, depasse, k, tirets):
        r = self.r
        p, q = np.array(p, float), np.array(q, float); d = q - p; L = np.linalg.norm(d)
        if L < 1e-6: return ""
        u = d / L; n = np.array([-u[1], u[0]])
        e1 = r.uniform(0.5, 1.8) if depasse else 0; e2 = r.uniform(0.5, 1.8) if depasse else 0
        p = p - u * e1; L += e1 + e2
        amp = min(0.25, 0.04 + L * 0.0022) * (1.4 if k else 1)
        ph1, ph2 = r.uniform(0, 6.3), r.uniform(0, 6.3); f1, f2 = r.uniform(0.6, 1.4), r.uniform(2, 3.5)
        dec = r.uniform(-0.15, 0.15) if k else 0
        npts = max(4, int(L / 3)); pts = []
        for i in range(npts + 1):
            t = i / npts
            w = amp * (math.sin(2*math.pi*f1*t + ph1) * 0.7 + math.sin(2*math.pi*f2*t + ph2) * 0.3) + dec
            x, y = p + u * L * t + n * w
            pts.append(f"{x:.2f},{y:.2f}")
        da = f' stroke-dasharray="{tirets}"' if tirets else ""
        return (f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="{lw:.2f}" '
                f'stroke-opacity="{op:.2f}" stroke-linecap="round" stroke-linejoin="round"{da}/>')

    def courbe(self, pts_px, sorte="moyen"):
        """courbe libre (plantes, chaises) passant par des points en px"""
        lw, op, col = self.TRAITS[sorte]
        pts = [P(*p) for p in pts_px]
        d = f"M{pts[0][0]:.2f},{pts[0][1]:.2f} " + " ".join(
            f"Q{pts[i][0]:.2f},{pts[i][1]:.2f} {(pts[i][0]+pts[i+1][0])/2:.2f},{(pts[i][1]+pts[i+1][1])/2:.2f}" for i in range(1, len(pts) - 1)
        ) + f" T{pts[-1][0]:.2f},{pts[-1][1]:.2f}"
        self.out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{lw:.2f}" stroke-opacity="{op:.2f}" stroke-linecap="round"/>')

    def cercle(self, cx, cy, r, sorte="moyen", ry=None):
        lw, op, col = self.TRAITS[sorte]; ry = ry or r
        ph = self.r.uniform(0, 6.3); pts = []
        for i in range(0, 76):
            a = 2*math.pi*i/72; j = 0.6*math.sin(3*a + ph)
            pts.append(P(cx + (r + j)*math.cos(a), cy + (ry + j)*math.sin(a)))
        self.out.append(f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}" fill="none" stroke="{col}" '
                        f'stroke-width="{lw:.2f}" stroke-opacity="{op:.2f}" stroke-linecap="round"/>')

    def texte(self, x, y, t, taille=3.2, couleur="#7d8fa6", ancre="start", op=0.9, rot=0):
        tr = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot else ""
        self.out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="\'Architects Daughter\', cursive" font-size="{taille}" '
                        f'fill="{couleur}" fill-opacity="{op}" text-anchor="{ancre}"{tr}>{t}</text>')


def L_(c, x1, y1, x2, y2, sorte="moyen", **kw):
    c.trait(P(x1, y1), P(x2, y2), sorte, **kw)


def fuyante(c, x1, y1, x2, sorte="moyen", **kw):
    L_(c, x1, y1, x2, sur(x1, y1, x2), sorte, **kw)


def quad_mur(c, x1, x2, yt, yb, sorte="fort"):
    """rectangle sur le mur aux fenêtres : haut et bas fuient vers PF"""
    fuyante(c, x1, yt, x2, sorte); fuyante(c, x1, yb, x2, sorte)
    L_(c, x1, yt, x1, yb, sorte); L_(c, x2, sur(x1, yt, x2), x2, sur(x1, yb, x2), sorte)


def grille(c, x1, x2, yt, yb, ncol, nlig):
    """la grille en béton d'une fenêtre"""
    quad_mur(c, x1, x2, yt, yb, "fort")
    fuyante(c, x1 + 4, yt + 5, x2, "fin");
    for i in range(1, ncol):
        x = x1 + (x2 - x1) * i / ncol
        L_(c, x, sur(x1, yt, x) + 2, x, sur(x1, yb, x) - 2, "moyen", depasse=False)
    for j in range(1, nlig):
        y = yt + (yb - yt) * j / nlig
        fuyante(c, x1 + 2, y, x2 - 2, "moyen", depasse=False)


def feuilles(c, bx, by, n, lmin, lmax, a0, a1, graine, courbure=0.25):
    r = random.Random(graine)
    for i in range(n):
        a = math.radians(a0 + (a1 - a0) * (i + r.uniform(-0.3, 0.3)) / max(1, n - 1))
        l = r.uniform(lmin, lmax); cb = r.uniform(-courbure, courbure)
        p1 = (bx + l*0.5*math.cos(a) + cb*l*math.sin(a), by - l*0.5*math.sin(a) + cb*l*math.cos(a)*0.3)
        p2 = (bx + l*math.cos(a + cb*0.6), by - l*math.sin(a + cb*0.6))
        c.courbe([(bx, by), p1, p2], "fin" if i % 3 else "moyen")


def buisson(c, cx, cy, rx, ry, graine, n=14):
    r = random.Random(graine)
    for _ in range(n):
        x = cx + r.uniform(-rx, rx); y = cy + r.uniform(-ry, ry) * (1 - abs(x - cx) / (rx * 1.6))
        s = r.uniform(5, 9); a = r.uniform(0, 6.3)
        c.courbe([(x, y), (x + s*math.cos(a), y + s*math.sin(a)), (x + s*1.5*math.cos(a + 0.9), y + s*1.5*math.sin(a + 0.9))], "fin")
    for _ in range(4):   # tiges
        x = cx + r.uniform(-rx*0.6, rx*0.6)
        c.courbe([(cx, cy + ry*1.2), ((cx + x)/2, cy + ry*0.4), (x, cy - ry*0.6)], "leger")


def chaise(c, x, y, s):
    """chaise empilée vue de trois quarts : dossier, accoudoir, assise, pieds"""
    c.courbe([(x, y - 44*s), (x + 16*s, y - 63*s), (x + 42*s, y - 60*s)], "moyen")      # dossier
    c.courbe([(x, y - 44*s), (x - 1*s, y - 22*s), (x + 2*s, y)], "moyen")
    c.courbe([(x + 2*s, y - 24*s), (x + 20*s, y - 30*s), (x + 40*s, y - 34*s)], "fin")  # accoudoir
    c.courbe([(x + 2*s, y), (x + 20*s, y - 3*s), (x + 41*s, y - 7*s)], "moyen")          # assise
    L_(c, x + 42*s, y - 60*s, x + 41*s, y - 7*s, "fin", depasse=False)
    for dx, dy, lg in ((4, 0, 52), (38, -6, 50), (22, -3, 44)):                          # pieds
        L_(c, x + dx*s, y + dy*s, x + (dx + 1)*s, y + (dy + lg)*s, "moyen" if dx != 22 else "fin", depasse=False)


def croquis():
    c = Crayon(7)
    A, B = (412, 296), (412, 642)
    XP = 600                                    # A'B' : côté gauche de la grande fenêtre à grille

    # --- l'auvent et le bâtiment au-dessus
    L_(c, 195, 257, W, 257 - 0.495*(W - 195), "fort", double=True)                                    # arête haute de la dalle
    L_(c, 230, 282, W, 282 - 0.44*(W - 230), "fort")                                                    # arête basse de la dalle
    L_(c, 195, 257, 230, 282, "moyen")                                                                  # bout de la dalle
    fuyante(c, A[0], A[1], W, "fort", double=True)                                                      # sous-face / mur aux fenêtres
    L_(c, 230, 298, A[0], A[1], "fort")                                                                 # haut du mur du fond (de face)
    L_(c, 123, 31, 188, 31, "moyen"); L_(c, 123, 31, 123, 118, "moyen"); L_(c, 188, 31, 188, 118, "moyen")   # climatiseur du haut
    L_(c, 123, 118, 188, 118, "moyen"); c.cercle(140, 78, 14, "fin", 30)
    L_(c, 112, 124, 210, 124, "moyen"); L_(c, 112, 132, 210, 132, "fin")                               # son support
    L_(c, 196, 124, 205, 160, "fin")
    L_(c, 150, 46, 150, 579, "moyen"); L_(c, 156, 46, 156, 576, "fin", depasse=False)                 # descente d'eau
    c.courbe([(150, 579), (148, 590), (136, 594)], "moyen")
    L_(c, 194, 210, 194, 510, "fin")                                                                    # tuyau
    L_(c, 490, 0, 491, 257 - 0.495*(491 - 195) - 4, "moyen"); L_(c, 547, 0, 547, 257 - 0.495*(547 - 195) - 4, "fin")                                     # câbles de la façade
    L_(c, 40, 60, 40, 230, "moyen"); L_(c, 58, 55, 58, 232, "moyen")                                    # fente de fenêtre à gauche
    L_(c, 40, 60, 58, 55, "fin"); L_(c, 40, 230, 58, 232, "fin")
    c.cercle(104, 311, 8, "fin")                                                                        # applique (mur de gauche)

    # --- le mur du fond (de face) et le coin AB
    L_(c, *A, *B, "fort", double=True)
    L_(c, 54, 640, B[0], B[1], "fort")                                                                  # pied du mur du fond
    L_(c, 296, 300, 404, 300, "moyen"); L_(c, 296, 385, 404, 385, "moyen")                             # climatiseur
    L_(c, 296, 300, 296, 385, "moyen"); L_(c, 404, 300, 404, 385, "moyen")
    c.cercle(335, 342, 28, "moyen"); c.cercle(335, 342, 5, "fin")
    L_(c, 372, 318, 396, 318, "fin"); L_(c, 372, 360, 396, 360, "fin"); L_(c, 372, 318, 372, 360, "fin")
    L_(c, 300, 385, 312, 396, "fin"); L_(c, 392, 385, 380, 396, "fin")
    c.courbe([(410, 350), (418, 420), (414, 520), (404, 590)], "fin")                                  # câble
    # banc maçonné
    L_(c, 54, 594, 404, 597, "fort"); L_(c, 54, 636, 404, 638, "fort"); L_(c, 54, 594, 54, 638, "fort")
    L_(c, 30, 612, 54, 612, "moyen"); L_(c, 30, 612, 30, 645, "moyen"); L_(c, 10, 628, 30, 628, "moyen")  # marches
    # bac à plante, pots, plantes
    L_(c, 69, 530, 127, 530, "fort"); L_(c, 69, 530, 69, 590, "fort"); L_(c, 127, 530, 127, 590, "fort")
    L_(c, 69, 590, 127, 590, "moyen")
    feuilles(c, 98, 528, 16, 45, 110, 25, 155, 3)                                                       # yucca
    feuilles(c, 22, 560, 14, 40, 90, 30, 150, 5, 0.15)                                                  # plante piquante
    for cx, cy, rx in ((163, 575, 18), (217, 576, 21)):                                                 # pots
        c.courbe([(cx - rx, cy - 16), (cx - rx - 3, cy + 4), (cx, cy + 18), (cx + rx + 3, cy + 4), (cx + rx, cy - 16)], "moyen")
        L_(c, cx - rx, cy - 16, cx + rx, cy - 16, "moyen", depasse=False)
    buisson(c, 163, 528, 16, 26, 11, 10); buisson(c, 222, 520, 34, 30, 13, 18)

    # --- le mur aux fenêtres (fuit vers PF)
    fuyante(c, B[0], B[1], 470, "fort")                                                                 # pied du mur (le reste est caché par les chaises)
    grille(c, 464, 556, 358, 527, 6, 6)
    grille(c, 597, W, 317, 506, 5, 7)
    c.cercle(433, 314, 11, "moyen", 14); c.cercle(667, 231, 17, "moyen", 22)                           # appliques rondes

    # --- les chaises empilées le long du mur
    for i in range(7):
        t = i / 6
        chaise(c, 478 + 170*t, 590 + 55*t, 1.0 + 0.55*t)

    # --- le sol : joints du carrelage, en trait fin
    sol = Crayon(9)
    k = 0; y_avant = 1e9
    while True:                                   # joints parallèles au mur du fond : 1/(y - YH) régulier
        y = YH + 1 / (0.001916 + k * 0.0002)
        if y < 650: break
        if y_avant - y < 11: k += 1; continue        # au fond, on n'en garde qu'un sur deux
        y_avant = y
        x_d = min(W, 412 + (y - 642) / 0.3805) if y < 744 else W
        x_g = PF[0] + (30 - PF[0]) * (y - YH) / (990 - YH)       # le bord du trottoir
        L_(sol, x_g, y, x_d, y - 0.02*(x_d - x_g), "fin", depasse=False)
        k += 1
    for x990 in (30, 220, 410, 601, 791):          # joints qui fuient vers PF
        y0 = 640
        xs = PF[0] + (x990 - PF[0]) * (y0 - YH) / (990 - YH)
        L_(sol, xs, y0, PF[0] + (x990 - PF[0]) * (H - YH) / (990 - YH), H, "fin", depasse=False)
    L_(sol, 0, 1018, W, 1004, "moyen")                                                                  # caniveau au premier plan
    L_(sol, 0, 1030, W, 1020, "fin")
    return c, sol, A, B, XP


def construction(A, B, XP):
    k = Crayon(3)
    for i in range(5):                                         # grille de 4 cm
        x = (4*i - X0) * S; L_(k, x, 0, x, H, "construction", depasse=False)
    for j in range(7):
        y = (4*j - Y0) * S; L_(k, 0, y, W, y, "construction", depasse=False)
    xg, xd = -OX / MM + 2, (PAGE_W - OX) / MM - 2
    L_(k, xg, YH, xd, YH, "construction", depasse=False)       # ligne d'horizon
    Cy, Dy = sur(*A, XP), sur(*B, XP)
    for y0 in (Cy, Dy):                                        # fuyantes C→A→PF et D→B→PF
        L_(k, XP, y0, PF[0], PF[1], "construction", depasse=False)
    L_(k, XP, Cy - 12, XP, Dy + 12, "construction", depasse=False)     # A'B'
    L_(k, *A, XP, A[1], "construction", depasse=False, tirets="1.2 1")  # horizontales
    L_(k, *B, XP, B[1], "construction", depasse=False, tirets="1.2 1")
    lab = [(A, "A", (-2.6, -1)), (B, "B", (-2.6, 3.4)), ((XP, A[1]), "A'", (1.2, 3.4)), ((XP, B[1]), "B'", (1.2, -1)),
           ((XP, Cy), "C", (1.2, -0.8)), ((XP, Dy), "D", (1.2, 3.4))]
    for (x, y), t, (dx, dy) in lab:
        px, py = P(x, y); k.texte(px + dx, py + dy, t, 3.2)
    px, py = P(*PF); k.out.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="0.5" fill="#7d8fa6" fill-opacity="0.6"/>')
    k.texte(px - 1, py - 1.5, "PF", 3.0, ancre="end")
    k.texte(OX + W*MM + 1.2, P(0, YH)[1] - 1, "LH", 3.0)
    for (ya, yb) in ((Cy, A[1]), (B[1], Dy)):
        a, b = P(0, ya)[1], P(0, yb)[1]; x = P(XP, 0)[0] + 6
        k.texte(x, (a + b)/2 + 1, f"{abs(yb - ya)*MM/10:.1f} cm".replace(".", ","), 2.6)
    return k


def page():
    c, sol, A, B, XP = croquis()
    k = construction(A, B, XP)
    t = Crayon(5)
    t.texte(OX, 12, "Croquis 3 · la cour, sous l'auvent", 6.0, "#1f1f1f", op=1)
    t.texte(OX, 18, "méthode du cadrage à l'acétate · grille de 4 cm", 3.6, "#666", op=1)
    etapes = ["1  cadrage à l'acétate, grille de 4 cm", "2  l'arête verticale AB (le coin)",
              "3  la verticale A'B' (côté de la fenêtre) et les horizontales",
              "4  C et D relevés au crayon, bras tendu", "5  fuyantes AC et BD → PF sur la LH"]
    for i, e in enumerate(etapes):
        t.texte(PAGE_W - 12, 7.5 + i*3.4, e, 2.8, "#7d8fa6", "end")
    t.texte(OX, PAGE_H - 6, "LH : ligne d'horizon, à hauteur des yeux · PF : point de fuite (1 cm à gauche du cadre)", 2.9, "#888", op=1)
    cadre = Crayon(6)
    co = [(0, 0), (W, 0), (W, H), (0, H)]
    for i in range(4): L_(cadre, *co[i], *co[(i+1) % 4], "moyen")
    clip = f'<clipPath id="fen"><rect x="{OX}" y="{OY}" width="{W*MM}" height="{H*MM}"/></clipPath>'
    sol_clip = (f'<clipPath id="sol"><polygon points="{" ".join(f"{P(x, y)[0]:.2f},{P(x, y)[1]:.2f}" for x, y in [(0, 640), (412, 642), (470, sur(412, 642, 470)), (W, 760), (W, H), (0, H)])}"/></clipPath>')
    svg = (f'<svg viewBox="0 0 {PAGE_W} {PAGE_H}" xmlns="http://www.w3.org/2000/svg"><defs>{clip}{sol_clip}</defs>'
           f'{"".join(k.out)}<g clip-path="url(#fen)"><g clip-path="url(#sol)">{"".join(sol.out)}</g>{"".join(c.out)}</g>'
           f'{"".join(cadre.out)}{"".join(t.out)}</svg>')
    return svg


if __name__ == "__main__":
    html = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Croquis 3</title>
<link rel="stylesheet" href="../polices-local.css">
<style>@page {{ size: 210mm 297mm; margin: 0; }} html, body {{ margin: 0; background: #fff; }}
.p {{ width: 210mm; height: 297mm; overflow: hidden; background: #fdfcf8; }} svg {{ width: 100%; height: 100%; display: block; }}</style></head>
<body><div class="p">{page()}</div></body></html>"""
    open(f"{ICI}/croquis-3.html", "w", encoding="utf-8").write(html)
    print("croquis-3.html écrit")

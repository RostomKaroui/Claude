"""Séance 4 : deux croquis de la médina de Tunis (la voûte, la rue aux portes bleues), version détaillée.

Même méthode que les séances 2 et 3 : grille de 4 cm, arête AB, verticale A'B', horizontales,
C et D relevés au crayon bras tendu, fuyantes AC et BD jusqu'au point de fuite PF sur la LH.
Remarques de la prof : pas de hachures, contours forts, détails fins, construction très légère.
La moto, la main au premier plan et la végétation sont laissées de côté.

Entrée : redresse_*.png (cadre 18 x 24 cm, 40 px = 1 cm) et redresse2_*.jpg (la même, 2x, pour les relevés).
Sortie : croquis-4-voute.html et croquis-4-rue.html (A4) ; avec CALQUE=1, aussi calque-*.html (dessin sur la photo).
"""
import math, os, random, sys
import cv2
import numpy as np
import releve

ICI = sys.argv[1] if len(sys.argv) > 1 else "."
S = 40; MM = 10 / S
W, H = 720, 960
X0, Y0 = -1.0, -2.0          # grille : lignes à 1, 5, 9, 13, 17 cm et 2, 6, ..., 22 cm
PAGE_W, PAGE_H = 210, 297
OX, OY = 15, 30

PF = (0, 0); YH = 0


def regler(pf):
    global PF, YH
    PF = pf; YH = pf[1]


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
        """courbe libre passant près des points donnés en px"""
        lw, op, col = self.TRAITS[sorte]
        pts = [P(*p) for p in pts_px]
        if len(pts) == 2: pts.insert(1, ((pts[0][0] + pts[1][0]) / 2, (pts[0][1] + pts[1][1]) / 2))
        d = f"M{pts[0][0]:.2f},{pts[0][1]:.2f} " + " ".join(
            f"Q{pts[i][0]:.2f},{pts[i][1]:.2f} {(pts[i][0]+pts[i+1][0])/2:.2f},{(pts[i][1]+pts[i+1][1])/2:.2f}" for i in range(1, len(pts) - 1)
        ) + f" T{pts[-1][0]:.2f},{pts[-1][1]:.2f}"
        self.out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{lw:.2f}" stroke-opacity="{op:.2f}" stroke-linecap="round"/>')

    def brisee(self, pts_px, sorte="leger", ferme=False):
        """ligne brisée à main levée (pierres anguleuses)"""
        lw, op, col = self.TRAITS[sorte]
        p = [P(*q) for q in pts_px] + ([P(*pts_px[0])] if ferme else [])
        self.out.append(f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in p)}" fill="none" stroke="{col}" '
                        f'stroke-width="{lw:.2f}" stroke-opacity="{op:.2f}" stroke-linecap="round" stroke-linejoin="round"/>')

    def forme(self, pts_px, sorte="leger"):
        """contour fermé arrondi (tache d'enduit)"""
        lw, op, col = self.TRAITS[sorte]
        p = [P(*q) for q in pts_px]; n = len(p)
        if n < 3: return
        m = [((p[i][0] + p[(i+1) % n][0]) / 2, (p[i][1] + p[(i+1) % n][1]) / 2) for i in range(n)]
        d = f"M{m[-1][0]:.2f},{m[-1][1]:.2f} " + " ".join(f"Q{p[i][0]:.2f},{p[i][1]:.2f} {m[i][0]:.2f},{m[i][1]:.2f}" for i in range(n)) + " Z"
        self.out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{lw:.2f}" stroke-opacity="{op:.2f}" stroke-linejoin="round"/>')

    def arc(self, cx, cy, r, a0, a1, sorte="moyen", ry=None, double=False):
        """arc d'ellipse (angles en degrés, 0 = droite, 90 = haut), tremblé à la main"""
        lw, op, col = self.TRAITS[sorte]; ry = ry or r
        for k in range(2 if double else 1):
            ph = self.r.uniform(0, 6.3); n = max(12, int(abs(a1 - a0) / 3)); pts = []
            for i in range(n + 1):
                a = math.radians(a0 + (a1 - a0) * i / n)
                j = min(1.6, 0.25 + 0.012 * r) * (1 + 0.5*k) * math.sin(2.3*a + ph)     # tremblé en px
                pts.append(P(cx + (r + j) * math.cos(a), cy - (ry + j) * math.sin(a)))
            self.out.append(f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}" fill="none" stroke="{col}" '
                            f'stroke-width="{lw*(0.7 if k else 1):.2f}" stroke-opacity="{op*(0.45 if k else 1):.2f}" '
                            f'stroke-linecap="round" stroke-linejoin="round"/>')

    def cercle(self, cx, cy, r, sorte="moyen", ry=None):
        self.arc(cx, cy, r, 0, 365, sorte, ry)

    def volute(self, cx, cy, r, tours=1.6, a0=0, sens=1, sorte="fin", queue=None):
        """spirale de fer forgé ; queue = point (px) où la spirale rejoint la barre"""
        lw, op, col = self.TRAITS[sorte]
        pts = []
        n = int(40 * tours)
        for i in range(n + 1):
            t = i / n; a = math.radians(a0) + sens * t * tours * 2 * math.pi; rr = r * (1 - 0.82 * t)
            pts.append(P(cx + rr * math.cos(a), cy - rr * math.sin(a)))
        if queue: pts.insert(0, P(*queue))
        self.out.append(f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}" fill="none" stroke="{col}" '
                        f'stroke-width="{lw:.2f}" stroke-opacity="{op:.2f}" stroke-linecap="round" stroke-linejoin="round"/>')

    def texte(self, x, y, t, taille=3.2, couleur="#7d8fa6", ancre="start", op=0.9, rot=0):
        tr = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot else ""
        self.out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="\'Architects Daughter\', cursive" font-size="{taille}" '
                        f'fill="{couleur}" fill-opacity="{op}" text-anchor="{ancre}"{tr}>{t}</text>')


def L_(c, x1, y1, x2, y2, sorte="moyen", **kw):
    c.trait(P(x1, y1), P(x2, y2), sorte, **kw)


def fuyante(c, x1, y1, x2, sorte="moyen", **kw):
    L_(c, x1, y1, x2, sur(x1, y1, x2), sorte, **kw)


def rect(c, x1, y1, x2, y2, sorte="moyen", **kw):
    for a, b in (((x1, y1), (x2, y1)), ((x2, y1), (x2, y2)), ((x2, y2), (x1, y2)), ((x1, y2), (x1, y1))):
        L_(c, *a, *b, sorte, **kw)


def quad_mur(c, x1, x2, yt, yb, sorte="fort", **kw):
    """rectangle sur un mur qui fuit : haut et bas vont vers PF"""
    fuyante(c, x1, yt, x2, sorte, **kw); fuyante(c, x1, yb, x2, sorte, **kw)
    L_(c, x1, yt, x1, yb, sorte, **kw); L_(c, x2, sur(x1, yt, x2), x2, sur(x1, yb, x2), sorte, **kw)


def pierres(c, poly, y_fond, graine, pas=1.25e-4, garde=None, larg=(0.11, 0.22)):
    """les pavés, un par un : des pierres plates arrondies, rang par rang (perspective : 1/(y - YH) régulier).
    On en laisse une partie en blanc, surtout au fond, comme on le fait à la main."""
    r = random.Random(graine)
    pp = np.array(poly, np.float32)
    y = H + 25
    while True:
        y2 = YH + 1 / (1 / (y - YH) + pas)           # rang suivant, plus au fond
        if y2 < y_fond: break
        h = y - y2; prof = (y - YH) / (H - YH)
        if h >= 3.2:
            x = -r.uniform(0, 30)
            while x < W + 10:
                w = (y - YH) * r.uniform(*larg)
                g = max(0.9, 0.13 * h)
                cx, cy = x + w / 2, y2 + h / 2 + r.uniform(-0.12, 0.12) * h
                p_garde = (0.2 + 0.5 * prof) if garde is None else garde(cx, cy, prof)
                if cv2.pointPolygonTest(pp, (cx, cy), False) > 0 and r.random() < p_garde:
                    a, b = w / 2 - g, (h / 2 - g) * r.uniform(0.7, 1.0)
                    pen = r.uniform(-0.25, 0.25) * b                                  # pierre un peu de travers
                    pts = []
                    for (ux, uy) in ((-1, -0.75), (r.uniform(-0.5, 0.3), -1.1), (0.92, -0.95), (1.06, r.uniform(-0.2, 0.4)),
                                     (0.85, 1.0), (r.uniform(-0.4, 0.2), 1.08), (-1.04, 0.8)):
                        pts.append((cx + ux * a * r.uniform(0.9, 1.05), cy + uy * b + pen * ux + r.uniform(-0.18, 0.18) * b))
                    sorte = "leger" if prof < 0.75 or r.random() < 0.6 else "fin"
                    if r.random() < 0.45:                                             # contour laissé ouvert, comme à la main
                        k0 = r.randrange(len(pts)); pts = pts[k0:] + pts[:k0]
                        c.brisee(pts[:-r.randint(1, 3)], sorte)
                    else:
                        c.brisee(pts, sorte, ferme=True)
                x += w
        y = y2


def rosaces(c, x1, x2, y1, y2, s, mur=True, sorte="leger"):
    """motif de zellige : petites rosaces en quinconce ; mur=True -> les rangs suivent les fuyantes"""
    j = 0; y = y1
    while y < y2:
        x = x1 + (s / 2 if j % 2 else 0) + s / 2
        while x < x2 - s / 3:
            yy = sur(x1, y, x) if mur else y
            c.cercle(x, yy, s * 0.3, sorte)
            x += s
        y += s * 0.9; j += 1


def briques(c, x1, x2, y1, y2, hb=7, sorte="leger", graine=1):
    """quelques assises de briques (joints horizontaux et joints verticaux décalés)"""
    r = random.Random(graine); y = y1; k = 0
    while y < y2:
        L_(c, x1, y, x2, y + r.uniform(-0.6, 0.6), sorte, depasse=False)
        xv = x1 + (6 if k % 2 else 12)
        while xv < x2 - 2:
            L_(c, xv, y, xv, y + hb, sorte, depasse=False); xv += 13
        y += hb; k += 1


def grillage(c, x1, y1, x2, y2, pas=9, sorte="leger"):
    """grillage juste suggéré : quelques fils verticaux et deux fils horizontaux (pas de hachures)"""
    x = x1 + pas
    while x < x2 - 2:
        L_(c, x, y1, x, y2, sorte, depasse=False); x += pas * 1.6
    for y in (y1 + (y2 - y1) * 0.3, y1 + (y2 - y1) * 0.7):
        L_(c, x1, y, x2, y, sorte, depasse=False)


def taches_auto(c, hi, zone, aire_max=5000, sorte="leger", **kw):
    """plaques d'enduit tombé relevées sur la photo"""
    for t in releve.taches(hi, zone, **kw):
        if cv2.contourArea(np.float32(t)) > aire_max: continue
        c.forme([tuple(p) for p in t[:-1]], sorte)


# ================================================================ 1. la voûte
def voute():
    regler((335, 615))
    hi = cv2.imread(f"{ICI}/redresse2_voute.jpg")
    c = Crayon(41)
    A, B, XP = (506, sur(518, 353, 506)), (506, sur(720, 923, 506)), 640

    # --- le bâtiment au fond, au-dessus de la voûte
    L_(c, 200, 4, 200, 247, "fort"); L_(c, 308, 4, 308, 247, "fort")                # fenêtre verte (porte-fenêtre)
    L_(c, 196, 8, 312, 8, "moyen")
    L_(c, 207, 14, 207, 245, "fin"); L_(c, 301, 14, 301, 245, "fin"); L_(c, 207, 14, 301, 14, "fin")
    L_(c, 251, 14, 251, 245, "moyen"); L_(c, 256, 14, 256, 245, "fin", depasse=False)
    L_(c, 207, 100, 301, 100, "fin"); L_(c, 207, 104, 301, 104, "leger", depasse=False)
    for x0, x1 in ((212, 247), (260, 296)):                                         # carreaux
        for ya, yb in ((20, 96), (110, 240)):
            rect(c, x0, ya, x1, yb, "leger", depasse=False)
    c.courbe([(262, 22), (270, 60), (266, 96)], "leger")                           # rideau
    L_(c, 226, 247, 332, 247, "fort"); L_(c, 226, 256, 332, 256, "moyen")          # balcon
    L_(c, 226, 247, 226, 256, "fin"); L_(c, 332, 247, 332, 256, "fin")
    L_(c, 234, 256, 234, 276, "moyen"); L_(c, 326, 256, 326, 276, "moyen"); L_(c, 234, 276, 326, 276, "moyen")
    for x in range(244, 320, 10): L_(c, x, 258, x, 274, "leger", depasse=False)
    L_(c, 300, 276, 300, 321, "fin"); L_(c, 325, 276, 325, 321, "fin"); L_(c, 300, 321, 325, 321, "fin")   # console
    c.courbe([(300, 300), (310, 312), (325, 316)], "leger")
    L_(c, 462, 97, 462, 200, "fort")                                               # angle du bâtiment de droite
    L_(c, 488, 0, 452, 97, "fort")                                                 # rive du toit en tuiles
    for i in range(1, 9):
        t = i / 9; x, y = 488 - 36 * t, 97 * t; L_(c, x, y, x - 10, y - 2, "fin", depasse=False)
    L_(c, 452, 97, 462, 97, "moyen")
    L_(c, 503, 40, 503, 200, "fin"); L_(c, 513, 36, 513, 205, "fin")              # renfoncement haut
    taches_auto(c, hi, releve.masque_poly([[(330, 190), (455, 190), (455, 380), (330, 380)]]) & ~releve.vert(hi), aire_max=3000)

    # --- le mur de gauche
    L_(c, 57, 0, 57, 700, "fort", double=True)                                     # l'angle avec la façade
    L_(c, 28, 238, 28, 524, "moyen"); L_(c, 37, 245, 37, 520, "fin")              # cadre bleu d'une porte
    L_(c, 28, 238, 37, 245, "moyen")
    L_(c, 3, 578, 3, 950, "fin"); L_(c, 21, 582, 21, 948, "fin"); L_(c, 3, 578, 21, 582, "fin")   # grillage du coin
    grillage(c, 3, 600, 21, 760)
    # le bac de l'arbre et sa cage (on laisse l'arbre de côté)
    L_(c, 60, 560, 60, 700, "fin"); L_(c, 130, 562, 130, 700, "fin"); L_(c, 60, 560, 130, 562, "fin")
    grillage(c, 62, 600, 128, 698, 11)
    L_(c, 52, 700, 138, 700, "fort"); L_(c, 55, 700, 55, 800, "fort"); L_(c, 134, 700, 134, 800, "fort")
    L_(c, 55, 710, 134, 710, "fin", depasse=False)
    L_(c, 48, 800, 140, 800, "moyen"); L_(c, 48, 800, 48, 815, "fin"); L_(c, 140, 800, 140, 812, "fin")
    L_(c, 48, 815, 140, 812, "fin")

    # --- l'arc d'entrée (épais) et la voûte
    c.arc(247, 540, 170, 3, 180, "fort", double=True)                              # extrados
    c.arc(246, 540, 146, 0, 180, "moyen")                                          # intrados
    L_(c, 77, 540, 77, 700, "fort"); L_(c, 100, 540, 100, 700, "moyen")            # pied gauche de l'arc
    L_(c, 392, 545, 318, 612, "fin")                                               # naissance de la voûte, à droite
    # l'arc du fond : bord extérieur et ouverture (plus large à gauche, on voit le tableau de droite)
    c.arc(213, 612, 112, 90, 180, "moyen", ry=105); c.arc(213, 612, 104, 0, 90, "moyen", ry=105)
    c.arc(213, 615, 95, 90, 180, "moyen", ry=83); c.arc(213, 615, 85, 0, 90, "moyen", ry=83)
    L_(c, 298, 615, 298, 736, "moyen"); L_(c, 317, 612, 317, 741, "moyen")
    L_(c, 101, 612, 101, 700, "fin")
    # la lanterne suspendue
    L_(c, 210, 396, 210, 407, "fin", depasse=False)
    L_(c, 202, 407, 218, 407, "moyen"); L_(c, 195, 417, 225, 417, "moyen")
    L_(c, 202, 407, 195, 417, "moyen", depasse=False); L_(c, 218, 407, 225, 417, "moyen", depasse=False)
    L_(c, 196, 420, 226, 420, "fin", depasse=False)
    L_(c, 196, 420, 202, 462, "moyen"); L_(c, 226, 420, 220, 462, "moyen"); L_(c, 202, 462, 220, 462, "moyen")
    L_(c, 211, 420, 211, 462, "leger", depasse=False); L_(c, 199, 440, 223, 440, "leger", depasse=False)
    L_(c, 211, 462, 211, 470, "fin", depasse=False)

    # --- au fond, sous l'arc : porte bleue, imposte, plaque, compteur
    L_(c, 118, 583, 205, 583, "moyen"); L_(c, 133, 579, 203, 579, "fin")
    rect(c, 137, 540, 200, 576, "leger", depasse=False)                            # imposte vitrée
    L_(c, 118, 583, 118, 733, "moyen"); L_(c, 203, 532, 203, 734, "moyen"); L_(c, 209, 534, 209, 734, "fin")
    L_(c, 161, 586, 161, 732, "fin")
    for xa, xb in ((123, 157), (165, 199)):                                         # panneaux de la porte
        for ya, yb in ((591, 620), (625, 656), (661, 693), (698, 727)):
            rect(c, xa, ya, xb, yb, "leger", depasse=False)
    c.cercle(161, 621, 2, "fin"); c.cercle(163, 690, 2, "fin")
    L_(c, 116, 734, 300, 736, "moyen")                                             # pied du mur du fond
    L_(c, 112, 744, 318, 745, "fin")
    rect(c, 225, 537, 258, 552, "fin"); L_(c, 229, 545, 254, 545, "leger", depasse=False)   # plaque de la rue
    rect(c, 245, 674, 266, 706, "fin"); rect(c, 249, 678, 262, 702, "leger", depasse=False)  # compteur
    c.courbe([(262, 703), (275, 708), (288, 702)], "leger")
    L_(c, 278, 575, 278, 734, "fin"); L_(c, 290, 575, 290, 735, "fin")
    for y in (600, 640, 690): L_(c, 280, y, 288, y, "leger", depasse=False)

    # --- la colonne (sous l'arc) et le pilier sculpté
    L_(c, 375, 545, 416, 545, "moyen"); L_(c, 375, 550, 416, 550, "fin")          # tailloir
    c.courbe([(379, 550), (382, 560), (383, 566)], "fin"); c.courbe([(412, 550), (409, 560), (408, 566)], "fin")
    L_(c, 381, 566, 409, 566, "fin"); L_(c, 381, 588, 409, 588, "leger", depasse=False)
    L_(c, 381, 566, 381, 683, "fort"); L_(c, 409, 566, 409, 745, "fort")           # fût
    L_(c, 403, 531, 463, 531, "fort"); L_(c, 403, 541, 463, 541, "moyen")          # tailloir du pilier
    L_(c, 403, 531, 403, 541, "fin"); L_(c, 463, 531, 463, 541, "fin")
    L_(c, 414, 541, 414, 600, "moyen"); L_(c, 458, 541, 458, 600, "moyen")         # chapiteau
    c.volute(423, 552, 6, 1.5, 90, 1, "fin"); c.volute(449, 552, 6, 1.5, 90, -1, "fin")
    for x0 in (420, 436, 452):                                                      # feuilles d'acanthe
        c.courbe([(x0 - 5, 600), (x0 - 4, 585), (x0, 574), (x0 + 4, 585), (x0 + 5, 600)], "fin")
    L_(c, 414, 566, 458, 566, "leger", depasse=False)
    L_(c, 412, 600, 460, 600, "moyen")
    L_(c, 412, 600, 412, 732, "moyen"); L_(c, 460, 600, 460, 732, "moyen")         # le pilier sous grillage
    rect(c, 416, 606, 456, 728, "fin", depasse=False); grillage(c, 416, 640, 456, 728, 8)
    L_(c, 408, 732, 464, 732, "moyen"); L_(c, 406, 748, 466, 750, "moyen")         # base
    L_(c, 408, 732, 406, 748, "fin"); L_(c, 464, 732, 466, 750, "fin")
    # l'encadrement de porte en brique et pierre (mur de droite)
    L_(c, 461, 200, 461, 750, "fort", double=True)
    L_(c, 477, 205, 477, 752, "fin"); L_(c, 500, 205, 500, 752, "fin")
    L_(c, 461, 200, 506, 206, "moyen")
    briques(c, 478, 499, 330, 372, graine=2); briques(c, 478, 499, 470, 512, graine=3); briques(c, 478, 499, 610, 645, graine=4)
    c.arc(478, 304, 9, 0, 180, "moyen"); L_(c, 469, 304, 469, 742, "moyen"); L_(c, 487, 304, 487, 744, "moyen")
    L_(c, 458, 750, 506, 754, "moyen"); L_(c, 456, 760, 506, 765, "fin")         # seuil

    # --- le mur de droite (fuit vers PF)
    fuyante(c, *B, W, "fort", double=True)                                         # pied du mur
    L_(c, A[0], 206, A[0], B[1], "fort", double=True)                              # l'arête AB
    fuyante(c, 506, B[1] - 14, W, "leger")                                         # soubassement
    quad_mur(c, 518, 531, 353, 437, "moyen")                                       # petite fenêtre à barreaux
    fuyante(c, 515, 350, 534, "fin"); fuyante(c, 515, 441, 534, "fin")
    for x in (522, 527): L_(c, x, sur(518, 353, x) + 3, x, sur(518, 437, x) - 3, "fin", depasse=False)
    quad_mur(c, 527, 537, 649, 696, "fin")                                         # petite trappe
    yb = sur(506, 705, 601)                                                        # niche en arc
    L_(c, 601, 300, 601, yb, "fort"); L_(c, XP, 300, XP, sur(601, yb, XP), "fort")
    c.courbe([(601, 300), (604, 282), (620, 270), (636, 282), (XP, 300)], "fort")
    fuyante(c, 601, yb, XP, "moyen")
    L_(c, 608, 302, 608, yb - 2, "leger", depasse=False); c.courbe([(608, 302), (612, 288), (622, 282)], "leger")
    c.courbe([(615, 380), (622, 410), (618, 450)], "leger")                        # fissure
    quad_mur(c, 702, W, 225, 338, "moyen")                                         # fenêtre à grille
    for i, y in enumerate((250, 280, 310)):
        c.volute(711, sur(702, y, 711), 5, 1.4, 90, 1 if i % 2 else -1, "fin")
    zone = releve.masque_poly([[(512, 0), (720, 0), (720, 530), (560, 530), (560, 780), (512, 760)]])
    zone &= ~releve.masque_poly([[(596, 262), (645, 262), (645, 730), (596, 730)], [(512, 340), (540, 340), (540, 450), (512, 450)],
                                [(695, 215), (720, 215), (720, 345), (695, 345)]])
    taches_auto(c, hi, zone & ~releve.vert(hi))

    # --- un personnage assis contre la colonne (pour l'échelle)
    c.cercle(381, 692, 9, "moyen")
    c.courbe([(372, 690), (376, 681), (388, 682), (391, 690)], "fin")               # cheveux
    c.courbe([(373, 702), (368, 722), (368, 746)], "moyen"); c.courbe([(389, 702), (398, 716), (400, 742)], "moyen")
    c.courbe([(391, 707), (402, 716), (407, 727)], "fin")                           # bras
    c.courbe([(373, 712), (362, 728), (378, 736), (392, 732)], "fin")
    c.courbe([(368, 746), (345, 750), (328, 752)], "moyen"); c.courbe([(400, 745), (365, 757), (330, 760)], "moyen")
    c.courbe([(328, 752), (322, 755), (330, 760)], "fin")

    # --- le sol en pavés
    sol = Crayon(43)
    sol_poly = [(0, 960), (0, 950), (24, 945), (48, 818), (140, 814), (140, 748), (318, 748), (370, 752), (506, 756),
                (W, sur(506, 756, W)), (W, H)]
    pierres(sol, sol_poly, 748, 5)

    lignes = {"ab": "le bord de la niche", "omis": "la moto, la main et la végétation sont laissées de côté",
              "titre": "Croquis 1 · la voûte", "pf": "PF : point de fuite, au fond sous la voûte"}
    return c, sol, sol_poly, A, B, XP, lignes


# ================================================================ 2. la rue aux portes bleues
def rue():
    regler((528, 570))
    hi = cv2.imread(f"{ICI}/redresse2_rue.jpg")
    c = Crayon(51)
    A, B, XP = (346, 448), (346, 660), 232

    # --- façade de gauche : la fenêtre à grille bleue
    L_(c, 11, 14, 11, 222, "fort"); L_(c, 79, 82, 79, 262, "fort")
    L_(c, 11, 14, 79, 82, "fort"); L_(c, 9, 215, 80, 262, "fort")
    L_(c, 16, 22, 16, 220, "fin", depasse=False); L_(c, 74, 84, 74, 256, "fin", depasse=False)
    for yl, yr in ((70, 130), (128, 180), (178, 228)):                              # barres en biais (suivent le mur)
        L_(c, 12, yl, 78, yr, "fin", depasse=False)
    for x in (27, 45, 62):                                                          # barres ondulées
        c.courbe([(x, 14 + 0.98 * (x - 11) + 4), (x + 4, 60 + x * 0.9), (x - 3, 120 + x * 0.8), (x + 4, 170 + x * 0.7), (x, 214 + 0.68 * (x - 9) - 3)], "fin")
    for cx, cy, r, s in ((25, 40, 6, 1), (68, 90, 6, -1), (50, 145, 10, 1), (25, 205, 6, -1), (70, 244, 6, 1), (38, 100, 5, -1)):
        c.volute(cx, cy, r, 1.5, 0, s, "fin")
    L_(c, 6, 222, 84, 270, "moyen"); L_(c, 6, 233, 84, 279, "fin"); L_(c, 6, 222, 6, 233, "fin")   # appui
    L_(c, 3, 8, 3, 222, "leger"); L_(c, 3, 8, 11, 14, "leger")                     # tableau de la fenêtre

    # --- l'auvent au-dessus de la porte
    L_(c, 99, 54, 180, 44, "moyen"); L_(c, 104, 64, 180, 58, "fin"); L_(c, 99, 54, 104, 64, "fin")
    L_(c, 180, 44, 297, 196, "fort", double=True)                                  # rive avec les tuiles
    L_(c, 180, 58, 297, 216, "moyen")
    L_(c, 107, 73, 231, 219, "fort")                                               # contre le mur
    L_(c, 231, 219, 297, 216, "moyen"); L_(c, 297, 196, 297, 216, "moyen")
    for i in range(12):                                                            # tuiles rondes, en écailles
        t = (i + 0.5) / 12; x, y = 180 + 117 * t, 44 + 152 * t
        c.arc(x, y, 6, -52, 128, "fin")
    L_(c, 298, 229, 352, 300, "leger")                                             # câble

    # --- l'encadrement en zellige et la porte bleue
    L_(c, 106, 73, 106, 762, "fort", double=True); L_(c, 231, 219, 231, 714, "fort", double=True)
    L_(c, 129, 160, 129, 707, "moyen")                                             # tableau gauche
    L_(c, 129, 160, 218, 243, "moyen")                                             # haut du renfoncement
    L_(c, 184, sur(129, 160, 184) + 2, 184, 700, "moyen")                          # la porte, côté droit
    L_(c, 222, 238, 222, 708, "fin")
    rosaces(c, 108, 128, 80, 750, 7.5)                                             # zellige, face avant
    rosaces(c, 186, 221, 250, 700, 8, mur=False)                                   # zellige, dans le tableau
    for i in range(1, 15):                                                         # zellige du linteau (biais)
        t = i / 15; x = 112 + 108 * t; c.cercle(x, 80 + 137 * t + 8 + 4 * t, 2.0, "leger"); c.cercle(x + 4, 80 + 137 * t + 22 + 4 * t, 2.0, "leger")
    L_(c, 129, 318, 184, 318, "moyen")                                             # haut de la porte
    for y in (200, 240, 280):                                                      # imposte à grille, en arabesques
        c.courbe([(133, y), (146, y - 6), (158, y), (170, y + 6), (182, y)], "leger")
    L_(c, 147, 322, 147, 700, "leger", depasse=False)                              # battant
    rect(c, 152, 362, 167, 525, "fin"); rect(c, 155, 367, 164, 520, "leger", depasse=False)   # panneaux
    rect(c, 152, 580, 167, 662, "fin"); rect(c, 155, 585, 164, 657, "leger", depasse=False)
    L_(c, 132, 540, 182, 540, "fin"); L_(c, 132, 562, 182, 562, "fin")
    c.cercle(163, 553, 3, "fin"); c.cercle(147, 550, 2, "fin")
    L_(c, 125, 705, 215, 697, "moyen"); L_(c, 115, 732, 228, 706, "fin")            # seuil en marbre
    L_(c, 125, 705, 115, 732, "fin")
    L_(c, 106, 762, 231, 714, "fort")
    # descente, applique, plinthe, barres et coffrets bleus
    c.courbe([(231, 250), (238, 252), (240, 262)], "moyen"); L_(c, 240, 262, 240, 294, "moyen")
    rect(c, 232, 294, 247, 310, "moyen"); L_(c, 239, 310, 239, 318, "fin")
    L_(c, 241, 318, 243, 560, "fin"); L_(c, 245, 318, 247, 560, "leger", depasse=False)
    L_(c, 0, 594, 106, 614, "fin"); fuyante(c, 231, 594, 345, "fin")
    rect(c, 81, 580, 93, 759, "moyen"); rect(c, 254, 569, 261, 676, "moyen"); rect(c, 238, 609, 249, 655, "fin")
    L_(c, 4, 647, 68, 641, "moyen"); L_(c, 68, 641, 68, 734, "moyen"); L_(c, 68, 734, 4, 736, "moyen"); L_(c, 4, 736, 4, 647, "moyen")
    L_(c, 10, 652, 62, 647, "leger", depasse=False)
    c.cercle(22, 440, 3, "fin"); L_(c, 22, 443, 24, 452, "fin")                     # crochet au mur
    taches_auto(c, hi, releve.masque_poly([[(250, 330), (340, 380), (340, 640), (250, 640)]]), aire_max=1500)

    # --- fenêtre à grille du rez-de-chaussée
    quad_mur(c, 287, 323, 419, 557, "fort")
    for i in range(1, 6):
        x = 287 + 6 * i; L_(c, x, sur(287, 419, x) + 2, x, sur(287, 557, x) - 2, "fin", depasse=False)
    for j in range(1, 8):
        fuyante(c, 289, 419 + 17 * j, 321, "fin", depasse=False)

    # --- porte en arc et son encadrement de pierre, puis le fond
    L_(c, A[0], A[1] + 20, A[0], B[1], "fort", double=True)
    c.arc(369, 471, 23, 0, 180, "moyen"); L_(c, 392, 471, 392, 666, "moyen")
    c.arc(368.5, 476, 13.5, 0, 180, "moyen"); L_(c, 355, 476, 355, 637, "moyen"); L_(c, 382, 476, 382, 637, "moyen")
    L_(c, 355, 637, 382, 637, "fin"); L_(c, 368, 480, 368, 636, "leger", depasse=False)
    c.arc(369, 471, 18, 10, 170, "leger")
    L_(c, 340, 650, 398, 652, "fin"); L_(c, 342, 664, 400, 660, "fin")             # marche
    for y in (520, 570, 610): c.courbe([(347, y), (350, y + 8), (347, y + 16)], "leger")   # pierre usée
    L_(c, 395, 410, 395, 645, "moyen"); L_(c, 407, 405, 407, 643, "fin")           # pilastre blanc
    c.arc(420, 510, 6, 0, 180, "fin"); L_(c, 414, 510, 414, 541, "fin"); L_(c, 426, 510, 426, 541, "fin")   # petite niche
    L_(c, 418, 330, 418, 645, "fin"); L_(c, 407, 643, 480, 645, "moyen")            # le fond de la rue
    c.forme([(395, 648), (402, 641), (412, 643), (416, 652), (408, 657), (398, 656)], "fin")   # sac blanc
    L_(c, 418, 330, 445, 330, "leger")
    rr = random.Random(9)                                                          # le mur de pierre au fond (sans le figuier)
    for _ in range(26):
        x, y = rr.uniform(424, 556), rr.uniform(400, 600)
        if 470 < x < 562 and y > 595: continue
        w, h = rr.uniform(10, 20), rr.uniform(6, 11)
        c.brisee([(x, y), (x + w * 0.55, y - 1), (x + w, y + 1), (x + w + 1, y + h * 0.6), (x + w * 0.6, y + h), (x - 1, y + h * 0.8)], "leger", ferme=True)

    # --- les balcons en fer forgé, en haut
    L_(c, 258, 12, 302, 112, "moyen")                                              # balcon-corbeille
    c.courbe([(300, 0), (326, 30), (340, 70), (332, 102), (304, 114)], "moyen")
    for t in (0.2, 0.4, 0.6, 0.8):
        x0, y0 = 258 + 44 * t, 12 + 100 * t
        c.courbe([(x0, y0), (x0 + 22, y0 - 10), (x0 + 38 - 12 * t, y0 + 4)], "fin")
    for x, y in ((276, 20), (290, 48), (305, 75)): c.volute(x, y, 4, 1.3, 0, 1, "leger")
    L_(c, 339, 62, 339, 248, "moyen"); L_(c, 357, 66, 357, 250, "moyen"); L_(c, 339, 62, 357, 66, "moyen")   # 2e balcon
    c.courbe([(352, 62), (376, 120), (394, 190), (393, 236), (376, 258)], "moyen")
    for t in (0.25, 0.5, 0.75):
        y0 = 70 + 180 * t; c.courbe([(357, y0), (372, y0 + 12), (388 - 4 * (1 - t), y0 + 30)], "fin")
    for y in (110, 150, 195, 230): c.volute(348, y, 5, 1.4, 90, 1 if y % 20 else -1, "fin")
    L_(c, 336, 246, 374, 252, "moyen"); L_(c, 336, 260, 374, 266, "fin"); L_(c, 336, 246, 336, 260, "fin")
    L_(c, 345, 266, 345, 290, "leger"); L_(c, 372, 268, 372, 290, "leger")
    for (ya, yb) in ((42, 192), (262, 320)):                                        # balcons plus loin
        L_(c, 407, ya - 17, 436, ya, "fin"); L_(c, 412, ya, 412, yb, "fin"); L_(c, 434, ya + 4, 434, yb, "fin")
        for y in range(ya + 18, yb, 28): c.volute(423, y, 4, 1.3, 0, 1, "leger")
    L_(c, 400, 0, 400, 330, "fin")                                                 # arête de la façade, au loin

    # --- la lanterne
    L_(c, 448, 107, 466, 107, "moyen"); L_(c, 448, 107, 457, 98, "fin"); L_(c, 466, 107, 457, 98, "fin")
    L_(c, 441, 119, 472, 119, "moyen"); L_(c, 448, 107, 441, 119, "fin"); L_(c, 466, 107, 472, 119, "fin")
    L_(c, 441, 119, 448, 160, "moyen"); L_(c, 472, 119, 465, 160, "moyen"); L_(c, 448, 160, 465, 160, "moyen")
    L_(c, 456, 119, 456, 160, "leger", depasse=False); L_(c, 444, 138, 469, 138, "leger", depasse=False)
    L_(c, 456, 160, 456, 192, "fin"); c.courbe([(456, 172), (444, 176), (430, 186)], "fin"); c.courbe([(456, 192), (444, 192), (428, 188)], "fin")

    # --- la banquette couverte d'un tissu rayé
    c.courbe([(484, 624), (520, 618), (561, 626)], "moyen")                        # haut du dossier
    c.courbe([(484, 624), (480, 650), (480, 672)], "moyen")
    L_(c, 561, 626, 561, 718, "moyen")
    c.courbe([(480, 672), (450, 676), (428, 686)], "moyen")                        # l'assise
    c.courbe([(428, 686), (422, 712), (423, 742)], "moyen")
    c.courbe([(423, 742), (470, 748), (516, 758)], "moyen")                        # bas du tissu
    c.courbe([(516, 758), (540, 742), (561, 718)], "moyen")
    c.courbe([(480, 672), (505, 684), (516, 720), (516, 758)], "fin")
    for y0 in (636, 650, 664): c.courbe([(482, y0), (522, y0 - 4), (560, y0 + 3)], "leger")   # rayures
    for y0 in (696, 712, 728): c.courbe([(425, y0 - 4), (470, y0 + 2), (514, y0 + 12)], "leger")
    for x in range(426, 512, 7): L_(c, x, 742 + (x - 423) * 0.14, x - 1, 748 + (x - 423) * 0.14, "leger", depasse=False)   # franges
    L_(c, 440, 745, 441, 752, "fin", depasse=False); L_(c, 518, 760, 519, 768, "fin", depasse=False)

    # --- façade de droite, toute proche
    L_(c, 579, 150, 579, 776, "moyen"); L_(c, 561, 470, 561, 780, "fort", double=True)
    L_(c, 591, 0, 591, 776, "fort"); L_(c, 651, 0, 651, 774, "fort", double=True); L_(c, 686, 0, 686, 778, "fort")
    L_(c, 604, 40, 604, 760, "leger", depasse=False); L_(c, 626, 300, 626, 760, "leger", depasse=False)
    L_(c, 640, 40, 640, 760, "leger", depasse=False)
    L_(c, 659, 0, 659, 770, "fin", depasse=False); L_(c, 680, 0, 680, 772, "leger", depasse=False)
    L_(c, 700, 0, 700, 790, "fin")
    for y in (420, 520): L_(c, 686, y, 700, y + 2, "leger", depasse=False)
    # les marches en marbre
    L_(c, 561, 780, 651, 796, "moyen"); L_(c, 561, 780, 622, H, "fort"); L_(c, 586, 776, 645, H, "moyen")
    L_(c, 651, 777, 720, 800, "moyen"); L_(c, 640, 790, 720, 880, "moyen"); L_(c, 651, 777, 640, 790, "fin")
    L_(c, 700, 790, 720, 812, "fin")
    # le balcon arrondi en fer forgé
    c.courbe([(557, 154), (579, 154)], "moyen")
    c.courbe([(557, 154), (548, 210), (530, 290), (510, 370), (507, 420), (516, 460), (545, 468), (570, 456), (579, 430)], "moyen")
    L_(c, 579, 154, 579, 430, "moyen")
    c.courbe([(568, 160), (560, 240), (548, 330), (538, 420), (548, 462)], "fin")
    for (x, y, r, s) in ((564, 247, 7, 1), (545, 329, 8, -1), (551, 385, 7, 1), (528, 412, 6, -1), (564, 429, 6, 1), (566, 300, 5, -1)):
        c.volute(x, y, r, 1.5, 0, s, "fin")
    for y in (360, 400, 440): c.courbe([(512, y), (540, y + 6), (578, y)], "leger")

    sol = Crayon(53)
    c.cercle(262, 828, 45, "fin", 11); c.cercle(262, 828, 40, "leger", 9)          # plaque d'égout
    sol_poly = [(0, 960), (0, 772), (106, 764), (231, 716), (407, 646), (480, 646), (480, 660), (423, 690), (423, 745),
                (516, 762), (561, 782), (622, 960)]
    pierres(sol, sol_poly, 648, 7,                                                   # pas de pavé sur la plaque
            garde=lambda x, y, prof: 0 if ((x - 262) / 52) ** 2 + ((y - 828) / 16) ** 2 < 1 else 0.2 + 0.5 * prof)

    lignes = {"ab": "le bord de l'encadrement en zellige", "omis": "la végétation est laissée de côté",
              "titre": "Croquis 2 · la rue aux portes bleues", "pf": "PF : point de fuite, au bout de la rue"}
    return c, sol, sol_poly, A, B, XP, lignes


# ================================================================ construction et page
def construction(A, B, XP):
    k = Crayon(3)
    for i in range(5):                                         # grille de 4 cm
        x = (4*i - X0) * S; L_(k, x, 0, x, H, "construction", depasse=False)
    for j in range(6):
        y = (4*j - Y0) * S; L_(k, 0, y, W, y, "construction", depasse=False)
    xg, xd = -OX / MM + 2, (PAGE_W - OX) / MM - 2
    L_(k, xg, YH, xd, YH, "construction", depasse=False)       # ligne d'horizon
    Cy, Dy = sur(*A, XP), sur(*B, XP)
    for y0 in (Cy, Dy):                                        # fuyantes C→A→PF et D→B→PF
        L_(k, XP, y0, PF[0], PF[1], "construction", depasse=False)
    L_(k, XP, Cy - 12, XP, Dy + 12, "construction", depasse=False)     # A'B'
    L_(k, *A, XP, A[1], "construction", depasse=False, tirets="1.2 1")  # horizontales
    L_(k, *B, XP, B[1], "construction", depasse=False, tirets="1.2 1")
    g = XP < A[0]                                              # A'B' à gauche de AB ?
    dxA, dxP = ((1.2, -2.8) if g else (-2.8, 1.2))
    lab = [(A, "A", (dxA, -1)), (B, "B", (dxA, 3.4)), ((XP, A[1]), "A'", (dxP - (0.8 if g else 0), 3.4)),
           ((XP, B[1]), "B'", (dxP - (0.8 if g else 0), -1)), ((XP, Cy), "C", (dxP, -0.8)), ((XP, Dy), "D", (dxP, 3.4))]
    for (x, y), t, (dx, dy) in lab:
        px, py = P(x, y); k.texte(px + dx, py + dy, t, 3.2, ancre="start")
    px, py = P(*PF); k.out.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="0.55" fill="#7d8fa6" fill-opacity="0.7"/>')
    k.texte(px + 1.2, py - 1.5, "PF", 3.0)
    k.texte(OX + W*MM + 1.2, P(0, YH)[1] - 1, "LH", 3.0)
    for (ya, yb) in ((Cy, A[1]), (B[1], Dy)):
        a, b = P(0, ya)[1], P(0, yb)[1]; x = P(XP, 0)[0] + (-6 if g else 4)
        k.texte(x, (a + b)/2 + 1, f"{abs(yb - ya)*MM/10:.1f} cm".replace(".", ","), 2.6, ancre="end" if g else "start")
    return k


def page(vue, nom, calque=False):
    c, sol, sol_poly, A, B, XP, lg = vue()
    k = construction(A, B, XP)
    t = Crayon(5)
    t.texte(OX, 12, lg["titre"], 6.0, "#1f1f1f", op=1)
    t.texte(OX, 18, "Séance 4 · médina de Tunis · méthode AB → A'B' · grille de 4 cm", 3.6, "#666", op=1)
    etapes = ["1  cadrage, grille de 4 cm", "2  l'arête verticale AB",
              "3  la verticale A'B' et les horizontales",
              "4  C et D relevés au crayon, bras tendu", "5  fuyantes AC et BD → PF sur la LH"]
    for i, e in enumerate(etapes):
        t.texte(PAGE_W - 12, 6.5 + i*3.4, e, 2.8, "#7d8fa6", "end")
    t.texte(OX, PAGE_H - 9, f"LH : ligne d'horizon, à hauteur des yeux · {lg['pf']}", 2.9, "#888", op=1)
    t.texte(OX, PAGE_H - 5, f"A'B' : {lg['ab']} · {lg['omis']}", 2.9, "#888", op=1)
    cadre = Crayon(6)
    co = [(0, 0), (W, 0), (W, H), (0, H)]
    for i in range(4): L_(cadre, *co[i], *co[(i+1) % 4], "moyen")
    clip = f'<clipPath id="fen"><rect x="{OX}" y="{OY}" width="{W*MM}" height="{H*MM}"/></clipPath>'
    sol_clip = (f'<clipPath id="sol"><polygon points="{" ".join(f"{P(x, y)[0]:.2f},{P(x, y)[1]:.2f}" for x, y in sol_poly)}"/></clipPath>')
    photo = (f'<image href="redresse2_{nom}.jpg" x="{OX}" y="{OY}" width="{W*MM}" height="{H*MM}" opacity="0.45" '
             f'preserveAspectRatio="none"/>') if calque else ""
    return (f'<svg viewBox="0 0 {PAGE_W} {PAGE_H}" xmlns="http://www.w3.org/2000/svg"><defs>{clip}{sol_clip}</defs>{photo}'
            f'{"".join(k.out)}<g clip-path="url(#fen)"><g clip-path="url(#sol)">{"".join(sol.out)}</g>{"".join(c.out)}</g>'
            f'{"".join(cadre.out)}{"".join(t.out)}</svg>')


def html(svg, nom):
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Croquis {nom}</title>
<link rel="stylesheet" href="../polices-local.css">
<style>@page {{ size: 210mm 297mm; margin: 0; }} html, body {{ margin: 0; background: #fff; }}
.p {{ width: 210mm; height: 297mm; overflow: hidden; background: #fdfcf8; }} svg {{ width: 100%; height: 100%; display: block; }}</style></head>
<body><div class="p">{svg}</div></body></html>"""


if __name__ == "__main__":
    for nom, vue in (("voute", voute), ("rue", rue)):
        open(f"{ICI}/croquis-4-{nom}.html", "w", encoding="utf-8").write(html(page(vue, nom), nom))
        print(f"croquis-4-{nom}.html écrit")
        if os.environ.get("CALQUE"):
            open(f"{ICI}/calque-{nom}.html", "w", encoding="utf-8").write(html(page(vue, nom, True), nom))

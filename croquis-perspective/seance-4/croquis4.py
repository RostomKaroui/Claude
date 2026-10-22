"""Séance 4 : deux croquis de la médina de Tunis (la voûte, la rue aux portes bleues).

Même méthode que les séances 2 et 3 : grille de 4 cm, arête AB, verticale A'B', horizontales,
C et D relevés au crayon bras tendu, fuyantes AC et BD jusqu'au point de fuite PF sur la LH.
Remarques de la prof : pas de hachures, contours forts, détails fins, construction très légère.
La moto et la végétation sont laissées de côté.

Entrée : redresse_voute.png, redresse_rue.png (cadre 18 x 24 cm, 40 px = 1 cm).
Sortie : croquis-4-voute.html et croquis-4-rue.html (A4).
"""
import math, random, sys
import numpy as np

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

    def arc(self, cx, cy, r, a0, a1, sorte="moyen", ry=None, double=False):
        """arc de cercle (angles en degrés, 0 = droite, 90 = haut), tremblé à la main"""
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


def paves(c, y_debut, y_fin, pas, graine, x_min=0, x_max=W, saut=9):
    """les pavés : des rangs de joints interrompus, plus serrés au fond (1/(y - YH) régulier).
    Ce ne sont pas des hachures : chaque joint est un petit trait court, avec des vides."""
    r = random.Random(graine)
    a0 = 1 / (y_fin - YH); a1 = 1 / (y_debut - YH)
    k = 0; y_av = None
    while True:
        a = a0 + k * pas
        if a > a1: break
        y = YH + 1 / a; k += 1
        if y_av is not None and y_av - y < saut: continue
        ech = (y - YH) / (H - YH)                         # taille des pavés à cette profondeur
        x = x_min + r.uniform(0, 30) * ech
        while x < x_max:
            lg = r.uniform(26, 60) * ech + 4
            dy = r.uniform(-2.5, 2.5) * ech
            L_(c, x, y + dy, min(x_max, x + lg), y + dy + r.uniform(-2, 2) * ech, "leger", depasse=False)
            if y_av is not None and r.random() < 0.4:      # joint de travers entre deux rangs
                xm = x + lg * r.uniform(0.3, 0.9)
                L_(c, xm, y + dy, xm + (xm - PF[0]) * (y_av - y) / (y - YH) * 0.15 + r.uniform(-3, 3) * ech,
                   y_av + 2, "leger", depasse=False)
            x += lg + r.uniform(6, 16) * ech
        y_av = y


# ================================================================ 1. la voûte
def voute():
    regler((335, 615))
    c = Crayon(41)
    A, B, XP = (506, sur(518, 353, 506)), (506, sur(720, 923, 506)), 640

    # --- le bâtiment au fond, au-dessus de la voûte
    rect(c, 200, 9, 306, 169, "moyen")                                             # fenêtre verte
    L_(c, 208, 17, 298, 17, "fin", depasse=False); L_(c, 208, 17, 208, 165, "fin", depasse=False)
    L_(c, 298, 17, 298, 165, "fin", depasse=False); L_(c, 253, 17, 253, 165, "fin")
    L_(c, 208, 100, 298, 100, "fin")
    L_(c, 196, 169, 310, 169, "moyen")                                             # appui
    L_(c, 226, 240, 326, 240, "moyen"); L_(c, 226, 252, 326, 252, "moyen")         # balcon
    L_(c, 226, 240, 226, 252, "moyen"); L_(c, 326, 240, 326, 252, "moyen")
    for x in (240, 262, 290, 312): L_(c, x, 252, x - 2, 262, "fin", depasse=False)
    L_(c, 236, 262, 316, 262, "fin")
    for x0, y0 in ((262, 262), (300, 262)):                                       # consoles
        c.courbe([(x0, y0), (x0 + 4, y0 + 18), (x0 + 1, y0 + 34)], "fin")

    # --- le mur de gauche (fuit vers PF)
    L_(c, 58, 0, 58, 705, "fort", double=True)                                     # l'angle avec la façade
    L_(c, 28, 238, 28, 524, "moyen"); L_(c, 37, 245, 37, 520, "fin")              # cadre bleu d'une porte
    fuyante(c, 28, 238, 37, "moyen")
    rect(c, 0, 580, 20, 950, "fin")                                                # grillage
    L_(c, 10, 580, 10, 950, "leger", depasse=False)
    # bac (on laisse l'arbre de côté)
    L_(c, 55, 705, 134, 705, "fort"); L_(c, 55, 705, 55, 800, "fort"); L_(c, 134, 705, 134, 800, "fort")
    L_(c, 55, 714, 134, 714, "fin", depasse=False); L_(c, 50, 800, 140, 800, "moyen")
    L_(c, 50, 800, 52, 815, "fin"); L_(c, 140, 800, 138, 812, "fin")

    # --- la voûte : arc d'entrée (épais), puis l'arc du fond
    c.arc(243, 540, 166, 0, 180, "fort", double=True)                              # extrados
    c.arc(240, 545, 148, 0, 180, "moyen")                                          # intrados
    L_(c, 77, 540, 77, 705, "fort"); L_(c, 92, 545, 92, 705, "moyen")             # pied gauche
    L_(c, 92, 548, 121, 582, "fin")                                               # naissance de la voûte
    L_(c, 384, 548, 318, 598, "fin")
    c.arc(218, 600, 97, 0, 180, "moyen")                                           # arc du fond
    c.arc(215, 615, 82, 5, 175, "fin")
    L_(c, 315, 600, 315, 740, "moyen"); L_(c, 297, 612, 297, 737, "fin")
    L_(c, 121, 600, 121, 705, "moyen")
    # lanterne suspendue
    L_(c, 211, 400, 211, 414, "fin", depasse=False)
    L_(c, 201, 414, 221, 414, "moyen"); L_(c, 197, 422, 225, 422, "moyen")
    L_(c, 201, 414, 197, 422, "fin", depasse=False); L_(c, 221, 414, 225, 422, "fin", depasse=False)
    L_(c, 197, 422, 204, 462, "moyen"); L_(c, 225, 422, 218, 462, "moyen"); L_(c, 204, 462, 218, 462, "moyen")
    L_(c, 211, 422, 211, 462, "leger", depasse=False); L_(c, 211, 462, 211, 470, "fin", depasse=False)

    # --- au fond, sous l'arc : porte bleue, panneau, compteur
    L_(c, 118, 577, 206, 577, "moyen"); L_(c, 118, 584, 206, 584, "fin")
    L_(c, 134, 584, 134, 732, "moyen"); L_(c, 206, 584, 206, 734, "moyen"); L_(c, 210, 531, 210, 734, "fin")
    L_(c, 162, 586, 162, 732, "fin")
    for xa, xb in ((138, 158), (166, 202)):
        for ya, yb in ((594, 632), (642, 688), (698, 726)):
            rect(c, xa, ya, xb, yb, "leger", depasse=False)
    rect(c, 224, 539, 256, 554, "fin")                                             # plaque de la rue
    rect(c, 246, 674, 265, 706, "fin")                                             # compteur
    L_(c, 279, 577, 279, 734, "fin"); L_(c, 290, 577, 290, 734, "fin")
    L_(c, 121, 737, 315, 740, "moyen")                                             # pied du mur du fond

    # --- colonne, pilastre, encadrement en brique
    L_(c, 362, 540, 418, 540, "moyen"); L_(c, 362, 548, 418, 548, "moyen")         # tailloir
    L_(c, 362, 540, 362, 548, "fin"); L_(c, 418, 540, 418, 548, "fin")
    c.courbe([(368, 548), (372, 558), (379, 563)], "fin"); c.courbe([(412, 548), (408, 558), (408, 563)], "fin")
    L_(c, 379, 563, 379, 724, "fort"); L_(c, 408, 563, 408, 724, "fort")           # fût
    L_(c, 373, 724, 414, 724, "moyen"); L_(c, 371, 738, 416, 738, "moyen")         # base
    L_(c, 373, 724, 371, 738, "fin"); L_(c, 414, 724, 416, 738, "fin")
    L_(c, 418, 532, 458, 532, "moyen"); L_(c, 418, 558, 458, 558, "fin")           # pilastre
    L_(c, 418, 532, 418, 745, "moyen"); L_(c, 458, 532, 458, 745, "moyen")
    rect(c, 423, 600, 453, 742, "leger", depasse=False)                            # son grillage
    L_(c, 462, 125, 462, 745, "fort", double=True)
    L_(c, 462, 125, 506, 132, "moyen")
    c.arc(479, 312, 11, 0, 180, "moyen")
    L_(c, 468, 312, 468, 740, "moyen"); L_(c, 490, 312, 490, 742, "moyen")
    L_(c, 458, 745, 506, 754, "moyen")
    L_(c, 505, 0, 462, sur(505, 0, 462), "fort")                                   # bord du toit en tuiles
    for x in (500, 492, 484, 476, 468):
        y = sur(505, 0, x); L_(c, x, y, x - 9, y - 4, "fin", depasse=False)

    # --- le mur de droite (fuit vers PF)
    fuyante(c, *B, W, "fort", double=True)                                         # pied du mur
    L_(c, A[0], 132, A[0], B[1], "fort", double=True)                              # l'arête AB
    quad_mur(c, 518, 531, 353, 437, "moyen")                                       # petite fenêtre
    for x in (522, 527): L_(c, x, sur(518, 353, x) + 3, x, sur(518, 437, x) - 3, "fin", depasse=False)
    quad_mur(c, 527, 537, 649, 696, "fin")                                         # petite trappe
    yb = sur(509, 700, 601)                                                        # niche en arc
    L_(c, 601, 300, 601, yb, "fort"); L_(c, XP, 300, XP, sur(601, yb, XP), "fort")
    c.courbe([(601, 300), (606, 280), (620, 272), (634, 280), (XP, 300)], "fort")
    fuyante(c, 601, yb, XP, "moyen")
    L_(c, 607, 305, 607, yb - 3, "leger", depasse=False)
    quad_mur(c, 702, W, 225, 338, "moyen")                                         # fenêtre à grille
    for i in range(3):
        x = 706 + i * 6; c.courbe([(x, sur(702, 225, x) + 8), (x + 4, sur(702, 280, x)), (x, sur(702, 338, x) - 8)], "fin")

    # --- un personnage assis (pour l'échelle)
    c.cercle(379, 690, 8, "moyen")
    c.courbe([(371, 703), (366, 722), (370, 746)], "moyen"); c.courbe([(386, 700), (396, 718), (394, 746)], "moyen")
    c.courbe([(370, 712), (360, 730), (372, 734)], "fin")
    c.courbe([(370, 746), (348, 750), (326, 752)], "moyen"); c.courbe([(394, 746), (360, 758), (330, 759)], "moyen")
    L_(c, 326, 752, 322, 760, "fin", depasse=False)

    # --- le sol en pavés
    sol = Crayon(43)
    paves(sol, 748, H, 0.00045, 5)
    sol_poly = [(0, 960), (0, 900), (20, 880), (50, 815), (140, 812), (140, 740), (318, 742), (370, 748), (509, 755), (W, sur(509, 755, W)), (W, H)]

    lignes = {"ab": "le bord de la niche", "omis": "la moto et la végétation sont laissées de côté", "titre": "Croquis 1 · la voûte",
              "pf": "PF : point de fuite, au fond sous la voûte"}
    return c, sol, sol_poly, A, B, XP, lignes


# ================================================================ 2. la rue aux portes bleues
def rue():
    regler((528, 570))
    c = Crayon(51)
    A, B, XP = (346, 448), (346, 660), 232

    # --- façade de gauche (fuit vers PF)
    quad_mur(c, 12, 80, 14, 228, "fort")                                           # fenêtre à grille bleue
    for x in (30, 48, 64):
        c.courbe([(x, sur(12, 14, x) + 8), (x + 5, sur(12, 80, x)), (x - 4, sur(12, 140, x)), (x + 3, sur(12, 220, x) - 6)], "fin")
    c.cercle(40, sur(12, 60, 40), 8, "fin"); c.cercle(56, sur(12, 165, 56), 7, "fin")
    fuyante(c, 8, 234, 88, "moyen"); fuyante(c, 8, 246, 88, "fin"); L_(c, 8, 234, 8, 246, "fin")   # appui

    # l'auvent au-dessus de la porte
    L_(c, 99, 54, 180, 44, "moyen"); L_(c, 104, 64, 180, 58, "fin"); L_(c, 99, 54, 104, 64, "fin")
    L_(c, 180, 44, 297, 196, "fort", double=True)                                  # rive avec les tuiles
    L_(c, 180, 58, 297, 216, "moyen")
    L_(c, 107, 72, 230, 219, "fort")                                               # contre le mur
    L_(c, 230, 219, 297, 216, "moyen"); L_(c, 297, 196, 297, 216, "moyen")
    for i in range(11):                                                            # tuiles rondes, en écailles
        t = (i + 0.5) / 11; x, y = 180 + 117 * t, 44 + 152 * t
        c.arc(x, y, 6, -52, 128, "fin")
    # l'encadrement en zellige et la porte
    L_(c, 106, 72, 106, 762, "fort", double=True); L_(c, 232, 219, 232, 716, "fort", double=True)
    L_(c, 113, 80, 113, 755, "leger", depasse=False); L_(c, 226, 226, 226, 712, "leger", depasse=False)
    L_(c, 129, 150, 129, 703, "moyen"); fuyante(c, 129, 150, 184, "moyen")
    L_(c, 184, sur(129, 150, 184), 184, sur(129, 703, 184), "moyen")
    fuyante(c, 129, 298, 184, "moyen")                                             # haut de la porte
    quad_mur(c, 150, 168, 330, 520, "fin"); quad_mur(c, 150, 168, 580, 672, "fin")  # panneaux
    c.cercle(165, sur(150, 552, 165), 4, "fin")
    fuyante(c, 120, 704, 218, "moyen"); fuyante(c, 106, 718, 226, "fin")           # seuil en marbre
    L_(c, 106, 762, 232, 716, "fort")
    # descente, applique, plinthe, barres bleues
    c.courbe([(232, 238), (244, 244), (247, 262)], "moyen"); L_(c, 247, 262, 247, 298, "moyen")
    rect(c, 240, 298, 254, 312, "moyen"); L_(c, 252, 312, 255, 560, "fin")
    L_(c, 0, 594, 106, 614, "fin"); fuyante(c, 232, 594, 345, "fin")
    rect(c, 81, 580, 93, 759, "moyen"); rect(c, 254, 569, 261, 676, "moyen"); rect(c, 238, 609, 249, 655, "fin")
    L_(c, 4, 647, 68, 641, "moyen"); L_(c, 68, 641, 68, 734, "moyen"); L_(c, 68, 734, 4, 736, "moyen"); L_(c, 4, 736, 4, 647, "moyen")
    # fenêtre à grille du rez-de-chaussée
    quad_mur(c, 287, 323, 419, 557, "fort")
    for i in range(1, 4):
        x = 287 + 9 * i; L_(c, x, sur(287, 419, x) + 2, x, sur(287, 557, x) - 2, "fin", depasse=False)
    for j in range(1, 6):
        fuyante(c, 289, 419 + 23 * j, 321, "fin", depasse=False)
    # porte en arc et son encadrement en pierre
    L_(c, A[0], A[1] + 20, A[0], B[1], "fort")
    c.arc(369, 471, 23, 0, 180, "moyen"); L_(c, 392, 471, 392, 666, "moyen")
    c.arc(368.5, 476, 13.5, 0, 180, "moyen"); L_(c, 355, 476, 355, 637, "moyen"); L_(c, 382, 476, 382, 637, "moyen")
    L_(c, 355, 637, 382, 637, "fin")
    L_(c, 340, 650, 398, 652, "fin")
    L_(c, 400, 425, 400, 640, "moyen"); L_(c, 414, 420, 414, 638, "fin"); L_(c, 400, 425, 414, 420, "fin")
    # les balcons en fer forgé, en haut
    c.courbe([(262, 0), (272, 50), (290, 108)], "moyen"); c.courbe([(305, 0), (334, 55), (318, 112)], "moyen")
    c.courbe([(290, 108), (305, 116), (318, 112)], "moyen")
    for x in (280, 298): c.courbe([(x, 4), (x + 12, 50), (x + 10, 100)], "fin")
    L_(c, 340, 62, 340, 244, "moyen"); L_(c, 364, 74, 364, 248, "moyen")
    c.courbe([(352, 0), (376, 95), (396, 200), (392, 238), (366, 248)], "moyen")
    for y in (110, 160, 210): c.cercle(358, y, 6, "fin")
    fuyante(c, 336, 248, 372, "moyen"); fuyante(c, 336, 262, 372, "fin"); L_(c, 336, 248, 336, 262, "fin")
    for ya, yb in ((30, 150), (230, 310), (360, 470)):
        rect(c, 405, ya, 425, yb, "fin")
    # la lanterne
    L_(c, 446, 107, 468, 107, "moyen"); L_(c, 446, 107, 457, 99, "fin"); L_(c, 468, 107, 457, 99, "fin")
    L_(c, 440, 120, 473, 120, "moyen"); L_(c, 446, 107, 440, 120, "fin"); L_(c, 468, 107, 473, 120, "fin")
    L_(c, 440, 120, 447, 160, "moyen"); L_(c, 473, 120, 466, 160, "moyen"); L_(c, 447, 160, 466, 160, "moyen")
    L_(c, 457, 160, 457, 192, "fin"); c.courbe([(457, 192), (442, 192), (428, 186)], "fin")

    # --- au fond
    L_(c, 418, 330, 418, 640, "fin"); L_(c, 418, 640, 470, 640, "moyen")

    # --- la banquette couverte d'un tissu rayé
    c.courbe([(483, 612), (520, 606), (560, 612)], "moyen")                        # haut du dossier
    c.courbe([(483, 612), (474, 650), (470, 690)], "moyen")
    L_(c, 560, 612, 562, 735, "moyen")
    c.courbe([(470, 690), (440, 696), (423, 708)], "moyen")                        # l'assise
    c.courbe([(423, 708), (420, 725), (424, 740)], "moyen")
    c.courbe([(424, 740), (470, 748), (525, 760)], "moyen")                        # bas du tissu
    c.courbe([(525, 760), (545, 748), (562, 735)], "moyen")
    c.courbe([(470, 690), (500, 698), (526, 712), (525, 760)], "fin")
    for y0 in (640, 668): c.courbe([(480, y0), (520, y0 - 3), (558, y0 + 2)], "leger")
    for y0 in (716, 730): c.courbe([(426, y0), (470, y0 + 6), (522, y0 + 14)], "leger")
    L_(c, 440, 740, 441, 750, "fin", depasse=False); L_(c, 522, 760, 523, 770, "fin", depasse=False)

    # --- façade de droite (très proche, elle fuit vite)
    L_(c, 560, 470, 560, 776, "fort", double=True)
    L_(c, 587, 0, 587, 776, "fort"); L_(c, 653, 0, 653, 774, "fort", double=True); L_(c, 687, 0, 687, 776, "fort")
    L_(c, 600, 300, 600, 760, "leger", depasse=False); L_(c, 640, 300, 640, 760, "leger", depasse=False)
    L_(c, 661, 0, 661, 772, "fin", depasse=False)
    L_(c, 700, 0, 700, 790, "fin")
    # les marches en marbre
    L_(c, 558, 776, 690, 806, "moyen"); L_(c, 558, 776, 600, H, "fort"); L_(c, 578, 782, 628, H, "moyen")
    L_(c, 638, 806, 720, 925, "moyen"); L_(c, 653, 774, 720, 786, "fin")
    # le balcon arrondi en fer forgé
    c.courbe([(575, 160), (580, 300), (580, 420), (566, 470), (530, 474), (507, 430), (512, 350), (540, 260), (566, 190), (575, 160)], "moyen")
    for (x, y, r) in ((548, 330, 9), (556, 400, 11), (532, 430, 8)): c.cercle(x, y, r, "fin")
    c.courbe([(565, 200), (552, 300), (545, 380), (546, 460)], "fin")

    sol = Crayon(53)
    c.cercle(262, 828, 45, "fin", 11)                                              # plaque d'égout
    paves(sol, 652, H, 0.00055, 7, saut=10)
    sol_poly = [(0, 960), (0, 772), (106, 764), (232, 718), (418, 642), (430, 645), (420, 742), (525, 764), (558, 778), (600, 960)]

    lignes = {"ab": "le bord de l'encadrement en zellige", "omis": "la végétation est laissée de côté", "titre": "Croquis 2 · la rue aux portes bleues",
              "pf": "PF : point de fuite, au bout de la rue"}
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


def page(vue):
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
    return (f'<svg viewBox="0 0 {PAGE_W} {PAGE_H}" xmlns="http://www.w3.org/2000/svg"><defs>{clip}{sol_clip}</defs>'
            f'{"".join(k.out)}<g clip-path="url(#fen)"><g clip-path="url(#sol)">{"".join(sol.out)}</g>{"".join(c.out)}</g>'
            f'{"".join(cadre.out)}{"".join(t.out)}</svg>')


if __name__ == "__main__":
    for nom, vue in (("voute", voute), ("rue", rue)):
        html = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Croquis {nom}</title>
<link rel="stylesheet" href="../polices-local.css">
<style>@page {{ size: 210mm 297mm; margin: 0; }} html, body {{ margin: 0; background: #fff; }}
.p {{ width: 210mm; height: 297mm; overflow: hidden; background: #fdfcf8; }} svg {{ width: 100%; height: 100%; display: block; }}</style></head>
<body><div class="p">{page(vue)}</div></body></html>"""
        open(f"{ICI}/croquis-4-{nom}.html", "w", encoding="utf-8").write(html)
        print(f"croquis-4-{nom}.html écrit")

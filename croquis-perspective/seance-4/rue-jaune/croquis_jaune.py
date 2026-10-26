"""Croquis de la rue aux portes jaunes (médina de Tunis), relevé fidèlement sur la photo, comme un filtre.

Sans les personnes, sans la végétation, sans le sac poubelle. On garde l'architecture à sa place exacte :
portes cloutées (les clous sont relevés un par un sur la photo), moucharabiehs, lanterne, câbles, pavés.
Construction : A, B, A', B', C, D, horizontales et fuyantes, en très léger.
Le point de fuite (vers x = 1320 px, hors du cadre) n'apparaît pas : les fuyantes s'arrêtent au bord du cadre.

Entrée : redresse_jaune.png / redresse2_jaune.jpg (cadre 18 x 24 cm, 40 px = 1 cm).
Sortie : croquis-jaune.html (A4) ; avec CALQUE=1, aussi calque-jaune.html (dessin posé sur la photo).
"""
import math, os, random, sys
import cv2
import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(ICI))
import croquis4 as k4                         # le crayon, les traits et les fuyantes de la séance 4
import releve
from croquis4 import L_, P, Crayon, fuyante, rect, quad_mur

W, H, MM = k4.W, k4.H, k4.MM
OX, OY = k4.OX, k4.OY
k4.regler((1320, 706))
PF, YH = k4.PF, k4.YH
sur = k4.sur


def base(x):
    """pied de la façade (le sol contre le mur, au nu de la façade)"""
    return sur(206, 813, x)


PF2 = (-300, 706)       # point de fuite des lignes perpendiculaires à la façade (embrasures, saillies) : hors du cadre, à gauche


def vers(p, t):
    """le point p enfoncé dans le mur (vers PF2) de la fraction t"""
    return (p[0] + t * (PF2[0] - p[0]), p[1] + t * (PF2[1] - p[1]))


def devant(p, t):
    """le point p avancé vers la rue (à l'opposé de PF2) ; inverse de vers()"""
    return ((p[0] - t * PF2[0]) / (1 - t), (p[1] - t * PF2[1]) / (1 - t))


def embrasure(c, xbL, xbR, xfR, ytb, ybb, xfL=None):
    """porte au fond d'une embrasure : la porte (le fond) va de xbL à xbR, le nu de la façade est en xfR à droite.
    On voit le tableau de droite (éclairé) et le dessous du linteau ; le tableau de gauche est caché.
    Renvoie la profondeur t."""
    t = (xfR - xbR) / (xfR - PF2[0])
    BRt, BRb = (xbR, sur(xbL, ytb, xbR)), (xbR, sur(xbL, ybb, xbR))
    FRt, FRb = devant(BRt, t), devant(BRb, t)
    xfL = xbL if xfL is None else xfL
    ytf = lambda x: sur(*FRt, x)
    fuyante(c, xfL, ytf(xfL), FRt[0], "fort")                                      # arête du linteau
    L_(c, xfL, ytf(xfL), xfL, sur(*FRb, xfL), "fort")                              # tableau gauche (vu par la tranche)
    L_(c, *FRt, *FRb, "fort", double=True)                                         # arête du tableau droit
    L_(c, *FRt, *BRt, "moyen"); L_(c, *FRb, *BRb, "moyen")                         # profondeur du tableau droit
    return t


def paves(c, poly, y_fond, graine, pas=1.55e-4, larg=(0.075, 0.13)):
    """les pavés en rangs parallèles à la façade (les rangs fuient vers PF), plus serrés au fond"""
    r = random.Random(graine)
    pp = np.array(poly, np.float32)
    rang = lambda y0, x: y0 + (YH - y0) * x / PF[0]            # le rang qui passe par (0, y0) et PF
    y0 = H + 40
    while True:
        y1 = YH + 1 / (1 / (y0 - YH) + pas)
        if rang(y1, W) < y_fond and rang(y1, 0) < y_fond: break
        x = -r.uniform(0, 20)
        while x < W + 10:
            yb, yt = rang(y0, x), rang(y1, x); h = yb - yt
            w = (yb - YH) * r.uniform(*larg)
            if h >= 2.6:
                g = max(0.8, 0.14 * h); cx = x + w / 2
                cy = (rang(y0, cx) + rang(y1, cx)) / 2 + r.uniform(-0.1, 0.1) * h
                prof = (yb - YH) / (H - YH)
                if cv2.pointPolygonTest(pp, (cx, cy), False) > 0 and r.random() < 0.25 + 0.55 * prof:
                    a, b = w / 2 - g, (h / 2 - g) * r.uniform(0.75, 1.0)
                    pente = (YH - cy) / (PF[0] - cx)
                    pts = []
                    for ux, uy in ((-1, -0.75), (r.uniform(-0.5, 0.3), -1.1), (0.92, -0.95), (1.06, r.uniform(-0.2, 0.4)),
                                   (0.85, 1.0), (r.uniform(-0.4, 0.2), 1.08), (-1.04, 0.8)):
                        px = cx + ux * a * r.uniform(0.9, 1.05)
                        pts.append((px, cy + uy * b + pente * (px - cx) + r.uniform(-0.15, 0.15) * b))
                    sorte = "leger" if r.random() < 0.75 else "fin"
                    if r.random() < 0.4:
                        k0 = r.randrange(len(pts)); pts = pts[k0:] + pts[:k0]
                        c.brisee(pts[:-r.randint(1, 3)], sorte)
                    else:
                        c.brisee(pts, sorte, ferme=True)
            x += w
        y0 = y1


def clou(c, x, y):
    px, py = P(x, y)
    c.out.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="0.28" fill="#2e2e2e" fill-opacity="0.75"/>')


def rangees(c, x1, x2, yt, yb, cols, ligs, pas=4.6):
    """les rangées de clous d'un battant : verticales aux abscisses cols, horizontales (fuyantes) aux hauteurs ligs"""
    for x in cols:
        y0, y1 = sur(x1, yt, x) + 3, sur(x1, yb, x) - 3
        for t in np.arange(y0, y1 + 0.1, pas): clou(c, x, t)
    for y in ligs:
        for x in np.arange(x1 + 3, x2 - 2, pas): clou(c, x, sur(x1, y, x))


def etoile(c, cx, cy, rx, ry, pas=4.6):
    """étoile de clous : quatre branches (verticale, horizontale, deux diagonales) autour du centre"""
    clou(c, cx, cy)
    for dx, dy in ((0, 1), (1, 0), (1, 1), (1, -1)):
        L = math.hypot(dx * rx, dy * ry); n = int(L / pas)
        for i in range(1, n + 1):
            t = i / n
            clou(c, cx + dx * rx * t, cy + dy * ry * t); clou(c, cx - dx * rx * t, cy - dy * ry * t)


def clous(c, hi, boites, seuil=22):
    """les clous des motifs (étoiles, croix) : petits points sombres relevés sur la photo (black-hat), dans les boîtes données"""
    g = cv2.cvtColor(hi, cv2.COLOR_BGR2GRAY)
    bh = cv2.morphologyEx(g, cv2.MORPH_BLACKHAT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    zone = releve.masque_poly([[(a, b), (cc, b), (cc, d), (a, d)] for a, b, cc, d in boites])
    zone &= ~releve.vert(hi)
    z2 = cv2.resize(zone, (g.shape[1], g.shape[0]), interpolation=cv2.INTER_NEAREST)
    th = ((bh > seuil) & (z2 > 0)).astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(th)
    pts = np.array([(cen[i][0] / 2, cen[i][1] / 2) for i in range(1, n) if 3 <= st[i, 4] <= 45 and max(st[i, 2], st[i, 3]) <= 9])
    if len(pts):                      # un clou fait partie d'une rangée : au moins 2 voisins proches, mais pas un amas (feuillage)
        d = np.hypot(*(pts[:, None, :] - pts[None, :, :]).transpose(2, 0, 1))
        proches, amas = (d < 6.5).sum(1) - 1, (d < 5).sum(1) - 1
        pts = pts[(proches >= 2) & (amas <= 3)]
    for x, y in pts: clou(c, x, y)
    return len(pts)


def moucharabieh(c, x1, x2, yt, yb, n=4, sorte="leger", saillie=0.013):
    """moucharabieh : un caisson en bois qui avance sur la rue. La face avant (x1..x2, yt..yb) porte la grille en losanges ;
    on voit aussi son côté gauche et son dessous, jusqu'au mur (vers PF2)."""
    quad_mur(c, x1, x2, yt, yb, "moyen")
    quad_mur(c, x1 + 2.5, x2 - 2.5, yt + 3, yb - 3, "fin", depasse=False)
    pas = (x2 - x1 - 5) / n; y = yt + 3 + pas * 0.6
    while y < yb - 3 - pas * 0.3:
        for i in range(n):
            cx = x1 + 2.5 + pas * (i + 0.5); cy = sur(x1, y, cx); d = pas * 0.38
            c.brisee([(cx, cy - d), (cx + d, cy), (cx, cy + d), (cx - d, cy)], sorte, ferme=True)
        y += pas * 0.95
    TL, BL, BR = (x1, yt), (x1, yb), (x2, sur(x1, yb, x2))                        # le caisson jusqu'au mur
    mTL, mBL, mBR = vers(TL, saillie), vers(BL, saillie), vers(BR, saillie)
    L_(c, *TL, *mTL, "fin"); L_(c, *BL, *mBL, "moyen"); L_(c, *BR, *mBR, "fin")
    L_(c, *mTL, *mBL, "fin"); L_(c, *mBL, *mBR, "fin")


def fenetre(c, x1, x2, yt, yb, prof=0.012):
    """fenêtre haute à barreaux : grille au nu du mur, vitrage au fond (tableau droit et linteau visibles), appui en saillie"""
    quad_mur(c, x1, x2, yt, yb, "moyen")
    for x in np.linspace(x1 + 4, x2 - 4, 3): L_(c, x, sur(x1, yt, x) + 3, x, sur(x1, yb, x) - 3, "fin", depasse=False)
    for y in (yt + 46, yt + 96): fuyante(c, x1 + 1, y, x2 - 1, "leger", depasse=False)
    TR, BR = (x2, sur(x1, yt, x2)), (x2, sur(x1, yb, x2))
    bTR, bBR = vers(TR, prof), vers(BR, prof)
    L_(c, *TR, *bTR, "fin"); L_(c, *bTR, *bBR, "leger"); L_(c, *BR, *bBR, "fin")
    fuyante(c, x1, sur(*bTR, x1), bTR[0], "leger", depasse=False)
    a1, a2 = (x1 - 4, sur(x1, yb, x1 - 4) + 4), (x2 + 4, sur(x1, yb, x2 + 4) + 4)  # appui : dalle qui avance
    f1, f2 = devant(a1, 0.02), devant(a2, 0.02)
    L_(c, *a1, *a2, "fin"); L_(c, *f1, *f2, "moyen"); L_(c, f1[0], f1[1] + 4, f2[0], f2[1] + 4, "fin")
    L_(c, *a1, *f1, "fin"); L_(c, *f1, f1[0], f1[1] + 4, "fin"); L_(c, *f2, f2[0], f2[1] + 4, "fin")


def seuil(c, x1, x2, s=0.025, h=5):
    """marche de seuil en pierre devant une porte : elle avance sur la rue"""
    b1, b2 = (x1, base(x1)), (x2, base(x2))
    f1, f2 = devant(b1, s), devant(b2, s)
    L_(c, *f1, *f2, "moyen"); L_(c, f1[0], f1[1] + h, f2[0], f2[1] + h, "fin")
    L_(c, *b1, *f1, "fin"); L_(c, *f1, f1[0], f1[1] + h, "fin"); L_(c, *f2, f2[0], f2[1] + h, "fin")


def jaune():
    hi = cv2.imread(f"{ICI}/redresse2_jaune.jpg")
    c = Crayon(61)
    A = (497, 540); B = (497, base(497)); XP = 41

    # --- la façade (fuit doucement vers la droite) et son soubassement
    fuyante(c, 0, base(0), 646, "fort", double=True)                               # pied de la façade
    L_(c, 646, 0, 646, base(646), "fort", double=True)                             # bout de la façade, sur le ciel
    for x1, x2 in ((0, 37), (206, 269), (373, 408), (485, 500), (556, 575), (624, 646)):
        fuyante(c, x1, base(x1) - 14, x2, "leger", depasse=False)

    # porte 1 : grande porte cloutée à deux battants, au fond d'une embrasure profonde
    embrasure(c, 37, 170, 206, 470, 817)
    quad_mur(c, 37, 170, 470, 817, "moyen")
    quad_mur(c, 41, 166, 476, 811, "fin", depasse=False)
    L_(c, 86, sur(37, 476, 86), 86, sur(37, 811, 86), "moyen")                     # battants
    L_(c, 107, sur(37, 476, 107), 107, sur(37, 811, 107), "moyen")
    L_(c, 160, sur(37, 476, 160), 160, sur(37, 811, 160), "fin")
    for y in (556, 700): fuyante(c, 41, y, 86, "leger", depasse=False); fuyante(c, 107, y, 160, "leger", depasse=False)
    fuyante(c, 37, 817, 170, "moyen")                                              # le bas de la porte, au fond
    rangees(c, 41, 86, 476, 811, (44, 83), (480, 556, 700, 806))
    rangees(c, 107, 166, 476, 811, (110, 157), (480, 556, 700, 806))
    n1 = clous(c, hi, [(115, 720, 152, 800)])
    seuil(c, 30, 206)

    # porte 2 : cloutée, étoile de clous, applique ; embrasure moins profonde
    embrasure(c, 269, 336, 373, 533, 797)
    quad_mur(c, 269, 336, 533, 797, "moyen")
    quad_mur(c, 273, 332, 538, 793, "fin", depasse=False)
    L_(c, 287, sur(269, 538, 287), 287, sur(269, 793, 287), "leger", depasse=False)
    fuyante(c, 273, 572, 332, "fin", depasse=False); fuyante(c, 273, 712, 332, "fin", depasse=False)
    c.cercle(311, 579, 6, "fin"); L_(c, 311, 566, 311, 573, "fin", depasse=False)       # anneau / applique
    c.courbe([(305, 586), (311, 592), (317, 586)], "leger")
    rangees(c, 273, 332, 538, 793, (276, 287, 329), (541, 572, 712, 790))
    etoile(c, 309, sur(269, 650, 309), 13, 36)
    n2 = clous(c, hi, [(292, 720, 326, 785)])
    seuil(c, 262, 373)

    # le porche profond : linteau, plafond, mur de droite éclairé (avec l'interphone), porte jaune au fond
    tp = (485 - 451) / (485 - PF2[0])
    FRt, FRb = (485, 506), (485, base(485))
    BRt, BRb = vers(FRt, tp), vers(FRb, tp)
    fuyante(c, 408, sur(*FRt, 408), 485, "fort")                                    # arête du linteau
    L_(c, 408, sur(*FRt, 408), 408, base(408), "fort", double=True)                # tableau gauche
    L_(c, *FRt, *FRb, "fort", double=True)
    L_(c, *FRt, *BRt, "moyen"); L_(c, *FRb, *BRb, "moyen"); L_(c, *BRt, *BRb, "moyen")
    fuyante(c, 408, sur(*BRt, 408), BRt[0], "fin")                                 # le fond du plafond
    fuyante(c, 408, sur(*BRb, 408), BRb[0], "fin")                                 # le fond du sol
    quad_mur(c, 440, 454, sur(*BRt, 440) + 4, sur(*BRb, 440), "moyen")            # porte jaune du fond
    rangees(c, 440, 454, sur(*BRt, 440) + 4, sur(*BRb, 440), (442, 452), (600, 680))
    m = [(461, 605), (471, 609), (471, 626), (461, 622)]                          # interphone, sur le mur du porche
    c.brisee(m, "fin", ferme=True)

    # porte 3 : jaune et cloutée, sous un linteau en saillie ; le pilier entre le porche et la porte 3 porte l'arête AB
    L_(c, A[0], A[1], A[0], B[1], "fort", double=True)                             # l'arête AB
    quad_mur(c, 497, 556, 538, 553, "moyen")                                       # linteau
    l1, l2 = vers((497, 553), 0.02), vers((556, sur(497, 553, 556)), 0.02)
    L_(c, 497, 553, *l1, "fin"); L_(c, *l1, *l2, "leger", depasse=False)
    embrasure(c, 500, 526, 556, 556, 765, xfL=500)
    quad_mur(c, 500, 526, 556, 765, "moyen")
    L_(c, 513, sur(500, 556, 513), 513, sur(500, 765, 513), "leger", depasse=False)
    rangees(c, 500, 526, 556, 765, (503, 523), (559, 650, 762))
    etoile(c, 513, sur(500, 650, 513), 7, 30); n3 = 0

    # porte 4 (ouverte, l'intérieur dans l'ombre) sous le second moucharabieh
    quad_mur(c, 572, 627, 556, 565, "moyen")
    L_(c, 575, 565, 575, base(575), "fort"); L_(c, 624, sur(575, 565, 624), 624, base(624), "fort")
    q1, q2 = vers((624, sur(575, 565, 624)), 0.03), vers((624, base(624)), 0.03)
    L_(c, 624, sur(575, 565, 624), *q1, "moyen"); L_(c, 624, base(624), *q2, "moyen"); L_(c, *q1, *q2, "fin")
    fuyante(c, 575, sur(*q1, 575), q1[0], "fin")

    # moucharabiehs (caissons en saillie) et fenêtres hautes à barreaux (en retrait)
    moucharabieh(c, 496, 559, 464, 518, 6)
    moucharabieh(c, 579, 626, 480, 533, 5)
    moucharabieh(c, 586, 621, 252, 392, 4)
    moucharabieh(c, 592, 624, 25, 108, 4)
    moucharabieh(c, 516, 548, 256, 296, 4)
    moucharabieh(c, 462, 492, 17, 47, 3)
    fenetre(c, 415, 434, 254, 398); fenetre(c, 458, 478, 256, 398)
    L_(c, 441, 0, 441, 120, "fin")                                                 # retrait de la façade, en haut

    # la lanterne : une lanterne carrée (face avant + côté gauche), toit en pointe, sur sa potence
    fa = [(566, 250), (591, 252)]                                                  # haut de la face avant
    ga = vers(fa[0], 0.006)                                                        # coin arrière gauche
    fb = [(571, 292), (587, 293)]; gb = vers(fb[0], 0.005)
    sommet = (575, 230)
    sil = [sommet, fa[1], fb[1], fb[0], gb, ga]                                    # la lanterne cache la grille derrière
    c.out.append('<polygon points="' + " ".join(f"{P(*p)[0]:.2f},{P(*p)[1]:.2f}" for p in sil) + '" fill="#fdfcf8"/>')
    L_(c, *fa[0], *fa[1], "moyen"); L_(c, *fa[0], *ga, "moyen")
    L_(c, *fa[0], *fb[0], "moyen"); L_(c, *fa[1], *fb[1], "moyen"); L_(c, *ga, *gb, "moyen")
    L_(c, *fb[0], *fb[1], "moyen"); L_(c, *fb[0], *gb, "moyen")
    L_(c, (fa[0][0] + fb[0][0]) / 2, 271, (fa[1][0] + fb[1][0]) / 2, 272, "leger", depasse=False)
    for p in (fa[0], fa[1], ga): L_(c, *sommet, *p, "fin")
    L_(c, 575, 230, 575, 225, "fin", depasse=False)
    L_(c, 579, 293, 579, 330, "fin"); c.courbe([(579, 305), (590, 314), (596, 330)], "fin")   # potence
    L_(c, 572, 330, 600, 334, "fin"); L_(c, 572, 330, *vers((572, 330), 0.03), "fin")

    # les câbles tendus en travers
    c.courbe([(668, 152), (560, 168), (430, 186), (290, 205)], "fin")
    c.courbe([(668, 162), (580, 186), (470, 204), (330, 222)], "fin")
    c.courbe([(668, 206), (610, 214), (540, 226)], "leger")
    c.courbe([(655, 230), (620, 250), (600, 262)], "leger")

    # au fond, entre la façade et le mur de droite
    L_(c, 646, 386, 668, 384, "leger"); L_(c, 646, 450, 668, 448, "leger")

    # --- le mur de droite, tout proche : son nu, l'encadrement jaune en saillie (avec son épaisseur) et les gonds
    L_(c, 668, 0, 668, H, "fort", double=True)
    L_(c, 692, 232, 692, H, "fin"); L_(c, 699, 228, 699, H, "fort"); L_(c, 718, 222, 718, H, "moyen")
    L_(c, 692, 232, 699, 228, "fin"); L_(c, 699, 228, 718, 222, "moyen")
    for ya, yb in ((231, 262), (536, 555), (705, 720), (795, 825)):                  # gonds
        rect(c, 699, ya, 711, yb, "fin"); L_(c, 699, ya, 695, ya + 2, "leger", depasse=False); L_(c, 699, yb, 695, yb + 2, "leger", depasse=False)
    for x in (674, 681, 688): c.courbe([(x, 0), (x + 3, 90), (x - 2, 180), (x + 2, 260)], "leger")   # câbles sur le mur

    # --- le sol en pavés
    sol = Crayon(63)
    sol_poly = [(0, base(0) + 6), (646, base(646) + 4), (668, base(646) + 3), (668, H), (0, H)]
    paves(sol, sol_poly, base(646), 7)
    return c, sol, sol_poly, A, B, XP, (n1, n2, n3)


def construction(A, B, XP):
    """A, B, A', B', C, D, horizontales et fuyantes, très légères ; pas de point de fuite"""
    k = Crayon(3)
    Cy, Dy = sur(*A, XP), sur(*B, XP)
    for y0 in (Cy, Dy):                                        # fuyantes C→A et D→B, arrêtées au bord du cadre
        L_(k, XP, y0, W, sur(XP, y0, W), "construction", depasse=False)
    L_(k, XP, Cy - 12, XP, Dy + 12, "construction", depasse=False)     # A'B'
    L_(k, *A, XP, A[1], "construction", depasse=False, tirets="1.2 1")  # horizontales
    L_(k, *B, XP, B[1], "construction", depasse=False, tirets="1.2 1")
    for (x, y), t, (dx, dy) in [(A, "A", (1.2, -1)), (B, "B", (1.2, 3.4)), ((XP, A[1]), "A'", (-3.6, 3.4)),
                                ((XP, B[1]), "B'", (-3.6, -1)), ((XP, Cy), "C", (-2.8, -0.8)), ((XP, Dy), "D", (-2.8, 3.4))]:
        px, py = P(x, y); k.texte(px + dx, py + dy, t, 3.2)
    return k


def page(calque=False):
    c, sol, sol_poly, A, B, XP, n = jaune()
    print("clous relevés :", n)
    k = construction(A, B, XP)
    t = Crayon(5)
    t.texte(OX, 12, "Croquis · la rue aux portes jaunes", 6.0, "#1f1f1f", op=1)
    t.texte(OX, 18, "médina de Tunis · relevé fidèle de la photo · A, B → A', B' et fuyantes", 3.6, "#666", op=1)
    t.texte(OX, k4.PAGE_H - 5, "sans les personnes ni la végétation · le point de fuite est hors du cadre", 2.9, "#888", op=1)
    cadre = Crayon(6)
    co = [(0, 0), (W, 0), (W, H), (0, H)]
    for i in range(4): L_(cadre, *co[i], *co[(i + 1) % 4], "moyen")
    clip = f'<clipPath id="fen"><rect x="{OX}" y="{OY}" width="{W*MM}" height="{H*MM}"/></clipPath>'
    sol_clip = f'<clipPath id="sol"><polygon points="{" ".join(f"{P(x, y)[0]:.2f},{P(x, y)[1]:.2f}" for x, y in sol_poly)}"/></clipPath>'
    photo = (f'<image href="redresse2_jaune.jpg" x="{OX}" y="{OY}" width="{W*MM}" height="{H*MM}" opacity="0.45" '
             f'preserveAspectRatio="none"/>') if calque else ""
    svg = (f'<svg viewBox="0 0 {k4.PAGE_W} {k4.PAGE_H}" xmlns="http://www.w3.org/2000/svg"><defs>{clip}{sol_clip}</defs>{photo}'
           f'<g clip-path="url(#fen)">{"".join(k.out)}<g clip-path="url(#sol)">{"".join(sol.out)}</g>{"".join(c.out)}</g>'
           f'{"".join(cadre.out)}{"".join(t.out)}</svg>')
    return k4.html(svg, "jaune").replace("../polices-local.css", "../../polices-local.css")


if __name__ == "__main__":
    open(f"{ICI}/croquis-jaune.html", "w", encoding="utf-8").write(page())
    print("croquis-jaune.html écrit")
    if os.environ.get("CALQUE"):
        open(f"{ICI}/calque-jaune.html", "w", encoding="utf-8").write(page(True))

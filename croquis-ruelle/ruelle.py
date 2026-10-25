"""Croquis au trait de la ruelle à la porte bleue, vue d'une personne ASSISE, en perspective frontale.

La scène est reconstruite en 3D à partir de relevés faits sur la photo (photos/ruelle-photo-telephone.jpg),
élément par élément, puis dessinée depuis la place de l'élève : assis (yeux à 1,20 m), regard droit
devant, face à la porte du fond, un tout petit peu à droite, à 20 m d'elle.

Échelles relevées sur la photo : la porte du fond (2,40 m) donne l'échelle du mur du fond ; les murs de
la ruelle sont placés en profondeur par la projection centrale (z = f·X / (u − u_PF)) ; chaque élément
est mesuré dans le plan de son mur. Seul ce qui est sur la photo est dessiné (pas de plantes, pas de passants).

Dessin au trait seulement : ni hachures ni remplissages. Format A3 portrait.
Repère : x vers la droite, y vers le haut, z en profondeur depuis l'œil (en m).
Sorties : croquis-A3.html (A3 portrait) et croquis-2xA4.html (moitié haute et moitié basse de l'A3,
à l'échelle 1, sur 2 A4 paysage), à rendre en PDF avec rendu.js.
"""
import math, random, sys, os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "perspective-frontale-rue"))
from croquis import Crayon, html, FOND, GRIS, CON  # même crayon que le croquis de la rue (fig. 44)

ICI = sys.argv[1] if len(sys.argv) > 1 else "."
PAGE_W, PAGE_H = 297, 420                  # A3 portrait
FX0, FY0, FX1, FY1 = 15, 46, 282, 382      # le cadre (26,7 x 33,6 cm)
JONCTION = PAGE_H / 2                      # la coupure entre les deux A4
OEIL = 1.20                                # assis : les yeux à 1,20 m du sol
F = 300                                    # distance principale (mm) : ~48° de champ en largeur
CX, LHY = (FX0 + FX1) / 2, 226             # regard droit devant : PF au centre, LH au milieu (1,6 cm sous la jonction)
PF = (CX, LHY)
ZT = F * OEIL / (FY1 - LHY)                # le tableau : son pied (la LT) est le bas du cadre


def pr(x, y, z):
    return (CX + F * x / z, LHY - F * (y - OEIL) / z)


def k(z):                                  # mm par m à la distance z
    return F / z


# ---------------------------------------------------------------- la scène (relevée sur la photo, en m)
XA = -1.6              # mur à l'arc (et à la potence), à gauche de la placette
XL, XR = -0.9, 0.79    # murs de la ruelle (1,70 m de large)
Z_RUE, Z_FOND = 11, 20 # entrée de la ruelle, mur du fond (la porte bleue est à 20 m)
PORTE = (-0.78, 0.18, 0, 2.4)          # 0,96 x 2,40 m ; on est un tout petit peu à droite de son milieu
X_PIL = (-1.6, -0.9)                   # le pilier au panneau, à l'entrée de la ruelle
Z_PIL = 10.85
GATE = (1.96, 3.51)                    # le portail (1,55 m de large)


class Dessin:
    def __init__(self, graine):
        self.c = Crayon(graine); self.defs = []; self.n = 0; self.r = random.Random(graine + 1)

    def L(self, p, q, poids="fin", op=None, depasse=False):
        self.c.trait(p, q, poids, op=op, depasse=depasse)

    def poly(self, pts, poids="fin", depasse=False):
        self.c.poly(pts, poids, depasse=depasse)

    def id_clip(self, pts):
        self.n += 1; pid = f"c{self.n}"
        self.defs.append(f'<clipPath id="{pid}"><polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}"/></clipPath>')
        return pid

    def courbe(self, pts, lw=0.22, op=0.85, ferme=False, fond=None):
        """trait courbe tremblé"""
        r = self.r
        q = [(x + r.uniform(-0.04, 0.04), y + r.uniform(-0.04, 0.04)) for x, y in pts]
        if ferme: q = q + q[:1]
        d = " ".join(f"{x:.2f},{y:.2f}" for x, y in q)
        f = f'fill="{fond}"' if fond else 'fill="none"'
        tag = "polygon" if fond else "polyline"
        self.c.out.append(f'<{tag} points="{d}" {f} stroke="{GRIS}" stroke-width="{lw}" stroke-opacity="{op}" '
                          f'stroke-linecap="round" stroke-linejoin="round"/>')

    def spirale(self, cx, cy, r, tours=1.5, sens=1, a0=0.0, lw=0.2):
        n = int(18 * tours)
        pts = [(cx + r * (1 - i / n * 0.85) * math.cos(a0 + sens * 2 * math.pi * tours * i / n),
                cy + r * (1 - i / n * 0.85) * math.sin(a0 + sens * 2 * math.pi * tours * i / n)) for i in range(n + 1)]
        self.courbe(pts, lw)

    def rond(self, cx, cy, r, lw=0.2, op=0.85, fond=None):
        self.courbe([(cx + r*math.cos(t), cy + r*math.sin(t)) for t in np.linspace(0, 2*math.pi, 14)[:-1]], lw, op, ferme=True, fond=fond)


def lisse(pts, n=5):
    """courbe ouverte lissée passant par les points (Catmull-Rom)"""
    P = [pts[0]] + list(pts) + [pts[-1]]; out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = (np.array(P[i + j]) for j in (-1, 0, 1, 2))
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(tuple(0.5 * ((2*p1) + (-p0 + p2)*t + (2*p0 - 5*p1 + 4*p2 - p3)*t*t + (-p0 + 3*p1 - 3*p2 + p3)*t**3)))
    return out + [tuple(pts[-1])]


def rect_x(x, z1, z2, y1, y2):              # rectangle sur un mur parallèle à la ruelle (plan x = cte)
    return [pr(x, y2, z1), pr(x, y2, z2), pr(x, y1, z2), pr(x, y1, z1)]


def rect_z(z, x1, x2, y1, y2):              # rectangle de face (plan z = cte) : il garde sa vraie forme
    return [pr(x1, y2, z), pr(x2, y2, z), pr(x2, y1, z), pr(x1, y1, z)]


# ---------------------------------------------------------------- le sol : pavés de la placette, dalles de la ruelle
def sol(dz):
    r = dz.r
    z = ZT - 0.3
    while z < Z_RUE:
        pas_z = 0.24 + 0.02 * z
        x = XA + r.uniform(0, 0.3)
        while x < 7:
            w = r.uniform(0.18, 0.4); p = r.uniform(0.1, 0.18); zz = z + r.uniform(-0.04, 0.04)
            ph = r.uniform(0, 6.3); pts = []
            for i in range(12):
                a = 2 * math.pi * i / 12; e = 1 + 0.12 * math.sin(3*a + ph)
                pts.append(pr(x + w/2 + e*w/2 * math.copysign(abs(math.cos(a))**0.7, math.cos(a)), 0,
                              zz + e*p/2 * math.copysign(abs(math.sin(a))**0.7, math.sin(a))))
            if FX0 - 5 < pts[0][0] < FX1 + 5 and zz + p/2 < Z_RUE - 0.05:
                dz.courbe(pts, 0.2 if z < 9 else 0.15, 0.45 if z < 9 else 0.35, ferme=True)
            x += w + r.uniform(0.04, 0.1)
        z += pas_z
    dz.L(pr(XL, 0, Z_RUE), pr(XR, 0, Z_RUE), "fin")                              # le seuil de la ruelle
    z = Z_RUE                                                                     # les dalles de la ruelle
    while z < Z_FOND - 0.2:
        h = r.uniform(0.5, 0.8)
        dz.L(pr(XL, 0, min(z + h, Z_FOND)), pr(XR, 0, min(z + h, Z_FOND)), "fin", op=0.5)
        x = XL + r.uniform(0.35, 0.8)
        while x < XR - 0.2:
            dz.L(pr(x, 0, z), pr(x, 0, min(z + h, Z_FOND)), "fin", op=0.5); x += r.uniform(0.5, 0.9)
        z += h
    # la planche couchée contre le pied du mur à l'arc
    dz.poly([pr(XA + 0.01, 0.12, 5.1), pr(XA + 0.01, 0.05, 6.7), pr(XA + 0.1, 0, 6.7), pr(XA + 0.15, 0, 5.1)], "fin")
    dz.L(pr(XA + 0.08, 0.06, 5.1), pr(XA + 0.06, 0.03, 6.7), "fin", op=0.6)


# ---------------------------------------------------------------- le fond de la ruelle
def porte_bleue(dz):
    x1, x2, y1, y2 = PORTE; z = Z_FOND; kz = k(z)
    dz.poly(rect_z(z, x1 - 0.04, x2 + 0.04, 0.08, y2 + 0.04), "fin")              # le cadre
    dz.poly(rect_z(z, x1 - 0.08, x2 + 0.08, 0, 0.08), "fin")                      # la marche du seuil
    dz.poly(rect_z(z, x1, x2, 0.08, y2), "fort")
    for y in (2.28, 2.11, 1.9):                                                   # les traverses du haut
        dz.L(pr(x1, y, z), pr(x2, y, z), "fin")
    for off in (0.24, 0.40, 0.50, 0.68, 0.80):                                    # les planches verticales
        dz.L(pr(x1 + off, 0.08, z), pr(x1 + off, 1.9, z), "fin", op=0.6)
    u, v = pr(x1 + 0.56, 1.05, z); dz.rond(u, v, 0.025 * kz, 0.18)               # la poignée
    dz.L((u, v), (u, v + 0.08 * kz))


def fond(dz):
    r = dz.r
    # le vieux mur derrière, enduit, avec des pierres visibles par endroits, et l'antenne sur le dessus
    dz.poly(rect_z(24, -2.2, 2.2, 0, 6.0), "fin")
    for (cx0, cy0, w, h) in ((0.55, 5.82, 0.2, 0.13), (0.72, 5.8, 0.14, 0.15), (0.6, 5.62, 0.24, 0.12), (0.76, 5.6, 0.1, 0.12),
                             (0.18, 5.18, 0.18, 0.12), (0.34, 5.15, 0.12, 0.1), (0.24, 5.02, 0.2, 0.1)):
        pts = [pr(cx0 + w/2 * math.cos(t) * r.uniform(0.8, 1.1), cy0 + h/2 * math.sin(t) * r.uniform(0.8, 1.1), 24) for t in np.linspace(0, 2*math.pi, 7)[:-1]]
        dz.courbe(pts, 0.16, 0.6, ferme=True)                                     # des moellons, là où l'enduit est tombé
    cx, cy = pr(0.6, 6.0, 24); rr = 0.18 * k(24)
    dz.courbe([(cx + rr*math.cos(t), cy - rr*math.sin(t)) for t in np.linspace(0, math.pi, 14)], 0.22, ferme=True, fond=FOND)
    # le mur du fond, de face : son haut s'arrondit un peu à gauche
    haut = [pr(x, y, Z_FOND) for x, y in ((XL - 0.3, 4.9), (-0.6, 4.86), (-0.3, 4.76), (0.2, 4.7), (XR + 0.3, 4.7))]
    dz.courbe(lisse(haut) + [pr(XR + 0.3, 0, Z_FOND), pr(XL - 0.3, 0, Z_FOND)], 0.3, ferme=True, fond=FOND)
    porte_bleue(dz)
    x2 = PORTE[1]
    dz.poly(rect_z(Z_FOND, x2 + 0.28, x2 + 0.59, 1.41, 2.22), "moyen")            # la fenêtre (simple cadre)
    dz.poly(rect_z(Z_FOND, x2 + 0.31, x2 + 0.56, 1.44, 2.19), "fin")
    dz.poly(rect_z(Z_FOND, x2 + 0.08, x2 + 0.22, 2.15, 2.26), "fin")              # la plaque du numéro
    dz.poly(rect_z(Z_FOND, x2 + 0.11, x2 + 0.50, 0.37, 0.69), "fin")              # le compteur
    dz.L(pr(x2 + 0.13, 0.41, Z_FOND), pr(x2 + 0.48, 0.41, Z_FOND))
    u, v = pr(x2 + 0.15, 0.53, Z_FOND); dz.rond(u, v, 0.015 * k(Z_FOND), 0.15)
    # le mur droit de la ruelle (il fuit vers le PF) : son haut monte vers le fond
    dz.poly([pr(XR, 4.9, Z_RUE), pr(XR, 6.2, Z_FOND), pr(XR, 0, Z_FOND), pr(XR, 0, Z_RUE)], "moyen")
    dz.L(pr(XR, 3.3, 13.2), pr(XR, 4.9 + 1.3 * 2.2 / 9, 13.2), "fin", op=0.6)    # le joint vertical
    for z1, z2, y1, y2 in ((12.17, 12.8, 3.75, 4.49), (15.5, 16.5, 4.17, 4.93), (15.06, 15.66, 2.37, 2.96),
                           (12.3, 12.7, 1.31, 1.85), (16.55, 17.27, 1.94, 2.14), (12.7, 13.1, 0.37, 0.63)):
        dz.poly(rect_x(XR, z1, z2, y1, y2), "fin")
    dz.poly(rect_x(XR, 18.0, 19.6, 0, 2.15), "moyen")                             # la porte au bout, vue de profil
    dz.poly(rect_x(XR, 18.15, 19.5, 0.05, 2.08), "fin")
    zc = 12.2                                                                     # le col de cygne et son câble
    dz.L(pr(XR, 0.3, zc), pr(XR, 3.0, zc)); dz.L(pr(XR, 0.3, zc + 0.05), pr(XR, 3.0, zc + 0.05))
    crosse = [pr(XR, 3.0, zc), pr(XR, 3.14, zc), pr(XR - 0.04, 3.22, zc), pr(XR - 0.12, 3.24, zc), pr(XR - 0.18, 3.17, zc), pr(XR - 0.19, 3.08, zc)]
    dz.courbe(lisse(crosse), 0.3)
    dz.poly([pr(XR - 0.23, 3.08, zc), pr(XR - 0.15, 3.08, zc), pr(XR - 0.15, 3.0, zc), pr(XR - 0.23, 3.0, zc)], "fin")
    bout = pr(XR - 0.05, 3.5, 19.6)
    dz.L(pr(XR - 0.19, 3.0, zc), bout)
    dz.poly([(bout[0] - 0.4, bout[1]), (bout[0] + 0.4, bout[1]), (bout[0] + 0.2, bout[1] + 0.7), (bout[0] - 0.2, bout[1] + 0.7)], "fin")
    # le mur gauche de la ruelle
    dz.poly(rect_x(XL, Z_RUE, Z_FOND, 0, 11), "moyen")
    # la grille ventrue en fer forgé, en haut du mur gauche (vue de profil)
    zg = 16.6; kg = k(zg)
    G = lambda dx, y: pr(XL + dx, y, zg)
    dz.poly([G(0, 5.5), G(0.12, 5.5), G(0.12, 4.95), G(0, 4.95)], "fin")          # la partie plate, en haut
    for y in (5.43, 5.02): dz.L(G(0, y), G(0.12, y))
    for y in (5.33, 5.22, 5.11):
        u, v = G(0.06, y); dz.rond(u, v, 0.04 * kg, 0.15)
    ventre = [G(0.12, 4.95), G(0.25, 4.88), G(0.35, 4.72), G(0.4, 4.52), G(0.38, 4.36), G(0.28, 4.24), G(0.14, 4.2), G(0, 4.2)]
    dz.courbe(lisse(ventre) + [G(0, 4.95)], 0.3, ferme=True, fond=FOND)
    for i, (dx, y, rr) in enumerate(((0.15, 4.77, 0.08), (0.11, 4.55, 0.08), (0.28, 4.55, 0.075), (0.2, 4.68, 0.04))):
        u, v = G(dx, y); dz.spirale(u, v, rr * kg, 1.7, 1 if i % 2 else -1, 0.6 * i, 0.2)
    for t in (0.3, 0.55, 0.8):                                                    # les barres courbes du bas
        dz.courbe([G(0.38 * t * math.sin(a) + 0.02, 4.2 + 0.25 * t + (0.4 - 0.3 * t) * (1 - math.cos(a)) * 0.3) for a in np.linspace(0, math.pi * 0.62, 10)], 0.18, 0.75)
    # la lanterne, posée au bout de sa potence à volutes
    zl = 15.5; kl = k(zl)
    Lp = lambda dx, y: pr(XL + dx, y, zl)
    yb = 3.35; lg = 1.1
    dz.L(Lp(0, yb), Lp(lg, yb), "moyen")
    dz.L(Lp(0.02, yb + 0.06), Lp(0.02, yb - 0.34), "moyen")                       # la platine
    bras = [Lp(0.02, yb - 0.3), Lp(0.2, yb - 0.29), Lp(0.42, yb - 0.22), Lp(0.6, yb - 0.12), Lp(0.76, yb - 0.02)]
    dz.courbe(lisse(bras), 0.24)
    for i, (dx, dy, rr, sens) in enumerate(((0.13, -0.17, 0.085, 1), (0.35, -0.13, 0.055, -1), (0.51, -0.08, 0.045, 1),
                                            (0.66, -0.05, 0.035, -1), (0.86, -0.04, 0.03, 1))):
        u, v = Lp(dx, yb + dy); dz.spirale(u, v, rr * kl, 1.6, sens, 1.2 * i, 0.18)
    s1 = lambda dx, y: Lp(lg - 0.03 + dx, yb + y)
    dz.poly([s1(-0.03, 0.0), s1(0.03, 0.0), s1(0.05, 0.1), s1(-0.05, 0.1)], "fin")
    dz.poly([s1(-0.12, 0.1), s1(0.12, 0.1), s1(0.12, 0.13), s1(-0.12, 0.13)], "fin")
    dz.poly([s1(-0.1, 0.13), s1(0.1, 0.13), s1(0.15, 0.45), s1(-0.15, 0.45)], "fin")
    for dx0, dx1 in ((-0.04, -0.06), (0.04, 0.06)): dz.L(s1(dx0, 0.13), s1(dx1, 0.45))
    dz.poly([s1(-0.15, 0.45), s1(0.15, 0.45), s1(0.2, 0.5), s1(-0.2, 0.5)], "fin")
    dz.courbe([s1(-0.2, 0.5), s1(-0.12, 0.58), s1(0, 0.6), s1(0.12, 0.58), s1(0.2, 0.5)], 0.22)
    dz.poly([s1(-0.07, 0.6), s1(0.07, 0.6), s1(0.07, 0.65), s1(-0.07, 0.65)], "fin")
    for dx in (-0.06, 0, 0.06): dz.L(s1(dx, 0.65), s1(dx, 0.69))


# ---------------------------------------------------------------- à gauche : le mur à l'arc, la potence, le pilier
def potence(dz):
    """le grand support en fer forgé (relevé sur la photo) : barre, platine, bras, volutes, crochet du fil"""
    z = 6.0; kz = k(z); yb = 4.66
    P = lambda s, t: pr(XA + s, yb - t, z)                                        # s : depuis le mur, t : sous la barre
    dz.L(P(0, -0.03), P(1.27, -0.03), "moyen"); dz.L(P(0, 0.0), P(1.25, 0.0), "moyen")   # la barre
    u, v = P(1.27, -0.015); dz.rond(u, v, 0.03 * kz, 0.25, fond=FOND)             # le bout arrondi
    dz.L(P(0, -0.05), P(0, 0.34), "moyen"); u, v = P(0, 0.36); dz.rond(u, v, 0.02 * kz, 0.2)   # la platine
    bras = [P(0.01, 0.3), P(0.15, 0.31), P(0.4, 0.28), P(0.65, 0.2), P(0.9, 0.1), P(1.05, 0.03), P(1.1, 0.0)]
    dz.courbe(lisse(bras), 0.3)
    for s, t, rr, sens, a0 in ((0.21, 0.13, 0.11, 1, 2.6), (0.53, 0.08, 0.07, -1, 0.3), (0.77, 0.1, 0.045, 1, 3.0), (0.93, 0.13, 0.055, -1, 0.0)):
        u, v = P(s, t); dz.spirale(u, v, rr * kz, 1.8, sens, a0, 0.24)
    dz.courbe(lisse([P(0.36, 0.02), P(0.42, 0.06), P(0.47, 0.1)]), 0.2)          # les petites attaches
    u, v = P(0.33, 0.25); dz.rond(u, v, 0.015 * kz, 0.18)
    crochet = P(0.91, 0.2)
    dz.L(P(0.91, 0.16), crochet, "fin")
    return crochet


def gauche(dz):
    X = XA
    dz.poly(rect_x(X, 2, Z_RUE, 0, 14), "fort")
    # l'ouverture en arc : mur blanc enduit, épaisseur brute, fond muré en briques
    za, zb, ya, ys, R = 8.7, 10.6, 1.9, 2.85, 0.95
    zc = (za + zb) / 2; ep = 0.15
    def contour(x):
        return ([pr(x, ya, za), pr(x, ys, za)] +
                [pr(x, ys + R * math.sin(t), zc - R * math.cos(t)) for t in np.linspace(0, math.pi, 30)] +
                [pr(x, ys, zb), pr(x, ya, zb)])
    ouv, fondb = contour(X), contour(X - ep)
    c1, c2 = dz.id_clip(ouv), dz.id_clip(fondb)
    br = Crayon(41); y = ya + 0.065
    while y < ys + R:
        demi = R * math.sqrt(max(0, 1 - ((y - ys) / R) ** 2)) if y > ys else R
        br.trait(pr(X - ep, y, zc - demi), pr(X - ep, y, zc + demi), "fin", op=0.4, depasse=False)
        y += 0.065
    bord_fond = Crayon(42); bord_fond.out.append(
        f'<polyline points="{" ".join(f"{u:.2f},{v:.2f}" for u, v in fondb)}" fill="none" stroke="{GRIS}" stroke-width="0.22" stroke-opacity="0.8"/>')
    dz.c.out.append(f'<g clip-path="url(#{c1})"><g clip-path="url(#{c2})">{"".join(br.out)}</g>{"".join(bord_fond.out)}</g>')
    dz.courbe(ouv, 0.32)
    # la fenêtre haute et étroite, au-dessus, à deux battants vitrés
    z1, z2, y1, y2 = 10.13, 10.8, 4.34, 6.44
    dz.poly(rect_x(X, z1, z2, y1, y2), "moyen")
    dz.poly(rect_x(X, z1 + 0.05, z2 - 0.05, y1 + 0.05, y2 - 0.05), "fin")
    zm = (z1 + z2) / 2; dz.L(pr(X, y1 + 0.05, zm), pr(X, y2 - 0.05, zm))
    for yy in (y1 + (y2 - y1) / 3, y1 + 2 * (y2 - y1) / 3):
        dz.L(pr(X, yy, z1 + 0.05), pr(X, yy, z2 - 0.05))
    # la descente d'eau (gros tuyau, colliers, sabot) et la gaine fine à côté
    xp = X + 0.1
    for e in (0, 0.12): dz.L(pr(xp, 0.35, 8.5 + e), pr(xp, 14, 8.5 + e))
    for y in (1.2, 2.6, 4.0, 5.4):
        dz.L(pr(xp, y, 8.47), pr(xp, y, 8.65)); dz.L(pr(xp, y + 0.06, 8.47), pr(xp, y + 0.06, 8.65))
    dz.poly([pr(xp, 0.35, 8.46), pr(xp, 0.35, 8.66), pr(xp, 0, 8.66), pr(xp, 0, 8.46)], "fin")
    for e in (0, 0.03): dz.L(pr(X + 0.03, 0, 8.36 + e), pr(X + 0.03, 14, 8.36 + e), "fin", op=0.7)
    # la petite tige noire et ses attaches, en bas du mur
    dz.courbe([pr(X, 0.33, 5.25), pr(X, 0.5, 5.27), pr(X, 0.65, 5.26)], 0.35)
    for y in (0.38, 0.5, 0.6): dz.L(pr(X, y, 5.22), pr(X, y, 5.32))
    # la tour (de face) à l'entrée de la ruelle, avec son anneau d'angle et sa gargouille
    dz.poly(rect_z(Z_RUE, X, XL, 0, 14), "fort")
    a = pr(XL, 4.2, Z_RUE); b = pr(XL, 3.9, Z_RUE)
    dz.courbe([a] + [((a[0] + b[0]) / 2 + 0.09 * k(Z_RUE) * math.sin(t), a[1] + (b[1] - a[1]) * (1 - math.cos(t)) / 2) for t in np.linspace(0, math.pi, 10)] + [b], 0.28)
    for e in (0, 0.1): dz.L(pr(XL, 6.1 + e, 11.3), pr(-0.4, 6.1 + e, 11.3))
    u, v = pr(-0.4, 6.15, 11.3); dz.courbe([(u + 0.25*math.cos(t), v + 0.5*math.sin(t)) for t in np.linspace(0, 2*math.pi, 12)], 0.2, ferme=True)
    # le pilier : panneau en creux en bas, tablette de marbre, plaque « Rue du Tribunal »
    x1, x2 = X_PIL; zp = Z_PIL; kp = k(zp)
    dz.poly(rect_z(zp, x1, x2, 0, 3.7), "moyen")
    dz.poly([pr(x2, 3.7, zp), pr(x2, 3.7, Z_RUE), pr(x2, 0, Z_RUE), pr(x2, 0, zp)], "fin")
    dz.L(pr(x1, 0.1, zp), pr(x2, 0.1, zp)); dz.L(pr(x2, 0.1, zp), pr(x2, 0.1, Z_RUE))
    dz.poly(rect_z(zp, x1 + 0.07, x1 + 0.45, 0.12, 1.7), "fin")
    dz.poly(rect_z(zp - 0.12, x1 + 0.09, x1 + 0.5, 1.79, 1.85), "fin")
    dz.poly([pr(x1 + 0.09, 1.79, zp - 0.12), pr(x1 + 0.5, 1.79, zp - 0.12), pr(x1 + 0.5, 1.79, zp), pr(x1 + 0.09, 1.79, zp)], "fin")
    dz.poly(rect_z(zp, x1 + 0.09, x1 + 0.40, 2.04, 2.34), "moyen")
    dz.poly(rect_z(zp, x1 + 0.11, x1 + 0.38, 2.06, 2.32), "fin")
    u, v = pr(x1 + 0.245, 2.24, zp); dz.c.texte(u, v + 0.4, "نهج التريبونال", 0.075 * kp, GRIS, "middle", halo=False)
    u, v = pr(x1 + 0.245, 2.12, zp); dz.c.texte(u, v + 0.3, "Rue Du Tribunal", 0.05 * kp, GRIS, "middle", halo=False)
    # la potence en fer forgé (plus près que la tour : dessinée après), en haut à gauche, et le fil qui part de son crochet
    crochet = potence(dz)
    fin_fil = pr(2.46, 4.49, Z_RUE)
    m = ((crochet[0] + fin_fil[0]) / 2, (crochet[1] + fin_fil[1]) / 2 + 4)
    dz.courbe([((1-t)**2*crochet[0] + 2*(1-t)*t*m[0] + t*t*fin_fil[0], (1-t)**2*crochet[1] + 2*(1-t)*t*m[1] + t*t*fin_fil[1]) for t in np.linspace(0, 1, 30)], 0.2)


# ---------------------------------------------------------------- à droite : le mur au portail
def portail(dz):
    z = Z_RUE; kz = k(z); x1, x2 = GATE
    dz.poly(rect_z(z, x1 - 0.05, x2 + 0.05, 0, 0.16), "fin")                      # la marche blanche
    dz.poly(rect_z(z, x1 - 0.03, x2 + 0.03, 2.47, 2.53), "fin")                   # le linteau
    dz.poly(rect_z(z, x1, x2, 0.16, 2.47), "fort")
    dz.L(pr(x1, 2.0, z), pr(x2, 2.0, z), "moyen")                                 # l'imposte en fer forgé
    dz.L(pr(x1, 2.36, z), pr(x2, 2.36, z))                                        # sa bande pleine du haut
    ya, yh = 2.02, 2.36; n = 11; w = (x2 - x1) / n
    for i in range(n):
        a = x1 + i * w; M = lambda u_, v_: pr(a + u_ * w, ya + v_ * (yh - ya), z)
        if i: dz.L(M(0, 0), M(0, 1))
        dz.L(M(0.5, 0.02), M(0.5, 0.78), "fin")
        dz.L(M(0.5, 0.02), M(0.06, 0.8), "fin"); dz.L(M(0.5, 0.02), M(0.94, 0.8), "fin")
        for v_, rr in ((0.87, 0.2), (0.53, 0.19), (0.3, 0.17)):
            for u_, sens in ((0.27, 1), (0.73, -1)):
                cx, cy = M(u_, v_); dz.spirale(cx, cy, rr * w * kz, 1.5, sens, 0 if sens > 0 else math.pi, 0.15)
    xm = (x1 + x2) / 2
    dz.L(pr(xm, 0.16, z), pr(xm, 2.0, z), "moyen")                                # deux battants en tôle lisse
    dz.L(pr(x1 + 0.06, 0.16, z), pr(x1 + 0.06, 2.0, z), "fin", op=0.6)
    dz.poly(rect_z(z, xm - 0.06, xm + 0.02, 1.3, 1.36), "fin")                    # le loquet
    # le tag : « M+D » (le D plus bas) et le cœur, au trait
    T = lambda dx, y: pr(x1 + dx, y, z)
    dz.courbe([T(0.28, 1.45), T(0.29, 1.62), T(0.36, 1.5), T(0.43, 1.62), T(0.45, 1.46)], 0.28, 0.75)
    dz.L(T(0.5, 1.5), T(0.56, 1.5)); dz.L(T(0.53, 1.45), T(0.53, 1.55))
    dz.courbe([T(0.6, 1.3), T(0.6, 1.53), T(0.7, 1.5), T(0.73, 1.41), T(0.69, 1.32), T(0.6, 1.3)], 0.28, 0.75)
    cx, cy = T(0.45, 1.13); s = 0.17 * kz
    dz.courbe([(cx + s*0.95*math.sin(t)**3, cy - s*(0.8*math.cos(t) - 0.3*math.cos(2*t) - 0.12*math.cos(3*t) - 0.05*math.cos(4*t)))
               for t in np.linspace(0, 2*math.pi, 40)], 0.28, 0.75)


def sac(dz, x, w, h, z, noeud=True, rond=False):
    a, b, t = pr(x, 0, z), pr(x + w, 0, z), pr(x + w/2, h, z)
    if rond:
        pts = [a, pr(x, h * 0.75, z), pr(x + w * 0.2, h * 0.98, z), t, pr(x + w * 0.8, h * 0.98, z), pr(x + w, h * 0.75, z), b]
    else:
        pts = [a, pr(x - 0.02, h * 0.5, z), pr(x + w * 0.25, h * 0.9, z), t, pr(x + w * 0.75, h * 0.85, z), pr(x + w + 0.02, h * 0.45, z), b]
    dz.courbe(lisse(pts), 0.25, ferme=True, fond=FOND)
    if noeud:
        dz.L(t, pr(x + w/2 - 0.02, h + 0.06, z)); dz.L(t, pr(x + w/2 + 0.03, h + 0.05, z))
    dz.courbe([pr(x + w * 0.3, h * 0.7, z), pr(x + w * 0.45, h * 0.4, z), pr(x + w * 0.4, h * 0.15, z)], 0.15, 0.6)


def droite(dz):
    z = Z_RUE
    pente = lambda x: 4.9 - 0.205 * (x - XR)                                      # le haut du mur descend vers la droite
    dz.poly([pr(XR, pente(XR), z), pr(7, pente(7), z), pr(7, 0, z), pr(XR, 0, z)], "fort")
    dz.c.trait(pr(XR, pente(XR), z), pr(XR, 0, z), "fort", double=True, depasse=False)   # l'arête du coin
    dz.L(pr(1.08, pente(1.08), z), pr(1.08, 2.24, z))                             # le pilier en saillie de l'angle
    dz.L(pr(XR, 2.24, z), pr(1.08, 2.24, z)); dz.L(pr(XR, 2.2, z), pr(1.08, 2.2, z))
    for x, y in ((1.0, 4.65), (1.03, 3.03)):                                      # les deux pitons
        dz.poly(rect_z(z, x - 0.025, x + 0.025, y - 0.015, y + 0.015), "fin")
    portail(dz)
    zs = 10.9                                                                     # au pied du mur : sacs et boîtes
    sac(dz, 1.40, 0.24, 0.42, zs, noeud=False, rond=True)
    sac(dz, 1.12, 0.3, 0.28, zs - 0.05)
    sac(dz, 1.62, 0.32, 0.34, zs - 0.03)
    dz.poly(rect_z(zs - 0.25, 1.30, 1.45, 0, 0.18), "fin"); dz.L(pr(1.30, 0.14, zs - 0.25), pr(1.45, 0.14, zs - 0.25))
    dz.poly(rect_z(zs - 0.3, 1.66, 1.88, 0, 0.06), "fin")
    dz.courbe([pr(3.25, 0.16, 10.95), pr(3.3, 0.24, 10.95), pr(3.38, 0.2, 10.95), pr(3.42, 0.16, 10.95)], 0.2, ferme=True, fond=FOND)


# ---------------------------------------------------------------- la construction, en bleu
def bord(p):
    d = np.subtract(p, PF); ts = []
    for v, i, lo, hi in ((FX0, 0, FY0, FY1), (FX1, 0, FY0, FY1), (FY0, 1, FX0, FX1), (FY1, 1, FX0, FX1)):
        if abs(d[i]) < 1e-9: continue
        t = (v - PF[i]) / d[i]
        if t > 0 and lo - 1e-6 <= PF[1-i] + t*d[1-i] <= hi + 1e-6: ts.append(t)
    t = min(ts); return (PF[0] + t*d[0], PF[1] + t*d[1])


def construction():
    c = Crayon(7)
    for i in range(-5, 6):                                                        # grille de report de 3 cm
        x = CX + 30*i
        if FX0 < x < FX1: c.trait((x, FY0), (x, FY1), "construction", CON, 0.22, depasse=False)
    for j in range(-6, 6):
        y = LHY + 30*j
        if FY0 < y < FY1 and j: c.trait((FX0, y), (FX1, y), "construction", CON, 0.22, depasse=False)
    fuy = [pr(XA, 0, 5), pr(XA, 1.9, 5), pr(XL, 0, Z_RUE), pr(XR, 0, Z_RUE), pr(XA, 6.44, 9), pr(XA, 4.34, 9),
           pr(XR, 4.49, 12.17), pr(XR, 3.75, 12.17)]
    for p in fuy:
        c.trait(bord(p), PF, "construction", CON, 0.8, depasse=False, tirets="2 1.4")
    c.trait((0, LHY), (PAGE_W, LHY), "moyen", CON, 0.9, depasse=False, tirets="4 1.4 0.7 1.4")
    c.trait((FX0 - 6, FY1), (FX1 + 6, FY1), "construction", CON, 0.85, depasse=False, tirets="1.6 1.2")
    c.texte(FX0 - 1.5, LHY - 1.3, "LH", 4.2, CON, "end"); c.texte(FX1 + 1.5, LHY - 1.3, "LH", 4.2, CON, "start")
    c.texte(FX0 - 1.5, FY1 - 1.3, "LT", 3.8, CON, "end"); c.texte(FX1 + 1.5, FY1 - 1.3, "LT", 3.8, CON, "start")
    c.out.append(f'<circle cx="{CX}" cy="{LHY}" r="3" fill="none" stroke="{CON}" stroke-width="0.35"/>')
    c.point(CX, LHY, CON, 0.7)
    c.texte(CX + 3.8, LHY + 5.2, "PF", 4.4, CON, "start")
    xc = FX1 - 6                                                                  # cote : 1,20 m, assis
    c.trait((xc, FY1), (xc, LHY), "moyen", CON, 0.95, depasse=False)
    for y, s in ((FY1, -1), (LHY, 1)):
        c.trait((xc - 1.2, y), (xc + 1.2, y), "moyen", CON, 0.95, depasse=False)
        c.trait((xc, y), (xc - 0.8, y + s*1.6), "moyen", CON, 0.95, depasse=False)
        c.trait((xc, y), (xc + 0.8, y + s*1.6), "moyen", CON, 0.95, depasse=False)
    c.texte(xc - 1.6, (FY1 + LHY)/2 + 18, "1,20 m", 3.6, CON, "end")
    c.texte(xc - 1.6, (FY1 + LHY)/2 + 22.4, "yeux, assis", 3.0, CON, "end")
    c.texte(FX0 + 3, LHY + 4.4, "LH : à hauteur des yeux, ASSIS (1,20 m)", 2.9, CON)
    c.texte(FX0 + 3, LHY + 8, "plus bas que la photo, prise debout", 2.9, CON)
    p = pr(PORTE[0], PORTE[3], Z_FOND)
    q = pr(PORTE[0], 0.3, Z_FOND)
    c.texte(FX0 + 3, LHY + 15, "la porte bleue, à 20 m : petite, coupée en deux par la LH", 2.9, CON)
    c.trait((FX0 + 80, LHY + 15.6), (q[0] - 0.6, q[1]), "construction", CON, 0.9, depasse=False)
    c.texte(184, 150, "les murs de la ruelle", 2.8, CON)
    c.texte(184, 153.4, "fuient vers le PF", 2.8, CON)
    c.texte(FX1 - 3, 168, "mur de face : vraie forme,", 2.8, CON, "end")
    c.texte(FX1 - 3, 171.4, "horizontales horizontales", 2.8, CON, "end")
    q = pr(XA, 0.6, 5.2)
    c.texte(q[0] + 3, q[1] - 3, "mur à l'arc : il fuit vers le PF", 2.8, CON, rot=math.degrees(math.atan2(LHY - q[1], CX - q[0])))
    return "".join(c.out)


def dessin():
    dz = Dessin(31)
    sol(dz); fond(dz); droite(dz); gauche(dz)
    cadre = Crayon(3)
    coins = [(FX0, FY0), (FX1, FY0), (FX1, FY1), (FX0, FY1)]
    for i in range(4):
        cadre.trait(coins[i], coins[(i+1) % 4], "fort", "#1c1c1c", 0.95)
    defs = "".join(dz.defs) + f'<clipPath id="cadre"><rect x="{FX0}" y="{FY0}" width="{FX1-FX0}" height="{FY1-FY0}"/></clipPath>'
    return defs, f'<g clip-path="url(#cadre)">{"".join(dz.c.out)}</g>' + construction() + "".join(cadre.out)


def textes():
    t = Crayon(4)
    t.texte(FX0, 13, "La ruelle à la porte bleue · vue assise", 6.6, "#1f1f1f")
    t.texte(FX0, 20, "perspective frontale · 1 point de fuite · assis face à la porte, un peu à droite, à 20 m", 3.4, "#555")
    etapes = ["1  le cadre, la LH au milieu (regard droit devant), le PF au centre",
              "2  la porte bleue et le mur du fond : de face, petits, coupés par la LH",
              "3  les murs de la ruelle : pieds et hauts sur des fuyantes vers le PF",
              "4  le mur au portail (de face) et le mur à l'arc (il fuit vers le PF)",
              "5  les détails : arc muré de briques, fers forgés, lanterne, portail",
              "6  le sol : pavés dans la placette, dalles dans la ruelle"]
    for i, e in enumerate(etapes):
        t.texte(FX0 + (i // 3) * 134, 28.5 + (i % 3) * 3.9, e, 2.9, CON)
    for i, l in enumerate(["en bleu : la construction (LH, LT, PF, fuyantes) · au crayon : le croquis, au trait, sans hachures",
                           "carreaux bleus de 3 cm, partant du PF, pour reporter le dessin",
                           "dessiné depuis ta place, pas depuis le téléphone : yeux à 1,20 m, regard droit devant",
                           "chaque élément est relevé sur la photo (place, nombre, forme) : rien d'ajouté"]):
        t.texte(FX0, 391 + i*5, l, 3.0, "#666", halo=False)
    return "".join(t.out)


def etiquettes_a4():
    t = Crayon(9)
    t.texte(8, JONCTION / 2, "feuille 1/2 · moitié HAUTE de l'A3 · la jonction est en bas ↓", 3.0, "#a0302a", "middle", rot=-90, halo=False)
    g = "".join(t.out); t.out = []
    t.texte(8, JONCTION * 1.5, "↑ la jonction est en haut · feuille 2/2 · moitié BASSE de l'A3", 3.0, "#a0302a", "middle", rot=-90, halo=False)
    return g, "".join(t.out)


if __name__ == "__main__":
    defs, corps = dessin()
    txt = textes()
    eg, ed = etiquettes_a4()
    svg = lambda vb, extra="": (f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg"><defs>{defs}</defs>'
                                f'{corps}{txt}{extra}</svg>')
    open(f"{ICI}/croquis-A3.html", "w", encoding="utf-8").write(html([svg(f"0 0 {PAGE_W} {PAGE_H}")], 297, 420, "Ruelle porte bleue A3"))
    open(f"{ICI}/croquis-2xA4.html", "w", encoding="utf-8").write(
        html([svg(f"0 0 297 {JONCTION:g}", eg), svg(f"0 {JONCTION:g} 297 {JONCTION:g}", ed)], 297, 210, "Ruelle porte bleue 2 x A4"))
    print("croquis-A3.html et croquis-2xA4.html écrits")

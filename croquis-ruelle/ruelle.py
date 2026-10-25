"""Croquis au trait de la ruelle à la porte bleue, vue d'une personne ASSISE, en perspective frontale.

Ce n'est pas un calque de la photo du téléphone (prise debout, en zoom) : la scène est reconstruite
en 3D d'après la photo, puis dessinée depuis la place de l'élève : assis (yeux à 1,20 m), regard droit
devant, face à la porte du fond, un tout petit peu à droite, à 20 m d'elle.

Dessin au trait seulement : ni hachures ni remplissages, des détails (pierres taillées de l'arc,
panneaux et clous de la porte, fer forgé, lanterne, pavés...). Format A3 portrait.

Repère : x vers la droite, y vers le haut, z en profondeur depuis l'œil (en m).
Sorties : croquis-A3.html (A3 portrait) et croquis-2xA4.html (les deux moitiés de l'A3, haut et bas,
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
XL_PLACE = -1.9        # façade à l'arc, à gauche de la placette
XL, XR = -1.0, 1.3     # murs de la ruelle
Z_RUE, Z_FOND = 11, 20 # entrée de la ruelle, mur du fond (la porte bleue est à 20 m)
PORTE = (-0.85, 0.15, 0, 2.5)          # x1, x2, y1, y2 : on est un peu à droite de la porte
FENETRE = (0.55, 0.87, 1.55, 2.35)
H_FOND, H_RUE_D, H_RUE_G = 4.9, 6.0, 11
PASSANTS = [(0.95, 6.5, 1), (3.6, 9.5, -1), (0.55, 14.5, 1)]   # des gens DEBOUT (1,75 m) : x, z, sens


class Dessin:
    def __init__(self, graine):
        self.c = Crayon(graine); self.defs = []; self.n = 0; self.r = random.Random(graine + 1)

    def L(self, p, q, poids="fin", op=None, depasse=False):
        self.c.trait(p, q, poids, op=op, depasse=depasse)

    def poly(self, pts, poids="fin", depasse=False):
        self.c.poly(pts, poids, depasse=depasse)

    def clip(self, pts, contenu):
        self.n += 1; pid = f"c{self.n}"
        self.defs.append(f'<clipPath id="{pid}"><polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}"/></clipPath>')
        self.c.out.append(f'<g clip-path="url(#{pid})">{contenu}</g>')

    def courbe(self, pts, lw=0.22, op=0.85, ferme=False, fond=None):
        """trait courbe tremblé (arc, volute, feuille, pavé)"""
        r = self.r
        q = [(x + r.uniform(-0.05, 0.05), y + r.uniform(-0.05, 0.05)) for x, y in pts]
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

    def rond(self, cx, cy, r, lw=0.2, op=0.85):
        self.courbe([(cx + r*math.cos(t), cy + r*math.sin(t)) for t in np.linspace(0, 2*math.pi, 14)[:-1]], lw, op, ferme=True)


def rect_x(x, z1, z2, y1, y2):              # rectangle sur un mur parallèle à la ruelle (plan x = cte)
    return [pr(x, y2, z1), pr(x, y2, z2), pr(x, y1, z2), pr(x, y1, z1)]


def rect_z(z, x1, x2, y1, y2):              # rectangle de face (plan z = cte) : il garde sa vraie forme
    return [pr(x1, y2, z), pr(x2, y2, z), pr(x2, y1, z), pr(x1, y1, z)]


# ---------------------------------------------------------------- le sol
def sol(dz):
    """pavés : des rangées de pierres arrondies, de plus en plus petites et serrées vers le PF"""
    r = dz.r
    z = ZT - 0.3
    while z < Z_FOND:
        pas_z = 0.24 + 0.02 * z
        xg = XL_PLACE if z < Z_RUE else XL
        xd = 7 if z < Z_RUE else XR
        x = xg + r.uniform(0, 0.3)
        while x < xd - 0.1:
            w = r.uniform(0.16, 0.38); p = r.uniform(0.1, 0.2); zz = z + r.uniform(-0.04, 0.04)
            if z > 15 and r.random() < 0.5: x += w + 0.06; continue
            ph = r.uniform(0, 6.3); pts = []
            for i in range(12):
                a = 2 * math.pi * i / 12; e = 1 + 0.12 * math.sin(3*a + ph)
                pts.append(pr(x + w/2 + e*w/2 * math.copysign(abs(math.cos(a))**0.7, math.cos(a)), 0,
                              zz + e*p/2 * math.copysign(abs(math.sin(a))**0.7, math.sin(a))))
            if FX0 - 5 < pts[0][0] < FX1 + 5:
                dz.courbe(pts, 0.2 if z < 9 else 0.15, 0.45 if z < 9 else 0.35, ferme=True)
            x += w + r.uniform(0.04, 0.1)
        z += pas_z
    # la planche posée contre le mur à l'arc
    dz.poly([pr(-1.88, 0.03, 4.7), pr(-0.7, 0.03, 4.5), pr(-0.7, 0.03, 4.68), pr(-1.88, 0.03, 4.88)], "fin")
    dz.L(pr(-0.7, 0.0, 4.5), pr(-0.7, 0.03, 4.5)); dz.L(pr(-1.88, 0, 4.7), pr(-0.7, 0, 4.5), "fin")


# ---------------------------------------------------------------- le fond de la ruelle
def porte_bleue(dz):
    x1, x2, y1, y2 = PORTE; z = Z_FOND; kz = k(z)
    dz.poly(rect_z(z, x1 - 0.12, x2 + 0.12, 0, y2 + 0.14), "fin")                 # le chambranle
    dz.poly(rect_z(z, x1 - 0.2, x2 + 0.2, -0.02, 0.08), "fin")                    # la marche de seuil
    dz.poly(rect_z(z, x1, x2, 0.08, y2), "fort")
    xm = (x1 + x2) / 2
    dz.L(pr(xm, 0.08, z), pr(xm, y2, z), "moyen")
    for a, b in ((x1, xm), (xm, x2)):                                             # 2 battants, 2 panneaux chacun
        for ya, yb in ((0.3, 1.2), (1.4, 2.3)):
            dz.poly(rect_z(z, a + 0.08, b - 0.08, ya, yb), "fin")
            for t in np.linspace(0, 1, 6):                                        # les clous, autour du panneau
                for (px, py) in ((a + 0.08 + t*(b - a - 0.16), yb + 0.05), (a + 0.08 + t*(b - a - 0.16), ya - 0.05)):
                    u, v = pr(px, py, z); dz.rond(u, v, 0.012*kz, 0.15, 0.7)
    u, v = pr(xm + 0.12, 1.3, z); dz.rond(u, v, 0.05*kz, 0.18)                    # le heurtoir
    u, v = pr(xm - 0.12, 1.3, z); dz.rond(u, v, 0.05*kz, 0.18)


def fond(dz):
    r = dz.r
    # le mur de pierre derrière, qui dépasse au-dessus du mur du fond : des moellons
    dz.poly(rect_z(24, -3, 3, 0, 6.6), "fin")
    y = 4.7
    while y < 6.6:
        h = r.uniform(0.22, 0.32); x = -3 + r.uniform(0, 0.3)
        while x < 3:
            w = r.uniform(0.3, 0.6)
            pts = [pr(x + 0.03, min(6.58, y + h - 0.03), 24), pr(x + w - 0.03, min(6.58, y + h - 0.02), 24),
                   pr(x + w - 0.04, y + 0.03, 24), pr(x + 0.02, y + 0.02, 24)]
            dz.courbe(pts, 0.16, 0.55, ferme=True); x += w
        y += h
    cx, cy = pr(0.9, 6.6, 24); rr = 0.35 * k(24)                                  # l'antenne
    dz.courbe([(cx + rr*math.cos(t), cy - rr*math.sin(t)) for t in np.linspace(0, math.pi, 14)], 0.22, ferme=True, fond=FOND)
    dz.L((cx, cy - rr*0.4), (cx + rr*0.9, cy - rr*1.1)); dz.L((cx, cy), (cx, cy + 0.4))
    # le mur du fond, de face
    dz.poly(rect_z(Z_FOND, XL - 0.5, XR + 0.5, 0, H_FOND), "moyen")
    dz.L(pr(XL - 0.5, 0.2, Z_FOND), pr(XR + 0.5, 0.2, Z_FOND))                    # le soubassement
    dz.L(pr(XL - 0.5, H_FOND - 0.15, Z_FOND), pr(XR + 0.5, H_FOND - 0.15, Z_FOND))  # la couvertine
    porte_bleue(dz)
    a, b, ya, yb = FENETRE
    dz.poly(rect_z(Z_FOND, a - 0.05, b + 0.05, ya - 0.05, yb + 0.05), "fin")
    dz.poly(rect_z(Z_FOND, a, b, ya, yb), "moyen")
    for xx in np.linspace(a, b, 4)[1:-1]: dz.L(pr(xx, ya, Z_FOND), pr(xx, yb, Z_FOND))   # la grille
    dz.L(pr(a, (ya + yb)/2, Z_FOND), pr(b, (ya + yb)/2, Z_FOND))
    dz.poly(rect_z(Z_FOND, a - 0.08, b + 0.08, ya - 0.1, ya - 0.05), "fin")       # l'appui
    dz.poly(rect_z(Z_FOND, 0.6, 0.85, 0.6, 0.95), "fin"); dz.poly(rect_z(Z_FOND, 0.64, 0.81, 0.66, 0.89), "fin")  # compteur
    u, v = pr(0.36, 2.62, Z_FOND); dz.rond(u, v, 0.07 * k(Z_FOND), 0.18)          # le numéro
    # le mur droit de la ruelle (il fuit vers le PF)
    dz.poly(rect_x(XR, Z_RUE, Z_FOND, 0, H_RUE_D), "moyen")
    dz.L(pr(XR, 0.2, Z_RUE), pr(XR, 0.2, Z_FOND)); dz.L(pr(XR, H_RUE_D - 0.15, Z_RUE), pr(XR, H_RUE_D - 0.15, Z_FOND))
    for z1, z2, y1, y2 in ((11.5, 11.8, 3.7, 5.1), (13.2, 13.45, 3.5, 4.6), (12.6, 12.75, 1.7, 2.5)):
        dz.poly(rect_x(XR, z1 - 0.04, z2 + 0.04, y1 - 0.05, y2 + 0.05), "fin")
        dz.poly(rect_x(XR, z1, z2, y1, y2), "moyen")
        dz.L(pr(XR, y1, (z1 + z2)/2), pr(XR, y2, (z1 + z2)/2))
        for yy in np.linspace(y1, y2, 4)[1:-1]: dz.L(pr(XR, yy, z1), pr(XR, yy, z2))
    dz.poly(rect_x(XR, 15.5, 15.65, 1.9, 2.15), "fin")                            # l'aération
    dz.poly(rect_x(XR, 12.2, 12.5, 0.3, 0.75), "fin"); dz.poly(rect_x(XR, 12.24, 12.46, 0.36, 0.69), "fin")
    for e in (0, 0.08):                                                           # descente d'eau et colliers
        dz.L(pr(XR, 0.1, 11.42 + e), pr(XR, 4.3, 11.42 + e))
    for yy in (0.8, 1.9, 3.0, 4.0): dz.L(pr(XR, yy, 11.38), pr(XR, yy, 11.54))
    a, b = pr(XR, 4.3, 11.46), pr(XR - 0.45, 4.55, 11.7)                          # la lampe en col de cygne
    dz.courbe([a, (a[0] + 0.4, b[1] - 1.6), (a[0] - 0.3, b[1] - 0.2), b], 0.28)
    dz.poly([(b[0] - 0.9, b[1]), (b[0] + 0.9, b[1]), (b[0] + 0.5, b[1] + 1.1), (b[0] - 0.5, b[1] + 1.1)], "fin")
    c2 = pr(XR - 0.05, 3.0, 12.9)
    dz.courbe([(b[0], b[1] + 1.1), ((b[0] + c2[0]) / 2, (b[1] + c2[1]) / 2 + 3), c2], 0.16, 0.6)   # le câble
    # le mur gauche de la ruelle
    dz.poly(rect_x(XL, Z_RUE, Z_FOND, 0, H_RUE_G), "moyen")
    dz.L(pr(XL, 0.2, Z_RUE), pr(XL, 0.2, Z_FOND))
    # le moucharabieh en fer forgé : un ventre arrondi, des barreaux, des volutes
    z1 = 16.6; kz = k(z1)
    h, b, v = pr(XL, 6.1, z1), pr(XL + 0.55, 6.1, z1), pr(XL + 0.55, 5.3, z1)
    bas = pr(XL, 4.7, z1)
    ventre = [h, b, v] + [(v[0] + (bas[0] - v[0]) * (1 - math.cos(t)), v[1] + (bas[1] - v[1]) * math.sin(t)) for t in np.linspace(0, math.pi/2, 10)]
    dz.courbe(ventre, 0.3, ferme=True, fond=FOND)
    dz.L((h[0], h[1] + 0.5), (b[0], b[1] + 0.5))
    for i in range(1, 6):
        x = h[0] + (b[0] - h[0]) * i / 6
        t = math.acos(max(-1, min(1, 1 - (x - v[0]) / (bas[0] - v[0] - 1e-9)))) if x < v[0] else 0
        yb = v[1] + (bas[1] - v[1]) * math.sin(t)
        dz.L((x, h[1] + 0.5), (x, yb - 0.2))
    rr = (b[0] - h[0]) / 6
    for i, (cx, cy) in enumerate(((h[0] + rr*1.5, h[1] + rr*3), (h[0] + rr*4.4, h[1] + rr*3), (h[0] + rr*3, h[1] + rr*6.5),
                                  (h[0] + rr*1.5, h[1] + rr*10), (h[0] + rr*4.4, h[1] + rr*10))):
        dz.spirale(cx, cy, rr*1.1, 1.4, 1 if i % 2 else -1, 0.18)
    dz.courbe([pr(XL, 4.75, z1 - 0.1), pr(XL + 0.25, 4.95, z1), pr(XL + 0.15, 4.4, z1)], 0.2)   # la console
    # la lanterne sur sa potence
    zl = 15.5; kz = k(zl)
    a, b = pr(XL, 3.55, zl), pr(XL + 1.25, 3.55, zl)
    dz.L(a, b, "moyen"); dz.L((a[0], a[1] - 0.3*kz), (a[0], a[1] + 0.25*kz), "moyen")
    for i in range(3):                                                            # les volutes sous la potence
        cx = a[0] + (i + 0.6) * (b[0] - a[0]) / 3.6
        dz.spirale(cx, a[1] + 0.13*kz, 0.11*kz, 1.3, 1 if i % 2 else -1, -1.5, 0.18)
    dz.courbe([(a[0], a[1] + 0.25*kz), (a[0] + 0.5*(b[0] - a[0]), a[1] + 0.05*kz), b], 0.18)
    lx, ly = b[0], b[1]; s = 0.1 * kz                                             # s : 10 cm
    dz.L((lx, ly), (lx, ly + 0.4*s))
    dz.courbe([(lx - 2.2*s, ly + 1.2*s), (lx, ly + 0.4*s), (lx + 2.2*s, ly + 1.2*s)], 0.22)        # le chapeau
    dz.poly([(lx - 2.2*s, ly + 1.2*s), (lx + 2.2*s, ly + 1.2*s), (lx + 1.6*s, ly + 1.5*s), (lx - 1.6*s, ly + 1.5*s)], "fin")
    corps = [(lx - 1.6*s, ly + 1.5*s), (lx + 1.6*s, ly + 1.5*s), (lx + 1.0*s, ly + 4.3*s), (lx - 1.0*s, ly + 4.3*s)]
    dz.poly(corps, "fin")
    for t in (-0.45, 0.45): dz.L((lx + t*1.6*s, ly + 1.5*s), (lx + t*1.0*s, ly + 4.3*s))
    dz.poly([(lx - 1.0*s, ly + 4.3*s), (lx + 1.0*s, ly + 4.3*s), (lx, ly + 5.3*s)], "fin")
    dz.L((lx, ly + 5.3*s), (lx, ly + 5.8*s))


# ---------------------------------------------------------------- à gauche : le mur à l'arc et le pilier
def gauche(dz):
    X = XL_PLACE
    f = rect_x(X, 2, Z_RUE, 0, 14)
    dz.poly(f, "fort")
    dz.L(pr(X, 0.25, 2), pr(X, 0.25, Z_RUE))                                      # le soubassement
    # l'arc en plein cintre : piédroits et claveaux en pierre taillée, fond en briques
    za, zb, ys, R0, R1 = 8.7, 10.5, 2.6, 0.9, 1.22
    zc = (za + zb) / 2
    def contour(x, ray):
        return ([pr(x, 0, zc - ray), pr(x, ys, zc - ray)] +
                [pr(x, ys + ray * math.sin(t), zc - ray * math.cos(t)) for t in np.linspace(0, math.pi, 30)] +
                [pr(x, ys, zc + ray), pr(x, 0, zc + ray)])
    ouv = contour(X, R0)
    # par l'ouverture, on voit en biais l'épaisseur du mur (côté fond) : un plan de face, en briques
    ep = 0.45
    tab = Crayon(41)
    tab.trait(pr(X - ep, 0, zb), pr(X - ep, ys + R0, zb), "fin", op=0.8, depasse=False)
    yb, rang = 0.0, 0
    while yb < ys + R0:
        tab.trait(pr(X, yb, zb), pr(X - ep, yb, zb), "fin", op=0.5, depasse=False)
        xj = X - (0.15 if rang % 2 else 0.3)
        tab.trait(pr(xj, yb, zb), pr(xj, yb + 0.2, zb), "fin", op=0.5, depasse=False)
        yb += 0.2; rang += 1
    dz.clip(ouv, "".join(tab.out))
    dz.courbe(ouv, 0.32)
    dz.courbe([pr(X, ys + R1 * math.sin(t), zc - R1 * math.cos(t)) for t in np.linspace(0, math.pi, 30)], 0.3)
    for i in range(1, 13):                                                        # les claveaux : joints rayonnants
        t = math.pi * i / 13
        ext = R1 + (0.12 if i in (6, 7) else 0)                                   # la clé dépasse un peu
        dz.L(pr(X, ys + R0 * math.sin(t), zc - R0 * math.cos(t)), pr(X, ys + ext * math.sin(t), zc - ext * math.cos(t)))
    t6, t7 = math.pi * 6 / 13, math.pi * 7 / 13
    dz.L(pr(X, ys + (R1 + 0.12) * math.sin(t6), zc - (R1 + 0.12) * math.cos(t6)),
         pr(X, ys + (R1 + 0.12) * math.sin(t7), zc - (R1 + 0.12) * math.cos(t7)))
    for cote in (-1, 1):                                                          # les piédroits : pierres alternées
        y = 0; j = 0
        while y < ys - 0.05:
            h = 0.32; w = 0.38 if j % 2 else 0.24
            z0 = zc + cote * R0
            dz.poly(rect_x(X, min(z0, z0 + cote * w), max(z0, z0 + cote * w), y, min(ys, y + h)), "fin")
            y += h; j += 1
        dz.L(pr(X, ys, zc + cote * R0), pr(X, ys, zc + cote * R1))                # l'imposte
    # la fenêtre haute et étroite, à deux volets à panneaux
    z1, z2, y1, y2 = 9.7, 10.3, 4.4, 6.9
    dz.poly(rect_x(X, z1 - 0.06, z2 + 0.06, y1 - 0.06, y2 + 0.06), "fin")
    dz.poly(rect_x(X, z1, z2, y1, y2), "moyen")
    zm = (z1 + z2) / 2; dz.L(pr(X, y1, zm), pr(X, y2, zm))
    for a, b in ((z1, zm), (zm, z2)):
        for ya, yb in ((y1 + 0.12, y1 + 1.15), (y1 + 1.3, y2 - 0.12)):
            dz.poly(rect_x(X, a + 0.05, b - 0.05, ya, yb), "fin")
    dz.poly(rect_x(X, z1 - 0.12, z2 + 0.12, y1 - 0.14, y1 - 0.06), "fin")          # l'appui
    # la descente d'eau : tuyau, colliers, dauphin en bas
    for e in (0, 0.12):
        dz.L(pr(X, 0.35, 7.4 + e), pr(X, 14, 7.4 + e))
    for y in (1.2, 2.9, 4.6, 6.3):
        dz.L(pr(X, y, 7.34), pr(X, y, 7.58)); dz.L(pr(X, y + 0.08, 7.34), pr(X, y + 0.08, 7.58))
    dz.courbe([pr(X, 0.35, 7.4), pr(X, 0.15, 7.32), pr(X, 0.08, 7.2)], 0.22)
    dz.courbe([pr(X, 0.35, 7.52), pr(X, 0.12, 7.48), pr(X, 0.05, 7.3)], 0.22)
    # le mur de face à l'entrée de la ruelle, et le pilier au panneau « rue du Tribunal »
    dz.poly(rect_z(Z_RUE, X, XL, 0, 14), "fort")
    dz.poly(rect_z(10.7, -1.55, XL, 0, 3.4), "moyen")
    dz.poly([pr(XL, 3.4, 10.7), pr(XL, 3.4, Z_RUE), pr(XL, 0, Z_RUE), pr(XL, 0, 10.7)], "fin")
    for y in (3.25, 3.15): dz.L(pr(-1.55, y, 10.7), pr(XL, y, 10.7))              # la corniche du pilier
    dz.L(pr(-1.55, 0.25, 10.7), pr(XL, 0.25, 10.7)); dz.L(pr(XL, 0.25, 10.7), pr(XL, 0.25, Z_RUE))
    zp = 10.68; kz = k(zp)
    dz.poly(rect_z(zp, -1.5, -1.12, 2.45, 2.75), "moyen")
    dz.poly(rect_z(zp, -1.48, -1.14, 2.47, 2.73), "fin")
    u, v = pr(-1.31, 2.66, zp); dz.c.texte(u, v + 0.4, "نهج التريبونال", 0.09 * kz, GRIS, "middle", halo=False)
    u, v = pr(-1.31, 2.52, zp); dz.c.texte(u, v + 0.3, "Rue du Tribunal", 0.055 * kz, GRIS, "middle", halo=False)
    dz.poly(rect_z(zp, -1.52, -1.1, 1.95, 2.02), "fin")                           # la tablette de marbre
    dz.poly([pr(-1.52, 1.95, zp), pr(-1.1, 1.95, zp), pr(-1.1, 1.95, 10.5), pr(-1.52, 1.95, 10.5)], "fin")


# ---------------------------------------------------------------- à droite : le mur au portail
def portail(dz):
    z = Z_RUE; kz = k(z); x1, x2 = 2.4, 4.2
    dz.poly(rect_z(z, x1 - 0.06, x2 + 0.06, 0.12, 2.78), "moyen")
    dz.poly(rect_z(z, x1, x2, 2.22, 2.72), "moyen")                               # la grille en fer forgé
    n = 6; w = (x2 - x1) / n
    for i in range(n):
        a = x1 + i * w
        if i: dz.L(pr(a, 2.22, z), pr(a, 2.72, z))
        cx, cy = pr(a + w/2, 2.47, z); r = 0.1 * kz
        dz.spirale(cx - r*0.55, cy, r*0.6, 1.3, 1, 0, 0.18)                       # deux volutes en C, dos à dos
        dz.spirale(cx + r*0.55, cy, r*0.6, 1.3, -1, math.pi, 0.18)
        dz.rond(cx, cy - r*1.0, r*0.22, 0.16); dz.rond(cx, cy + r*1.0, r*0.22, 0.16)
    dz.poly(rect_z(z, x1, x2, 0.12, 2.2), "fort")                                 # les deux battants en tôle
    xm = (x1 + x2) / 2 + 0.1
    dz.L(pr(xm, 0.12, z), pr(xm, 2.2, z), "moyen")
    for a, b in ((x1, xm), (xm, x2)):
        dz.poly(rect_z(z, a + 0.06, b - 0.06, 0.2, 2.12), "fin")
        dz.L(pr(a + 0.06, 1.15, z), pr(b - 0.06, 1.15, z))
    dz.poly(rect_z(z, xm - 0.14, xm - 0.02, 1.0, 1.25), "fin")                    # la serrure
    u, v = pr(xm - 0.08, 1.07, z); dz.rond(u, v, 0.02 * kz, 0.15)
    dz.L(pr(xm + 0.03, 1.12, z), pr(xm + 0.15, 1.12, z))                          # la poignée
    dz.poly(rect_z(z, x2 - 0.55, x2 - 0.45, 1.9, 1.98), "fin")                    # le petit verrou
    # le cœur tagué « M + D », juste au trait
    cx, cy = pr(2.95, 1.35, z); s = 0.32 * kz
    dz.courbe([(cx + s*0.95*math.sin(t)**3, cy - s*(0.8*math.cos(t) - 0.3*math.cos(2*t) - 0.12*math.cos(3*t) - 0.05*math.cos(4*t)))
               for t in np.linspace(0, 2*math.pi, 40)], 0.25, 0.7)
    dz.c.texte(cx - s*0.1, cy - s*1.15, "M+D", 0.3 * kz, GRIS, "middle", halo=False)


def droite(dz):
    z = Z_RUE
    haut = [(XR, 5.8), (4.5, 5.15), (9, 5.15)]
    dz.poly([pr(x, y, z) for x, y in haut] + [pr(9, 0, z), pr(XR, 0, z)], "fort")
    dz.c.trait(pr(XR, 5.8, z), pr(XR, 0, z), "fort", double=True, depasse=False)   # l'arête du coin
    dz.courbe([pr(XR, 5.65, z), pr(4.5, 5.0, z), pr(9, 5.0, z)], 0.2, 0.7)        # la couvertine
    dz.L(pr(XR, 0.18, z), pr(9, 0.18, z))                                         # le soubassement
    dz.L(pr(XR, 2.6, z), pr(XR + 0.35, 2.6, z)); dz.L(pr(XR + 0.35, 2.6, z), pr(XR + 0.35, 2.75, z))   # le petit rebord
    portail(dz)
    for x, w, h in ((1.75, 0.35, 0.32), (2.05, 0.4, 0.42), (2.3, 0.3, 0.26)):    # les sacs posés au pied du mur
        a, b, t = pr(x, 0, 10.75), pr(x + w, 0, 10.75), pr(x + w/2, h, 10.75)
        pts = [a] + [((1-s)**2*a[0] + 2*(1-s)*s*a[0] + s*s*t[0], (1-s)**2*a[1] + 2*(1-s)*s*t[1] + s*s*t[1]) for s in np.linspace(0, 1, 8)] \
              + [((1-s)**2*t[0] + 2*(1-s)*s*b[0] + s*s*b[0], (1-s)**2*t[1] + 2*(1-s)*s*t[1] + s*s*b[1]) for s in np.linspace(0, 1, 8)]
        dz.courbe(pts, 0.25, ferme=True, fond=FOND)
        dz.L((t[0] - 0.6, t[1] + 0.4), (t[0] + 0.6, t[1] + 0.4))                  # le nœud
        dz.courbe([(t[0] - 1.2, t[1] + 2.2), (t[0] - 0.4, t[1] + 3.4), (t[0] + 0.2, (t[1] + a[1]) / 2 + 1)], 0.15, 0.6)  # un pli


# ---------------------------------------------------------------- premier plan : fil, treille, passants
def passant(dz, x, z, sens):
    """une personne debout de 1,75 m : comme on est assis (yeux à 1,20 m), la LH lui passe à la poitrine"""
    P = lambda dx, y: pr(x + dx * sens, y, z)
    pd = "moyen" if z < 10 else "fin"
    for j, (a, b) in enumerate(((-0.13, -0.02), (0.02, 0.13))):                  # jambes, l'une devant l'autre
        d = -0.13 if j == 0 else 0.1
        dz.c.poly([P(a, 0.92), P(b, 0.92), P(b + d*0.9 + 0.01, 0.05), P(a + d - 0.01, 0.03)], pd, depasse=False)
        dz.L(P(a + d - 0.03, 0.02), P(b + d*0.9 + 0.06, 0.02), pd)
    dz.c.poly([P(-0.06, 1.53), P(0.06, 1.53), P(0.19, 1.47), P(0.21, 1.36), P(0.15, 0.9), P(-0.15, 0.9), P(-0.21, 1.36), P(-0.19, 1.47)], pd, depasse=False)
    dz.L(P(-0.05, 1.52), P(0, 1.42)); dz.L(P(0.05, 1.52), P(0, 1.42))             # le col
    dz.L(P(-0.15, 0.98), P(0.15, 0.98))                                           # la ceinture
    dz.L(P(-0.19, 1.42), P(-0.25, 0.9), pd); dz.L(P(0.19, 1.42), P(0.27, 0.92), pd)
    t = pr(x, 1.645, z); rx, ry = 0.085 * k(z), 0.11 * k(z)
    dz.courbe([(t[0] + rx*math.cos(a), t[1] + ry*math.sin(a)) for a in np.linspace(0, 2*math.pi, 18)[:-1]], 0.3, ferme=True, fond=FOND)
    dz.courbe([(t[0] - rx*0.95, t[1] - ry*0.1), (t[0] - rx*0.4, t[1] - ry*0.9), (t[0] + rx*0.5, t[1] - ry*0.85), (t[0] + rx*0.95, t[1] - ry*0.1)], 0.2, 0.7)


def lisse(pts, n=4):
    """courbe fermée lissée passant par les points (Catmull-Rom)"""
    out = []; m = len(pts)
    for i in range(m):
        p0, p1, p2, p3 = (np.array(pts[(i + j) % m]) for j in (-1, 0, 1, 2))
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(tuple(0.5 * ((2*p1) + (-p0 + p2)*t + (2*p0 - 5*p1 + 4*p2 - p3)*t*t + (-p0 + 3*p1 - 3*p2 + p3)*t**3)))
    return out


def feuille(dz, x, y, s, a):
    pts = [(0, -s), (0.38*s, -0.62*s), (0.5*s, -0.1*s), (0.3*s, 0.25*s), (0, 0.12*s), (-0.3*s, 0.25*s), (-0.5*s, -0.1*s), (-0.38*s, -0.62*s)]
    rot = lambda p: (x + p[0]*math.cos(a) - p[1]*math.sin(a), y + p[0]*math.sin(a) + p[1]*math.cos(a))
    dz.courbe(lisse([rot(p) for p in pts]), 0.22, 0.8, ferme=True, fond=FOND)
    dz.courbe([rot((0, 0.12*s)), rot((0.05*s, -0.4*s)), rot((0, -0.85*s))], 0.15, 0.6)


def premier_plan(dz):
    r = dz.r
    # le fil tendu au-dessus de la placette
    a, b = pr(XL, 8.5, Z_RUE), pr(4.3, 5.1, 10.9)
    m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 5)
    dz.courbe([((1-t)**2*a[0] + 2*(1-t)*t*m[0] + t*t*b[0], (1-t)**2*a[1] + 2*(1-t)*t*m[1] + t*t*b[1]) for t in np.linspace(0, 1, 24)], 0.22)
    # la treille qui pend en haut à droite : branches et grappes de feuilles
    for branche in ([(6.5, 6.75), (5.0, 6.45), (3.6, 6.3), (2.5, 6.35), (1.7, 6.15)], [(5.6, 6.05), (4.6, 5.85), (3.7, 5.72), (2.8, 5.68)]):
        pts = [pr(x, y, 9) for x, y in branche]
        dz.courbe(pts, 0.45); dz.courbe([(x, y + 0.6) for x, y in pts], 0.25, 0.7)
        for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
            for t in np.linspace(0.05, 0.95, 8):
                px, py = x0 + (x1 - x0)*t, y0 + (y1 - y0)*t
                fx, fy = px + r.uniform(-4, 4), py + r.uniform(-4, 8)
                dz.L((px, py), (fx, fy), "fin", op=0.6)
                feuille(dz, fx, fy, r.uniform(3.2, 4.6), r.uniform(-1.0, 1.0) + (math.pi if fy > py else 0))
    for x, z, sens in sorted(PASSANTS, key=lambda p: -p[1]):
        passant(dz, x, z, sens)


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
    fuy = [pr(XL_PLACE, 0, 5), pr(XL_PLACE, 2.6, 5), pr(XL, 0, Z_RUE), pr(XR, 0, Z_RUE), pr(XR, H_RUE_D, Z_RUE),
           pr(XR, 3.7, 11.5), pr(XR, 5.1, 11.5), pr(XL_PLACE, 6.9, 9.7), pr(XL_PLACE, 4.4, 9.7)]
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
    # annotations
    c.texte(FX0 + 3, LHY + 4.4, "LH : à hauteur des yeux, ASSIS (1,20 m)", 2.9, CON)
    c.texte(FX0 + 3, LHY + 8, "plus bas que la photo, prise debout", 2.9, CON)
    p = pr(PORTE[0], PORTE[3], Z_FOND)
    c.texte(p[0] - 1.5, p[1] - 8.5, "la porte bleue, à 20 m :", 2.8, CON, "end")
    c.texte(p[0] - 1.5, p[1] - 5.2, "petite, coupée par la LH", 2.8, CON, "end")
    c.trait((p[0] - 1.2, p[1] - 5.6), (p[0] + 0.4, p[1] + 0.6), "construction", CON, 0.9, depasse=False)
    q = pr(XR, 4.4, 11.6)
    c.texte(q[0] + 3, q[1] - 1, "les murs de la ruelle", 2.8, CON)
    c.texte(q[0] + 3, q[1] + 2.4, "fuient vers le PF", 2.8, CON)
    c.texte(FX1 - 3, 132, "mur de face : vraie forme,", 2.8, CON, "end")
    c.texte(FX1 - 3, 135.4, "horizontales horizontales", 2.8, CON, "end")
    q = pr(XL_PLACE, 0.6, 5.2)
    c.texte(q[0] + 3, q[1] - 3, "mur à l'arc : il fuit vers le PF", 2.8, CON, rot=math.degrees(math.atan2(LHY - q[1], CX - q[0])))
    t = pr(PASSANTS[0][0], 1.75, PASSANTS[0][1])
    c.trait((t[0] - 1, 165.5), (t[0] - 0.5, t[1] - 1.2), "construction", CON, 0.9, depasse=False)
    for i, l in enumerate(["les passants DEBOUT (1,75 m) :", "leur tête dépasse la LH, qui leur",
                           "passe à la poitrine → tu es assis"]):
        c.texte(t[0] - 3, 154 + i*3.6, l, 2.9, CON)
    return "".join(c.out)


def dessin():
    dz = Dessin(31)
    sol(dz); fond(dz); droite(dz); gauche(dz); premier_plan(dz)
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
              "5  les détails : pierres de l'arc, porte, fer forgé, lanterne, pavés",
              "6  les passants debout : la LH leur passe à la poitrine"]
    for i, e in enumerate(etapes):
        t.texte(FX0 + (i // 3) * 134, 28.5 + (i % 3) * 3.9, e, 2.9, CON)
    for i, l in enumerate(["en bleu : la construction (LH, LT, PF, fuyantes) · au crayon : le croquis, au trait, sans hachures",
                           "carreaux bleus de 3 cm, partant du PF, pour reporter le dessin",
                           "dessiné depuis ta place, pas depuis le téléphone : yeux à 1,20 m, regard droit devant",
                           "le support en fer forgé de la photo est au-dessus du regard : hors cadre"]):
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

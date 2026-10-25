"""Croquis « à la main » de la ruelle à la porte bleue, vue d'une personne ASSISE, en perspective frontale.

Ce n'est pas un calque de la photo du téléphone (prise debout, en zoom, cadrée en hauteur) :
la scène est reconstruite en 3D d'après la photo, puis dessinée depuis la place de l'élève :
assis (yeux à 1,20 m), face à la porte du fond, un tout petit peu à droite, à 20 m d'elle,
avec un champ de vision naturel (environ 55° en largeur).

Repère : x vers la droite, y vers le haut, z en profondeur depuis l'œil (en m).
Sorties : croquis-A3.html (A3 paysage) et croquis-2xA4.html (les deux moitiés de l'A3 à l'échelle 1),
à rendre en PDF avec ../perspective-frontale-rue/rendu.js.
"""
import math, random, sys, os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "perspective-frontale-rue"))
from croquis import Crayon, html, FOND, GRIS, CON  # même crayon que le croquis de la rue (fig. 44)

ICI = sys.argv[1] if len(sys.argv) > 1 else "."
PAGE_W, PAGE_H = 420, 297
FX0, FY0, FX1, FY1 = 15, 34, 405, 272      # le cadre (39 x 24 cm)
OEIL = 1.20                                # assis : les yeux à 1,20 m du sol
F = 375                                    # distance principale (mm) : 55° de champ sur 39 cm
CX, LHY = 210, 194                         # le PF : au milieu du cadre, LH à 16 cm du haut
PF = (CX, LHY)
ZT = F * OEIL / (FY1 - LHY)                # le tableau : son pied (la LT) est le bas du cadre


def pr(x, y, z):
    return (CX + F * x / z, LHY - F * (y - OEIL) / z)


# ---------------------------------------------------------------- la scène (relevée sur la photo, en m)
XL_PLACE = -1.9        # façade à l'arc, à gauche de la placette
XL, XR = -1.0, 1.3     # murs de la ruelle
Z_RUE, Z_FOND = 11, 20 # entrée de la ruelle, mur du fond (la porte bleue est à 20 m)
PORTE = (-0.85, 0.15, 0, 2.5)          # x1, x2, y1, y2 : on est un peu à droite de la porte
FENETRE = (0.55, 0.87, 1.55, 2.35)
H_FOND, H_RUE_D, H_RUE_G = 4.9, 6.0, 11


class Dessin:
    def __init__(self, graine):
        self.c = Crayon(graine); self.defs = []; self.n = 0; self.r = random.Random(graine + 1)

    def clip(self, pts, contenu):
        self.n += 1; pid = f"c{self.n}"
        self.defs.append(f'<clipPath id="{pid}"><polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}"/></clipPath>')
        self.c.out.append(f'<g clip-path="url(#{pid})">{contenu}</g>')

    def hachures(self, pts, pas=0.9, angle=60, op=0.45, poids="fin"):
        """hachures parallèles dans un polygone (ombre, matière sombre)"""
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        R = math.hypot(max(xs) - min(xs), max(ys) - min(ys)) / 2 + 1
        a = math.radians(angle); u = np.array([math.cos(a), -math.sin(a)]); n = np.array([u[1], -u[0]])
        s = Crayon(self.r.randrange(10**6)); t = -R
        while t < R:
            p = np.array([cx, cy]) + n * t
            s.trait(p - u * R, p + u * R, poids, "#3a3a3a", op, depasse=False); t += pas
        self.clip(pts, "".join(s.out))

    def ovale(self, pts, op=0.5, lw=0.2):
        """petite forme fermée tremblée (pavé, boucle de fer forgé, feuille)"""
        r = self.r
        q = [(x + r.uniform(-0.08, 0.08), y + r.uniform(-0.08, 0.08)) for x, y in pts]
        d = " ".join(f"{x:.2f},{y:.2f}" for x, y in q + q[:1])
        self.c.out.append(f'<polyline points="{d}" fill="none" stroke="{GRIS}" stroke-width="{lw}" stroke-opacity="{op}" '
                          f'stroke-linecap="round" stroke-linejoin="round"/>')


def rect_x(dz, x, z1, z2, y1, y2):          # rectangle sur un mur parallèle à la ruelle (plan x = cte)
    return [pr(x, y2, z1), pr(x, y2, z2), pr(x, y1, z2), pr(x, y1, z1)]


def rect_z(z, x1, x2, y1, y2):              # rectangle de face (plan z = cte) : il garde sa vraie forme
    return [pr(x1, y2, z), pr(x2, y2, z), pr(x2, y1, z), pr(x1, y1, z)]


def sol(dz):
    """pavés : des rangées d'ovales, de plus en plus petits et serrés vers le PF"""
    r = dz.r
    z = ZT - 0.3
    while z < Z_FOND:
        dzr = 0.24 + 0.02 * z
        xg = XL_PLACE if z < Z_RUE else XL
        xd = 9 if z < Z_RUE else XR
        x = xg + r.uniform(0, 0.3)
        while x < xd - 0.1:
            w = r.uniform(0.16, 0.38); p = r.uniform(0.1, 0.2); zz = z + r.uniform(-0.04, 0.04)
            if z > 15 and r.random() < 0.5: x += w + 0.06; continue
            pts = []
            ph = r.uniform(0, 6.3)
            for i in range(12):
                a = 2 * math.pi * i / 12
                e = 1 + 0.12 * math.sin(3*a + ph)
                pts.append(pr(x + w/2 + e*w/2 * math.copysign(abs(math.cos(a))**0.7, math.cos(a)), 0,
                              zz + e*p/2 * math.copysign(abs(math.sin(a))**0.7, math.sin(a))))
            u0 = pts[0][0]
            if FX0 - 5 < u0 < FX1 + 5:
                dz.ovale(pts, op=0.42 if z < 9 else 0.32, lw=0.2 if z < 9 else 0.15)
            x += w + r.uniform(0.04, 0.1)
        z += dzr


def fond(dz):
    c = dz.c
    # le mur de pierre, derrière, qui dépasse au-dessus du mur du fond, et l'antenne
    m = rect_z(24, -3, 3, 0, 6.6)
    c.poly(m, "fin")
    dz.hachures(m, pas=1.4, angle=20, op=0.28)
    cx, cy = pr(0.9, 6.6, 24); rr = F * 0.35 / 24
    c.out.append(f'<path d="M{cx-rr:.2f},{cy:.2f} A{rr:.2f},{rr:.2f} 0 0 1 {cx+rr:.2f},{cy:.2f}" fill="{FOND}" stroke="{GRIS}" stroke-width="0.22" stroke-opacity="0.8"/>')
    # le mur du fond, de face, et la porte bleue
    c.poly(rect_z(Z_FOND, XL - 0.5, XR + 0.5, 0, H_FOND), "moyen")
    x1, x2, y1, y2 = PORTE
    p = rect_z(Z_FOND, x1, x2, y1, y2)
    c.poly(p, "fort", fond="#5a6b78")
    dz.hachures(p, pas=0.45, angle=90, op=0.7)
    c.trait(pr((x1 + x2)/2, y1, Z_FOND), pr((x1 + x2)/2, y2, Z_FOND), "fin", op=0.8, depasse=False)
    for y in (0.6, 1.6):
        c.trait(pr(x1 + 0.07, y, Z_FOND), pr(x2 - 0.07, y, Z_FOND), "fin", op=0.6, depasse=False)
    c.trait(pr(x1 - 0.08, y2 + 0.08, Z_FOND), pr(x2 + 0.08, y2 + 0.08, Z_FOND), "fin", depasse=False)   # linteau
    f = rect_z(Z_FOND, *FENETRE)
    c.poly(f, "moyen", fond="#5a6b78"); dz.hachures(f, pas=0.45, angle=90, op=0.7)
    c.poly(rect_z(Z_FOND, 0.6, 0.85, 0.6, 0.95), "fin")                      # le compteur
    c.trait(pr(0.3, 2.65, Z_FOND), pr(0.42, 2.65, Z_FOND), "fin", depasse=False)   # le numéro
    # les murs de la ruelle (ils fuient vers le PF)
    d = rect_x(dz, XR, Z_RUE, Z_FOND, 0, H_RUE_D)
    c.poly(d, "moyen")
    dz.hachures(d, pas=1.1, angle=75, op=0.22)
    for z1, z2, y1, y2 in ((11.5, 11.8, 3.7, 5.1), (13.2, 13.45, 3.5, 4.6), (12.6, 12.75, 1.7, 2.5), (15.5, 15.65, 1.9, 2.15)):
        w = rect_x(dz, XR, z1, z2, y1, y2); c.poly(w, "fin", fond="#5a6b78"); dz.hachures(w, pas=0.4, angle=90, op=0.6)
    c.poly(rect_x(dz, XR, 12.2, 12.5, 0.3, 0.75), "fin")
    c.trait(pr(XR, 0, 11.45), pr(XR, 4.3, 11.45), "fin", depasse=False)       # descente d'eau
    a, b = pr(XR, 4.3, 11.45), pr(XR, 4.55, 11.7)
    c.out.append(f'<path d="M{a[0]:.2f},{a[1]:.2f} Q{a[0]+0.2:.2f},{b[1]-1.4:.2f} {b[0]-1.6:.2f},{b[1]:.2f}" fill="none" stroke="{GRIS}" stroke-width="0.3" stroke-opacity="0.85"/>')
    a2 = pr(XR - 0.6, 3.1, 12.8)
    c.trait((b[0] - 1.6, b[1] + 0.6), a2, "fin", op=0.6, depasse=False)      # le câble de la lampe
    g = rect_x(dz, XL, Z_RUE, Z_FOND, 0, H_RUE_G)
    c.poly(g, "moyen")
    dz.hachures(g, pas=1.0, angle=105, op=0.3)
    # le moucharabieh en fer forgé (en haut de la ruelle, à gauche) : un ventre arrondi
    z1, z2 = 16.6, 17.6
    h, b, v = pr(XL, 6.1, z1), pr(XL + 0.55, 6.1, z1), pr(XL + 0.55, 5.3, z1)
    bas = pr(XL, 4.7, z1)
    ventre = (f'M{h[0]:.2f},{h[1]:.2f} L{b[0]:.2f},{b[1]:.2f} L{v[0]:.2f},{v[1]:.2f} '
              f'Q{v[0]:.2f},{bas[1]:.2f} {bas[0]:.2f},{bas[1]:.2f} Z')
    c.out.append(f'<path d="{ventre}" fill="{FOND}" stroke="{GRIS}" stroke-width="0.3" stroke-opacity="0.85"/>')
    n = 5
    for i in range(1, n):
        x = h[0] + (b[0] - h[0]) * i / n
        yb = v[1] + (bas[1] - v[1]) * (1 - (i / n) ** 2) ** 0.5 * 0.85
        c.trait((x, h[1] + 0.4), (x, yb), "fin", op=0.7, depasse=False)
    rr = (b[0] - h[0]) / 5
    for cx_, cy_ in ((h[0] + rr*1.4, h[1] + rr*2.2), (h[0] + rr*3.4, h[1] + rr*4.2), (h[0] + rr*1.6, h[1] + rr*6)):
        spi = [(cx_ + rr*(0.25 + 0.75*t/12)*math.cos(t), cy_ + rr*(0.25 + 0.75*t/12)*math.sin(t)) for t in np.linspace(0, 12, 22)]
        c.out.append(f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in spi)}" fill="none" stroke="{GRIS}" stroke-width="0.2" stroke-opacity="0.75"/>')
    c.trait(pr(XL + 0.55, 6.1, z1), pr(XL + 0.55, 6.1, z2), "fin", depasse=False)
    # la lanterne sur sa potence
    zl = 15.5
    a = pr(XL, 3.55, zl); b = pr(XL + 1.25, 3.55, zl)
    c.trait(a, b, "moyen", depasse=False)
    k = F / zl / 100                                                          # mm par cm à cette distance
    for i in range(3):
        cx_ = a[0] + (i + 0.7) * (b[0] - a[0]) / 3.4
        dz.ovale([(cx_ + 1.4*k*10*math.cos(t)/3, a[1] + 1.1*k*10*math.sin(t)/3 + 0.8) for t in np.linspace(0, 2*math.pi, 9)[:-1]], 0.6, 0.18)
    lx, ly = b[0], b[1]
    corps = [(lx - 0.9*k*10, ly - 3.6*k*10), (lx + 0.9*k*10, ly - 3.6*k*10), (lx + 0.55*k*10, ly - 0.6*k*10), (lx - 0.55*k*10, ly - 0.6*k*10)]
    c.poly(corps, "fin")
    c.poly([(lx - 1.2*k*10, ly - 3.6*k*10), (lx + 1.2*k*10, ly - 3.6*k*10), (lx, ly - 4.6*k*10)], "fin")
    c.trait((lx, ly - 0.6*k*10), (lx, ly), "fin", depasse=False)


def gauche(dz):
    c = dz.c
    # la façade à l'arc (elle fuit vers le PF), du bord du cadre jusqu'à l'entrée de la ruelle
    f = rect_x(dz, XL_PLACE, 2, Z_RUE, 0, 14)
    c.poly(f, "fort")
    dz.hachures(f, pas=3.2, angle=100, op=0.07)
    # l'arc en plein cintre, à l'encadrement de briques
    za, zb, ys = 8.7, 10.5, 2.75
    zc, rz = (za + zb) / 2, (zb - za) / 2
    def arc(e):
        pts = [pr(XL_PLACE, 0, za + e), pr(XL_PLACE, ys, za + e)]
        pts += [pr(XL_PLACE, ys + (rz - e) * 0.55 * math.sin(t), zc - (rz - e) * math.cos(t)) for t in np.linspace(0, math.pi, 24)]
        return pts + [pr(XL_PLACE, ys, zb - e), pr(XL_PLACE, 0, zb - e)]
    ext, inte = arc(0), arc(0.22)
    c.poly(ext, "moyen", fond="#ece6dc")
    for y in np.arange(0.2, ys + 1.0, 0.28):                                 # les briques
        for z0 in np.arange(za + 0.02, zb - 0.02, 0.22):
            if y > ys and abs(z0 + 0.1 - zc) > (rz) * math.sqrt(max(0, 1 - ((y - ys) / (rz * 0.55))**2)): continue
            c.trait(pr(XL_PLACE, y, z0), pr(XL_PLACE, y, z0 + 0.15), "fin", op=0.45, depasse=False)
    c.poly(inte, "fin", fond="#cfc8bd")
    dz.hachures(inte, pas=0.5, angle=90, op=0.5)
    # la fenêtre haute et étroite, à volets
    w = rect_x(dz, XL_PLACE, 9.7, 10.3, 4.4, 6.9)
    c.poly(w, "moyen", fond="#5a6b78"); dz.hachures(w, pas=0.45, angle=90, op=0.65)
    # la descente d'eau, avec ses colliers
    for e in (0, 0.12):
        c.trait(pr(XL_PLACE, 0, 7.4 + e), pr(XL_PLACE, 14, 7.4 + e), "fin", op=0.7, depasse=False)
    for y in (0.9, 2.6, 4.3, 6.0):
        c.trait(pr(XL_PLACE, y, 7.35), pr(XL_PLACE, y, 7.58), "fin", depasse=False)
    # le mur de face à l'entrée de la ruelle, et le pilier au panneau « rue du Tribunal »
    c.poly(rect_z(Z_RUE, XL_PLACE, XL, 0, 14), "fort")
    c.poly(rect_z(10.7, -1.55, XL, 0, 3.4), "moyen")
    side = [pr(XL, 3.4, 10.7), pr(XL, 3.4, Z_RUE), pr(XL, 0, Z_RUE), pr(XL, 0, 10.7)]
    c.poly(side, "fin"); dz.hachures(side, pas=0.5, angle=90, op=0.35)
    c.trait(pr(-1.55, 3.4, 10.7), pr(-1.55, 3.4, Z_RUE), "fin", depasse=False)
    pan = rect_z(10.68, -1.5, -1.12, 2.45, 2.75)
    c.poly(pan, "moyen", fond="#6d86a3")
    dz.hachures(pan, pas=0.35, angle=0, op=0.35)
    c.poly(rect_z(10.68, -1.52, -1.1, 1.95, 2.02), "fin")                    # la tablette de marbre


def droite(dz):
    c = dz.c
    # le grand mur de face, au portail (parallèle au tableau : vraie forme, horizontales horizontales)
    haut = [(XR, 5.8), (4.5, 5.15), (9, 5.15)]
    mur = [pr(x, y, Z_RUE) for x, y in haut] + [pr(9, 0, Z_RUE), pr(XR, 0, Z_RUE)]
    c.poly(mur, "fort")
    c.trait(pr(XR, 5.8, Z_RUE), pr(XR, 0, Z_RUE), "fort", double=True, depasse=False)   # l'arête du coin
    c.trait(pr(XR, 2.6, Z_RUE), pr(XR + 0.35, 2.6, Z_RUE), "fin", depasse=False)       # le petit rebord
    # le portail : grille de fer forgé en haut, battant gris tagué en bas
    x1, x2 = 2.4, 4.2
    c.poly(rect_z(Z_RUE, x1 - 0.06, x2 + 0.06, 0.12, 2.78), "moyen")
    g = rect_z(Z_RUE, x1, x2, 2.22, 2.72)
    c.poly(g, "moyen", fond="#d9dde2")
    k = F / Z_RUE
    for xx in np.arange(x1 + 0.12, x2 - 0.05, 0.2):
        cx_, cy_ = pr(xx, 2.47, Z_RUE); rr = 0.075 * k
        dz.ovale([(cx_ + rr*math.cos(t), cy_ + rr*math.sin(t)) for t in np.linspace(0, 2*math.pi, 9)[:-1]], 0.7, 0.2)
    p = rect_z(Z_RUE, x1, x2, 0.12, 2.2)
    c.poly(p, "fort", fond="#b9bec4")
    dz.hachures(p, pas=0.7, angle=90, op=0.4)
    c.trait(pr((x1 + x2)/2 + 0.1, 0.12, Z_RUE), pr((x1 + x2)/2 + 0.1, 2.2, Z_RUE), "fin", depasse=False)
    # le cœur tagué « M + D »
    cx_, cy_ = pr(2.95, 1.35, Z_RUE); s = 0.32 * k
    coeur = (f'M{cx_:.2f},{cy_ + s*0.9:.2f} C{cx_ - s*1.3:.2f},{cy_ + s*0.1:.2f} {cx_ - s*0.9:.2f},{cy_ - s*0.8:.2f} {cx_:.2f},{cy_ - s*0.25:.2f} '
             f'C{cx_ + s*0.9:.2f},{cy_ - s*0.8:.2f} {cx_ + s*1.3:.2f},{cy_ + s*0.1:.2f} {cx_:.2f},{cy_ + s*0.9:.2f}')
    c.out.append(f'<path d="{coeur}" fill="none" stroke="{FOND}" stroke-width="0.9" stroke-linecap="round"/>')
    c.out.append(f'<path d="{coeur}" fill="none" stroke="{GRIS}" stroke-width="0.22" stroke-opacity="0.7"/>')
    c.texte(cx_ - s*0.1, cy_ - s*1.05, "M+D", 0.3 * k, "#f4f4f2", "middle", halo=False)
    # les sacs posés au pied du mur
    for x, w, h in ((1.75, 0.35, 0.32), (2.05, 0.4, 0.42), (2.3, 0.3, 0.26)):
        a = pr(x, 0, 10.75); b = pr(x + w, 0, 10.75); t = pr(x + w/2, h, 10.75)
        c.out.append(f'<path d="M{a[0]:.2f},{a[1]:.2f} Q{a[0]:.2f},{t[1]:.2f} {t[0]:.2f},{t[1]:.2f} Q{b[0]:.2f},{t[1]:.2f} {b[0]:.2f},{b[1]:.2f} Z" '
                     f'fill="#8f9399" fill-opacity="0.55" stroke="{GRIS}" stroke-width="0.25" stroke-opacity="0.8"/>')


def premier_plan(dz):
    c = dz.c; r = dz.r
    # le fil tendu au-dessus de la placette
    a, b = pr(XL, 5.75, Z_RUE), pr(4.3, 5.05, 10.9)
    m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 3)
    c.out.append(f'<path d="M{a[0]:.2f},{a[1]:.2f} Q{m[0]:.2f},{m[1]:.2f} {b[0]:.2f},{b[1]:.2f}" fill="none" stroke="{GRIS}" stroke-width="0.25" stroke-opacity="0.8"/>')


def bord(p):
    d = np.subtract(p, PF); ts = []
    for v, i, lo, hi in ((FX0, 0, FY0, FY1), (FX1, 0, FY0, FY1), (FY0, 1, FX0, FX1), (FY1, 1, FX0, FX1)):
        if abs(d[i]) < 1e-9: continue
        t = (v - PF[i]) / d[i]
        if t > 0 and lo - 1e-6 <= PF[1-i] + t*d[1-i] <= hi + 1e-6: ts.append(t)
    t = min(ts); return (PF[0] + t*d[0], PF[1] + t*d[1])


def construction():
    k = Crayon(7)
    for i in range(-7, 8):                                                    # grille de report de 3 cm
        x = CX + 30*i
        if FX0 < x < FX1: k.trait((x, FY0), (x, FY1), "construction", CON, 0.22, depasse=False)
    for j in range(-6, 4):
        y = LHY + 30*j
        if FY0 < y < FY1 and j: k.trait((FX0, y), (FX1, y), "construction", CON, 0.22, depasse=False)
    fuy = [(pr(XL_PLACE, 0, 3)), pr(XL_PLACE, 2.75, 3), pr(XL, 0, Z_RUE), pr(XR, 0, Z_RUE), pr(XR, H_RUE_D, Z_RUE),
           pr(XR, 3.7, 11.5), pr(XR, 5.1, 11.5), pr(XL_PLACE, 6.9, 9.7), pr(XL_PLACE, 4.4, 9.7)]
    for p in fuy:
        k.trait(bord(p), PF, "construction", CON, 0.8, depasse=False, tirets="2 1.4")
    k.trait((0, LHY), (PAGE_W, LHY), "moyen", CON, 0.9, depasse=False, tirets="4 1.4 0.7 1.4")
    k.trait((FX0 - 6, FY1), (FX1 + 6, FY1), "construction", CON, 0.85, depasse=False, tirets="1.6 1.2")
    k.texte(FX0 - 1.5, LHY - 1.3, "LH", 4.4, CON, "end"); k.texte(FX1 + 1.5, LHY - 1.3, "LH", 4.4, CON, "start")
    k.texte(FX0 - 1.5, FY1 - 1.3, "LT", 4.0, CON, "end"); k.texte(FX1 + 1.5, FY1 - 1.3, "LT", 4.0, CON, "start")
    k.out.append(f'<circle cx="{CX}" cy="{LHY}" r="3.4" fill="none" stroke="{CON}" stroke-width="0.35"/>')
    k.point(CX, LHY, CON, 0.8)
    k.texte(CX + 4.2, LHY - 3.2, "PF", 4.6, CON, "start")
    xc = FX1 - 7                                                              # cote : 1,20 m, assis
    k.trait((xc, FY1), (xc, LHY), "moyen", CON, 0.95, depasse=False)
    for y, s in ((FY1, -1), (LHY, 1)):
        k.trait((xc - 1.2, y), (xc + 1.2, y), "moyen", CON, 0.95, depasse=False)
        k.trait((xc, y), (xc - 0.8, y + s*1.6), "moyen", CON, 0.95, depasse=False)
        k.trait((xc, y), (xc + 0.8, y + s*1.6), "moyen", CON, 0.95, depasse=False)
    k.texte(xc - 1.6, (FY1 + LHY)/2 - 1, "1,20 m", 3.8, CON, "end")
    k.texte(xc - 1.6, (FY1 + LHY)/2 + 3.6, "yeux, assis", 3.2, CON, "end")
    # annotations
    k.texte(FX0 + 3, LHY + 4.6, "LH : à hauteur des yeux, ASSIS (1,20 m) — plus bas que la photo, prise debout", 3.0, CON)
    p = pr(PORTE[0], PORTE[3], Z_FOND)
    k.texte(p[0] - 2, p[1] - 9.5, "la porte bleue, à 20 m :", 3.0, CON, "end")
    k.texte(p[0] - 2, p[1] - 6, "petite, juste sous la LH", 3.0, CON, "end")
    k.trait((p[0] - 1.6, p[1] - 6.6), (p[0] + 0.5, p[1] + 0.5), "construction", CON, 0.9, depasse=False)
    q = pr(XR, 2.0, 15)
    k.texte(q[0] + 2.5, q[1] - 3, "les murs de la ruelle", 3.0, CON)
    k.texte(q[0] + 2.5, q[1] + 0.6, "fuient vers le PF", 3.0, CON)
    q = pr(4.2, 2.9, Z_RUE)
    k.texte(q[0] + 2, q[1] - 2, "mur de face : vraie forme,", 3.0, CON)
    k.texte(q[0] + 2, q[1] + 1.6, "horizontales horizontales", 3.0, CON)
    q = pr(XL_PLACE, 0.6, 3.6)
    k.texte(q[0] + 4, q[1] - 6, "mur à l'arc : il fuit vers le PF", 3.0, CON, rot=-math.degrees(math.atan2(LHY - q[1], CX - q[0])) * -1)
    return "".join(k.out)


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
    t.texte(FX0, 14, "La ruelle à la porte bleue · vue assise", 7.2, "#1f1f1f")
    t.texte(FX0, 22.5, "perspective frontale · 1 point de fuite · assis face à la porte, un peu à droite, à 20 m", 4.0, "#555")
    etapes = ["1  le cadre, la LH à 16 cm du haut (1,20 m : les yeux, assis), le PF au milieu",
              "2  la porte bleue et le mur du fond : de face, petits, juste sous la LH",
              "3  les murs de la ruelle : pieds et hauts sur des fuyantes vers le PF",
              "4  le mur au portail (de face) et le mur à l'arc (il fuit vers le PF)",
              "5  les détails : arc, fenêtres, lanterne, panneau, portail, sacs",
              "6  les pavés : des rangées de plus en plus petites vers le PF"]
    for i, e in enumerate(etapes):
        t.texte(FX1, 7.6 + i*3.9, e, 3.2, CON, "end")
    t.texte(FX0, 281, "en bleu : la construction (LH, LT, PF, fuyantes) · en gris : le croquis", 3.2, "#666", halo=False)
    t.texte(FX0, 286.5, "carreaux bleus de 3 cm, partant du PF, pour reporter le dessin", 3.2, "#666", halo=False)
    t.texte(FX1, 281, "dessiné depuis ta place, pas depuis le téléphone : champ de vision de l'œil (~55°)", 3.2, "#666", "end", halo=False)
    t.texte(FX1, 286.5, "le support en fer forgé et la treille de la photo sont au-dessus du regard : hors cadre", 3.2, "#666", "end", halo=False)
    return "".join(t.out)


def etiquettes_a4():
    t = Crayon(9)
    t.texte(CX - 5.5, LHY - 5, "PF →", 3.6, CON, "end")
    t.texte(FX0, 293, "feuille 1/2 · moitié GAUCHE de l'A3 · la jonction est à droite →", 3.0, "#a0302a", halo=False)
    g = "".join(t.out); t.out = []
    t.texte(FX1, 293, "← la jonction est à gauche · feuille 2/2 · moitié DROITE de l'A3", 3.0, "#a0302a", "end", halo=False)
    return g, "".join(t.out)


if __name__ == "__main__":
    defs, corps = dessin()
    txt = textes()
    eg, ed = etiquettes_a4()
    svg = lambda vb, extra="": (f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg"><defs>{defs}</defs>'
                                f'{corps}{txt}{extra}</svg>')
    open(f"{ICI}/croquis-A3.html", "w", encoding="utf-8").write(html([svg(f"0 0 {PAGE_W} {PAGE_H}")], 420, 297, "Ruelle porte bleue A3"))
    open(f"{ICI}/croquis-2xA4.html", "w", encoding="utf-8").write(
        html([svg("0 0 210 297", eg), svg("210 0 210 297", ed)], 210, 297, "Ruelle porte bleue 2 x A4"))
    print("croquis-A3.html et croquis-2xA4.html écrits")

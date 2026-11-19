"""Croquis « à la main » d'une rue en perspective frontale (1 point de fuite), d'après la fig. 44.

La rue est construite en vraie 3D puis projetée : l'œil est à 1,75 m du sol, au milieu de la rue,
à 18 m du plan du tableau. Tout ce qui fuit en profondeur converge vers le point de fuite PF,
les verticales restent verticales et les horizontales frontales restent horizontales.

Sorties : croquis-A3.html (1 page A3 paysage) et croquis-2xA4.html (les deux moitiés de l'A3,
à l'échelle 1, sur 2 pages A4 portrait), à rendre en PDF avec rendu.js.
"""
import math, random, sys
import numpy as np

ICI = sys.argv[1] if len(sys.argv) > 1 else "."
PAGE_W, PAGE_H = 420, 297                  # A3 paysage, en mm
FX0, FY0, FX1, FY1 = 15, 34, 405, 272      # le cadre du dessin
S, D, OEIL = 17, 18, 1.75                  # mm par m sur le plan du tableau, distance œil-tableau (m), hauteur des yeux (m)
CX, LHY = 210, 190                         # le PF : au milieu, sur la LH
FOND = "#fdfcf8"; GRIS = "#2a2a2a"; CON = "#2f62b0"
PF = (CX, LHY)


def pr(x, y, z):
    """point 3D (x : vers la droite, y : hauteur, z : profondeur depuis le tableau, en m) -> mm sur la feuille"""
    k = D / (z + D)
    return (CX + S * x * k, LHY - S * (y - OEIL) * k)


# ---------------------------------------------------------------- la rue
CHAUSSEE, TROTTOIR = 3.5, 6.5              # demi-largeur de la chaussée, alignement des façades
# immeubles : (z début, z fin, hauteur, type, recul de la façade)
GAUCHE = [(-14, 7, 13, "fenetres", 6.5), (7, 15, 10, "fenetres", 6.5), (15, 24, 16, "bandeaux", 6.5),
          (24, 33, 12.5, "fenetres", 6.5), (33, 44, 10, "fenetres", 6.5), (44, 58, 14, "bandeaux", 6.5),
          (58, 80, 11, "simple", 6.5), (80, 120, 13, "simple", 6.5), (120, 200, 10, "simple", 6.5)]
DROITE = [(-14, 5, 9.5, "vitrine", 6.5), (5, 16, 15, "fenetres", 6.5), (16, 24, 12, "fenetres", 6.5),
          (24, 36, 13, "bandeaux", 9.0), (36, 48, 16, "fenetres", 6.5), (48, 62, 11, "fenetres", 6.5),
          (62, 90, 13, "simple", 6.5), (90, 140, 10, "simple", 6.5), (140, 200, 12, "simple", 6.5)]
PROFONDEUR = 12                            # profondeur des immeubles (m)
LAMPADAIRES = [3, 18, 33, 48, 63, 78, 93]
PERSONNES = [(-5.0, 1.5), (4.6, 13), (1.2, 27), (-4.4, 45)]


# ---------------------------------------------------------------- rendu « à la main »
class Crayon:
    def __init__(self, graine):
        self.r = random.Random(graine); self.out = []

    def trait(self, p, q, poids="moyen", couleur=GRIS, op=None, depasse=True, double=False, tirets=None):
        lw = {"fort": 0.42, "moyen": 0.32, "fin": 0.22, "construction": 0.18}[poids]
        op = op if op is not None else {"fort": 0.9, "moyen": 0.85, "fin": 0.75, "construction": 0.75}[poids]
        for k in range(2 if double else 1):
            self.out.append(self._chemin(p, q, lw*(0.8 if k else 1), couleur, op*(0.45 if k else 1), depasse, k, tirets))

    def _chemin(self, p, q, lw, couleur, op, depasse, k, tirets):
        r = self.r
        p, q = np.array(p, float), np.array(q, float); d = q - p; L = np.linalg.norm(d)
        if L < 1e-6: return ""
        u = d / L; n = np.array([-u[1], u[0]])
        dep = min(2.0, 0.25 + L*0.06)
        e1 = r.uniform(0.3, 1.0)*dep if depasse else 0; e2 = r.uniform(0.3, 1.0)*dep if depasse else 0
        p = p - u*e1; L = L + e1 + e2
        amp = min(0.28, 0.03 + L*0.0025) * (1.4 if k else 1)
        ph1, ph2 = r.uniform(0, 6.3), r.uniform(0, 6.3); f1, f2 = r.uniform(0.6, 1.4), r.uniform(2, 3.5)
        dec = r.uniform(-0.18, 0.18) if k else 0
        npts = max(3, int(L / 3))
        pts = []
        for i in range(npts + 1):
            t = i / npts
            w = amp*(math.sin(math.pi*f1*t*2 + ph1)*0.7 + math.sin(math.pi*f2*t*2 + ph2)*0.3) + dec
            x, y = p + u*L*t + n*w
            pts.append(f"{x:.2f},{y:.2f}")
        da = f' stroke-dasharray="{tirets}"' if tirets else ""
        return (f'<polyline points="{" ".join(pts)}" fill="none" stroke="{couleur}" stroke-width="{lw:.2f}" '
                f'stroke-opacity="{op:.2f}" stroke-linecap="round" stroke-linejoin="round"{da}/>')

    def poly(self, pts, poids="moyen", fond=FOND, op=None, depasse=True):
        """polygone opaque (cache ce qui est derrière), contour au crayon"""
        self.out.append(f'<polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}" fill="{fond}"/>')
        for i in range(len(pts)):
            self.trait(pts[i], pts[(i+1) % len(pts)], poids, op=op, depasse=depasse)

    def texte(self, x, y, t, taille=4.2, couleur=CON, ancre="start", rot=0, halo=True):
        tr = f' transform="rotate({rot:.2f} {x:.1f} {y:.1f})"' if rot else ""
        self.out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="\'Architects Daughter\', \'Caveat\', cursive" '
                        f'font-size="{taille}" fill="{couleur}" text-anchor="{ancre}"{tr}'
                        + (f' stroke="{FOND}" stroke-width="1.1" stroke-linejoin="round" paint-order="stroke"' if halo else '')
                        + f'>{t}</text>')

    def point(self, x, y, couleur=CON, r=0.7):
        self.out.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{couleur}"/>')


class Dessin:
    def __init__(self, graine):
        self.c = Crayon(graine); self.defs = []; self.n = 0

    def hachures(self, q, sorte="vertical"):
        """hachures dans un quadrilatère (fenêtres sombres, vitrines)"""
        xs = [p[0] for p in q]; ys = [p[1] for p in q]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        if w < 1.3 or h < 1.3:
            self.c.out.append(f'<polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in q)}" fill="{GRIS}" fill-opacity="0.45"/>')
            return
        self.n += 1; pid = f"h{self.n}"
        self.defs.append(f'<clipPath id="{pid}"><polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in q)}"/></clipPath>')
        sous = Crayon(self.n)
        if sorte == "vertical":
            t = min(xs) + 0.5
            while t < max(xs):
                sous.trait((t, min(ys) - 0.5), (t, max(ys) + 0.5), "fin", "#3a3a3a", 0.6, depasse=False); t += 0.75
        else:                                   # reflets à 45° sur une vitrine
            for f in (0.25, 0.38, 0.7):
                cx, cy = min(xs) + w*f, min(ys) + h*f; e = min(w, h)*0.3
                sous.trait((cx - e, cy + e), (cx + e, cy - e), "fin", "#3a3a3a", 0.5, depasse=False)
        self.c.out.append(f'<g clip-path="url(#{pid})">{"".join(sous.out)}</g>')


def quad(xf, za, zb, ya, yb):
    """rectangle sur une façade (plan x = xf), de za à zb en profondeur, de ya à yb en hauteur"""
    return [pr(xf, yb, za), pr(xf, yb, zb), pr(xf, ya, zb), pr(xf, ya, za)]


def facade(dz, xf, z0, z1, H, sorte, rnd):
    c = dz.c
    k = D / (z0 + D)
    loin = k < 0.2
    # le rez-de-chaussée (4 m), puis des étages de 3 m
    etages = [4 + 3*i for i in range(int((H - 4.6) // 3))]
    for y in [4] + etages[1:]:
        c.trait(pr(xf, y, z0), pr(xf, y, z1), "fin", op=0.55 if loin else 0.7, depasse=False)
    c.trait(pr(xf, H - 0.5, z0), pr(xf, H - 0.5, z1), "fin", depasse=False)       # corniche
    if sorte == "simple" or loin:
        pas = 4 if k > 0.12 else 8
        z = z0 + pas
        while z < z1 - 1:
            c.trait(pr(xf, 0, z), pr(xf, H - 0.5, z), "fin", op=0.45, depasse=False); z += pas
        return
    # rez-de-chaussée : vitrines et porte
    z = z0 + 0.8
    while z < z1 - 2.5:
        lg = min(3.4, z1 - 0.8 - z)
        q = quad(xf, z, z + lg, 0.3, 3.2)
        c.poly(q, "fin", depasse=False)
        if rnd.random() < 0.55: dz.hachures(q, "vertical")
        else: dz.hachures(q, "reflet")
        z += lg + 0.9
    # étages
    for y in etages:
        if sorte == "bandeaux":
            q = quad(xf, z0 + 0.8, z1 - 0.8, y + 0.9, y + 2.3)
            c.poly(q, "fin", depasse=False)
            zz = z0 + 0.8 + 1.6
            while zz < z1 - 1:
                c.trait(pr(xf, y + 0.9, zz), pr(xf, y + 2.3, zz), "fin", op=0.6, depasse=False); zz += 1.6
            if rnd.random() < 0.5: dz.hachures(q, "reflet")
        else:
            nb = max(1, int((z1 - z0 - 1) // 2.6))
            pas = (z1 - z0) / nb
            for i in range(nb):
                za = z0 + pas*i + (pas - 1.3)/2
                q = quad(xf, za, za + 1.3, y + 0.9, y + 2.5)
                c.poly(q, "fin", depasse=False)
                if rnd.random() < 0.4: dz.hachures(q, "vertical")
                c.trait(pr(xf, y + 0.8, za - 0.15), pr(xf, y + 0.8, za + 1.45), "fin", op=0.6, depasse=False)  # appui


def cote(rangee, signe, dz, rnd):
    """une rangée d'immeubles, du plus loin au plus proche (les plus proches cachent les plus loin)"""
    c = dz.c
    for i in range(len(rangee) - 1, -1, -1):
        z0, z1, H, sorte, rec = rangee[i]
        xf = signe*rec; xe = signe*(rec + PROFONDEUR)
        # mur de face (parallèle au tableau : il garde sa vraie forme)
        mur = [pr(xf, H, z0), pr(xe, H, z0), pr(xe, 0, z0), pr(xf, 0, z0)]
        c.poly(mur, "moyen")
        # façade sur la rue : ses horizontales fuient vers le PF
        f = [pr(xf, H, z0), pr(xf, H, z1), pr(xf, 0, z1), pr(xf, 0, z0)]
        c.poly(f, "fort" if z0 < 30 else "moyen")
        facade(dz, xf, z0, z1, H, sorte, rnd)
        c.trait(pr(xf, H, z0), pr(xf, 0, z0), "fort" if z0 < 30 else "moyen", double=z0 < 20)   # l'arête verticale
        # recul : le sol devant la façade reculée
        if rec > TROTTOIR:
            c.trait(pr(signe*TROTTOIR, 0, z0), pr(signe*TROTTOIR, 0, z1), "fin", op=0.5)


def sol(dz):
    c = dz.c
    for s in (-1, 1):
        c.trait(pr(s*CHAUSSEE, 0, -14), pr(s*CHAUSSEE, 0, 200), "fort")                # bord de chaussée
        c.trait(pr(s*CHAUSSEE, 0.15, -14), pr(s*CHAUSSEE, 0.15, 200), "fin", op=0.6)   # dessus de la bordure
        z = -13.0
        while z < 40:                                                                 # joints du trottoir
            c.trait(pr(s*CHAUSSEE, 0.15, z), pr(s*TROTTOIR, 0.15, z), "fin", op=0.4 if z < 15 else 0.3, depasse=False)
            z += 1.5
    z = -13.0
    while z < 150:                                                                    # ligne médiane
        c.trait(pr(0, 0, z), pr(0, 0, z + 3), "moyen", op=0.75, depasse=False); z += 6
    for xa in np.arange(-3.0, 3.0, 1.0):                                              # passage piéton
        q = [pr(xa, 0, 3), pr(xa + 0.5, 0, 3), pr(xa + 0.5, 0, 7), pr(xa, 0, 7)]
        c.poly(q, "fin", fond="#e9e7e1", depasse=False)


def lampadaire(c, s, z):
    x = s*5.2; k = D / (z + D); pd = "moyen" if k > 0.4 else "fin"
    c.trait(pr(x, 0, z), pr(x, 7.0, z), pd, depasse=False)
    c.trait(pr(x, 7.0, z), pr(x - s*0.6, 7.5, z), pd, depasse=False)
    c.trait(pr(x - s*0.6, 7.5, z), pr(x - s*1.9, 7.5, z), pd, depasse=False)
    a, b = pr(x - s*1.5, 7.5, z), pr(x - s*2.1, 7.35, z)
    c.out.append(f'<rect x="{min(a[0], b[0]):.2f}" y="{a[1]:.2f}" width="{abs(b[0]-a[0]):.2f}" height="{max(0.3, b[1]-a[1]):.2f}" '
                 f'fill="{GRIS}" fill-opacity="0.75"/>')


def personne(c, x, z, rnd):
    """un personnage de 1,75 m : sa tête est toujours sur la LH"""
    k = D / (z + D); h = S*OEIL*k
    px, sy = pr(x, 0, z)
    ty = sy - h; rt = h*0.065
    pd = "moyen" if h > 12 else "fin"
    c.out.append(f'<circle cx="{px:.2f}" cy="{ty + rt:.2f}" r="{rt:.2f}" fill="{FOND}" stroke="{GRIS}" stroke-width="0.3" stroke-opacity="0.85"/>')
    cou, hanche = ty + 2*rt, ty + h*0.52
    ep = h*0.12
    c.poly([(px - ep, cou + h*0.03), (px + ep, cou + h*0.03), (px + ep*0.85, hanche), (px - ep*0.85, hanche)], pd)
    c.trait((px - ep*0.6, hanche), (px - ep*0.7 + rnd.uniform(-0.3, 0.3)*h*0.1, sy), pd, depasse=False)
    c.trait((px + ep*0.6, hanche), (px + ep*0.7 + rnd.uniform(-0.3, 0.3)*h*0.1, sy), pd, depasse=False)
    c.trait((px - ep, cou + h*0.05), (px - ep*1.25, ty + h*0.5), pd, depasse=False)
    c.trait((px + ep, cou + h*0.05), (px + ep*1.25, ty + h*0.5), pd, depasse=False)


def bord(p):
    """la fuyante qui part du PF et passe par p, jusqu'au bord du cadre"""
    d = np.subtract(p, PF); ts = []
    for v, i, lo, hi in ((FX0, 0, FY0, FY1), (FX1, 0, FY0, FY1), (FY0, 1, FX0, FX1), (FY1, 1, FX0, FX1)):
        if abs(d[i]) < 1e-9: continue
        t = (v - PF[i]) / d[i]
        if t > 0 and lo - 1e-6 <= PF[1-i] + t*d[1-i] <= hi + 1e-6: ts.append(t)
    t = min(ts); return (PF[0] + t*d[0], PF[1] + t*d[1])


def construction():
    k = Crayon(7)
    # grille de report : carreaux de 3 cm partant du PF
    for i in range(-7, 8):
        x = CX + 30*i
        if FX0 < x < FX1: k.trait((x, FY0), (x, FY1), "construction", CON, 0.22, depasse=False)
    for j in range(-6, 4):
        y = LHY + 30*j
        if FY0 < y < FY1 and j: k.trait((FX0, y), (FX1, y), "construction", CON, 0.22, depasse=False)
    # fuyantes
    fuy = [(-TROTTOIR, 0), (TROTTOIR, 0), (-CHAUSSEE, 0), (CHAUSSEE, 0),
           (-TROTTOIR, 13), (-TROTTOIR, 10), (-TROTTOIR, 16), (TROTTOIR, 9.5), (TROTTOIR, 15), (TROTTOIR, 12),
           (-5.2, 7.5), (5.2, 7.5), (-TROTTOIR, 4), (TROTTOIR, 4)]
    for x, y in fuy:
        a = bord(pr(x, y, 0))
        k.trait(a, PF, "construction", CON, 0.8, depasse=False, tirets="2 1.4")
    # LH, LT, PF
    k.trait((0, LHY), (PAGE_W, LHY), "moyen", CON, 0.9, depasse=False, tirets="4 1.4 0.7 1.4")
    yt = pr(0, 0, 0)[1]
    k.trait((FX0 - 6, yt), (FX1 + 6, yt), "construction", CON, 0.85, depasse=False, tirets="1.6 1.2")
    k.texte(FX0 - 1.5, LHY - 1.3, "LH", 4.4, CON, "end"); k.texte(FX1 + 1.5, LHY - 1.3, "LH", 4.4, CON, "start")
    k.texte(FX0 - 1.5, yt - 1.3, "LT", 4.0, CON, "end"); k.texte(FX1 + 1.5, yt - 1.3, "LT", 4.0, CON, "start")
    k.out.append(f'<circle cx="{CX}" cy="{LHY}" r="4.2" fill="none" stroke="{CON}" stroke-width="0.35"/>')
    k.point(CX, LHY, CON, 0.85)
    k.texte(CX + 0.3, LHY - 5.6, "PF", 4.8, CON, "middle")
    # cote : 1,75 m entre la ligne de terre et l'horizon
    xc = FX1 - 7
    k.trait((xc, yt), (xc, LHY), "moyen", CON, 0.95, depasse=False)
    for y, s in ((yt, -1), (LHY, 1)):
        k.trait((xc - 1.2, y), (xc + 1.2, y), "moyen", CON, 0.95, depasse=False)
        k.trait((xc, y), (xc - 0.8, y + s*1.6), "moyen", CON, 0.95, depasse=False)
        k.trait((xc, y), (xc + 0.8, y + s*1.6), "moyen", CON, 0.95, depasse=False)
    k.texte(xc - 1.6, (yt + LHY)/2 + 1.3, "1,75 m", 3.8, CON, "end")
    # annotations
    k.texte(FX1 - 3, yt + 4.5, "LT : ligne de terre, le pied du tableau", 3.0, CON, "end")
    k.texte(FX0 + 3, LHY + 4.6, "LH : ligne d'horizon, à hauteur des yeux (1,75 m)", 3.0, CON, "start")
    p = pr(-5.0, OEIL, 1.5)
    k.texte(p[0] + 9, p[1] + 11, "les têtes des passants sont sur la LH", 3.2, CON, "start")
    k.trait((p[0] + 8.5, p[1] + 9.6), (p[0] + 2.4, p[1] + 1.4), "construction", CON, 0.9, depasse=False)
    a = pr(-CHAUSSEE, 0, -11.5); b = pr(-CHAUSSEE, 0, 9)
    ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    k.texte(a[0] + 4, a[1] - 4.2, "fuyante → PF", 3.6, CON, "start", rot=ang)
    a = pr(TROTTOIR, 11, 5)
    k.texte(a[0] + 2, a[1] - 3.6, "les verticales", 3.1, CON, "start")
    k.texte(a[0] + 2, a[1], "restent verticales", 3.1, CON, "start")
    k.texte(CX + 8, yt + 6.5, "les horizontales de face restent horizontales", 3.0, CON, "start")
    return "".join(k.out)


def dessin():
    dz = Dessin(11); rnd = random.Random(5)
    sol(dz)
    cote(GAUCHE, -1, dz, rnd)
    cote(DROITE, 1, dz, rnd)
    objets = [(z, "l", s) for z in LAMPADAIRES for s in (-1, 1)] + [(z, "p", x) for x, z in PERSONNES]
    for z, t, v in sorted(objets, reverse=True):
        lampadaire(dz.c, v, z) if t == "l" else personne(dz.c, v, z, rnd)
    cadre = Crayon(3)
    coins = [(FX0, FY0), (FX1, FY0), (FX1, FY1), (FX0, FY1)]
    for i in range(4):
        cadre.trait(coins[i], coins[(i+1) % 4], "fort", "#1c1c1c", 0.95)
    defs = "".join(dz.defs) + f'<clipPath id="cadre"><rect x="{FX0}" y="{FY0}" width="{FX1-FX0}" height="{FY1-FY0}"/></clipPath>'
    return defs, f'<g clip-path="url(#cadre)">{"".join(dz.c.out)}</g>' + construction() + "".join(cadre.out)


def textes():
    t = Crayon(4)
    t.texte(FX0, 14, "Perspective frontale · la rue", 7.2, "#1f1f1f")
    t.texte(FX0, 22.5, "1 seul point de fuite (PF) au milieu de la ligne d'horizon · d'après la fig. 44", 4.0, "#555")
    etapes = [f"1  le cadre (39 × 24 cm), la LH à {(LHY-FY0)/10:.1f} cm du haut, le PF au milieu".replace(".", ","),
              f"2  la LT à {S*OEIL/10:.1f} cm sous la LH (= 1,75 m, la hauteur des yeux)".replace(".", ","),
              "3  bords de la chaussée et pieds des façades : fuyantes vers le PF",
              "4  arêtes des immeubles : verticales ; toits : fuyantes vers le PF",
              "5  fenêtres : hauts et bas sur des fuyantes, côtés verticaux",
              "6  lampadaires et passants : la tête des passants sur la LH"]
    for i, e in enumerate(etapes):
        t.texte(FX1, 7.6 + i*3.9, e, 3.2, CON, "end")
    t.texte(FX0, 281, "en bleu : la construction (LH, LT, PF, fuyantes) · en gris : le croquis", 3.2, "#666", halo=False)
    t.texte(FX0, 286.5, "carreaux bleus de 3 cm, partant du PF, pour reporter le dessin", 3.2, "#666", halo=False)
    t.texte(FX1, 281, "l'œil : à 1,75 m du sol, au milieu de la rue, à 18 m du tableau", 3.2, "#666", "end", halo=False)
    t.texte(FX1, 286.5, "plus un objet s'éloigne, plus il rapetisse et se rapproche du PF", 3.2, "#666", "end", halo=False)
    return "".join(t.out)


def etiquettes_a4():
    t = Crayon(9)
    t.texte(CX - 5.5, LHY - 5, "PF →", 3.6, CON, "end")
    t.texte(FX0, 293, "feuille 1/2 · moitié GAUCHE de l'A3 · la jonction est à droite →", 3.0, "#a0302a", halo=False)
    g = t.out; t.out = []
    t.texte(CX + 5.5, LHY - 5, "← PF", 3.6, CON, "start")
    t.texte(FX1, 293, "← la jonction est à gauche · feuille 2/2 · moitié DROITE de l'A3", 3.0, "#a0302a", "end", halo=False)
    d = t.out
    return "".join(g), "".join(d)


def html(pages, w, h, titre):
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{titre}</title>
<link rel="stylesheet" href="polices-local.css">
<style>@page {{ size: {w}mm {h}mm; margin: 0; }} html, body {{ margin: 0; background: #fff; }}
.p {{ width: {w}mm; height: {h}mm; page-break-after: always; break-after: page; overflow: hidden; background: {FOND}; }}
.p:last-child {{ page-break-after: auto; break-after: auto; }} svg {{ width: 100%; height: 100%; display: block; }}</style></head>
<body>{"".join(f'<div class="p">{p}</div>' for p in pages)}</body></html>"""


if __name__ == "__main__":
    defs, corps = dessin()
    txt = textes()
    eg, ed = etiquettes_a4()
    svg = lambda vb, extra="": (f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg"><defs>{defs}</defs>'
                                f'{corps}{txt}{extra}</svg>')
    open(f"{ICI}/croquis-A3.html", "w", encoding="utf-8").write(
        html([svg(f"0 0 {PAGE_W} {PAGE_H}")], 420, 297, "Perspective frontale A3"))
    open(f"{ICI}/croquis-2xA4.html", "w", encoding="utf-8").write(
        html([svg("0 0 210 297", eg), svg("210 0 210 297", ed)], 210, 297, "Perspective frontale 2 x A4"))
    print("croquis-A3.html et croquis-2xA4.html écrits")

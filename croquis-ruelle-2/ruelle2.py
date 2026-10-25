"""Croquis au trait de la ruelle aux portes bleues (2e photo), vue ASSISE, en perspective frontale.

Méthode : la photo (photos/ruelle2-photo.jpg) est « redressée » (photos/ruelle2-photo-redressee.jpg) :
on calcule le point de fuite des verticales et celui de la ruelle, puis on fait tourner la vue pour
que les verticales soient verticales et que la ruelle fuie vers un seul point (perspective frontale).
Tout est relevé dans cette vue redressée (coordonnées u, v en px, PF = (1500, 1272)).

Échelle : la LH de la photo passe à hauteur des poignées de porte ; avec les yeux à 1,20 m (assis),
la plaque d'égout mesure 0,61 m — la taille d'une vraie plaque : la photo a bien été prise assis.
3D (m) : x vers la droite, y vers le haut, z en profondeur ; u = 1500 + f·x/z, v = 1272 − f·(y − 1,20)/z.

Ni hachures ni remplissages, pas de plantes. Les fers forgés des balcons et de la grille sont relevés
sur la photo (releve-fers-forges.json : contours du métal bleu). Format A3 portrait (+ 2 × A4 paysage).
"""
import math, random, sys, os, json
import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "..", "perspective-frontale-rue"))
from croquis import Crayon, html, FOND, GRIS, CON  # même crayon que les autres croquis

SORTIE = sys.argv[1] if len(sys.argv) > 1 else ICI
PAGE_W, PAGE_H = 297, 420
FX0, FY0 = 15, 46
U0, U1, V0 = 290, 1815, 120                 # la fenêtre de la vue redressée qui est dessinée
S = (282 - FX0) / (U1 - U0)                 # mm par px
FX1, FY1 = 282, FY0 + 336
V1 = V0 + 336 / S
JONCTION = PAGE_H / 2
F_PX, OEIL = 1250.0, 1.20
PFU, PFV = 1500.0, 1272.0


def P(u, v):                                 # vue redressée (px) -> feuille (mm)
    return (FX0 + (u - U0) * S, FY0 + (v - V0) * S)


PF = P(PFU, PFV)
LHY = PF[1]


def pr(x, y, z):                             # 3D (m) -> vue redressée (px)
    return (PFU + F_PX * x / z, PFV - F_PX * (y - OEIL) / z)


def P3(x, y, z):
    return P(*pr(x, y, z))


def fu(p, u):                                # point d'abscisse u sur la fuyante PF -> p
    t = (u - PFU) / (p[0] - PFU)
    return (u, PFV + (p[1] - PFV) * t)


XL = -2.36                                   # mur gauche (pied relevé en (564, 1748))
XD = -2.63                                   # plan de la porte, en retrait de 27 cm


class Dessin:
    def __init__(self, graine):
        self.c = Crayon(graine); self.defs = []; self.n = 0; self.r = random.Random(graine + 1)

    def L(self, a, b, poids="fin", op=None, depasse=False, mm=False):
        self.c.trait(a if mm else P(*a), b if mm else P(*b), poids, op=op, depasse=depasse)

    def F(self, p, u1, u2, poids="fin", op=None):          # un morceau de fuyante, de u1 à u2
        self.L(fu(p, u1), fu(p, u2), poids, op)

    def poly(self, pts, poids="fin", fond=None, ferme=True, op=None, mm=False):
        q = [p if mm else P(*p) for p in pts]
        if fond:
            self.c.out.append(f'<polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in q)}" fill="{fond}"/>')
        for i in range(len(q) - (0 if ferme else 1)):
            self.c.trait(q[i], q[(i + 1) % len(q)], poids, op=op, depasse=False)

    def courbe(self, pts, lw=0.22, op=0.85, ferme=False, fond=None, mm=False):
        q = [p if mm else P(*p) for p in pts]
        q = [(x + self.r.uniform(-0.03, 0.03), y + self.r.uniform(-0.03, 0.03)) for x, y in q]
        if ferme: q = q + q[:1]
        d = " ".join(f"{x:.2f},{y:.2f}" for x, y in q)
        tag = "polygon" if fond else "polyline"
        f = f'fill="{fond}"' if fond else 'fill="none"'
        self.c.out.append(f'<{tag} points="{d}" {f} stroke="{GRIS}" stroke-width="{lw}" stroke-opacity="{op}" '
                          f'stroke-linecap="round" stroke-linejoin="round"/>')

    def exact(self, pts, lw=0.18, op=0.75):                 # tracé relevé sur la photo, sans tremblé
        q = [P(*p) for p in pts]
        self.c.out.append(f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in q)}" fill="none" stroke="{GRIS}" '
                          f'stroke-width="{lw}" stroke-opacity="{op}" stroke-linecap="round" stroke-linejoin="round"/>')

    def spirale(self, cu, cv, r, tours=1.6, sens=1, a0=0.0, lw=0.2, sx=1.0):
        n = int(20 * tours)
        self.courbe([(cu + sx * r * (1 - i / n * 0.85) * math.cos(a0 + sens * 2 * math.pi * tours * i / n),
                      cv + r * (1 - i / n * 0.85) * math.sin(a0 + sens * 2 * math.pi * tours * i / n)) for i in range(n + 1)], lw)

    def clip(self, pts, contenu):
        self.n += 1; pid = f"k{self.n}"
        q = [P(*p) for p in pts]
        self.defs.append(f'<clipPath id="{pid}"><polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in q)}"/></clipPath>')
        self.c.out.append(f'<g clip-path="url(#{pid})">{contenu}</g>')


def lisse(pts, n=6):
    P_ = [pts[0]] + list(pts) + [pts[-1]]; out = []
    for i in range(1, len(P_) - 2):
        p0, p1, p2, p3 = (np.array(P_[i + j], float) for j in (-1, 0, 1, 2))
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(tuple(0.5 * ((2*p1) + (-p0 + p2)*t + (2*p0 - 5*p1 + 4*p2 - p3)*t*t + (-p0 + 3*p1 - 3*p2 + p3)*t**3)))
    return out + [tuple(pts[-1])]


# ---------------------------------------------------------------- les carreaux de faïence (cadre de la porte)
def carreaux(dz, plan, a1, a2, b1, b2, pas=0.054, clip=None):
    """carreaux sur un plan : 'mur' (x = XL : a = z, b = y), 'tableau' (z = 4,50 : a = x, b = y), 'sous' (y = 3,66 : a = x, b = z).
    une rosace par carreau de 5,4 cm, un joint tous les 2 carreaux"""
    def Q(a, b):
        if plan == "mur": return pr(XL, b, a)
        if plan == "tableau": return pr(a, b, 4.50)
        return pr(XD, b, a)                                  # 'fond' : le fond de la baie, au-dessus de la porte
    sous = Crayon(dz.r.randrange(10**6))
    na, nb = int(round((a2 - a1) / pas)), int(round((b2 - b1) / pas))
    for i in range(0, na + 1, 2):
        a = min(a2, a1 + i * pas); sous.trait(P(*Q(a, b1)), P(*Q(a, b2)), "fin", "#3a3a3a", 0.45, depasse=False)
    for j in range(0, nb + 1, 2):
        b = min(b2, b1 + j * pas); sous.trait(P(*Q(a1, b)), P(*Q(a2, b)), "fin", "#3a3a3a", 0.45, depasse=False)
    for i in range(na):
        for j in range(nb):
            ca, cb = a1 + (i + 0.5) * pas, b1 + (j + 0.5) * pas
            if ca > a2 or cb > b2: continue
            pts = [P(*Q(ca + 0.019 * math.cos(t), cb + 0.019 * math.sin(t))) for t in np.linspace(0, 2 * math.pi, 9)[:-1]]
            sous.out.append(f'<polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}" fill="none" stroke="#3a3a3a" '
                            f'stroke-width="0.13" stroke-opacity="0.5"/>')
    if clip: dz.clip(clip, "".join(sous.out))
    else: dz.c.out.extend(sous.out)


# ---------------------------------------------------------------- le mur gauche, près de nous
def mur_gauche(dz):
    base = (564, 1748)
    dz.F(base, U0, 1140, "fort")                                         # le pied du mur
    dz.F((300, 1425), U0, 525, "fin", 0.7)                               # le haut du soubassement
    dz.F((880, 1371), 882, 1140, "fin", 0.7)
    dz.L((525, 175), fu(base, 525), "moyen")                             # le jambage blanc du cadre
    # le crochet
    dz.L((400, 872), (400, 928), "fin"); dz.courbe([(400, 928), (403, 936), (411, 936), (414, 928)], 0.22)
    # la fenêtre basse : appui de pierre, ébrasement ; la grille est relevée (fers forgés)
    dz.L((297, V0), (297, 480), "fin")
    dz.L((307, fu((307, -4), 307)[1] if False else V0), (307, 486), "moyen"); dz.L((497, 199), (497, 611), "moyen")
    dz.L(fu((490, 192), 307 if 192 > V0 else 307), (497, 199), "moyen") if False else dz.F((490, 192), 400, 497, "moyen")
    dz.F((502, 614), 307, 497, "moyen")
    dz.F((504, 626), 286, 512, "moyen"); dz.F((512, 648), 290, 512, "fin")
    dz.L(fu((504, 626), 512), fu((512, 648), 512), "fin")
    # le panneau bleu (compteur) et sa serrure
    dz.poly([(294, 1513), (457, 1476), (469, 1650), (291, 1701)], "moyen")
    dz.courbe([P(355, 1598), P(359, 1601)], 0.4, mm=True)
    # la barre bleue et son crochet en haut
    dz.L((507, 1360), (507, 1752), "moyen"); dz.L((533, 1343), (533, 1748), "moyen")
    dz.poly([(533, 1343), (497, 1343), (497, 1360), (507, 1360)], "moyen", ferme=False)


def cadre_porte(dz):
    # le cadre de faïence : bande gauche, bande du haut, bande droite, tableau, sous-face, seuil
    for (pl, a1, a2, b1, b2) in (("mur", 3.158, 3.38, 0.0, 3.96), ("mur", 4.50, 4.773, 0.0, 3.96), ("mur", 3.38, 4.50, 3.66, 3.96),
                                 ("mur", 3.38, 4.50, 0.0, 0.10), ("tableau", XD, XL, 0.10, 3.66)):
        carreaux(dz, pl, a1, a2, b1, b2)
    carreaux(dz, "fond", 3.3, 4.6, 2.6, 4.2, clip=[(627, 362), (844, 590), (768, 587), (626, 454)])   # vu seulement par la baie
    M = lambda y, z: pr(XL, y, z)
    for z in (3.158, 4.773): dz.L(M(0, z), M(3.96, z), "fort")              # bords extérieurs du cadre
    dz.L(M(3.96, 3.158), M(3.96, 4.773), "moyen")
    dz.L(M(3.66, 3.38), M(3.66, 4.50), "moyen")                              # le haut de la baie
    dz.L(M(0.10, 3.38), M(3.66, 3.38), "moyen"); dz.L(M(0.10, 4.50), M(3.66, 4.50), "moyen")
    dz.L(pr(XD, 0.10, 4.50), pr(XD, 3.66, 4.50), "fin")                       # fond du tableau
    # le seuil de marbre
    dz.L(M(0.10, 3.38), M(0.10, 4.50), "moyen"); dz.L(pr(XD, 0.10, 3.85), pr(XD, 0.10, 4.50), "fin")
    dz.L(pr(XD, 0.10, 4.50), M(0.10, 4.50), "fin")


def porte(dz):
    # la porte, dans son plan en retrait : vantail, chambranle, panneaux à baguette, poignées
    dz.L((626, 454), (626, 1636), "moyen"); dz.L((748, 573), (748, 1574), "moyen"); dz.L((768, 587), (768, 1572), "fin")
    dz.F((767, 1575), 626, 768, "moyen")                                    # le bas du vantail
    dz.F((756, 836), 626, 748, "moyen"); dz.F((756, 851), 626, 748, "fin")  # la traverse sous l'imposte
    for (a, b, t, bas) in ((682, 725, 856, 1215), (680, 721, 1330, 1509)):
        dz.poly([fu((a, t), a), fu((a, t), b), fu((a, bas), b), fu((a, bas), a)], "moyen")
        dz.poly([fu((a + 6, t + 9), a + 6), fu((a + 6, t + 9), b - 6), fu((a + 6, bas - 8), b - 6), fu((a + 6, bas - 8), a + 6)], "fin")
    for v in (1228, 1243, 1296, 1314):                                       # la traverse aux poignées
        dz.F((700, v), 640, 745, "fin", 0.8)
    for cu, cv, r in ((714, 1267, 7), (735, 1266, 6)):
        dz.courbe([(cu + r * math.cos(t), cv + r * 1.1 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 14)], 0.25, ferme=True)
    dz.poly([(655, 1262), (668, 1262), (668, 1288), (655, 1288)], "fin")      # l'entrée de serrure
    dz.poly([(770, 1040), (798, 1040), (798, 1062), (770, 1062)], "fin")      # la plaquette sur le tableau
    # l'imposte en fer forgé : barres ondulées, montant au milieu
    dz.F((626, 454), 626, 768, "fin")
    dz.L((687, fu((626, 454), 687)[1]), (687, fu((756, 836), 687)[1]), "fin")
    for v0 in range(498, 760, 38):
        pts = []
        for u in np.linspace(628, 746, 30):
            base = fu((626, v0), u)[1]; k = (PFU - u) / (PFU - 626)
            pts.append((u, base + 4.5 * k * math.sin((u - 626) / 15.0 * math.pi)))
        dz.courbe(pts, 0.2, 0.75)
    for u in (640, 666, 708, 734):                                           # les volutes du haut
        cv = fu((626, 470), u)[1]; dz.spirale(u, cv + 6, 6 * (PFU - u) / (PFU - 626), 1.4, 1 if u < 690 else -1, 0, 0.18)


def auvent(dz):
    """l'auvent au-dessus de la porte : dessous en pente, bandeau, tuiles rondes"""
    zn, zf, xo = 3.12, 4.76, -1.85
    A = lambda x, y, z: pr(x, y, z)
    face = [A(XL, 4.05, zn), A(xo, 4.01, zn), A(xo, 3.87, zn), A(XL, 3.96, zn)]
    dz.poly(face, "moyen", fond=FOND)
    dz.poly([A(XL, 3.96, zn), A(xo, 3.87, zn), A(xo, 3.87, zf), A(XL, 3.96, zf)], "moyen", fond=FOND)   # le dessous
    dz.poly([A(xo, 4.01, zn), A(xo, 4.01, zf), A(xo, 3.87, zf), A(xo, 3.87, zn)], "moyen", fond=FOND)   # le bandeau
    dz.L(A(xo, 3.95, zn), A(xo, 3.95, zf), "fin", 0.7)
    dz.L(A(XL, 3.96, zf), A(xo, 3.87, zf), "fin")
    n = 14
    for i in range(n):                                                       # les tuiles rondes
        z1, z2 = zn + (zf - zn) * i / n, zn + (zf - zn) * (i + 1) / n
        zc, r = (z1 + z2) / 2, (z2 - z1) / 2
        dz.courbe([A(xo, 4.01 + 0.9 * r * math.sin(t), zc - r * math.cos(t)) for t in np.linspace(0, math.pi, 12)], 0.24)


def tuyaux(dz):
    # le col de cygne noir et son boîtier, le conduit blanc, la 2e barre bleue, la petite boîte bleue
    dz.courbe(lisse([(880, 620), (905, 624), (915, 640), (917, 665), (917, 690)]), 0.35)
    dz.courbe(lisse([(880, 628), (903, 632), (909, 645), (910, 665), (910, 690)]), 0.25)
    dz.poly([(900, 690), (930, 690), (930, 728), (900, 728)], "moyen")
    dz.L((899, 730), (899, 1300)); dz.L((908, 730), (908, 1300))
    for v in (850, 1050, 1250): dz.L((897, v), (910, v))
    dz.poly([(936, 1296), (948, 1294), (948, 1525), (936, 1527)], "moyen")
    dz.poly([(891, 1386), (917, 1382), (918, 1480), (891, 1486)], "moyen")


def fenetre_grille(dz):
    # la petite fenêtre à barreaux
    dz.poly([(1005, 977), (1087, 1023), (1081, 1273), (1006, 1276)], "moyen")
    dz.poly([(1009, 985), (1083, 1027), (1077, 1269), (1010, 1271)], "fin")
    for u in (1028, 1052):
        dz.L(fu((1005, 977), u), fu((1006, 1276), u), "fin")
    for k in range(1, 8):
        dz.F((1008, 977 + 36.5 * k), 1007, 1082, "fin")
    dz.F((1006, 1281), 1003, 1084, "fin")


def porte_arc(dz):
    # la vieille porte à arc (encadrement de pierre), le pilier blanc et sa borne
    dz.L((1140, 930), (1140, 1458), "moyen"); dz.L((1218, 930), (1218, 1445), "moyen")
    dz.poly([(1148, 929), (1200, 929), (1200, 1020), (1148, 1020)], "fin")
    dz.courbe(lisse([(1150, 1430), (1150, 1110), (1160, 1050), (1187, 1009), (1210, 1050), (1215, 1110), (1215, 1430)]), 0.3)
    dz.courbe(lisse([(1160, 1428), (1160, 1112), (1168, 1080), (1189, 1066), (1203, 1085), (1205, 1112), (1205, 1426)]), 0.3)
    dz.L((1180, 1100), (1180, 1426), "fin"); dz.L((1168, 1090), (1168, 1426), "fin", 0.6)
    for v in (1426, 1452): dz.L((1143, v), (1223, v - 10), "fin")
    dz.L((1225, 900), (1225, 1428), "moyen"); dz.L((1278, 900), (1278, 1425), "moyen")
    dz.poly([(1247, 1206), (1257, 1206), (1257, 1222), (1247, 1222)], "fin")
    dz.courbe(lisse([(1217, 1466), (1219, 1440), (1240, 1424), (1265, 1426), (1280, 1440), (1281, 1466)]) + [P(1217, 1466)], 0.25,
              ferme=True, fond=FOND, mm=False) if False else dz.courbe(lisse([(1217, 1466), (1219, 1440), (1240, 1424), (1265, 1426), (1280, 1440), (1281, 1466)]), 0.25)
    dz.L((1217, 1466), (1281, 1466), "fin")


def haut_gauche(dz, fer):
    # la haute fenêtre et son appui, les fils, les balcons du fond et leurs auvents, la lanterne
    for u in (1121, 1129, 1163): dz.L(fu((1121, 256), u), fu((1121, 624), u), "fin")
    dz.F((1121, 256), 1121, 1163, "fin"); dz.F((1121, 624), 1121, 1163, "fin")
    dz.poly([(1118, 622), (1203, 690), (1203, 714), (1118, 642)], "moyen")
    dz.L((965, V0), (1257, 760), "fin", 0.7)                                 # le câble électrique
    dz.L((1086, 700), (1234, 900), "fin", 0.7); dz.L((1090, 700), (1238, 896), "fin", 0.5)
    dz.poly([(1228, 871), (1238, 871), (1238, 900), (1228, 900)], "fin")
    dz.L((1269, 180), (1269, 1000), "fin")                                   # le mur du fond à gauche
    for pts in ([(1266, 190), (1318, 214), (1326, 335), (1272, 302)], [(1263, 636), (1310, 660), (1323, 730), (1270, 705)]):
        dz.poly(pts, "fin", fond=FOND)
    for nom in ("B1", "B2", "B4", "W1"):                                     # les fers forgés relevés sur la photo
        for c in fer[nom]:
            if len(c) >= 2 and sum(math.dist(c[i], c[i + 1]) for i in range(len(c) - 1)) > {"B1": 22, "B2": 18, "B4": 18, "W1": 10}[nom]:
                dz.exact(c, 0.17 if nom != "W1" else 0.22, 0.8)
    dz.L((1125, 256), (1125, 630), "fin")
    dz.courbe(lisse([(1125, 256), (1160, 300), (1185, 380), (1205, 460), (1225, 530), (1236, 580), (1225, 620), (1195, 640), (1150, 640), (1125, 630)]), 0.26)
    # la lanterne sur sa potence
    dz.poly([(1344, 387), (1379, 387), (1400, 421), (1319, 421)], "moyen", fond=FOND)
    dz.poly([(1352, 372), (1371, 372), (1379, 387), (1344, 387)], "fin", fond=FOND)
    dz.L((1361, 360), (1361, 372), "fin")
    dz.poly([(1325, 421), (1394, 421), (1381, 495), (1338, 495)], "moyen", fond=FOND)
    for u0, u1 in ((1348, 1352), (1371, 1367)): dz.L((u0, 421), (u1, 495), "fin")
    for v in (440, 458, 476): dz.L((1328 + (v - 421) * 0.17, v), (1391 - (v - 421) * 0.17, v), "fin", 0.5)
    dz.poly([(1338, 495), (1381, 495), (1377, 507), (1342, 507)], "fin", fond=FOND)
    dz.L((1350, 507), (1350, 585)); dz.L((1361, 507), (1361, 585))
    dz.courbe(lisse([(1350, 560), (1320, 548), (1295, 545), (1270, 548)]), 0.28)
    dz.spirale(1305, 556, 7, 1.4, 1, 0, 0.18)


# ---------------------------------------------------------------- le fond et le côté droit
def fond(dz):
    # le mur ocre au bout de la ruelle (de face) : son pied, ses bords, l'enduit tombé par plaques
    dz.L((1290, 1420), (1548, 1420), "moyen")
    dz.L((1290, 1000), (1290, 1420), "fin"); dz.L((1548, 980), (1548, 1640), "moyen")
    for pts in ([(1300, 1240), (1318, 1228), (1345, 1236), (1360, 1262), (1352, 1300), (1330, 1330), (1308, 1320), (1300, 1290)],
                [(1302, 1150), (1325, 1146), (1333, 1172), (1318, 1196), (1303, 1188)],
                [(1372, 1290), (1395, 1286), (1410, 1305), (1400, 1330), (1378, 1328)],
                [(1320, 1050), (1345, 1046), (1352, 1070), (1335, 1090), (1318, 1080)]):
        dz.courbe(lisse(pts + pts[:1]), 0.18, 0.6)
    dz.courbe([(1304 + 3 * math.cos(t), 1405 + 3 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 10)], 0.25, ferme=True)


def balcon_droit(dz, fer):
    dz.courbe(lisse([(1592, 500), (1575, 560), (1555, 640), (1530, 720), (1500, 800), (1475, 880), (1460, 960), (1462, 1030),
                     (1480, 1070), (1520, 1086), (1565, 1080), (1592, 1062)]), 0.3)
    dz.L((1592, 500), (1592, 1062), "fin"); dz.L((1560, 500), (1592, 500), "fin")
    for c in fer["B3"]:
        if len(c) >= 2 and sum(math.dist(c[i], c[i + 1]) for i in range(len(c) - 1)) > 22:
            dz.exact(c, 0.17, 0.8)


def droite(dz):
    # la pierre rose, le pilier de marbre cannelé, le cadre bleu de la porte, l'ébrasement à côtes
    for u in (1553, 1600, 1707, 1757): dz.L((u, V0), (u, {1553: 1650, 1600: 1525, 1707: 1607, 1757: 1607}[u]), "moyen")
    dz.L((1740, V0), (1740, 1600), "fin")
    for u in (1625, 1643, 1661, 1680):                                       # les cannelures, terminées en pointe
        dz.L((u, V0), (u, 1480), "fin", 0.7); dz.L((u + 6, V0), (u + 6, 1480), "fin", 0.5)
        dz.courbe([(u, 1480), (u + 3, 1494), (u + 6, 1480)], 0.18, 0.7)
    dz.L((1600, 1521), (1707, 1550), "moyen"); dz.L((1600, 1540), (1707, 1568), "fin")   # la base du pilier
    dz.L((1600, 1525), (1600, 1686), "moyen"); dz.L((1707, 1550), (1707, 1690), "moyen")
    dz.L((1600, 1686), (1707, 1690), "moyen")
    for u in np.arange(1765, 1812, 8):                                       # l'ébrasement à côtes, en bas à droite
        dz.L((u, 1640 + (u - 1757) * 0.3), (u, 1950), "fin", 0.6)
    dz.L((1757, 1640), (1815, 1658), "fin")
    # les marches de marbre
    dz.L((1555, 1666), (1676, V1), "moyen"); dz.L((1543, 1676), (1655, V1), "fin")
    dz.L((1543, 1650), (1600, 1686), "fin"); dz.L((1543, 1650), (1543, 1676), "fin")
    dz.L((1682, 1655), (1764, V1), "moyen"); dz.L((1672, 1660), (1752, V1), "fin")
    dz.L((1707, 1690), (1764, 1710), "fin")


def banc(dz):
    # le banc couvert de sa couverture rayée
    face = [(1289, 1543), (1500, 1543), (1505, 1622), (1283, 1615)]
    dz.poly([(1289, 1543), (1400, 1482), (1420, 1362), (1480, 1348), (1545, 1345), (1550, 1640), (1505, 1622), (1283, 1615)],
            "fin", fond=FOND)
    dz.poly(face, "moyen")
    dz.courbe(lisse([(1420, 1362), (1450, 1352), (1480, 1348), (1515, 1345), (1545, 1345)]), 0.3)
    dz.L((1400, 1482), (1420, 1362), "moyen"); dz.L((1400, 1482), (1540, 1478), "moyen"); dz.L((1500, 1543), (1540, 1478), "moyen")
    dz.L((1289, 1543), (1400, 1482), "moyen"); dz.L((1545, 1345), (1550, 1640), "moyen")
    for v in (1380, 1395, 1414, 1428, 1446, 1464):                           # les rayures
        dz.L((1420 - (v - 1362) * 0.17, v), (1546, v - 2), "fin", 0.55)
    for t in (0.3, 0.55, 0.8):
        a = (1289 + (1400 - 1289) * t, 1543 - 61 * t); b = (1500 + 40 * t, 1543 - 65 * t)
        dz.L(a, b, "fin", 0.55)
    for v in (1556, 1568, 1586, 1601): dz.L((1288, v), (1502, v + 2), "fin", 0.55)
    for u in np.arange(1288, 1505, 7): dz.L((u, 1616 + (u - 1283) * 0.03), (u - 1, 1626 + (u - 1283) * 0.03), "fin", 0.6)   # les franges
    for u in (1340, 1450): dz.L((u, 1620), (u, 1632), "moyen")
    dz.courbe(lisse([(1422, 1350), (1440, 1333), (1465, 1328), (1490, 1336), (1500, 1348)]), 0.2, 0.7)   # le panier derrière


def sol(dz):
    # les dalles irrégulières, la plaque d'égout
    r = random.Random(8)
    z, rangs = 1.9, []
    while z < 10.2:
        rangs.append(z); z += r.uniform(0.26, 0.42) * (1 + z / 18)
    sous = Crayon(77)
    for i, z in enumerate(rangs):
        xs = np.linspace(-2.6, 0.5, 14)
        pts = [P3(x, 0, z + r.uniform(-0.04, 0.04)) for x in xs]
        for a, b in zip(pts[:-1], pts[1:]): sous.trait(a, b, "fin", "#3a3a3a", 0.42, depasse=False)
        if i + 1 < len(rangs):
            x = -2.6 + r.uniform(0, 0.4)
            while x < 0.5:
                x2 = x + r.uniform(-0.08, 0.08)
                sous.trait(P3(x, 0, z), P3(x2, 0, rangs[i + 1]), "fin", "#3a3a3a", 0.42, depasse=False)
                x += r.uniform(0.32, 0.62)
    zone = [(U0, V1), (U0, 1887), (1140, 1455), (1222, 1440), (1290, 1420), (1548, 1420), (1548, 1676), (1543, 1676), (1655, V1)]
    dz.clip(zone, "".join(sous.out))
    xc, zc, R = -1.69, 3.84, 0.305
    pts = [pr(xc + R * math.cos(t), 0, zc + R * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 40)[:-1]]
    dz.courbe(pts, 0.3, ferme=True, fond=FOND)
    dz.courbe([pr(xc + 0.86 * R * math.cos(t), 0, zc + 0.86 * R * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 40)[:-1]], 0.2, 0.7, ferme=True)


# ---------------------------------------------------------------- la construction, en bleu
def construction():
    c = Crayon(7)
    for i in range(-8, 4):                                                    # grille de report de 3 cm, depuis le PF
        x = PF[0] + 30 * i
        if FX0 < x < FX1: c.trait((x, FY0), (x, FY1), "construction", CON, 0.22, depasse=False)
    for j in range(-7, 5):
        y = LHY + 30 * j
        if FY0 < y < FY1 and j: c.trait((FX0, y), (FX1, y), "construction", CON, 0.22, depasse=False)
    for p in ((564, 1748), (300, 1425), (566, 179), (1006, 1276), (1005, 977), (1555, 1666), (497, 199), (759, 146)):
        a = P(*p); d = np.subtract(a, PF)
        ts = [t for t in ((FX0 - PF[0]) / d[0] if d[0] else 9e9, (FY0 - PF[1]) / d[1] if d[1] else 9e9,
                          (FY1 - PF[1]) / d[1] if d[1] else 9e9, (FX1 - PF[0]) / d[0] if d[0] else 9e9) if t > 0]
        t = min(ts); c.trait((PF[0] + t * d[0], PF[1] + t * d[1]), PF, "construction", CON, 0.8, depasse=False, tirets="2 1.4")
    c.trait((0, LHY), (PAGE_W, LHY), "moyen", CON, 0.9, depasse=False, tirets="4 1.4 0.7 1.4")
    c.trait((FX0 - 6, FY1), (FX1 + 6, FY1), "construction", CON, 0.85, depasse=False, tirets="1.6 1.2")
    c.texte(FX0 - 1.5, LHY - 1.3, "LH", 4.2, CON, "end"); c.texte(FX1 + 1.5, LHY - 1.3, "LH", 4.2, CON, "start")
    c.texte(FX0 - 1.5, FY1 - 1.3, "LT", 3.8, CON, "end"); c.texte(FX1 + 1.5, FY1 - 1.3, "LT", 3.8, CON, "start")
    c.out.append(f'<circle cx="{PF[0]:.2f}" cy="{LHY:.2f}" r="3" fill="none" stroke="{CON}" stroke-width="0.35"/>')
    c.point(PF[0], LHY, CON, 0.7)
    c.texte(PF[0] - 4, LHY - 4, "PF", 4.4, CON, "end")
    xc = FX1 + 6                                                              # cote : 1,20 m, dans la marge
    c.trait((xc, FY1), (xc, LHY), "moyen", CON, 0.95, depasse=False)
    for y, s in ((FY1, -1), (LHY, 1)):
        c.trait((xc - 1.2, y), (xc + 1.2, y), "moyen", CON, 0.95, depasse=False)
        c.trait((xc, y), (xc - 0.8, y + s * 1.6), "moyen", CON, 0.95, depasse=False)
        c.trait((xc, y), (xc + 0.8, y + s * 1.6), "moyen", CON, 0.95, depasse=False)
    c.texte(xc + 3.2, (FY1 + LHY) / 2, "1,20 m : les yeux, assis", 3.2, CON, "middle", rot=-90)
    c.texte(FX0 + 3, LHY + 4.4, "LH : à hauteur des yeux, ASSIS (1,20 m),", 2.9, CON)
    c.texte(FX0 + 3, LHY + 8, "à la hauteur des poignées de porte", 2.9, CON)
    m = P3(-1.69, 0, 3.84)
    c.texte(m[0] - 20, m[1] + 9, "plaque d'égout : 60 cm → l'échelle", 2.9, CON)
    c.trait((m[0] - 6, m[1] + 6.4), (m[0] - 1, m[1] + 2), "construction", CON, 0.9, depasse=False)
    c.texte(FX0 + 3, 200, "les murs fuient", 2.9, CON); c.texte(FX0 + 3, 203.6, "vers le PF", 2.9, CON)
    return "".join(c.out)


def dessin():
    fer = json.load(open(os.path.join(ICI, "releve-fers-forges.json")))
    dz = Dessin(31)
    sol(dz); fond(dz); mur_gauche(dz); cadre_porte(dz); porte(dz); tuyaux(dz); fenetre_grille(dz); porte_arc(dz)
    haut_gauche(dz, fer); auvent(dz); droite(dz); balcon_droit(dz, fer); banc(dz)
    cadre = Crayon(3)
    coins = [(FX0, FY0), (FX1, FY0), (FX1, FY1), (FX0, FY1)]
    for i in range(4):
        cadre.trait(coins[i], coins[(i + 1) % 4], "fort", "#1c1c1c", 0.95)
    defs = "".join(dz.defs) + f'<clipPath id="cadre"><rect x="{FX0}" y="{FY0}" width="{FX1 - FX0}" height="{FY1 - FY0}"/></clipPath>'
    return defs, f'<g clip-path="url(#cadre)">{"".join(dz.c.out)}</g>' + construction() + "".join(cadre.out)


def textes():
    t = Crayon(4)
    t.texte(FX0, 13, "La ruelle aux portes bleues · vue assise", 6.6, "#1f1f1f")
    t.texte(FX0, 20, "perspective frontale · 1 point de fuite · assis près des marches de droite, vers le fond de la ruelle", 3.3, "#555")
    etapes = ["1  le cadre, la LH (yeux assis, 1,20 m), le PF à droite du milieu",
              "2  le pied des murs, le haut du soubassement : fuyantes vers le PF",
              "3  le cadre de faïence et la porte (en retrait), l'auvent",
              "4  les fenêtres, les balcons, la lanterne, la porte à arc",
              "5  à droite : pilier cannelé, cadre bleu, marches ; le banc",
              "6  le sol : dalles irrégulières, plaque d'égout"]
    for i, e in enumerate(etapes):
        t.texte(FX0 + (i // 3) * 134, 28.5 + (i % 3) * 3.9, e, 2.9, CON)
    for i, l in enumerate(["en bleu : la construction (LH, LT, PF, fuyantes) · au crayon : le croquis, au trait, sans hachures",
                           "carreaux bleus de 3 cm, partant du PF, pour reporter le dessin",
                           "relevé sur la photo redressée (verticales verticales) · pas de plantes",
                           "les dalles du sol : leur dessin est représentatif, pas pierre par pierre"]):
        t.texte(FX0, 391 + i * 5, l, 3.0, "#666", halo=False)
    return "".join(t.out)


def etiquettes_a4():
    t = Crayon(9)
    t.texte(6, JONCTION / 2, "feuille 1/2 · moitié HAUTE de l'A3 · la jonction est en bas ↓", 3.0, "#a0302a", "middle", rot=-90, halo=False)
    g = "".join(t.out); t.out = []
    t.texte(6, JONCTION * 1.5, "↑ la jonction est en haut · feuille 2/2 · moitié BASSE de l'A3", 3.0, "#a0302a", "middle", rot=-90, halo=False)
    return g, "".join(t.out)


if __name__ == "__main__":
    defs, corps = dessin()
    txt = textes()
    eg, ed = etiquettes_a4()
    svg = lambda vb, extra="": (f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg"><defs>{defs}</defs>'
                                f'{corps}{txt}{extra}</svg>')
    open(f"{SORTIE}/croquis-A3.html", "w", encoding="utf-8").write(html([svg(f"0 0 {PAGE_W} {PAGE_H}")], 297, 420, "Ruelle portes bleues A3"))
    open(f"{SORTIE}/croquis-2xA4.html", "w", encoding="utf-8").write(
        html([svg(f"0 0 297 {JONCTION:g}", eg), svg(f"0 {JONCTION:g} 297 {JONCTION:g}", ed)], 297, 210, "Ruelle portes bleues 2 x A4"))
    print("croquis-A3.html et croquis-2xA4.html écrits")

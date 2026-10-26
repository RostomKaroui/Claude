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
    """pied de la façade (le sol contre le mur)"""
    return sur(37, 817, x)


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


def moucharabieh(c, x1, x2, yt, yb, n=4, sorte="leger"):
    """grille en bois tourné : cadre + petits losanges, les rangs suivent les fuyantes"""
    quad_mur(c, x1, x2, yt, yb, "moyen")
    quad_mur(c, x1 + 2.5, x2 - 2.5, yt + 3, yb - 3, "fin", depasse=False)
    pas = (x2 - x1 - 5) / n; y = yt + 3 + pas * 0.6
    while y < yb - 3 - pas * 0.3:
        for i in range(n):
            cx = x1 + 2.5 + pas * (i + 0.5); cy = sur(x1, y, cx); d = pas * 0.38
            c.brisee([(cx, cy - d), (cx + d, cy), (cx, cy + d), (cx - d, cy)], sorte, ferme=True)
        y += pas * 0.95


def jaune():
    hi = cv2.imread(f"{ICI}/redresse2_jaune.jpg")
    c = Crayon(61)
    A = (497, 540); B = (497, base(497)); XP = 41

    # --- la façade (fuit doucement vers la droite)
    fuyante(c, 0, base(0), 646, "fort", double=True)                               # pied de la façade
    L_(c, 646, 0, 646, base(646), "fort", double=True)                             # bout de la façade, sur le ciel
    L_(c, 0, base(0) - 30, 37, base(37) - 30, "leger", depasse=False)              # soubassement

    # porte 1 (grande porte cloutée, à deux battants)
    quad_mur(c, 37, 170, 470, 817, "fort")
    quad_mur(c, 41, 166, 476, 811, "fin", depasse=False)
    L_(c, 86, sur(37, 476, 86), 86, sur(37, 811, 86), "moyen")                     # battants
    L_(c, 107, sur(37, 476, 107), 107, sur(37, 811, 107), "moyen")
    L_(c, 160, sur(37, 476, 160), 160, sur(37, 811, 160), "fin")
    for y in (556, 700): fuyante(c, 41, y, 86, "leger", depasse=False); fuyante(c, 107, y, 160, "leger", depasse=False)
    fuyante(c, 30, 820, 178, "moyen"); L_(c, 30, 820, 30, 828, "fin"); fuyante(c, 30, 828, 178, "fin")   # seuil
    rangees(c, 41, 86, 476, 811, (44, 83), (480, 556, 700, 806))
    rangees(c, 107, 166, 476, 811, (110, 157), (480, 556, 700, 806))
    n1 = clous(c, hi, [(115, 720, 152, 800)])

    # porte 2 (cloutée, étoile de clous, applique)
    quad_mur(c, 269, 336, 533, base(269), "fort")
    quad_mur(c, 273, 332, 538, base(273) - 4, "fin", depasse=False)
    L_(c, 287, sur(269, 538, 287), 287, sur(269, base(269) - 4, 287), "leger", depasse=False)
    fuyante(c, 273, 572, 332, "fin", depasse=False); fuyante(c, 273, 712, 332, "fin", depasse=False)
    c.cercle(311, 579, 6, "fin"); L_(c, 311, 566, 311, 573, "fin", depasse=False)       # anneau / applique
    c.courbe([(305, 586), (311, 592), (317, 586)], "leger")
    fuyante(c, 262, base(262) + 2, 345, "moyen"); fuyante(c, 262, base(262) + 9, 345, "fin")   # seuil
    rangees(c, 273, 332, 538, base(273) - 4, (276, 287, 329), (541, 572, 712, base(273) - 7))
    etoile(c, 309, sur(269, 650, 309), 13, 36)
    n2 = clous(c, hi, [(292, 720, 326, base(300) - 10)])

    # le renfoncement, la porte 3 et le linteau
    L_(c, 435, 520, 435, base(435), "moyen")                                       # pilier du renfoncement
    L_(c, A[0], A[1], A[0], B[1], "fort", double=True)                             # l'arête AB (tableau de la porte 3)
    quad_mur(c, 497, 556, 538, 553, "moyen")                                       # linteau
    quad_mur(c, 500, 526, 556, base(500) - 12, "fort")                             # porte 3 (jaune, cloutée)
    L_(c, 513, sur(500, 556, 513), 513, sur(500, base(500) - 12, 513), "leger", depasse=False)
    rangees(c, 500, 526, 556, base(500) - 12, (503, 523), (559, 650, base(500) - 15))
    etoile(c, 513, sur(500, 650, 513), 7, 30); n3 = 0
    L_(c, 553, sur(497, 553, 553), 553, base(553), "moyen")
    rect(c, 447, 574, 459, 586, "fin")                                             # boîte aux lettres
    # porte 4 (ouverte) sous le second moucharabieh
    L_(c, 575, sur(575, 560, 575), 575, base(575), "moyen"); L_(c, 624, sur(575, 560, 624), 624, base(624), "moyen")
    quad_mur(c, 572, 627, 556, 565, "moyen")
    L_(c, 582, sur(575, 568, 582), 582, base(582) - 4, "leger", depasse=False)

    # moucharabiehs et fenêtres à grille
    moucharabieh(c, 496, 559, 464, 518, 6)
    moucharabieh(c, 579, 626, 480, 533, 5)
    moucharabieh(c, 586, 621, 252, 392, 4)
    moucharabieh(c, 592, 624, 25, 108, 4)
    for x1, x2 in ((415, 434), (458, 478)):                                         # fenêtres hautes à barreaux
        quad_mur(c, x1, x2, 254, 398, "moyen")
        for x in np.linspace(x1 + 4, x2 - 4, 3): L_(c, x, sur(x1, 254, x) + 3, x, sur(x1, 398, x) - 3, "fin", depasse=False)
        for y in (300, 350): fuyante(c, x1 + 1, y, x2 - 1, "leger", depasse=False)
        fuyante(c, x1 - 4, 404, x2 + 4, "fin")                                      # appui

    moucharabieh(c, 516, 548, 256, 296, 4)
    moucharabieh(c, 462, 492, 17, 47, 3)
    L_(c, 368, 270, 368, base(368), "moyen")                                       # avant-corps éclairé
    L_(c, 441, 0, 441, 120, "fin")                                                 # retrait de la façade, en haut

    # la lanterne sur sa potence
    L_(c, 575, 240, 587, 240, "moyen"); L_(c, 575, 240, 581, 233, "fin"); L_(c, 587, 240, 581, 233, "fin")
    L_(c, 563, 250, 599, 250, "moyen"); L_(c, 575, 240, 563, 250, "fin"); L_(c, 587, 240, 599, 250, "fin")
    L_(c, 563, 250, 570, 292, "moyen"); L_(c, 599, 250, 592, 292, "moyen"); L_(c, 570, 292, 592, 292, "moyen")
    L_(c, 581, 250, 581, 292, "leger", depasse=False); L_(c, 566, 270, 596, 270, "leger", depasse=False)
    L_(c, 581, 292, 581, 330, "fin"); c.courbe([(581, 305), (592, 314), (598, 330)], "fin")
    L_(c, 576, 330, 600, 334, "fin")

    # les câbles tendus en travers
    c.courbe([(668, 152), (560, 168), (430, 186), (290, 205)], "fin")
    c.courbe([(668, 162), (580, 186), (470, 204), (330, 222)], "fin")
    c.courbe([(668, 206), (610, 214), (540, 226)], "leger")
    c.courbe([(655, 230), (620, 250), (600, 262)], "leger")

    # au fond, entre la façade et le mur de droite
    L_(c, 646, 386, 668, 384, "leger"); L_(c, 646, 450, 668, 448, "leger")

    # --- le mur de droite, tout proche, et sa porte jaune
    L_(c, 668, 0, 668, H, "fort", double=True)
    L_(c, 699, 228, 699, H, "fort"); L_(c, 718, 222, 718, H, "moyen")
    L_(c, 699, 228, 718, 222, "moyen")
    for ya, yb in ((231, 262), (536, 555), (705, 720), (795, 825)):                  # gonds
        rect(c, 696, ya, 711, yb, "fin")
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

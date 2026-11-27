"""Croquis en perspective « à la main » des deux angles, selon la méthode du cadrage à l'acétate.

Entrées : redresse_angle1.png / redresse_angle2.png (la vue dans la fenêtre de l'acétate, 40 px = 1 cm).
Sorties : croquis.html (2 pages A4) et croquis-a3.html (2 pages A3), à rendre en PDF avec rendu.js.

Méthode dessinée (en bleu, la construction) :
  1. le cadrage : la fenêtre de l'acétate et sa grille de carrés de 4 cm ;
  2. l'arête verticale AB (le coin) ;
  3. une verticale parallèle plus longue (le côté d'une fenêtre) et les horizontales A→A', B→B' ;
  4. au crayon bras tendu, les vrais points haut et bas C et D sur cette verticale ;
  5. les fuyantes AC et BD, prolongées jusqu'au point de fuite sur la ligne d'horizon.
"""
import math, json, random, sys
import numpy as np, cv2

ICI = sys.argv[1] if len(sys.argv) > 1 else "."
S = 40                      # px par cm dans les images redressées
MM = 10 / S                 # px -> mm
W, H = 680, 1040            # fenêtre de l'acétate en px (17 x 26 cm)
X0, Y0 = -0.5, -1.0         # coin de la fenêtre dans le repère de la grille (cm)
PAGE_W, PAGE_H = 210, 297   # A4 en mm
OX, OY = 20, 25             # position de la fenêtre sur la page (mm)


# ---------------------------------------------------------------- géométrie des deux angles
def sur(P, x0, y0, x):
    """y à l'abscisse x sur la droite (x0, y0) -> P"""
    return y0 + (x - x0) * (P[1] - y0) / (P[0] - x0)


ANGLES = {}

# ---- angle 1 : le mur aux fenêtres (gauche) et le mur de l'écran (fond)
yh = 305; PR = (1278, yh); PL = (-2050, yh)
A, B = (415, 141), (415, 553)
ANGLES["angle1"] = dict(
    titre="Croquis 1 · le coin des fenêtres et de l'écran",
    yh=yh, PL=PL, PR=PR, A=A, B=B, xp=135, PF=PR, cote_xp="côté de la fenêtre",
    murs=[  # (point de fuite, x de départ, y de départ, x d'arrivée, épaisseur)
        (PR, *A, 0, "fort"), (PR, *B, 0, "fort"), (PL, *A, W, "fort"), (PL, *B, W, "fort")],
    rects=[  # rectangles sur un mur : (PF, x1, x2, y haut en x1, y bas en x1, poids, remplissage)
        (PR, 14, 150, 133, 458, "moyen", None),          # fenêtre 1 : dormant
        (PR, 18, 137, 159, 237, "fin", "vitre"),
        (PR, 26, 137, 260, 431, "fin", "vitre"),
        (PR, 248, 333, 182, 416, "moyen", None),         # fenêtre 2
        (PR, 253, 324, 193, 246, "fin", "vitre"),
        (PR, 259, 325, 271, 408, "fin", "vitre"),
        (PR, 349, 412, 195, 405, "moyen", None),         # fenêtre 3
        (PR, 353, 407, 205, 253, "fin", "vitre"),
        (PR, 355, 409, 272, 398, "fin", "vitre"),
        (PR, 147, 278, 107, 168, "moyen", None),         # climatiseur
        (PR, 162, 206, 268, 420, "fin", "panneau"),      # panneaux acoustiques
        (PR, 209, 250, 268, 418, "fin", "panneau"),
        (PR, 165, 250, 440, 588, "fin", "panneau"),
        (PR, 262, 334, 425, 505, "fin", "panneau"),
        (PR, 262, 334, 511, 575, "fin", "panneau"),
        (PR, 362, 411, 418, 485, "fin", "panneau"),
        (PR, 362, 411, 491, 547, "fin", "panneau"),
        (PR, 78, 172, 490, 612, "moyen", "radiateur"),   # radiateur
        (PL, 420, W, 150, 518, "fort", "ecran"),         # l'écran
        (PL, 426, W, 156, 512, "fin", None),
    ],
    lignes=[  # traits libres (x1, y1, x2, y2, poids)
        (14, 236, 150, sur(PR, 14, 236, 150), "fin"), (14, 258, 150, sur(PR, 14, 258, 150), "fin"),
        (147, 175, 278, sur(PR, 147, 175, 278), "fin"),
    ] + [(x, sur(PR, *A, x), x, sur(PR, *B, x), "moyen") for x in (152, 246, 340)],
    spots=[(320, 75, 110), (408, 58, 95), (378, 108, 135), (489, 95, 120), (517, 48, 85)],
    ecran=[(420, 150), (W, sur(PL, 420, 150, W)), (W, sur(PL, 420, 518, W)), (420, 518)],
    personnes=[],
    zone_plafond=150,
)

# ---- angle 2 : le bureau vitré (gauche) et le mur rouge aux fenêtres (droite)
yh = 372; PR = (1850, yh); PL = (-620, yh)
A, B = (350, 112), (350, 633)
ANGLES["angle2"] = dict(
    titre="Croquis 2 · le bureau vitré et le mur rouge",
    yh=yh, PL=PL, PR=PR, A=A, B=B, xp=500, PF=PL, cote_xp="côté de la fenêtre",
    murs=[(PL, *A, W, "fort"), (PL, *B, W, "fort"),
          (PR, 350, 153, 41, "fort"), (PR, 350, 638, 41, "fort"),          # bureau vitré : face avant
          (PL, 41, sur(PR, 350, 153, 41), 0, "moyen"), (PL, 41, sur(PR, 350, 638, 41), 0, "moyen")],
    rects=[
        (PL, 379, 507, 197, 477, "moyen", None),         # fenêtre
        (PL, 385, 502, 223, 281, "fin", "vitre"),
        (PL, 385, 498, 305, 450, "fin", "vitre"),
        (PL, 487, W, 100, 203, "moyen", None),           # climatiseur
        (PL, 510, W, 205, 292, "fin", "panneau"),        # panneaux rouges
        (PL, 508, 579, 300, 473, "fin", "panneau"),
        (PL, 585, 667, 300, 473, "fin", "panneau"),
        (PL, 507, 657, 487, 697, "fin", "panneau"),
        (PL, 368, 483, 480, 570, "fin", "panneau"),
        (PL, 368, 483, 576, 660, "fin", "panneau"),
        (PR, 75, 130, 540, 650, "fin", "radiateur"),     # radiateur dans le bureau
        (PR, 300, 340, 567, 620, "fin", None),           # mallette
    ],
    lignes=[
        (41, sur(PR, 350, 153, 41), 41, sur(PR, 350, 638, 41), "moyen"),   # montants du vitrage
        (200, sur(PR, 350, 153, 200), 200, sur(PR, 350, 638, 200), "moyen"),
        (350, 153, 41, sur(PR, 350, 153, 41) + 0, "fin"),
        (350, 161, 41, sur(PR, 350, 161, 41), "fin"),                         # profil haut du vitrage
        (80, sur(PR, 213, 437, 80), 213, 437, "fort"),                        # barre de la porte
        (143, 400, 143, 557, "moyen"),
        (0, 470, 143, sur(PR, 0, 470, 143), "fin"), (143, sur(PR, 0, 470, 143), 143, 655, "fin"),   # comptoir
        (372, sur(PL, *A, 372), 372, sur(PL, *B, 372), "moyen"),             # poteau sombre
        (487, 210, W, sur(PL, 487, 210, W), "fin"),                           # dessous du climatiseur
        (313, 567, 313, 560, "fin"), (327, 567, 327, 560, "fin"), (313, 560, 327, 560, "fin"),   # poignée mallette
    ],
    rideaux=(120, 207, 175, 560),
    personnes=[(107, 412)],
    spots=[],
    ecran=None,
    zone_plafond=118,
)


# ---------------------------------------------------------------- lignes relevées automatiquement (plafond, sol)
def releve(nom, c):
    im = cv2.imread(f"{ICI}/redresse_{nom}.png", cv2.IMREAD_GRAYSCALE)
    im = cv2.createCLAHE(2.0, (8, 8)).apply(cv2.GaussianBlur(im, (3, 3), 0))
    L = cv2.createLineSegmentDetector(cv2.LSD_REFINE_STD).detect(im)[0].reshape(-1, 4)
    L = L[np.hypot(L[:, 2]-L[:, 0], L[:, 3]-L[:, 1]) > 0.5*S]
    PL, PR, A, B = c["PL"], c["PR"], c["A"], c["B"]
    plafond, sol = [], []
    yL = sur(PR, *B, 0); yR = sur(PL, *B, W)
    poly_sol = np.float32([(0, yL), B, (W, yR), (W, H), (0, H)])
    for x1, y1, x2, y2 in L:
        m = np.array([(x1+x2)/2, (y1+y2)/2]); d = np.array([x2-x1, y2-y1]); lg = np.linalg.norm(d); d /= lg
        best, dev = None, 99
        for k, v in {"V": np.array([0, 1.0]), "L": np.subtract(PL, m), "R": np.subtract(PR, m)}.items():
            v = v/np.linalg.norm(v); a = math.degrees(math.acos(min(1, abs(d @ v))))
            if a < dev: best, dev = k, a
        if dev > 2.5: continue
        if m[1] < c["zone_plafond"] and m[1] < sur(PR, *c["A"], m[0]) + 4 and m[1] < sur(PL, *c["A"], m[0]) + 4:
            if best == "V": plafond.append(("V", (m[0], m[1]-lg/2), (m[0], m[1]+lg/2)))
            else:
                P = PL if best == "L" else PR; v = np.subtract(P, m); v = v/np.linalg.norm(v)
                plafond.append((best, tuple(m-v*lg/2), tuple(m+v*lg/2)))
        elif best in "LR" and cv2.pointPolygonTest(poly_sol, tuple(map(float, m)), False) > 0 and m[1] > c["yh"] + 2.5*S:
            P = PL if best == "L" else PR
            sol.append((best, math.degrees(math.atan2(m[1]-P[1], m[0]-P[0])), lg))
    # sol : un joint = une droite vers son point de fuite, prolongée sur tout le sol (doublons fusionnés)
    joints = []
    for fam in "LR":
        angs = sorted([(a, lg) for f, a, lg in sol if f == fam])
        groupes = []
        for a, lg in angs:
            if groupes and abs(a - groupes[-1][-1][0]) < 0.6: groupes[-1].append((a, lg))
            else: groupes.append([(a, lg)])
        for g in groupes:
            if sum(lg for _, lg in g) < 1.2*S: continue
            a = sum(a*lg for a, lg in g) / sum(lg for _, lg in g)
            P = PL if fam == "L" else PR
            joints.append((P, a))
    # plafond : fusion des segments alignés
    traits = []
    for fam in ("V", "L", "R"):
        segs = [s for s in plafond if s[0] == fam]
        if fam == "V":
            segs.sort(key=lambda s: s[1][0]); grp = []
            for s in segs:
                if grp and abs(s[1][0] - grp[-1][-1][1][0]) < 3: grp[-1].append(s)
                else: grp.append([s])
            for g in grp:
                x = np.mean([s[1][0] for s in g]); y1 = min(min(s[1][1], s[2][1]) for s in g); y2 = max(max(s[1][1], s[2][1]) for s in g)
                if y2 - y1 > 0.5*S: traits.append((x, y1, x, y2, "fin"))
            continue
        P = PL if fam == "L" else PR
        def ang(s):
            m = np.add(s[1], s[2]) / 2; return math.degrees(math.atan2(m[1]-P[1], m[0]-P[0]))
        segs.sort(key=ang); grp = []
        for s in segs:
            if grp and abs(ang(s) - ang(grp[-1][-1])) < 0.12: grp[-1].append(s)
            else: grp.append([s])
        for g in grp:
            xs = [p[0] for s in g for p in (s[1], s[2])]
            a = np.mean([ang(s) for s in g]); x1, x2 = min(xs), max(xs)
            t = math.tan(math.radians(a))
            y = lambda x: P[1] + (x - P[0]) * t
            if x2 - x1 > 0.6*S: traits.append((x1, y(x1), x2, y(x2), "fin"))
    return traits, joints, poly_sol


# ---------------------------------------------------------------- rendu « à la main »
class Crayon:
    def __init__(self, graine):
        self.r = random.Random(graine); self.out = []

    def trait(self, p, q, poids="moyen", couleur="#2a2a2a", op=None, depasse=True, double=False, tirets=None):
        lw = {"fort": 0.42, "moyen": 0.32, "fin": 0.22, "construction": 0.18}[poids]
        op = op if op is not None else {"fort": 0.9, "moyen": 0.85, "fin": 0.75, "construction": 0.75}[poids]
        for k in range(2 if double else 1):
            self.out.append(self._chemin(p, q, lw*(0.8 if k else 1), couleur, op*(0.45 if k else 1), depasse, k, tirets))

    def _chemin(self, p, q, lw, couleur, op, depasse, k, tirets):
        r = self.r
        p, q = np.array(p, float), np.array(q, float); d = q - p; L = np.linalg.norm(d)
        if L < 1e-6: return ""
        u = d / L; n = np.array([-u[1], u[0]])
        e1 = r.uniform(0.6, 2.0) if depasse else 0; e2 = r.uniform(0.6, 2.0) if depasse else 0
        p = p - u*e1; q = q + u*e2; L = L + e1 + e2
        amp = min(0.28, 0.05 + L*0.0025) * (1.4 if k else 1)
        ph1, ph2 = r.uniform(0, 6.3), r.uniform(0, 6.3); f1, f2 = r.uniform(0.6, 1.4), r.uniform(2, 3.5)
        dec = r.uniform(-0.18, 0.18) if k else 0
        npts = max(4, int(L / 3))
        pts = []
        for i in range(npts + 1):
            t = i / npts
            w = amp*(math.sin(math.pi*f1*t*2 + ph1)*0.7 + math.sin(math.pi*f2*t*2 + ph2)*0.3) + dec
            x, y = p + d/np.linalg.norm(d)*L*t + n*w
            pts.append(f"{x:.2f},{y:.2f}")
        da = f' stroke-dasharray="{tirets}"' if tirets else ""
        return (f'<polyline points="{" ".join(pts)}" fill="none" stroke="{couleur}" stroke-width="{lw:.2f}" '
                f'stroke-opacity="{op:.2f}" stroke-linecap="round" stroke-linejoin="round"{da}/>')

    def texte(self, x, y, t, taille=4.2, couleur="#2c5aa0", ancre="start", police="main", rot=0, halo=True):
        fam = "'Architects Daughter', 'Caveat', cursive" if police == "main" else "'Caveat', cursive"
        tr = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot else ""
        self.out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{taille}" fill="{couleur}" '
                        f'text-anchor="{ancre}"{tr}' + (' stroke="#fdfcf8" stroke-width="1.1" stroke-linejoin="round" paint-order="stroke"' if halo else '') + f'>{t}</text>')

    def point(self, x, y, couleur="#2c5aa0", r=0.7):
        self.out.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{couleur}"/>')


def page(nom, c, graine):
    P = lambda x, y: (OX + x*MM, OY + y*MM)          # px de la fenêtre -> mm sur la page
    cr = Crayon(graine)
    CON = "#2f62b0"                                    # crayon bleu de construction
    traits_auto, joints, poly_sol = releve(nom, c)
    defs = []

    # 1 · le cadrage : la fenêtre de l'acétate et la grille de 4 cm
    for i in range(5):
        x = (0 + 4*i - X0) * S
        cr.trait(P(x, 0), P(x, H), "construction", CON, 0.32, depasse=False)
    for j in range(7):
        y = (0 + 4*j - Y0) * S
        cr.trait(P(0, y), P(W, y), "construction", CON, 0.32, depasse=False)
    coins = [(0, 0), (W, 0), (W, H), (0, H)]
    for i in range(4):
        cr.trait(P(*coins[i]), P(*coins[(i+1) % 4]), "fort", "#1c1c1c", 0.95, depasse=True)
    defs.append(f'<clipPath id="fen-{nom}"><rect x="{OX}" y="{OY}" width="{W*MM}" height="{H*MM}"/></clipPath>')

    corps = Crayon(graine + 1)
    # sol : joints du carrelage
    for Pf, a in joints:
        t = math.tan(math.radians(a)); xs = np.linspace(-50, W + 50, 2)
        p0 = (xs[0], Pf[1] + (xs[0]-Pf[0])*t); p1 = (xs[1], Pf[1] + (xs[1]-Pf[0])*t)
        corps.trait(P(*p0), P(*p1), "fin", "#3a3a3a", 0.55, depasse=False)
    sol_mm = " ".join(f"{OX + x*MM:.2f},{OY + y*MM:.2f}" for x, y in poly_sol)
    defs.append(f'<clipPath id="sol-{nom}"><polygon points="{sol_mm}"/></clipPath>')
    sol_svg = "".join(corps.out); corps.out = []

    # murs, plafond, détails
    for Pf, x0, y0, x1, poids in c["murs"]:
        corps.trait(P(x0, y0), P(x1, sur(Pf, x0, y0, x1)), poids, double=(poids == "fort"))
    corps.trait(P(*c["A"]), P(*c["B"]), "fort", double=True)
    for x1, y1, x2, y2, poids in c["lignes"]:
        corps.trait(P(x1, y1), P(x2, y2), poids)
    for x1, y1, x2, y2, poids in traits_auto:
        corps.trait(P(x1, y1), P(x2, y2), poids, op=0.7)
    hach = []
    for k, (Pf, x1, x2, yt, yb, poids, rem) in enumerate(c["rects"]):
        q = [(x1, yt), (x2, sur(Pf, x1, yt, x2)), (x2, sur(Pf, x1, yb, x2)), (x1, yb)]
        for i in range(4):
            corps.trait(P(*q[i]), P(*q[(i+1) % 4]), poids, depasse=(poids != "fin"))
        if rem:
            hach.append((k, q, rem))
    # hachures (vitres, panneaux, radiateur, écran)
    hs = Crayon(graine + 2)
    for k, q, rem in hach:
        pid = f"h-{nom}-{k}"
        pts = " ".join(f"{P(*p)[0]:.2f},{P(*p)[1]:.2f}" for p in q)
        defs.append(f'<clipPath id="{pid}"><polygon points="{pts}"/></clipPath>')
        xs = [P(*p)[0] for p in q]; ys = [P(*p)[1] for p in q]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        g = []
        hs.out = []
        if rem == "vitre":       # trois traits de reflet, à 45°
            w = x1 - x0; h = y1 - y0
            for f in (0.28, 0.40, 0.70):
                cx, cy = x0 + w*f, y0 + h*f
                hs.trait((cx - h*0.18, cy + h*0.18), (cx + h*0.18, cy - h*0.18), "fin", "#3a3a3a", 0.55, depasse=False)
        elif rem == "panneau":   # hachure légère : matière plus sombre
            pas = 1.6
            t = x0 - (y1 - y0)
            while t < x1:
                hs.trait((t, y1), (t + (y1-y0)*0.55, y0), "fin", "#4a4a4a", 0.35, depasse=False); t += pas
        elif rem == "radiateur":
            t = x0 + 1.2
            while t < x1 - 0.5:
                hs.trait((t, y0 + 1), (t, y1 - 1), "fin", "#3a3a3a", 0.6, depasse=False); t += 1.6
        elif rem == "ecran":     # l'image : le bassin rond et le pavillon, esquissés
            cx, cy = P(650, 330)
            for rx, ry, op in ((34, 13, 0.6), (22, 7.5, 0.5), (38, 16, 0.3)):
                pts_e = []
                ph = hs.r.uniform(0, 6)
                for i in range(73):
                    a = 2*math.pi*i/72
                    jit = 0.25*math.sin(3*a + ph)
                    pts_e.append(f"{cx + (rx+jit)*math.cos(a):.2f},{cy + (ry+jit)*math.sin(a):.2f}")
                hs.out.append(f'<polyline points="{" ".join(pts_e)}" fill="none" stroke="#3a3a3a" stroke-width="0.25" stroke-opacity="{op}" stroke-linecap="round"/>')
            hs.trait(P(426, 225), P(W, 205), "fin", "#3a3a3a", 0.45, depasse=False)             # horizon de l'image
            hs.trait((cx - 14, cy - 8), (cx + 6, cy - 18), "fin", "#3a3a3a", 0.6, depasse=False)  # le pavillon
            hs.trait((cx + 6, cy - 18), (cx + 26, cy - 9), "fin", "#3a3a3a", 0.6, depasse=False)
            t = x0
            while t < x1 + (y1-y0):
                hs.trait((t, y1), (t - (y1-y0)*0.35, y0), "fin", "#5a5a5a", 0.18, depasse=False); t += 2.2
        g = "".join(hs.out)
        corps.out.append(f'<g clip-path="url(#{pid})">{g}</g>')
    # spots du plafond (angle 1)
    for x, y1, y2 in c.get("spots", []):
        a, b = P(x - 4, y1), P(x + 4, y2)
        corps.out.append(f'<rect x="{a[0]:.2f}" y="{a[1]:.2f}" width="{b[0]-a[0]:.2f}" height="{b[1]-a[1]:.2f}" rx="0.6" fill="#2a2a2a" fill-opacity="0.75"/>')
        corps.trait(P(x, y1 - 12), P(x, y1), "fin")
    # rideaux du bureau vitré (angle 2)
    if c.get("rideaux"):
        x1, x2, y1, y2 = c["rideaux"]
        x = x1
        while x <= x2:
            corps.trait(P(x, y1 + corps.r.uniform(-4, 4)), P(x, y2 + corps.r.uniform(-6, 6)), "fin", "#3a3a3a", 0.35, depasse=False)
            x += 11
        for f in (0.15, 0.55):   # reflets sur le vitrage
            corps.trait(P(60 + 260*f, 260), P(60 + 260*f + 60, 200), "fin", "#3a3a3a", 0.35, depasse=False)
    # personnage assis (angle 2), à l'échelle
    for x, y in c.get("personnes", []):
        cx, cy = P(x, y)
        corps.out.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="2.4" fill="none" stroke="#2a2a2a" stroke-width="0.3" stroke-opacity="0.8"/>')
        corps.out.append(f'<path d="M{cx-4.6:.2f},{cy+12:.2f} Q{cx-4:.2f},{cy+3.4:.2f} {cx:.2f},{cy+3:.2f} Q{cx+4:.2f},{cy+3.4:.2f} {cx+4.8:.2f},{cy+12:.2f}" '
                         f'fill="none" stroke="#2a2a2a" stroke-width="0.3" stroke-opacity="0.8" stroke-linecap="round"/>')

    dessin = f'<g clip-path="url(#fen-{nom})"><g clip-path="url(#sol-{nom})">{sol_svg}</g>{"".join(corps.out)}</g>'

    # 2 à 5 · la construction, au crayon bleu
    k = Crayon(graine + 3)
    A, B, xp, Pf, yh = c["A"], c["B"], c["xp"], c["PF"], c["yh"]
    Cy = sur(Pf, *A, xp); Dy = sur(Pf, *B, xp)
    # ligne d'horizon, prolongée dans les marges
    xg, xd = (-OX/MM, (PAGE_W - OX)/MM)
    k.trait(P(xg, yh), P(xd, yh), "construction", CON, 0.8, depasse=False, tirets="3 1.2 0.6 1.2")
    k.texte(OX - 1.5, P(0, yh)[1] - 1.2, "LH", 4.2, CON, "end")
    k.texte(OX + W*MM + 1.5, P(0, yh)[1] - 1.2, "LH", 4.2, CON, "start")
    # fuyantes : de C par A, de D par B, jusqu'au bord de la feuille en direction du point de fuite
    bord = xd if Pf[0] > xp else xg
    for (y0, yq) in ((Cy, A[1]), (Dy, B[1])):
        k.trait(P(xp, y0), P(bord, sur(Pf, xp, y0, bord)), "construction", CON, 0.85, depasse=False)
    # le point de fuite est hors de la feuille : flèche + distance au bord du cadre
    dist = (Pf[0] - W)*MM/10 if Pf[0] > W else (-Pf[0])*MM/10
    xa = P(bord, yh)[0]
    sens = 1 if Pf[0] > xp else -1
    k.trait((xa - sens*7, P(0, yh)[1] + 4.5), (xa - sens*1, P(0, yh)[1] + 4.5), "moyen", CON, 0.95, depasse=False)
    k.trait((xa - sens*1, P(0, yh)[1] + 4.5), (xa - sens*2.6, P(0, yh)[1] + 3.6), "moyen", CON, 0.95, depasse=False)
    k.trait((xa - sens*1, P(0, yh)[1] + 4.5), (xa - sens*2.6, P(0, yh)[1] + 5.4), "moyen", CON, 0.95, depasse=False)
    k.texte(xa - sens*1, P(0, yh)[1] + 9.5, f"PF à {dist:.0f} cm", 3.6, CON, "end" if sens > 0 else "start")
    # A'B' : la verticale plus longue, et les horizontales A→A', B→B'
    k.trait(P(xp, Cy - 18), P(xp, Dy + 18), "moyen", CON, 0.95)
    k.trait(P(*A), P(xp, A[1]), "construction", CON, 0.9, depasse=False, tirets="1.4 1")
    k.trait(P(*B), P(xp, B[1]), "construction", CON, 0.9, depasse=False, tirets="1.4 1")
    for (x, y) in (A, B, (xp, A[1]), (xp, B[1]), (xp, Cy), (xp, Dy)):
        k.point(*P(x, y), CON, 0.75)
    cote = 1 if A[0] > xp else -1          # côté où écrire les lettres de A'B'
    k.texte(P(*A)[0] + 1.6*cote, P(*A)[1] - 1.6, "A", 5.2, CON, "start" if cote > 0 else "end")
    k.texte(P(*B)[0] + 1.6*cote, P(*B)[1] + 4.8, "B", 5.2, CON, "start" if cote > 0 else "end")
    k.texte(P(xp, A[1])[0] - 1.6*cote, P(xp, A[1])[1] + 4.6, "A'", 5.2, CON, "end" if cote > 0 else "start")
    k.texte(P(xp, B[1])[0] - 1.6*cote, P(xp, B[1])[1] - 1.4, "B'", 5.2, CON, "end" if cote > 0 else "start")
    k.texte(P(xp, Cy)[0] - 1.6*cote, P(xp, Cy)[1] - 1.2, "C", 5.2, CON, "end" if cote > 0 else "start")
    k.texte(P(xp, Dy)[0] - 1.6*cote, P(xp, Dy)[1] + 4.6, "D", 5.2, CON, "end" if cote > 0 else "start")
    # cotes relevées au crayon, bras tendu
    xc = P(xp, 0)[0] - 5.5*cote
    for (ya, yb) in ((Cy, A[1]), (B[1], Dy)):
        a, b = P(0, ya)[1], P(0, yb)[1]
        k.trait((xc, a), (xc, b), "construction", CON, 0.9, depasse=False)
        k.trait((xc - 1, a), (xc + 1, a), "construction", CON, 0.9, depasse=False)
        k.trait((xc - 1, b), (xc + 1, b), "construction", CON, 0.9, depasse=False)
        k.texte(xc - 1.4*cote, (a + b)/2 + 1.3, f"{abs(yb-ya)*MM/10:.1f} cm".replace(".", ","), 3.4, CON, "end" if cote > 0 else "start")
    # étiquette de A'B'
    k.texte(P(xp, (A[1]+B[1])/2)[0] + 1.4*cote*-1, P(xp, (A[1]+B[1])/2)[1], c["cote_xp"], 3.2, CON,
            "end" if cote > 0 else "start", rot=-90 if cote > 0 else 90)

    # en-tête et marges
    t = Crayon(graine + 4)
    t.texte(OX, 12, c["titre"], 6.2, "#1f1f1f")
    t.texte(OX, 18.2, "méthode du cadrage à l'acétate · grille de 4 cm", 3.9, "#555")
    etapes = ["1  cadrage à l'acétate, grille de 4 cm",
              "2  l'arête verticale AB (le coin)",
              "3  une verticale plus longue + horizontales → A', B'",
              "4  C et D relevés au crayon, bras tendu",
              "5  fuyantes AC et BD → point de fuite (PF)"]
    for i, e in enumerate(etapes):
        t.texte(PAGE_W - 12, 7.4 + i*3.5, e, 3.0, CON, "end")
    t.texte(OX, PAGE_H - 8, "carrés de 4 cm = carrés de l'acétate · en bleu : la construction · en gris : le croquis", 3.1, "#666", halo=False)
    t.texte(OX, PAGE_H - 4, "LH : ligne d'horizon, à hauteur des yeux · PF : point de fuite, hors de la feuille (distance depuis le bord du cadre)", 3.1, "#666", halo=False)
    corps_svg = "".join(cr.out) + dessin + "".join(k.out) + "".join(t.out)
    return f'<svg viewBox="0 0 {PAGE_W} {PAGE_H}" xmlns="http://www.w3.org/2000/svg"><defs>{"".join(defs)}</defs>{corps_svg}</svg>'


def html(pages, format_):
    taille = "210mm 297mm" if format_ == "A4" else "297mm 420mm"
    l, h = taille.split()
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Croquis en perspective</title>
<link rel="stylesheet" href="polices-local.css">
<style>@page {{ size: {taille}; margin: 0; }} html, body {{ margin: 0; background: #fff; }}
.p {{ width: {l}; height: {h}; page-break-after: always; break-after: page; overflow: hidden; background: #fdfcf8; }}
.p:last-child {{ page-break-after: auto; break-after: auto; }} svg {{ width: 100%; height: 100%; display: block; }}</style></head>
<body>{"".join(f'<div class="p">{p}</div>' for p in pages)}</body></html>"""


if __name__ == "__main__":
    pages = [page(n, c, g) for (n, c), g in zip(ANGLES.items(), (11, 23))]
    open(f"{ICI}/croquis.html", "w", encoding="utf-8").write(html(pages, "A4"))
    open(f"{ICI}/croquis-a3.html", "w", encoding="utf-8").write(html(pages, "A3"))
    print("croquis.html et croquis-a3.html écrits")

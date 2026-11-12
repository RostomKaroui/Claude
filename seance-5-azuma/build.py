"""Azuma House (Tadao Ando) : analyse des proportions de chaque vue à partir du carré a.

Toutes les positions sont en unités de a (a = largeur extérieure de la maison, face extérieure à face extérieure),
relevées sur les photos des deux feuilles (plans redressés, puis mesurés).
Quatre couleurs, une par mesure de la chaîne : a (bleu) -> 1/3 a (rouge) -> 1/4 a (vert) -> e = 1/21 a (violet).
Trame : modules de 1/3 a ; le tiers divisé en 7 (Thalès) donne e, divisé en 5 donne 1/15 a (marches, fentes).
Lancer : python3 build.py  ->  index.html
"""
import html, os

ICI = os.path.dirname(os.path.abspath(__file__))
S = 200                       # px par a dans les dessins
E = 1 / 21                    # épaisseur des murs : 1/21 a = le tiers plié en 7 (≈ 19 cm)
F = 1 / 15                    # la marche et la fente : le tiers plié en 5 (≈ 27 cm)
M0, M1 = 2 - 11 * F / 2, 2 + 11 * F / 2      # l'escalier : 11 marches de 1/15 a, centrées sur le patio
N = 1 / 9                     # le recul des fentes : le tiers du tiers (≈ 44 cm)
G1, G2 = 4 / 3 - N - 3 * F, 8 / 3 + N          # groupes de fentes (2 fentes + 1 trumeau = 1/5 a), à 1/9 a de l'axe des murs du patio
XD = 4 - 4 * E                # la douche et les lanterneaux : 4 e depuis la face extérieure
# les niveaux, en a, depuis le haut de l'acrotère (tout tombe sur des multiples de e = 1/21)
YT, YT2 = 1 / 7, 1 / 7 + 1 / 16     # dalle du toit : haut = 3 e, épaisseur ≈ 1/16 a (25 cm)
YR = 14 / 21                         # haut du garde-corps du pont = 2/3 a
YF, YD = 18 / 21, 20 / 21            # plancher de l'étage : haut = 18 e, dessous = 20 e (2 e d'épaisseur)
YP = 19 / 21                         # dessus de la dalle du pont : e plus bas que le plancher ; son dessous = a
YS = 13 / 8 - 1 / 21                 # dessus de la dalle du sol (épaisseur e)
PX = 5 * E / 2                       # la porte d'entrée : cadre de 5 e de large (0,238 a ; mesuré 0,237 sur la façade B), montants e/2, passage 4 e
SEUIL = 0.035                        # le seuil de la porte (≈ 14 cm = 3/4 e)
WT, WH = 1 - E / 2, 1 / 7            # fenêtres du jardin : haut = a − e/2, hauteur 1/7 a = 3 e (remesuré : 0,972 à 1,110 a)
VERRE = 0.01 / 4                     # le vitrage : 1 cm = 0,0025 a (convention, voir le détail)
TRAIT_MODE = False                   # True : rendu au trait (trait fort sur la coupe, moyen sur ce qu'on voit, fin pour le reste)
FORT, MOYEN, FIN = 2.4, 1.2, 0.55    # épaisseurs des traits (px, soit 0,67 / 0,33 / 0,15 mm sur le carnet)
A_REEL, A_FEUILLE, K_CARNET = 400, 3.7, 1.5       # a en cm : réel, sur la feuille, agrandissement pour le carnet
A_CARNET = A_FEUILLE * K_CARNET                    # 5,55 cm
COL = {"a": "#1f5fd1", "t": "#d9342b", "q": "#14965a", "e": "#8a3cc4", "g": "#6b6e70"}
GRIS, TRAIT = "#3b3d3f", "#6b6e70"
IMPRESSION = False            # True : marges serrées et cotes courtes (planches A4 pour les calques, calques.py)
MARGES_A4 = {(4, 1): (0.42, 0.62, 0.5, 0.55), (4, 13 / 8): (0.75, 0.25, 0.45, 0.62), (1, 13 / 8): (0.6, 0.6, 0.45, 0.6)}
COURT = {"650 = a + 5/8 a": "650", "250 = 5/8 a": "5/8 a", "porte 1/4 a": "1/4 a", "porte 5/8 a": "5/8 a", "40 = 2 e": "2 e",
         "95 ≈ 1/4 a": "≈ 1/4 a", "escalier 1/5 a = 4 e": "1/5 a = 4 e", "1/2 a = 2 × 1/4 a": "1/2 a", "e = 1/20 a": "e",
         "1/5 a = 4 e": "1/5 a", "3/8 a, centrés": "3/8 a", "porte 230": "230", "≈ 1/8 a": "1/8 a", "≈ 2/3 a": "2/3 a",
         "pont 1/3 a": "1/3 a", "sas : 1/3 a × 1/3 a": "1/3 a", "pont = 1/3 a": "1/3 a", "1/3 a − 2e": "1/3 a − 2e",
         "r = 1/6 a": "r = 1/6 a", "1 carré a × a": "a × a", "e = 1/21 a": "e", "95 = 5 e": "5 e", "porte 230 = 12 e": "12 e",
         "escalier 1/4 a − e": "1/4 a − e", "avec le mur : 1/4 a": "1/4 a", "3 × 1/15 a": "3 × 1/15", "cadre 1/4 a": "1/4 a",
         "11 marches de 1/15 a": "11 × 1/15 a", "1/7 a = 3 e": "3 e", "escalier + mur = 1/4 a": "1/4 a"}


class Dessin:
    def __init__(self, w, h, mg=0.55, md=0.55, mh=0.75, mb=0.7):
        if IMPRESSION: mg, md, mh, mb = MARGES_A4[(w, h)]
        self.w, self.h, self.mg, self.mh = w, h, mg, mh
        self.W, self.H = (w + mg + md) * S, (h + mh + mb) * S
        self.fond, self.par, self.dessus, self.cal = [], [], [], []     # par, dessus, cal : (couleur, svg) ; couleur None = gris
        self.murs = []                                                  # les éléments coupés (px), pour le rendu au trait

    def _t(self, t): return COURT.get(t, t) if IMPRESSION else t

    def X(self, x): return (x + self.mg) * S
    def Y(self, y): return (y + self.mh) * S

    # --- le bâtiment (gris) ---
    def mur(self, x0, y0, x1, y1):
        self.murs.append((self.X(x0), self.Y(y0), (x1 - x0) * S, (y1 - y0) * S))
        self.fond.append(f'<rect x="{self.X(x0):.1f}" y="{self.Y(y0):.1f}" width="{(x1-x0)*S:.1f}" height="{(y1-y0)*S:.1f}" fill="{GRIS}"/>')

    def ligne(self, x0, y0, x1, y1, w=1.2, c=TRAIT, dash=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.fond.append(f'<line x1="{self.X(x0):.1f}" y1="{self.Y(y0):.1f}" x2="{self.X(x1):.1f}" y2="{self.Y(y1):.1f}" stroke="{c}" stroke-width="{w}"{d}/>')

    def rect(self, x0, y0, x1, y1, w=1.2, c=TRAIT, fill="none", dash=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.fond.append(f'<rect x="{self.X(x0):.1f}" y="{self.Y(y0):.1f}" width="{(x1-x0)*S:.1f}" height="{(y1-y0)*S:.1f}" fill="{fill}" stroke="{c}" stroke-width="{w}"{d}/>')

    def anneau(self, x0, y0, x1, y1, e=E):
        self.mur(x0, y0, x1, y0 + e); self.mur(x0, y1 - e, x1, y1)
        self.mur(x0, y0, x0 + e, y1); self.mur(x1 - e, y0, x1, y1)

    def vitrage(self, x0, y0, x1, y1):
        """paroi vitrée : deux traits fins"""
        if abs(x1 - x0) < abs(y1 - y0):
            self.ligne(x0 - 0.008, y0, x0 - 0.008, y1, 1); self.ligne(x0 + 0.008, y0, x0 + 0.008, y1, 1)
        else:
            self.ligne(x0, y0 - 0.008, x1, y0 - 0.008, 1); self.ligne(x0, y0 + 0.008, x1, y0 + 0.008, 1)

    def fenetre(self, x0, y0, x1, y1, vitre=True):
        """ouverture dans un mur en plan : on efface le mur, deux traits fins + la vitre au milieu"""
        self.fond.append(f'<rect x="{self.X(x0):.1f}" y="{self.Y(y0):.1f}" width="{(x1-x0)*S:.1f}" height="{(y1-y0)*S:.1f}" fill="#fbfbf8"/>')
        if x1 - x0 > y1 - y0:
            self.ligne(x0, y0, x1, y0, 0.9); self.ligne(x0, y1, x1, y1, 0.9)
            self.ligne(x0, y0, x0, y1, 1.9); self.ligne(x1, y0, x1, y1, 1.9)             # les bouts du mur coupé : trait fort
            if vitre: self.ligne(x0, (y0 + y1) / 2, x1, (y0 + y1) / 2, 0.9)
        else:
            self.ligne(x0, y0, x0, y1, 0.9); self.ligne(x1, y0, x1, y1, 0.9)
            self.ligne(x0, y0, x1, y0, 1.9); self.ligne(x0, y1, x1, y1, 1.9)
            if vitre: self.ligne((x0 + x1) / 2, y0, (x0 + x1) / 2, y1, 0.9)

    def sol(self, y, x0=-0.12, x1=None):
        x1 = self.w + 0.12 if x1 is None else x1
        self.fond.append(f'<rect x="{self.X(x0):.1f}" y="{self.Y(y):.1f}" width="{(x1-x0)*S:.1f}" height="{0.1*S:.1f}" fill="url(#hach)" stroke="{TRAIT}" stroke-width="1"/>')

    def texte(self, x, y, t, c=TRAIT, taille=12, ancre="middle", gras=False):
        g = ' font-weight="700"' if gras else ""
        self.dessus.append((None, f'<text x="{self.X(x):.1f}" y="{self.Y(y):.1f}" fill="{c}" font-size="{taille}" text-anchor="{ancre}"{g}>{html.escape(t)}</text>'))

    # --- les tracés de proportion (couleurs) ---
    def zone(self, x0, y0, x1, y1, k, op=0.10, dash="6 4", w=1.6):
        c = COL[k]
        self.par.append((k, f'<rect x="{self.X(x0):.1f}" y="{self.Y(y0):.1f}" width="{(x1-x0)*S:.1f}" height="{(y1-y0)*S:.1f}" fill="{c}" fill-opacity="{op}" stroke="{c}" stroke-width="{w}" stroke-dasharray="{dash}"/>'))

    def forme(self, x0, y0, x1, y1, k, op=0.35, w=2.2, dash=""):
        """forme complète, seulement sur les calques : aplat de couleur + contour plein"""
        c, d = COL[k], (f' stroke-dasharray="{dash}"' if dash else "")
        self.cal.append((k, f'<rect x="{self.X(x0):.1f}" y="{self.Y(y0):.1f}" width="{(x1-x0)*S:.1f}" height="{(y1-y0)*S:.1f}" fill="{c}" fill-opacity="{op}" stroke="{c}" stroke-width="{w}"{d}/>'))

    def trait_c(self, x0, y0, x1, y1, k, w=2.2, dash=""):
        """trait de couleur, seulement sur les calques"""
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.cal.append((k, f'<line x1="{self.X(x0):.1f}" y1="{self.Y(y0):.1f}" x2="{self.X(x1):.1f}" y2="{self.Y(y1):.1f}" stroke="{COL[k]}" stroke-width="{w}"{d}/>'))

    def axe(self, x0, y0, x1, y1, k, w=1.6, dash="7 4"):
        self.par.append((k, f'<line x1="{self.X(x0):.1f}" y1="{self.Y(y0):.1f}" x2="{self.X(x1):.1f}" y2="{self.Y(y1):.1f}" stroke="{COL[k]}" stroke-width="{w}" stroke-dasharray="{dash}"/>'))

    def cote_h(self, x0, x1, y, t, k, ext=None, cote="c"):
        """cote horizontale à la hauteur y (unités a), lignes de rappel jusqu'à ext"""
        t = self._t(t)
        c, X0, X1, Yy = COL[k], self.X(x0), self.X(x1), self.Y(y)
        o = [f'<line x1="{X0:.1f}" y1="{Yy:.1f}" x2="{X1:.1f}" y2="{Yy:.1f}" stroke="{c}" stroke-width="1.6"/>']
        for X in (X0, X1):
            o.append(f'<line x1="{X-4:.1f}" y1="{Yy+4:.1f}" x2="{X+4:.1f}" y2="{Yy-4:.1f}" stroke="{c}" stroke-width="2"/>')
            if ext is not None:
                o.append(f'<line x1="{X:.1f}" y1="{Yy:.1f}" x2="{X:.1f}" y2="{self.Y(ext):.1f}" stroke="{c}" stroke-width="0.8" stroke-opacity="0.55"/>')
        tx, anc, ty = ((X0 + X1) / 2, "middle", Yy - 5) if cote == "c" else ((X1 + 8, "start", Yy + 4) if cote == "d" else (X0 - 8, "end", Yy + 4))
        o.append(f'<text x="{tx:.1f}" y="{ty:.1f}" fill="{c}" font-size="12.5" font-weight="700" text-anchor="{anc}" paint-order="stroke" stroke="#fbfbf8" stroke-width="3">{html.escape(t)}</text>')
        self.dessus += [(k, x) for x in o]

    def cote_v(self, y0, y1, x, t, k, ext=None, cote="g"):
        t = self._t(t)
        c, Y0, Y1, Xx = COL[k], self.Y(y0), self.Y(y1), self.X(x)
        o = [f'<line x1="{Xx:.1f}" y1="{Y0:.1f}" x2="{Xx:.1f}" y2="{Y1:.1f}" stroke="{c}" stroke-width="1.6"/>']
        for Y in (Y0, Y1):
            o.append(f'<line x1="{Xx-4:.1f}" y1="{Y+4:.1f}" x2="{Xx+4:.1f}" y2="{Y-4:.1f}" stroke="{c}" stroke-width="2"/>')
            if ext is not None:
                o.append(f'<line x1="{Xx:.1f}" y1="{Y:.1f}" x2="{self.X(ext):.1f}" y2="{Y:.1f}" stroke="{c}" stroke-width="0.8" stroke-opacity="0.55"/>')
        ym = (Y0 + Y1) / 2
        dx = -6 if cote == "g" else 6
        anc = "end" if cote == "g" else "start"
        o.append(f'<text x="{Xx+dx:.1f}" y="{ym+4:.1f}" fill="{c}" font-size="12.5" font-weight="700" text-anchor="{anc}" paint-order="stroke" stroke="#fbfbf8" stroke-width="3">{html.escape(t)}</text>')
        self.dessus += [(k, x) for x in o]

    def etiquette(self, x, y, t, k, taille=12.5):
        t = self._t(t)
        self.dessus.append((k, f'<text x="{self.X(x):.1f}" y="{self.Y(y):.1f}" fill="{COL[k]}" font-size="{taille}" font-weight="700" text-anchor="middle" paint-order="stroke" stroke="#fbfbf8" stroke-width="3">{html.escape(t)}</text>'))

    def _svg_trait(self, titre, mm):
        """rendu au trait : le coupé en trait fort (contour des murs réunis), ce qu'on voit en moyen, le reste en fin"""
        import re
        enc = "#151515"
        poids = lambda w: FORT if w >= 1.7 else (MOYEN if w >= 1.1 else FIN)
        p1 = "".join(f'<rect x="{x-FORT:.1f}" y="{y-FORT:.1f}" width="{w+2*FORT:.1f}" height="{h+2*FORT:.1f}" fill="{enc}"/>' for x, y, w, h in self.murs)
        p2 = "".join(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#efefef"/>' for x, y, w, h in self.murs)
        fond = "".join(x for x in self.fond if not x.endswith(f'fill="{GRIS}"/>'))
        fond = re.sub(r'stroke-width="([\d.]+)"', lambda m: f'stroke-width="{poids(float(m.group(1)))}"', fond)
        fond = fond.replace(f'stroke="{TRAIT}"', f'stroke="{enc}"').replace(f'stroke="{GRIS}"', f'stroke="{enc}"')
        textes = "".join(x for k, x in self.dessus if k is None).replace(TRAIT, "#777")
        defs = ('<defs><pattern id="hach" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                f'<line x1="0" y1="0" x2="0" y2="7" stroke="{enc}" stroke-width="{FIN}"/></pattern></defs>')
        taille = f' width="{self.W*mm:.2f}mm" height="{self.H*mm:.2f}mm"' if mm else ""
        fond_page = "" if mm else '<rect width="100%" height="100%" fill="#fbfbf8"/>'
        return (f'<svg viewBox="0 0 {self.W:.0f} {self.H:.0f}"{taille} role="img" aria-label="{html.escape(titre)}" '
                f'font-family="IBM Plex Mono, ui-monospace, monospace">{defs}{fond_page}{p1}{p2}{fond}{textes}</svg>')

    def svg(self, titre, couche=None, mm=None):
        """couche None : la page web (tout) ; "base" : le bâtiment seul ; ensemble de couleurs : un calque
        (le bâtiment en fantôme pâle, puis les formes et les cotes de ces couleurs). mm : mm par px pour l'impression."""
        if TRAIT_MODE and couche is None: return self._svg_trait(titre, mm)
        defs = ('<defs><pattern id="hach" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                f'<line x1="0" y1="0" x2="0" y2="7" stroke="{TRAIT}" stroke-width="1.2"/></pattern></defs>')
        gris = "".join(x for k, x in self.dessus if k is None)
        if couche is None:
            corps = "".join(x for _, x in self.par) + "".join(self.fond) + "".join(x for _, x in self.dessus)
        elif couche == "base":
            corps = "".join(self.fond) + gris
        else:
            garde = lambda l: "".join(x for k, x in l if k in couche)
            corps = (f'<g opacity="0.22">{"".join(self.fond)}</g>' + garde(self.cal) + garde(self.par) + garde(self.dessus))
        taille = f' width="{self.W*mm:.2f}mm" height="{self.H*mm:.2f}mm"' if mm else ""
        fond = "" if mm else '<rect width="100%" height="100%" fill="#fbfbf8"/>'
        return (f'<svg viewBox="0 0 {self.W:.0f} {self.H:.0f}"{taille} role="img" aria-label="{html.escape(titre)}" '
                f'font-family="IBM Plex Mono, ui-monospace, monospace">{defs}{fond}{corps}</svg>')


def murs_e(d, w, h):
    """calque : l'enveloppe des murs, épaisseur e, en violet"""
    for r in ((0, 0, w, E), (0, h - E, w, h), (0, 0, E, h), (w - E, 0, w, h)):
        d.forme(*r, "e", op=0.6, w=0)


def carres_et_tiers(d, y_bleu=-0.14, y_rouge=-0.36, y_tiers_g=-0.18):
    """les 4 carrés a (bleu) et les 3 parts de 4/3 a (rouge), communs aux 3 plans"""
    for i in range(4): d.forme(i, 0, i + 1, 1, "a", op=0.16 if i % 2 else 0.05, w=2.4)
    for i in range(3): d.forme(i * 4 / 3, 0.02, (i + 1) * 4 / 3, 0.98, "t", op=0, w=2.6, dash="10 5")
    for y in (1 / 3, 2 / 3): d.trait_c(0, y, 4, y, "t", w=1.6, dash="4 4")
    murs_e(d, 4, 1)
    for i in range(4):
        d.zone(i, 0, i + 1, 1, "a", op=0.05 if i % 2 else 0.11, dash="2 0", w=0)
        d.cote_h(i, i + 1, y_bleu, "a", "a", ext=0)
    for i in range(3):
        d.cote_h(i * 4 / 3, (i + 1) * 4 / 3, y_rouge, "a + 1/3 a", "t", ext=0)
    for x in (4 / 3, 8 / 3):
        d.axe(x, -0.04, x, 1.04, "t")
    for j in range(3):
        d.cote_v(j / 3, (j + 1) / 3, y_tiers_g, "1/3 a", "t", ext=0)


def fentes(d, cotes=True):
    """les fenêtres des deux longs murs : 2 fentes de 1/15 a + 1 trumeau de 1/15 a = 1/5 a, à 1/9 a de l'axe du mur du patio"""
    for g in (G1, G2):
        for x in (g, g + 2 * F):
            for y0, y1 in ((0, E), (1 - E, 1)):
                d.fenetre(x, y0, x + F, y1)
                d.forme(x, y0, x + F, y1, "t", op=0.75, w=0)
    d.forme(G1 + 3 * F, 1 - E, 4 / 3, 1, "e", op=0.55, w=0); d.forme(8 / 3, 1 - E, G2, 1, "e", op=0.55, w=0)
    if cotes:
        d.cote_h(G1, G1 + 3 * F, 1.12, "3 × 1/15 a", "t", ext=1); d.cote_h(G2, G2 + 3 * F, 1.12, "3 × 1/15 a", "t", ext=1)
        d.cote_h(G1 + 3 * F, 4 / 3, 1.3, "1/9 a", "t", ext=1, cote="d"); d.cote_h(8 / 3, G2, 1.3, "1/9 a", "t", ext=1, cote="g")


def escalier_plan(d, cote=None):
    """l'escalier vu en plan : 11 marches de 1/15 a, de la face intérieure du mur jusqu'à 1/4 a"""
    d.rect(M0, E, M1, 0.25)
    for i in range(1, 11): d.ligne(M0 + i * F, E, M0 + i * F, 0.25, 0.9)
    d.forme(M0, 0, M1, 0.25, "q", op=0.22, w=2)                                           # escalier + mur = 1/4 a
    for i in range(0, 12): d.trait_c(M0 + i * F, E, M0 + i * F, 0.25, "t", w=1.6)         # les marches, 1/15 a
    d.forme(M0, 0, M1, E, "e", op=0.7, w=0)
    if cote:
        d.cote_v(0, 0.25, M1 + 0.1, cote, "q", ext=M1, cote="d")
        d.cote_h(M0, M1, 0.31, "11 marches de 1/15 a", "t", ext=0.25)


def trame(vue=None):
    """le plan posé sur la trame : 12 × 3 modules de 1/3 a"""
    d, nom, _ = (vue or plan_rdc)()
    d.par, d.dessus, d.cal = [], [], []
    for i in range(13):
        k, w = ("a", 2.4) if i % 3 == 0 else (("t", 2.6) if i in (4, 8) else ("t", 0.9))
        op = 0.95 if w > 1 else 0.6
        d.dessus.append((k, f'<line x1="{d.X(i/3):.1f}" y1="{d.Y(-0.03):.1f}" x2="{d.X(i/3):.1f}" y2="{d.Y(1.03):.1f}" stroke="{COL[k]}" stroke-width="{w}" stroke-opacity="{op}"/>'))
    for j in range(4):
        w = 2.4 if j in (0, 3) else 0.9
        d.dessus.append(("t", f'<line x1="{d.X(-0.03):.1f}" y1="{d.Y(j/3):.1f}" x2="{d.X(4.03):.1f}" y2="{d.Y(j/3):.1f}" stroke="{COL["t" if w < 2 else "a"]}" stroke-width="{w}" stroke-opacity="0.75"/>'))
    for i in range(12):
        d.etiquette(i / 3 + 1 / 6, -0.05, str(i + 1), "t", 11)
    for i in range(4): d.cote_h(i, i + 1, -0.17, "a = 3 modules", "a", ext=0)
    for i in range(3): d.cote_h(i * 4 / 3, (i + 1) * 4 / 3, -0.33, "4 modules = a + 1/3 a", "t", ext=0)
    d.cote_v(0, 1 / 3, -0.12, "1/3 a", "t", ext=0)
    d.zone(4 / 3, 1 / 3, 8 / 3, 2 / 3, "t", op=0.16, dash="2 0", w=0); d.zone(11 / 3, 1 / 3, 4, 2 / 3, "t", op=0.16, dash="2 0", w=0)
    d.etiquette(2.0, 0.53, "pont : 4 modules", "t", 11)
    d.H = (1 + d.mh + 0.12) * S                                   # pas de cotes sous la trame : on recadre
    if vue is None: d.etiquette(3.83, 0.53, "sas : 1", "t", 10.5)
    return d, nom + " sur la trame", []


# ================================================================ les vues
def plan_rdc():
    d = Dessin(4, 1, md=1.0)
    d.anneau(0, 0, 4, 1)
    for x in (4 / 3, 8 / 3):                                         # murs du patio : pleins en haut, vitrés en bas
        d.mur(x - E / 2, E, x + E / 2, 0.42); d.vitrage(x, 0.42, x, 1 - E)
    d.mur(0.5 - E / 2, E, 0.5 + E / 2, 0.72)                         # salle de bain
    escalier_plan(d, "1/4 a")
    fentes(d)
    for y0 in (0.5 - 1 / 14 - 1 / 8, 0.5 + 1 / 14):                  # 2 fenêtres côté jardin (façade C)
        d.fenetre(0, y0, E, y0 + 1 / 8); d.forme(0, y0, E, y0 + 1 / 8, "q", op=0.8, w=0)
    d.forme(0, 0.5 - 1 / 14, E, 0.5 + 1 / 14, "e", op=0.4, w=0)
    for y in (1 / 3, 2 / 3): d.ligne(4 / 3 + E / 2, y, 8 / 3 - E / 2, y, 1, dash="5 4")     # passerelle au-dessus
    d.mur(11 / 3 - E / 2, 1 / 3 - E / 2, 11 / 3 + E / 2, 2 / 3 + E / 2)                      # sas d'entrée
    d.mur(11 / 3, 1 / 3 - E / 2, 4 - E, 1 / 3 + E / 2); d.mur(11 / 3, 2 / 3 - E / 2, 4 - E, 2 / 3 + E / 2)
    d.fenetre(4 - E, 0.5 - 2 * E, 4, 0.5 + 2 * E, vitre=False)                           # porte d'entrée : passage 4 e
    d.rect(4, 0.5 - 2 * E, 4 + 1.5 * E, 0.5 + 2 * E, 1.2)                                # encadrement en saillie : 1,5 e (mesuré 0,07 a)
    d.rect(4 - E / 2 - E / 8, 0.5 - 2 * E, 4 - E / 2 + E / 8, 0.5 + 2 * E, 1.2)          # vantail fermé : 4 e de large, e/4 d'épaisseur
    d.ligne(4 - E / 2, 0.5 - 2 * E, 4 - E / 2, 0.5 + 2 * E, 0.8)                         # le vitrage, au milieu du vantail
    hx, hy, r = 4 - E / 2, 0.5 + 2 * E, 4 * E                                            # l'arc d'ouverture (charnière en bas), vantail ouvert à 90°
    d.fond.append(f'<path d="M{d.X(hx):.1f} {d.Y(hy-r):.1f} A {r*S:.1f} {r*S:.1f} 0 0 0 {d.X(hx-r):.1f} {d.Y(hy):.1f}" fill="none" stroke="{TRAIT}" stroke-width="0.8" stroke-dasharray="5 3"/>')
    d.ligne(hx, hy, hx - r, hy, 1.3)
    for x, t in ((0.25, "bain"), (0.92, "cuisine"), (2.0, "patio"), (3.15, "séjour"), (3.83, "sas")):
        d.texte(x, 0.88 if t != "sas" else 0.52, t, taille=11)
    carres_et_tiers(d)
    d.zone(11 / 3, 1 / 3, 4, 2 / 3, "t", op=0.16)
    d.etiquette(3.5, 0.2, "sas : 1/3 a × 1/3 a", "t", 11.5)
    d.cote_h(0, 0.5, 1.2, "1/2 a = 2 × 1/4 a", "q", ext=1)
    d.cote_v(0.5 - 2 * E, 0.5 + 2 * E, 4.1, "4 e", "e", ext=4, cote="d")
    d.cote_v(0.375, 0.625, 4.3, "cadre 1/4 a", "q", ext=4, cote="d")
    d.cote_h(0, E, 1.42, "e = 1/21 a", "e", ext=1, cote="d")
    d.forme(11 / 3, 1 / 3, 4, 2 / 3, "t", op=0.45)                                        # sas 1/3 × 1/3
    d.forme(E, E, 0.5, 0.72, "q", op=0.30)                                                 # salle de bain 1/2 a
    d.trait_c(0.25, E, 0.25, 0.72, "q", w=1.6, dash="4 4")                                 # = 2 quarts
    d.forme(4 - E, 0.375, 4, 0.625, "q", op=0, w=1.8)                                      # cadre de la porte 1/4 a
    d.forme(4 - E, 0.5 - 2 * E, 4, 0.5 + 2 * E, "e", op=0.8, w=0)                         # passage 4 e
    for x in (4 / 3, 8 / 3): d.forme(x - E / 2, E, x + E / 2, 0.42, "e", op=0.6, w=0)     # murs du patio, e
    d.forme(0.5 - E / 2, E, 0.5 + E / 2, 0.72, "e", op=0.6, w=0)
    return d, "Plan du rez-de-chaussée", [
        ("a", "Le grand rectangle fait <b>4 carrés</b> de côté <b>a</b>. On mesure <b>a d'une face extérieure à l'autre</b> (épaisseur des murs de façade comprise), en largeur comme en longueur."),
        ("t", "Plié en trois, il donne <b>3 parts égales de 4/3 a, soit 1 carré + 1/3 de carré</b> : cuisine et salle de bain, patio, séjour. Les plis à 4/3 a et 8/3 a (mesurés depuis la face extérieure) tombent <b>sur l'axe des murs du patio</b>."),
        ("t", "La largeur se plie aussi en trois : les pointillés de la passerelle (au-dessus du patio) sont à <b>1/3 a et 2/3 a</b>. Le sas d'entrée est un petit carré de <b>1/3 a × 1/3 a</b> (aux axes de ses murs)."),
        ("q", "La salle de bain fait <b>1/2 a = 2 × 1/4 a</b> (de la face extérieure à l'axe de sa cloison)."),
        ("q", "La porte d'entrée : un cadre de <b>1/4 a</b> au milieu du mur (de 3/8 a à 5/8 a, vu sur la façade B), et dedans un passage de <b>4 e ≈ 76 cm</b>."),
        ("t", "Les fenêtres des deux longs murs sont des <b>fentes de 1/15 a</b> (le tiers divisé en 5 par Thalès, ≈ 27 cm) : 2 fentes et 1 trumeau de 1/15 a, soit un groupe de <b>1/5 a</b>. Chaque groupe est posé à <b>1/9 a</b> (le tiers du tiers) de l'axe d'un mur du patio, côté cuisine et côté séjour."),
        ("q", "Au bout gauche (côté jardin), deux fenêtres de <b>1/8 a</b>, séparées de <b>1/7 a = 3 e</b> et centrées : ce sont celles de la façade C."),
        ("t", "L'escalier a <b>11 marches de 1/15 a</b> (≈ 27 cm), et la volée est centrée sur le milieu du patio (x = 2 a)."),
        ("q", "Sa largeur : <b>escalier + mur = 1/4 a</b> depuis la face extérieure. L'escalier seul fait donc <b>1/4 a − e ≈ 81 cm</b>."),
        ("e", "Les murs ont une épaisseur <b>e = 1/21 a ≈ 19 cm</b> : c'est le tiers divisé en 7 par Thalès (1/3 × 1/7 = 1/21)."),
    ]


def plan_etage():
    d = Dessin(4, 1, md=1.0)
    d.anneau(0, 0, 4, 1)
    for x in (4 / 3, 8 / 3): d.vitrage(x, E, x, 1 - E)               # façades vitrées sur le patio
    d.rect(4 / 3, 1 / 3, 8 / 3, 2 / 3, 1.2)                           # passerelle
    d.mur(4 / 3, 1 / 3, 8 / 3, 1 / 3 + E); d.mur(4 / 3, 2 / 3 - E, 8 / 3, 2 / 3)
    for x, s in ((4 / 3, -1), (8 / 3, 1)):                            # bouts arrondis
        r = 1 / 6
        d.fond.append(f'<path d="M{d.X(x):.1f} {d.Y(0.5-r):.1f} A {r*S:.1f} {r*S:.1f} 0 0 {1 if s > 0 else 0} {d.X(x):.1f} {d.Y(0.5+r):.1f}" fill="none" stroke="{TRAIT}" stroke-width="1.4"/>')
    escalier_plan(d)
    fentes(d, cotes=False)
    d.mur(XD - E / 2, 0.375 - E / 2, XD + E / 2, 0.625 + E / 2)     # douche
    d.mur(XD, 0.375 - E / 2, 4 - E, 0.375 + E / 2); d.mur(XD, 0.625 - E / 2, 4 - E, 0.625 + E / 2)
    for x, t in ((0.66, "chambre"), (2.0, "pont"), (3.2, "chambre")): d.texte(x, 0.52 if t == "pont" else 0.9, t, taille=11)
    d.texte(2.0, 0.86, "vide", taille=11)
    carres_et_tiers(d)
    d.zone(4 / 3, 1 / 3, 8 / 3, 2 / 3, "t", op=0.14)
    d.etiquette(2.0, 0.44, "pont = 1/3 a", "t", 11.5)
    d.cote_v(1 / 3, 1 / 3 + E, 2.75, "e", "e", cote="d"); d.cote_v(2 / 3 - E, 2 / 3, 2.75, "e", "e", cote="d")
    d.cote_v(1 / 3 + E, 2 / 3 - E, 2.62, "1/3 a − 2e", "e", cote="g")
    for x, s in ((4 / 3, -1),):
        d.axe(x, 0.5, x - 1 / 6, 0.5, "t", w=1.4, dash="3 3"); d.etiquette(x - 0.3, 0.52, "r = 1/6 a", "t", 10.5)
    d.cote_v(0.375, 0.625, 4.2, "1/4 a", "q", ext=4, cote="d")
    d.cote_h(XD, 4, 1.2, "4 e", "e", ext=1, cote="g")
    d.cote_h(0, E, 1.42, "e = 1/21 a", "e", ext=1, cote="d")
    d.forme(4 / 3, 1 / 3, 8 / 3, 2 / 3, "t", op=0.40)                                     # pont 1/3 a
    for x, sw in ((4 / 3, 0), (8 / 3, 1)):
        r = 1 / 6
        d.cal.append(("t", f'<path d="M{d.X(x):.1f} {d.Y(0.5-r):.1f} A {r*S:.1f} {r*S:.1f} 0 0 {sw} {d.X(x):.1f} {d.Y(0.5+r):.1f} Z" fill="{COL["t"]}" fill-opacity="0.25" stroke="{COL["t"]}" stroke-width="2.2"/>'))
    d.forme(4 / 3, 1 / 3, 8 / 3, 1 / 3 + E, "e", op=0.7, w=0); d.forme(4 / 3, 2 / 3 - E, 8 / 3, 2 / 3, "e", op=0.7, w=0)
    d.forme(XD, 0.375, 4, 0.625, "q", op=0.35)                                            # douche 1/4 a
    d.forme(XD, 0.33, 4, 0.67, "e", op=0, w=2.2, dash="5 3")                               # profondeur 4 e
    for i in range(1, 4): d.trait_c(4 - i * E, 0.33, 4 - i * E, 0.67, "e", w=1.2, dash="2 2")
    return d, "Plan de l'étage", [
        ("a", "Même rectangle : <b>4 carrés a</b>, mesurés aux faces extérieures."),
        ("t", "Mêmes trois parts de <b>a + 1/3 a</b> : chambre, vide du patio avec le pont, chambre. Les façades vitrées sur le patio sont sur les plis à 4/3 a et 8/3 a."),
        ("t", "Le pont occupe <b>le tiers du milieu de la largeur</b> (de 1/3 a à 2/3 a, faces extérieures de ses garde-corps). Ses bouts arrondis sont des demi-cercles de rayon <b>1/6 a = moitié de 1/3 a</b>."),
        ("e", "Ses deux garde-corps ont chacun l'épaisseur d'un mur, <b>e</b>. Le passage entre eux fait donc <b>1/3 a − 2e = 5 e</b> (≈ 95 cm). Leur hauteur est aussi <b>5 e = 95 cm</b> (voir les coupes)."),
        ("q", "La douche (à droite) fait <b>1/4 a</b> de large, au milieu (axes de ses murs à 3/8 a et 5/8 a)."),
        ("e", "Elle fait <b>4 e ≈ 76 cm</b> de profondeur (de la face extérieure à l'axe de son mur)."),
        ("t", "Les mêmes fentes de <b>1/15 a</b> percent les longs murs des chambres, et le haut de l'escalier (11 marches de 1/15 a) arrive dans le vide du patio."),
    ]


def plan_toit():
    d = Dessin(4, 1, md=1.0)
    d.rect(0, 0, 4, 1, 1.4); d.rect(E, E, 4 - E, 1 - E, 1.2)          # acrotère : deux traits
    for x in (4 / 3, 8 / 3):
        d.ligne(x - E / 2, E, x - E / 2, 1 - E, 1.2); d.ligne(x + E / 2, E, x + E / 2, 1 - E, 1.2)
    d.rect(4 / 3 + E / 2, 1 / 3, 8 / 3 - E / 2, 2 / 3, 1.1); d.ligne(4 / 3 + E / 2, 1 / 3 + E, 8 / 3 - E / 2, 1 / 3 + E, 1); d.ligne(4 / 3 + E / 2, 2 / 3 - E, 8 / 3 - E / 2, 2 / 3 - E, 1)
    d.rect(M0, E, M1, 0.25, 1); [d.ligne(M0 + i * F, E, M0 + i * F, 0.25, 0.9) for i in range(1, 11)]
    for y0, y1 in ((E, 1 / 3), (0.375, 0.625), (2 / 3, 1 - E)):     # lanterneaux à droite
        d.rect(XD, y0 + 0.01, 4 - E, y1 - 0.01, 1.2)
    d.ligne(XD, 0.385, 4 - E, 0.615, 1); d.ligne(XD, 0.615, 4 - E, 0.385, 1)
    d.rect(E, 0.37, 0.21, 0.63, 1.2); d.rect(E, 0.42, 0.17, 0.58, 1)  # lanterneau gauche
    d.texte(0.66, 0.9, "toiture", taille=11); d.texte(2.0, 0.52, "pont (vu d'en haut)", taille=11); d.texte(3.2, 0.9, "toiture", taille=11)
    carres_et_tiers(d)
    d.zone(XD, E, 4 - E, 1 / 3, "t", op=0.12); d.zone(XD, 2 / 3, 4 - E, 1 - E, "t", op=0.12)
    d.zone(XD, 0.375, 4 - E, 0.625, "q", op=0.16)
    d.cote_v(0.375, 0.625, 4.2, "1/4 a", "q", ext=4, cote="d")
    d.cote_h(0, E, 1.2, "e = 1/21 a", "e", ext=1, cote="d")
    d.cote_h(XD, 4, 1.2, "4 e", "e", ext=1, cote="g")
    d.forme(XD, E, 4 - E, 1 / 3, "t", op=0.35); d.forme(XD, 2 / 3, 4 - E, 1 - E, "t", op=0.35)
    d.forme(XD, 0.375, 4 - E, 0.625, "q", op=0.40)
    d.forme(XD, 0, 4, 1, "e", op=0, w=2.2, dash="5 3")
    for i in range(0, 12): d.trait_c(M0 + i * F, E, M0 + i * F, 0.25, "t", w=1.4)
    return d, "Plan de toiture", [
        ("a", "Toujours <b>4 carrés a</b>. Le double trait du bord est l'acrotère (le muret du toit) : son épaisseur est <b>e</b>."),
        ("t", "Les trois parts de <b>a + 1/3 a</b> : toiture, patio ouvert (on voit le pont et l'escalier d'en haut), toiture."),
        ("t", "La colonne de lanterneaux à droite reprend <b>les tiers de la largeur</b> : deux cases de 1/3 a (rouge) de part et d'autre."),
        ("q", "La case du milieu, au-dessus de la douche, fait <b>1/4 a</b> (de 3/8 a à 5/8 a)."),
        ("e", "La colonne fait <b>4 e</b> de profondeur, comme la douche en dessous."),
        ("t", "Par le patio ouvert on voit l'escalier : <b>11 marches de 1/15 a</b>, centrées sur le patio."),
    ]


def coupe_longue():
    H = 13 / 8
    d = Dessin(4, H, mg=0.8, md=0.6, mh=0.7, mb=0.75)
    d.mur(0, 0, E, H); d.mur(4 - E, 0, 4, H)                          # murs d'extrémité
    d.mur(0, YT, 4 / 3 + E / 2, YT2); d.mur(8 / 3 - E / 2, YT, 4, YT2)   # toitures
    d.mur(4 / 3 - E / 2, 0.10, 4 / 3 + E / 2, YT2); d.mur(8 / 3 - E / 2, 0.10, 8 / 3 + E / 2, YT2)
    d.mur(0, YF, 4 / 3, YD); d.mur(4 / 3, YP, 8 / 3, 1.0); d.mur(8 / 3, YF, 4, YD)    # plancher de l'étage ; la dalle du pont est e plus bas
    for x in (4 / 3, 8 / 3): d.vitrage(x, YT2, x, YP); d.vitrage(x, 1.0, x, YS)
    d.mur(0.5 - E / 2, YD, 0.5 + E / 2, YS)                          # cloison salle de bain
    d.mur(11 / 3 - E / 2, YD, 11 / 3 + E / 2, YS)                    # cloison du sas
    d.mur(XD - E / 2, YT2, XD + E / 2, YF)                           # mur de la douche
    d.rect(1.36, YR, 2.36, YP, 1.2)                                   # garde-corps du pont : de 2/3 a à 19/21 a = 5 e
    x, y = M0, YS; pts = [(x, y)]                                     # escalier : 11 marches de 1/15 a, 12 hauteurs
    h = 0.70 / 12                                                     # 12 hauteurs égales : 280 cm = 7/10 a à monter (cote écrite)
    for i in range(12):
        y -= h; pts.append((x, y))
        if i < 11: x += F; pts.append((x, y))
    d.fond.append('<polyline points="' + " ".join(f"{d.X(p):.1f},{d.Y(q):.1f}" for p, q in pts) + f'" fill="none" stroke="{TRAIT}" stroke-width="1.3"/>')
    d.mur(0, YS, 4, H); d.sol(H)
    for x, t in ((0.66, "chambre"), (3.2, "chambre"), (0.25, "bain"), (0.92, "cuisine"), (2.0, "patio"), (3.15, "séjour")):
        d.texte(x, 0.55 if t == "chambre" else (1.38 if t != "patio" else 0.4), t, taille=11)
    for i in range(4): d.cote_h(i, i + 1, -0.14, "a", "a", ext=0)
    for i in range(3): d.cote_h(i * 4 / 3, (i + 1) * 4 / 3, -0.36, "a + 1/3 a", "t", ext=0)
    for x in (4 / 3, 8 / 3): d.axe(x, -0.04, x, H + 0.04, "t")
    d.zone(0, 0, 4 / 3, 1, "a", op=0.07, dash="8 4")
    d.cote_v(0, 1, -0.16, "a", "a", ext=0); d.cote_v(1, H, -0.16, "5/8 a", "q", ext=0)
    d.cote_v(0, YT, -0.38, "1/7 a", "e", ext=0)
    d.cote_v(YR, YP, 2.5, "95 = 5 e", "e", cote="d")
    d.cote_h(0, 0.5, H + 0.25, "1/2 a", "q", ext=H)
    d.cote_h(11 / 3, 4, H + 0.25, "1/3 a", "t", ext=H)
    d.cote_h(XD, 4, H + 0.47, "4 e", "e", ext=H, cote="g")
    d.cote_h(M0, M1, H + 0.25, "11 marches de 1/15 a", "t", ext=YS)
    d.cote_h(0, E, H + 0.47, "e", "e", ext=H, cote="d")
    d.forme(0, 0, 4 / 3, 1, "a", op=0.16, w=2.4)                                          # le carré a
    for i in range(3): d.forme(i * 4 / 3, 0.02, (i + 1) * 4 / 3, H - 0.02, "t", op=0, w=2.6, dash="10 5")
    d.trait_c(0, YR, 4, YR, "t", w=1.4, dash="4 4")                                        # la ligne des 2/3 : haut du garde-corps
    d.forme(11 / 3, YD, 4 - E, YS, "t", op=0.40)                                          # sas 1/3 a
    d.forme(0, 1, 4, H, "q", op=0.10, w=2.2)                                              # 5/8 a
    d.forme(0, 0, 4, YT, "e", op=0.30, w=0)                                               # acrotère 1/7 a = 3 e
    d.forme(E, YD, 0.5, YS, "q", op=0.30)                                                 # salle de bain 1/2 a
    d.forme(1.36, YR, 2.36, YP, "e", op=0.25)                                             # garde-corps 5 e
    d.forme(0, 0, E, H, "e", op=0.65, w=0); d.forme(4 - E, 0, 4, H, "e", op=0.65, w=0)
    d.forme(XD, YT2, 4, YF, "e", op=0, w=2.2, dash="5 3")                                  # douche 4 e
    for i in range(12): d.trait_c(M0 + i * F, YS - i * h - h, M0 + i * F, YS, "t", w=1.2, dash="3 2")
    return d, "Coupe longitudinale", [
        ("t", "En long, on retrouve <b>les trois parts de a + 1/3 a</b> : le patio du milieu n'a pas de toit, seul le pont le traverse."),
        ("a", "En hauteur, la coupe fait <b>a + 5/8 a = 650 cm</b> (du haut des murs jusqu'au sol). Le carré a (bleu) va du haut du mur jusqu'au <b>dessous de la dalle du pont</b>."),
        ("q", "Le rez-de-chaussée fait <b>5/8 a = 250 cm</b> sous plafond, et la salle de bain <b>1/2 a</b> de large."),
        ("e", "L'acrotère (le muret du toit) fait <b>1/7 a = 3 e ≈ 57 cm</b>."),
        ("e", "Le garde-corps du pont fait <b>95 cm = 5 e</b> de haut. Son sommet tombe sur la ligne <b>2/3 a</b> (14 e) ; la dalle du pont est <b>e plus bas</b> que le plancher de l'étage."),
        ("t", "L'escalier : <b>11 marches de 1/15 a</b> et 12 hauteurs égales (≈ 23 cm). Il monte de <b>280 cm = 7/10 a</b> (la cote écrite)."),
        ("e", "Les murs font <b>e</b> ; le plancher de l'étage <b>2 e</b> (≈ 38 cm) ; la dalle du sol <b>e</b> ; la dalle du toit ≈ <b>1/16 a</b> (25 cm)."),
    ]


def coupe_c():
    H = 13 / 8
    d = Dessin(1, H, mg=1.2, md=1.0, mh=0.45, mb=0.55)
    d.mur(0, 0, E, H); d.mur(1 - E, 0, 1, H)
    d.mur(0, YT, 1, YT2); d.mur(0, YF, 1, YD); d.mur(0, YS, 1, H); d.sol(H)
    d.rect(0.37, 0.02, 0.62, YT, 1.1)                                  # lanterneau en toiture
    d.texte(0.5, 0.6, "chambre", taille=11); d.texte(0.5, 1.3, "cuisine", taille=11)
    d.cote_h(0, 1, -0.16, "a", "a", ext=0)
    d.zone(0, 0, 1, 1, "a", op=0.08, dash="8 4")
    d.cote_v(0, 1, -0.18, "a", "a", ext=0); d.cote_v(1, H, -0.18, "5/8 a", "q", ext=0)
    d.cote_v(YD, YS, 1.18, "250 = 5/8 a", "q", ext=1, cote="d")
    d.cote_v(YT2, YF, 1.18, "≈ 2/3 a", "t", ext=1, cote="d")
    d.cote_v(0, YT, 1.18, "1/7 a", "e", ext=1, cote="d")
    d.cote_h(0, E, H + 0.3, "e = 1/21 a", "e", ext=H, cote="d")
    d.cote_v(0, H, -0.42, "650 = a + 5/8 a", "a", ext=0)
    d.forme(0, 0, 1, 1, "a", op=0.16, w=2.4)
    d.forme(0, YT2, 1, YF, "t", op=0, w=2.4, dash="10 5")                                   # chambre ≈ 2/3 a
    d.forme(0, 1, 1, H, "q", op=0.15, w=2.2)                                              # 5/8 a
    d.forme(0, 0, 1, YT, "e", op=0.30, w=0)                                               # acrotère 1/7 a
    d.forme(0, 0, E, H, "e", op=0.65, w=0); d.forme(1 - E, 0, 1, H, "e", op=0.65, w=0)
    return d, "Coupe C", [
        ("a", "La coupe est large de <b>a</b> et haute de <b>a + 5/8 a</b>. Avec la cote de 650 cm, on trouve <b>a = 400 cm</b>."),
        ("q", "Le rez-de-chaussée fait <b>250 cm = 5/8 a</b> sous plafond. C'est la deuxième cote qui donne a = 400 cm."),
        ("t", "La chambre de l'étage fait environ <b>2/3 a</b> sous plafond (≈ 260 cm ; la cote écrite sur la coupe longitudinale dit 250)."),
        ("e", "L'acrotère, au-dessus de la toiture, fait <b>1/7 a = 3 e</b> (≈ 57 cm)."),
        ("e", "Les murs font <b>e = 1/21 a ≈ 19 cm</b> (400 / 21 = 19,05). Le plancher de l'étage fait <b>2 e</b>, la dalle du sol <b>e</b>."),
    ]


def facade_b():
    H = 13 / 8
    d = Dessin(1, H, mg=1.0, md=1.0, mh=0.45, mb=0.55)
    d.rect(0, 0, 1, H, 1.8, c=GRIS); d.sol(H)
    PB = H - SEUIL                                                                        # le haut du seuil
    d.rect(0.5 - PX, 1.0, 0.5 + PX, PB, 1.5, c=GRIS)                                      # cadre dormant : 5 e de large, tête sur la ligne a
    d.rect(0.5 - 2 * E, 1.0 + E / 2, 0.5 + 2 * E, PB, 1.2, c=GRIS)                        # vantail : 4 e de large (montants e/2, traverse haute e/2)
    d.rect(0.5 - 2 * E + E / 3, 1.0 + E / 2 + E / 3, 0.5 + 2 * E - E / 3, PB - E / 3, 0.8, c=GRIS)   # le vitrage, dans le cadre du vantail (e/3)
    d.ligne(0.5 - PX, PB, 0.5 + PX, PB, 1.2)                                              # le seuil
    d.rect(0.5 + 1.6 * E, 1.0 + 0.30, 0.5 + 1.6 * E + 0.008, 1.0 + 0.36, 1.0, c=GRIS)    # la poignée
    d.cote_h(0, 1, -0.16, "a", "a", ext=0)
    d.zone(0, 0, 1, 1, "a", op=0.10, dash="8 4")
    d.etiquette(0.5, 0.52, "1 carré a × a", "a", 13)
    d.cote_v(0, 1, -0.18, "a", "a", ext=0); d.cote_v(1, H, -0.18, "5/8 a", "q", ext=0)
    d.cote_h(0.5 - PX, 0.5 + PX, H + 0.3, "cadre 5 e", "e", ext=H)
    d.cote_v(1.0, H, 1.18, "porte 5/8 a", "q", ext=0.625, cote="d")
    d.forme(0, 0, 1, 1, "a", op=0.16, w=2.4)
    d.forme(0.5 - PX, 1.0, 0.5 + PX, PB, "e", op=0.30)                                    # cadre 5 e × 5/8 a
    d.forme(0.5 - 2 * E, 1.0 + E / 2, 0.5 + 2 * E, PB, "e", op=0, w=1.6)                  # vantail 4 e
    return d, "Façade B, sur la rue", [
        ("a", "La façade sur la rue est un rectangle de <b>a</b> par <b>a + 5/8 a</b>. Au-dessus de la porte, le mur est <b>exactement un carré a × a</b>."),
        ("e", "La seule ouverture, la porte, a un cadre de <b>5 e = 95 cm</b> de large (mesuré 0,380 à 0,617 a : 0,5 a ± 2,5 e), au milieu. C'est presque 1/4 a (100 cm). Son haut tombe pile au bas du carré a, donc elle fait <b>5/8 a</b> de haut."),
        ("e", "Les montants du cadre font <b>e/2</b> : il reste un passage de <b>4 e ≈ 76 cm</b> (le même que sur le plan) et un vantail de <b>4 e × 12 e</b> (76 × 229 cm). Le seuil fait environ 14 cm."),
    ]


def coupe_e():
    H = 13 / 8
    d = Dessin(1, H, mg=1.0, md=1.0, mh=0.45, mb=0.55)
    d.mur(0, 0, E, H); d.mur(1 - E, 0, 1, H)
    d.ligne(E, YT2 - 2 * E, 1 - E, YT2 - 2 * E, 1.2); d.ligne(E, YT2, 1 - E, YT2, 1.1, dash="6 4")      # rives des toitures, au fond
    d.mur(1 / 3, YR, 1 / 3 + E, YP); d.mur(2 / 3 - E, YR, 2 / 3, YP)                       # garde-corps du pont : 5 e de haut
    d.mur(1 / 3, YP, 2 / 3, 1.0)                                                             # dalle du pont : le dessous = bas du carré a
    d.rect(0.5 - 2 * E, YS - 12 * E, 0.5 + 2 * E, YS, 1.3)                  # porte sous le pont : 4 e de large, 12 e de haut
    d.rect(0.5 - 2 * E + E / 3, YS - 12 * E + E / 3, 0.5 + 2 * E - E / 3, YS - E / 3, 0.8)       # le vitrage dans le vantail
    for x0 in (0.4, 0.4 + 2 * F): d.rect(x0, 0.26, x0 + F, YR, 1.1)      # fenêtres hautes : 2 fentes de 1/15 a, centrées
    d.rect(E, YS - 0.70, 0.25, YS, 1.2)                                 # escalier : 12 hauteurs, 280 cm à monter
    for i in range(1, 12): d.ligne(E, YS - 0.70 + i * 0.70 / 12, 0.25, YS - 0.70 + i * 0.70 / 12, 0.9)
    d.mur(0, YS, 1, H); d.sol(H)
    d.cote_h(0, 1, -0.16, "a", "a", ext=0)
    d.cote_h(1 / 3, 2 / 3, -0.34, "pont 1/3 a", "t", ext=0)
    d.cote_v(YR, YP, 1.18, "95 = 5 e", "e", ext=2 / 3, cote="d")
    d.cote_v(YT2 - 2 * E, YT2, 1.18, "40 = 2 e", "e", ext=1, cote="d")
    d.cote_h(E, 0.25, H + 0.28, "escalier 1/4 a − e", "e", ext=H, cote="d")
    d.cote_h(0, 0.25, H + 0.48, "avec le mur : 1/4 a", "q", ext=H, cote="d")
    d.cote_h(1 / 3, 1 / 3 + E, 0.52, "e", "e", cote="g"); d.cote_h(2 / 3 - E, 2 / 3, 0.52, "e", "e", cote="d")
    d.cote_v(YS - 12 * E, YS, -0.18, "porte 230 = 12 e", "e", ext=0.4)
    d.cote_h(0.4, 0.6, 0.2, "1/5 a", "t", ext=0.26)
    d.forme(1 / 3, YR, 2 / 3, 1.06, "t", op=0.30)                                         # pont 1/3 a
    for x in (1 / 3, 2 / 3): d.trait_c(x, 0, x, H, "t", w=1.4, dash="4 4")
    d.trait_c(0, YR, 1, YR, "t", w=1.4, dash="4 4")                                         # la ligne des 2/3
    d.forme(1 / 3, YR, 2 / 3, YP, "e", op=0, w=2.2, dash="6 3")                            # garde-corps 5 e
    d.forme(1 / 3, YR, 1 / 3 + E, YP, "e", op=0.7, w=0); d.forme(2 / 3 - E, YR, 2 / 3, YP, "e", op=0.7, w=0)
    d.forme(E, YS - 0.70, 0.25, YS, "e", op=0.25)                                          # escalier 1/4 a − e
    d.forme(0, YS - 0.70, 0.25, YS, "q", op=0, w=2.2, dash="6 3")                          # + le mur = 1/4 a
    d.forme(0.5 - 2 * E, YS - 12 * E, 0.5 + 2 * E, YS, "e", op=0.15, w=0)                  # porte : 12 e de haut, 4 e de large
    for x0 in (0.4, 0.4 + 2 * F): d.forme(x0, 0.26, x0 + F, YR, "t", op=0.5)
    d.forme(E, YT2 - 2 * E, 1 - E, YT2, "e", op=0.25, w=0)                                 # 40 = 2 e
    d.forme(0, 0, E, H, "e", op=0.65, w=0); d.forme(1 - E, 0, 1, H, "e", op=0.65, w=0)
    return d, "Coupe E, à travers le patio", [
        ("t", "Coupé à travers le patio, le pont fait <b>1/3 a</b> de large, pile au milieu (de 1/3 a à 2/3 a), comme sur le plan de l'étage."),
        ("e", "Ses garde-corps ont l'épaisseur <b>e</b> d'un mur."),
        ("e", "Leur hauteur est de <b>95 cm = 5 e</b> (5 × 19,05 = 95,2). Le sommet tombe sur la ligne <b>2/3 a</b> et la dalle du pont a son dessous <b>au bas du carré a</b>."),
        ("q", "L'escalier, contre le mur : <b>escalier + mur = 1/4 a</b>. Sans le mur, l'escalier fait <b>1/4 a − e ≈ 81 cm</b>."),
        ("t", "Les deux fenêtres hautes sont des fentes de <b>1/15 a</b>, séparées de 1/15 a : un groupe de <b>1/5 a</b>, centré sur le patio."),
        ("e", "La cote de 40 cm en haut vaut <b>2 e</b> (38 cm)."),
        ("e", "La porte sous le pont fait <b>4 e de large</b> (76 cm) et <b>12 e de haut</b> (12 × 19,05 = 228,6 ≈ la cote de 230), soit <b>4/7 a</b>. Son haut touche presque le dessous du pont (a)."),
    ]


def facade_c():
    H = 13 / 8
    d = Dessin(1, H, mg=1.0, md=1.0, mh=0.45, mb=0.55)
    d.rect(0, 0, 1, H, 1.8, c=GRIS); d.sol(H)
    W1, W2 = 0.5 - 1 / 14 - 1 / 8, 0.5 + 1 / 14                      # 2 fenêtres de 1/8 a, écart 1/7 a = 3 e, centrées
    for x0 in (W1, W2):
        d.rect(x0, WT, x0 + 0.125, WT + WH, 1.4, c=GRIS)                                      # cadre de la fenêtre
        d.rect(x0 + E / 3, WT + E / 3, x0 + 0.125 - E / 3, WT + WH - E / 3, 0.8, c=GRIS)       # le vitrage (cadre e/3)
    d.cote_h(0, 1, -0.16, "a", "a", ext=0)
    d.zone(0, 0, 1, 1, "a", op=0.10, dash="8 4")
    d.etiquette(0.5, 0.52, "1 carré a × a", "a", 13)
    d.cote_v(0, 1, -0.18, "a", "a", ext=0); d.cote_v(1, H, -0.18, "5/8 a", "q", ext=0)
    d.cote_h(W1, W1 + 0.125, H + 0.25, "1/8", "q", ext=WT + WH, cote="g"); d.cote_h(W2, W2 + 0.125, H + 0.25, "1/8", "q", ext=WT + WH, cote="d")
    d.cote_h(W1 + 0.125, W2, H + 0.45, "1/7 a = 3 e", "e", ext=WT + WH, cote="d")
    d.cote_v(WT, WT + WH, 1.18, "1/7 a = 3 e", "e", ext=W2 + 0.125, cote="d")
    d.forme(0, 0, 1, 1, "a", op=0.16, w=2.4)
    for x0 in (W1, W2): d.forme(x0, WT, x0 + 0.125, WT + WH, "q", op=0.45)
    d.forme(W1 + 0.125, WT, W2, WT + WH, "e", op=0.3, w=0)
    for i in range(1, 3): d.trait_c(W1 + 0.125 + i * E, WT, W1 + 0.125 + i * E, WT + WH, "e", w=1.2, dash="2 2")
    return d, "Façade C, sur le jardin", [
        ("a", "Même rectangle que la façade B : <b>a</b> par <b>a + 5/8 a</b>, avec <b>un carré a × a</b> au-dessus des ouvertures."),
        ("q", "Les deux petites fenêtres font <b>1/8 a</b> de large (50 cm) et <b>1/7 a = 3 e</b> de haut (57 cm). Leur haut est <b>e/2 au-dessus</b> de la ligne a (remesuré : de 0,972 à 1,110 a). Le cadre fait e/3, le vitrage est dedans."),
        ("e", "Elles sont séparées de <b>1/7 a = 3 e</b> (≈ 57 cm) et centrées. L'écart mesuré (0,15 a) est plus proche de 1/7 (0,143) que de 1/8 (0,125)."),
    ]


VUES = [
    ("Plan du rez-de-chaussée", "feuille 1 · 3e dessin", plan_rdc),
    ("Plan de l'étage", "feuille 1 · 2e dessin", plan_etage),
    ("Plan de toiture", "feuille 1 · 1er dessin", plan_toit),
    ("Coupe longitudinale", "feuille 1 · 4e dessin", coupe_longue),
    ("Coupe C", "feuille 2 · « Sezione C »", coupe_c),
    ("Façade B (rue)", "feuille 2 · « Prospetto B »", facade_b),
    ("Coupe E (patio)", "feuille 2 · « Sezione E »", coupe_e),
    ("Façade C (jardin)", "feuille 2 · « Prospetto C »", facade_c),
]

NOMS = {"a": "a · le carré", "t": "1/3 a · le tiers (et 1/9, 1/15 a)", "q": "1/4 a · le quart (et 1/8 a)", "e": "e = 1/21 a · le mur (1/7 du tiers)"}


# ================================================================ trame, pliages, hypothèses (schémas de la page)
FONTE = 'font-family="IBM Plex Mono, ui-monospace, monospace"'


def _svg(w, h, corps, titre):
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(titre)}" {FONTE}>'
            f'<rect width="100%" height="100%" fill="#fbfbf8"/>{corps}</svg>')


def _t(x, y, t, c="#1c2120", taille=13, ancre="middle", gras=True):
    g = ' font-weight="700"' if gras else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{taille}" text-anchor="{ancre}"{g}>{html.escape(t)}</text>'


def _l(x0, y0, x1, y1, c, w=1.2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'


def _r(x, y, w, h, c="none", op=1, trait="#1c2120", tw=1.4, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{c}" fill-opacity="{op}" stroke="{trait}" stroke-width="{tw}"{d}/>'


def _accolade(x0, x1, y, t, c):
    return (_l(x0, y, x1, y, c, 1.4) + _l(x0, y - 5, x0, y + 5, c, 1.4) + _l(x1, y - 5, x1, y + 5, c, 1.4)
            + _t((x0 + x1) / 2, y + 17, t, c, 12.5))


def regles_svg():
    """les 3 règles de la trame : a en 21 e, a en 15 quinzièmes, a en quarts et huitièmes"""
    x0, L, o = 120, 630, []
    A, T, Q, Ev = COL["a"], COL["t"], COL["q"], COL["e"]
    # 1. a = 3 tiers = 21 e
    y = 46
    o.append(_t(x0 - 14, y + 16, "a = 21 e", Ev, 13, "end"))
    o.append(_r(x0, y, 30, 22, Ev, 0.75, Ev, 0))
    o.append(_r(x0 + 210, y, 30, 22, Ev, 0.3, Ev, 0)); o.append(_r(x0 + 420, y, 30, 22, Ev, 0.3, Ev, 0))
    o.append(_r(x0, y, L, 22, "none", 1, A, 2.4))
    for i in range(1, 21): o.append(_l(x0 + 30 * i, y, x0 + 30 * i, y + 22, Ev, 1))
    for i in (1, 2): o.append(_l(x0 + 210 * i, y - 10, x0 + 210 * i, y + 32, T, 3))
    for i in range(3): o.append(_t(x0 + 105 + 210 * i, y - 8, "1/3 a = 7 e", T, 12.5))
    o.append(_t(x0 + 15, y + 16, "e", "#fff", 12))
    o.append(_accolade(x0, x0 + 90, y + 34, "1/7 a = 3 e", Ev))
    o.append(_accolade(x0 + 210, x0 + 330, y + 34, "4 e", Ev))
    o.append(_accolade(x0 + 420, x0 + 570, y + 34, "5 e = 95 cm", Ev))
    # 2. a = 15 × 1/15 a
    y = 160
    o.append(_t(x0 - 14, y + 16, "a = 15 × 1/15", T, 13, "end"))
    for i in range(15):
        if i % 2 == 0: o.append(_r(x0 + 42 * i, y, 42, 22, T, 0.16, T, 0))
    o.append(_r(x0, y, L, 22, "none", 1, A, 2.4))
    for i in range(1, 15): o.append(_l(x0 + 42 * i, y, x0 + 42 * i, y + 22, T, 1, "4 2"))
    for i in (1, 2): o.append(_l(x0 + 210 * i, y - 10, x0 + 210 * i, y + 32, T, 3))
    for i in range(3): o.append(_t(x0 + 105 + 210 * i, y - 8, "1/3 a = 5 × 1/15", T, 12.5))
    o.append(_accolade(x0, x0 + 42, y + 34, "1/15", T))
    o.append(_accolade(x0 + 210, x0 + 336, y + 34, "1/5 a = 3 × 1/15", T))
    # 3. a en 2, 4, 8
    y = 274
    o.append(_t(x0 - 14, y + 16, "a = 8 × 1/8", Q, 13, "end"))
    o.append(_r(x0, y, L, 22, "none", 1, A, 2.4))
    for i in range(1, 8):
        w = 3 if i == 4 else (2 if i % 2 == 0 else 1)
        o.append(_l(x0 + L * i / 8, y - (10 if i == 4 else 4), x0 + L * i / 8, y + 22 + (10 if i == 4 else 4), Q, w, "" if i % 2 == 0 else "4 2"))
    for i, t in enumerate(("1/8", "1/4", "3/8", "1/2", "5/8", "3/4", "7/8"), 1):
        o.append(_t(x0 + L * i / 8, y - (14 if i == 4 else 9), t, Q, 12.5 if i % 2 == 0 else 11, gras=i % 2 == 0))
    o.append(_accolade(x0, x0 + L / 4, y + 34, "1/4 a", Q))
    o.append(_accolade(x0 + L / 2, x0 + L * 5 / 8, y + 34, "1/8 a", Q))
    return _svg(780, 340, "".join(o), "Les trois règles de la trame")


# ================================================================ les plis, étape par étape, dessinés sur le plan
TRAIT_PLI = "16 5 3 5"          # trait mixte : la ligne de pli

# les plis de chaque étape (x0, y0, x1, y1, couleur, étiquette, position de l'étiquette)
PLIS_PLAN = {
    1: [(2, -0.1, 2, 1.1, "a", "pli 1", (2, -0.08))],
    2: [(1, -0.1, 1, 1.1, "a", "pli 2", (1, -0.08)), (3, -0.1, 3, 1.1, "a", "pli 2", (3, -0.08))],
    3: [(4 / 3, -0.1, 4 / 3, 1.1, "t", "pli 3", (4 / 3, -0.08)), (8 / 3, -0.1, 8 / 3, 1.1, "t", "pli 3", (8 / 3, -0.08))],
    4: [(-0.06, 1 / 3, 4.06, 1 / 3, "t", "pli 4", (-0.2, 1 / 3)), (-0.06, 2 / 3, 4.06, 2 / 3, "t", "pli 4", (-0.2, 2 / 3))],
    5: [(0.5, -0.1, 0.5, 1.1, "q", "1/2", (0.5, -0.08)), (4 / 3, 0.25, 8 / 3, 0.25, "q", "1/4", (2.85, 0.25)),
        (3, 0.375, 4.08, 0.375, "q", "3/8", (4.22, 0.375)), (3, 0.625, 4.08, 0.625, "q", "5/8", (4.22, 0.625))],
}


def _tag(d, x, y, t, k):
    X, Y, w = d.X(x), d.Y(y), 7.3 * len(t) + 14
    d.dessus.append((k, f'<rect x="{X-w/2:.1f}" y="{Y-10:.1f}" width="{w:.1f}" height="20" rx="10" fill="{COL[k]}"/>'
                        f'<text x="{X:.1f}" y="{Y+4.5:.1f}" fill="#fff" font-size="12" font-weight="700" text-anchor="middle">{html.escape(t)}</text>'))


def _pli(d, x0, y0, x1, y1, k, actif=True, w=None):
    w = w or (3.2 if actif else 1.4)
    op = 1 if actif else 0.4
    d.dessus.append((k, f'<line x1="{d.X(x0):.1f}" y1="{d.Y(y0):.1f}" x2="{d.X(x1):.1f}" y2="{d.Y(y1):.1f}" stroke="{COL[k]}" stroke-width="{w}" '
                        f'stroke-opacity="{op}" stroke-dasharray="{TRAIT_PLI}" stroke-linecap="round"/>'))


def _plis(d, n):
    """les plis d'avant en pâle, ceux de l'étape n en gras avec leur étiquette"""
    for m in sorted(PLIS_PLAN):
        if m > n: break
        for x0, y0, x1, y1, k, t, at in PLIS_PLAN[m]:
            _pli(d, x0, y0, x1, y1, k, actif=(m == n))
            if m == n: _tag(d, *at, t, k)


def _rond(d, x, y, k, r=0.07):
    d.dessus.append((k, f'<circle cx="{d.X(x):.1f}" cy="{d.Y(y):.1f}" r="{r*S:.1f}" fill="none" stroke="{COL[k]}" stroke-width="2.6"/>'))


def _bloc(d, x0, y0, x1, y1, k, op=0.3):
    d.dessus.append((k, f'<rect x="{d.X(x0):.1f}" y="{d.Y(y0):.1f}" width="{(x1-x0)*S:.1f}" height="{(y1-y0)*S:.1f}" fill="{COL[k]}" fill-opacity="{op}"/>'))


def _fleche(d, x0, x1, y, h, k):
    """flèche courbe : le sens du pliage"""
    X0, X1, Y, C = d.X(x0), d.X(x1), d.Y(y), d.Y(y - h)
    Xm = (X0 + X1) / 2
    vx, vy = X1 - Xm, Y - C; n = (vx * vx + vy * vy) ** 0.5; vx, vy = vx / n, vy / n
    p = [(X1, Y), (X1 - 13 * vx - 6 * vy, Y - 13 * vy + 6 * vx), (X1 - 13 * vx + 6 * vy, Y - 13 * vy - 6 * vx)]
    d.dessus.append((k, f'<path d="M{X0:.1f} {Y:.1f} Q {Xm:.1f} {C:.1f} {X1:.1f} {Y:.1f}" fill="none" stroke="{COL[k]}" stroke-width="2"/>'
                        f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in p)}" fill="{COL[k]}"/>'))


# ================================================================ les constructions à la règle et au compas
# Tous les points sont calculés en fractions exactes (Fraction) : les figures ne sont donc pas dessinées « à l'œil »,
# et chaque construction vérifie par un assert qu'elle tombe bien sur la fraction annoncée.
from fractions import Fraction as Fr
import math

E_, F_, N_ = Fr(1, 21), Fr(1, 15), Fr(1, 9)


def inter(p, q, r, s):
    """intersection des droites (pq) et (rs)"""
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p, q, r, s
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    assert den != 0
    a, b = x1 * y2 - y1 * x2, x3 * y4 - y3 * x4
    return ((a * (x3 - x4) - (x1 - x2) * b) / den, (a * (y3 - y4) - (y1 - y2) * b) / den)


def _f(p): return float(p[0]), float(p[1])


def _L(d, p, q, k="g", w=1.2, dash="", op=1.0):
    """un trait de construction entre deux points (en a)"""
    (x0, y0), (x1, y1) = _f(p), _f(q)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    d.dessus.append((k, f'<line x1="{d.X(x0):.1f}" y1="{d.Y(y0):.1f}" x2="{d.X(x1):.1f}" y2="{d.Y(y1):.1f}" stroke="{COL[k]}" stroke-width="{w}" stroke-opacity="{op}"{da} stroke-linecap="round"/>'))


def _fold(d, p, q, k):
    """une ligne obtenue : trait mixte épais (comme les plis)"""
    _L(d, p, q, k, 3.0, TRAIT_PLI)


def _P(d, p, k="g", r=4.5):
    x, y = _f(p)
    d.dessus.append((k, f'<circle cx="{d.X(x):.1f}" cy="{d.Y(y):.1f}" r="{r}" fill="{COL[k]}"/>'))


def _N(d, p, n, k="g", dx=0, dy=0):
    """le numéro d'une étape, dans un rond"""
    x, y = _f(p)
    d.dessus.append((k, f'<circle cx="{d.X(x)+dx:.1f}" cy="{d.Y(y)+dy:.1f}" r="9.5" fill="{COL[k]}" stroke="#fbfbf8" stroke-width="1.5"/>'
                        f'<text x="{d.X(x)+dx:.1f}" y="{d.Y(y)+dy+4.2:.1f}" fill="#fff" font-size="12" font-weight="700" text-anchor="middle">{n}</text>'))


def _arc(d, c, r, a0, a1, k="g", w=1.4, dash=""):
    """arc de compas : centre c, rayon r (en a), angles en degrés (0° = vers la droite, sens des aiguilles d'une montre)"""
    (cx, cy), r = _f(c), float(r)
    x0, y0 = d.X(cx) + r * S * math.cos(math.radians(a0)), d.Y(cy) + r * S * math.sin(math.radians(a0))
    x1, y1 = d.X(cx) + r * S * math.cos(math.radians(a1)), d.Y(cy) + r * S * math.sin(math.radians(a1))
    da = f' stroke-dasharray="{dash}"' if dash else ""
    d.dessus.append((k, f'<path d="M{x0:.1f} {y0:.1f} A {r*S:.1f} {r*S:.1f} 0 {1 if abs(a1-a0) > 180 else 0} {1 if a1 > a0 else 0} {x1:.1f} {y1:.1f}" '
                        f'fill="none" stroke="{COL[k]}" stroke-width="{w}"{da}/>'))


def _txt(d, p, t, k="g", taille=12, ancre="middle", dx=0, dy=0):
    x, y = _f(p)
    d.dessus.append((k, f'<text x="{d.X(x)+dx:.1f}" y="{d.Y(y)+dy:.1f}" fill="{COL[k]}" font-size="{taille}" font-weight="700" text-anchor="{ancre}" '
                        f'paint-order="stroke" stroke="#fbfbf8" stroke-width="3">{html.escape(t)}</text>'))


def _base(vue=None):
    """le plan (ou la coupe) en gris pâle : on dessine les constructions par-dessus"""
    d, _, _ = (vue or plan_rdc)()
    d.par, d.dessus, d.cal = [], [], []
    d.fond = ['<g opacity="0.5">'] + d.fond + ['</g>']
    return d


class Zoom:
    """un morceau du plan agrandi (le plan est redessiné à l'échelle z, puis recadré)"""
    mg, n = 0, 0

    def __init__(self, W, H, corps, ox, oy, z=1):
        self.W, self.H, self.corps, self.ox, self.oy, self.z = W, H, corps, ox, oy, z
        Zoom.n += 1; self.id = f"zc{Zoom.n}"           # un clipPath par zoom (les id sont partagés dans la page)

    def svg(self, titre, couche=None, mm=None):
        taille = f' width="{self.W*mm:.2f}mm" height="{self.H*mm:.2f}mm"' if mm else ""
        return (f'<svg viewBox="0 0 {self.W:.0f} {self.H:.0f}"{taille} role="img" aria-label="{html.escape(titre)}" font-family="IBM Plex Mono, ui-monospace, monospace">'
                f'<rect width="100%" height="100%" fill="#fbfbf8"/><defs><clipPath id="{self.id}"><rect width="{self.W:.0f}" height="{self.H:.0f}"/></clipPath></defs>'
                f'<g clip-path="url(#{self.id})"><g transform="translate({-self.ox:.1f} {-self.oy:.1f})">{self.corps}</g></g>'
                f'<rect x="0.75" y="0.75" width="{self.W-1.5:.0f}" height="{self.H-1.5:.0f}" fill="none" stroke="#1c2120" stroke-width="1.5"/></svg>')


def _zoomer(dessine, region, z, vue=None):
    """redessine la vue à l'échelle z (× S), ajoute les tracés de dessine(d), puis recadre sur region (x0, x1, y0, y1)"""
    global S
    s0 = S
    S = s0 * z
    try:
        d = _base(vue)
        dessine(d)
        x0, x1, y0, y1 = region
        ox, oy, W, H = d.X(x0), d.Y(y0), (x1 - x0) * S, (y1 - y0) * S
        corps = "".join(x for _, x in d.par) + "".join(d.fond) + "".join(x for _, x in d.dessus)
    finally:
        S = s0
    return Zoom(W, H, corps, ox, oy, z)


def _diagonales(d, x0, y0, x1, y1, k, w=1.1, op=0.9):
    """les deux diagonales d'un rectangle ; renvoie leur point de croisement (le centre)"""
    c = inter((x0, y0), (x1, y1), (x0, y1), (x1, y0))
    assert c == ((Fr(x0) + Fr(x1)) / 2, (Fr(y0) + Fr(y1)) / 2)
    _L(d, (x0, y0), (x1, y1), k, w, "", op); _L(d, (x0, y1), (x1, y0), k, w, "", op)
    return c


def _tiers_dans_rect(d, x0, y0, x1, y1, k_aux="g", k_res="t", etiquette=True, num=(1, 2, 3, 4, 5)):
    """le tiers par la diagonale et le milieu (valable pour tout rectangle) ; renvoie les 2 points I (1/3 et 2/3 de la hauteur)"""
    x0, y0, x1, y1 = Fr(x0), Fr(y0), Fr(x1), Fr(y1)
    xm, w, h = (x0 + x1) / 2, x1 - x0, y1 - y0
    # ① diagonale (bas-gauche → haut-droit), ② milieu M du côté du bas, ③ droite du coin haut-gauche à M, ④ intersection I
    M = (xm, y1)
    I = inter((x0, y1), (x1, y0), (x0, y0), M)
    assert I == (x0 + w / 3, y0 + 2 * h / 3), I
    _L(d, (x0, y1), (x1, y0), k_aux, 1.3); _P(d, M, k_aux, 4); _L(d, (x0, y0), (xm, y1 + h / 12), k_aux, 1.3)
    # ⑤ à l'envers : diagonale haut-gauche → bas-droit, milieu M' du côté du haut, droite du coin bas-gauche à M'
    M2 = (xm, y0)
    I2 = inter((x0, y0), (x1, y1), (x0, y1), M2)
    assert I2 == (x0 + w / 3, y0 + h / 3), I2
    _L(d, (x0, y0), (x1, y1), k_aux, 1.3, "6 4"); _P(d, M2, k_aux, 4); _L(d, (x0, y1), (xm, y0 - h / 12), k_aux, 1.3, "6 4")
    return I, I2


def _thales(d, A, B, n, k_res, vers=(1, 2), s_total=Fr(3, 10), parallele=True, vertical=False):
    """Thalès : on divise AB en n parts égales. Une demi-droite quelconque part de A, n pas de compas égaux, on joint le dernier
    point à B, puis les parallèles. Renvoie les n+1 points de division."""
    A, B = (Fr(A[0]), Fr(A[1])), (Fr(B[0]), Fr(B[1]))
    ux, uy = vers
    pas = Fr(s_total) / n
    P = [(A[0] + k * pas * ux / 2, A[1] + k * pas * uy / 2) for k in range(n + 1)]       # points de la demi-droite, équidistants
    _L(d, A, (A[0] + Fr(s_total) * ux / 2 * Fr(11, 10), A[1] + Fr(s_total) * uy / 2 * Fr(11, 10)), "g", 1.4)
    dirx, diry = B[0] - P[n][0], B[1] - P[n][1]
    _L(d, P[n], B, "g", 1.6)
    Q = [A]
    for k in range(1, n):
        q = inter(P[k], (P[k][0] + dirx, P[k][1] + diry), A, B)
        assert q == (A[0] + (B[0] - A[0]) * k / n, A[1] + (B[1] - A[1]) * k / n), q
        _L(d, P[k], q, k_res, 1.5, "5 3")
        Q.append(q)
    Q.append(B)
    L = math.hypot(*[float(v) for v in (ux, uy)]) * float(pas) / 2
    ang = math.degrees(math.atan2(float(uy), float(ux)))
    for k in range(1, n + 1):                                        # les arcs de compas entre les points de la demi-droite
        _arc(d, P[k - 1], L, ang - 16, ang + 16, "g", 1.2)
    for k in range(n + 1):
        _P(d, P[k], "g", 3.4)
    for q in Q: _P(d, q, k_res, 4)
    return P, Q


def _R(d, x0, y0, x1, y1, k="g", w=1.2, dash=""):
    _L(d, (x0, y0), (x1, y0), k, w, dash); _L(d, (x1, y0), (x1, y1), k, w, dash)
    _L(d, (x1, y1), (x0, y1), k, w, dash); _L(d, (x0, y1), (x0, y0), k, w, dash)


# ---- 1. le milieu : les diagonales
def fig_milieu(d):
    c = _diagonales(d, 0, 0, 4, 1, "a")
    assert c == (2, Fr(1, 2))
    _fold(d, (2, -0.1), (2, 1.1), "a"); _P(d, c, "a", 5.5); _N(d, (2, -0.1), 1, "a", dy=-14)
    _txt(d, (2, -0.1), "2 a (pli 1)", "a", 12, "start", dx=16, dy=-10)
    c2 = _diagonales(d, 0, 0, 1, 1, "q")
    assert c2 == (Fr(1, 2), Fr(1, 2))
    _fold(d, (Fr(1, 2), -0.1), (Fr(1, 2), 1.1), "q"); _P(d, c2, "q", 5.5); _N(d, (Fr(1, 2), -0.1), 2, "q", dy=-14)
    _txt(d, (Fr(1, 2), 1.1), "1/2 a", "q", 12, "middle", dy=18)


# ---- 2. les quarts et les huitièmes : on recommence
def fig_quarts(d):
    _R(d, 0, 0, Fr(1, 2), 1, "q", 1.2, "5 3")
    c = _diagonales(d, 0, 0, Fr(1, 2), 1, "q")
    assert c == (Fr(1, 4), Fr(1, 2))
    _fold(d, (Fr(1, 4), -0.06), (Fr(1, 4), 1.06), "q"); _P(d, c, "q", 5); _N(d, (Fr(1, 4), -0.06), 1, "q", dy=-14)
    c2 = _diagonales(d, 0, 0, Fr(1, 4), 1, "e")
    assert c2 == (Fr(1, 8), Fr(1, 2))
    _fold(d, (Fr(1, 8), -0.06), (Fr(1, 8), 1.06), "e"); _P(d, c2, "e", 5); _N(d, (Fr(1, 8), -0.06), 2, "e", dy=-14)
    _txt(d, (Fr(1, 2), 1.07), "1/2 a", "q", 12, "middle", dy=16); _txt(d, (Fr(1, 4), 1.07), "1/4 a", "q", 12, "middle", dy=16)
    _txt(d, (Fr(1, 8), 1.07), "1/8 a", "e", 12, "middle", dy=16)
    # ⑤ le compas ouvert de 1/8 a (de 0 à 1/8), pointe sur le milieu du côté gauche : il marque 3/8 a et 5/8 a
    cc = (0, Fr(1, 2))
    _L(d, (0, Fr(1, 2)), (Fr(1, 8), Fr(1, 2)), "e", 3.2)
    _arc(d, cc, Fr(1, 8), -112, -68, "e", 1.8); _arc(d, cc, Fr(1, 8), 68, 112, "e", 1.8)
    for y in (Fr(3, 8), Fr(5, 8)): _P(d, (0, y), "e", 5)
    _N(d, (Fr(1, 8), Fr(3, 8)), 3, "e", dx=14, dy=-6)
    for y, t in ((Fr(3, 8), "3/8"), (Fr(1, 2), "1/2"), (Fr(5, 8), "5/8")): _txt(d, (0, y), t, "q", 12, "end", dx=-10, dy=4)


# ---- 3. le tiers : la diagonale et le milieu
def fig_tiers(d):
    _R(d, 0, 0, 1, 1, "a", 1.6)
    I, I2 = _tiers_dans_rect(d, 0, 0, 1, 1, "g", "t")
    for x in (Fr(1, 3),): _fold(d, (x, -0.06), (x, 1.06), "t")
    for y in (Fr(1, 3), Fr(2, 3)): _fold(d, (-0.06, y), (1.06, y), "t")
    _P(d, I, "t", 5.5); _P(d, I2, "t", 5.5)
    _txt(d, (Fr(1, 3), -0.09), "1/3 a", "t", 12, "middle")
    _txt(d, (1.08, Fr(2, 3)), "2/3 a", "t", 12, "start", dy=4); _txt(d, (1.08, Fr(1, 3)), "1/3 a", "t", 12, "start", dy=4)
    _N(d, (0.9, 0.1), 1, "g"); _N(d, (0.5, 1.0), 2, "g", dy=14); _N(d, (0.17, 0.34), 3, "g", dx=-14)
    _N(d, I, 4, "t", dx=16, dy=14); _N(d, (0.5, 0.0), 5, "g", dy=-14)
    # ⑥ le compas ouvert de 1/3 a (de 0 à 1/3), pointe en x = a : il marque 4/3 a
    _L(d, (0, 0), (Fr(1, 3), 0), "t", 3.5)
    _arc(d, (1, 0), Fr(1, 3), -24, 24, "t", 2.2)
    _fold(d, (Fr(4, 3), -0.06), (Fr(4, 3), 1.06), "t"); _P(d, (Fr(4, 3), 0), "t", 5.5)
    _L(d, (1, 0), (Fr(4, 3), 0), "t", 3.5)
    _txt(d, (Fr(4, 3), -0.09), "a + 1/3 a (pli 3)", "t", 12, "middle"); _N(d, (Fr(4, 3), 0.1), 6, "t", dx=14)


# ---- 4/5. Thalès : le tiers en 7 (mur) et en 5 (marche, fente)
def _fig_thales(n, k, nom):
    def f(d):
        A, B = (Fr(1), Fr(0)), (Fr(4, 3), Fr(0))
        _R(d, 1, 0, Fr(4, 3), Fr(1, 3), "a", 1.4, "5 3")
        P, Q = _thales(d, A, B, n, k)
        assert Q[1][0] - A[0] == Fr(1, 3) / n
        _L(d, A, Q[1], k, 6)                                        # la première part
        for i in range(1, n + 1): _txt(d, P[i], str(i), "g", 11, "end", dx=-7, dy=4)
        d.cote_h(1, 4 / 3, -0.06, "1/3 a = %d parts" % n, "t", ext=0)
        _txt(d, ((A[0] + Q[1][0]) / 2, 0), nom, k, 13, "middle", dy=-26)
        _N(d, ((A[0] + P[n][0]) / 2, (A[1] + P[n][1]) / 2), 1, "g", dx=-18, dy=4); _N(d, P[3], 2, "g", dx=16, dy=-4)
        _N(d, ((P[n][0] + B[0]) / 2, P[n][1] / 2), 3, "g", dx=14, dy=6); _N(d, Q[n // 2 + 1], 4, k, dy=-16)
    return f


fig_thales7 = _fig_thales(7, "e", "e = 1/21 a")
fig_thales5 = _fig_thales(5, "t", "1/15 a")


# ---- 6. le tiers du tiers = 1/9 a
def fig_neuvieme(d):
    _R(d, 1, 0, Fr(4, 3), Fr(1, 3), "a", 1.8)
    I, I2 = _tiers_dans_rect(d, 1, 0, Fr(4, 3), Fr(1, 3), "g", "t")
    assert I[0] == 1 + N_ and I2[0] == 1 + N_
    _fold(d, (1 + N_, -0.04), (1 + N_, Fr(1, 3) + 0.04), "t"); _P(d, I, "t", 5.5); _P(d, I2, "t", 5.5)
    _txt(d, (1 + N_, -0.065), "1/9 a", "t", 13, "middle")
    # le compas ouvert de 1/9 a (de 1 à 1 + 1/9), pointe sur l'axe du mur (4/3) : il marque 4/3 − 1/9
    _L(d, (1, Fr(1, 3) + 0.06), (1 + N_, Fr(1, 3) + 0.06), "t", 3.5)
    _arc(d, (Fr(4, 3), 0), N_, 156, 204, "t", 2.2)
    _P(d, (Fr(4, 3) - N_, 0), "t", 5.5); _txt(d, (Fr(4, 3) - N_, -0.065), "1/9 a du mur", "t", 11, "middle")
    _N(d, (1.05, 0.255), 1, "g"); _N(d, (1 + Fr(1, 6), Fr(1, 3)), 2, "g", dy=15); _N(d, (1.06, 0.1), 3, "g")
    _N(d, I, 4, "t", dx=14, dy=14); _N(d, (1 + Fr(1, 6), 0), 5, "g", dy=-10, dx=34)
    _L(d, (Fr(4, 3), -0.03), (Fr(4, 3), Fr(1, 3) + 0.03), "t", 2.0, "6 4")


# ---- 7. le pont : le demi-cercle au compas
def fig_pont(d):
    C = (Fr(4, 3), Fr(1, 2))
    _fold(d, (Fr(4, 3), 0.2), (Fr(4, 3), 0.8), "t")
    c = _diagonales(d, 1, Fr(1, 3), Fr(4, 3), Fr(2, 3), "a")
    assert c[1] == Fr(1, 2)
    _L(d, (0.9, Fr(1, 2)), (1.7, Fr(1, 2)), "a", 1.6, "6 4"); _P(d, C, "t", 6)
    _L(d, C, (Fr(4, 3), Fr(1, 3)), "t", 2.6); _L(d, C, (Fr(4, 3), Fr(2, 3)), "t", 2.6)
    _arc(d, C, Fr(1, 6), 90, 270, "t", 3.4)
    _P(d, (Fr(4, 3), Fr(1, 3)), "t", 4.5); _P(d, (Fr(4, 3), Fr(2, 3)), "t", 4.5)
    _txt(d, (Fr(4, 3) + 0.045, Fr(1, 2) - 0.05), "r = 1/6 a", "t", 12, "start")
    _N(d, (Fr(4, 3), 0.2), 1, "t", dx=14); _N(d, (1, Fr(1, 3)), 2, "g", dx=-14, dy=-10); _N(d, C, 3, "t", dx=15, dy=15)
    _N(d, (Fr(4, 3) - Fr(1, 6), Fr(1, 2)), 4, "t", dx=-20)


# ---- 8. les fenêtres des longs murs (plan)
def fig_fentes(d):
    X3 = Fr(4, 3)
    _L(d, (X3, -0.125), (X3, 0.2), "t", 2.8, TRAIT_PLI); _txt(d, (X3, -0.145), "pli 3 = axe du mur du patio", "t", 11, "end", dx=60)
    R1 = X3 - N_
    g1 = R1 - 3 * F_
    assert abs(float(g1) - G1) < 1e-12
    # ① le recul : compas ouvert de 1/9 a, pointe sur le pli 3
    _arc(d, (X3, 0), N_, 160, 200, "t", 2.6); _P(d, (R1, 0), "t", 5.5)
    # ② trois pas de compas de 1/15 a, vers la gauche
    for j in range(3): _arc(d, (R1 - j * F_, 0), F_, 160, 200, "q", 2.4)
    for j in range(4): _P(d, (R1 - j * F_, 0), "q", 5)
    for x in (g1, g1 + 2 * F_): _bloc(d, float(x), 0, float(x + F_), float(E), "q", 0.9)
    _txt(d, (R1 + N_ / 2, -0.03), "1/9", "t", 12, "middle")
    for j in range(3): _txt(d, (R1 - j * F_ - F_ / 2, -0.03), "1/15", "q", 12, "middle")
    for j, t in enumerate(("fente", "trumeau", "fente")): _txt(d, (R1 - j * F_ - F_ / 2, 0.105), t, "q", 11.5, "middle")
    d.cote_h(float(g1), float(R1), -0.085, "1/5 a", "q", ext=0)
    _N(d, (R1, 0), 1, "t", dy=-30, dx=6); _N(d, (g1 + F_, 0), 2, "q", dy=-30)


# ---- 9. l'escalier en plan : les marches et la largeur
def fig_escalier_plan(d):
    _L(d, (2, -0.115), (2, 0.3), "a", 2.8, TRAIT_PLI); _txt(d, (2, -0.135), "pli 1 = milieu du patio", "a", 11, "middle")
    # ① un demi-pas de 1/15 a (= 1/30 a) de chaque côté du pli 1
    _arc(d, (2, 0), Fr(1, 30), -26, 26, "q", 2.4); _arc(d, (2, 0), Fr(1, 30), 154, 206, "q", 2.4)
    # ② puis 5 pas de 1/15 a de chaque côté
    for s_ in (1, -1):
        x = Fr(2) + s_ * Fr(1, 30)
        for j in range(5):
            a0, a1 = (-26, 26) if s_ > 0 else (154, 206)
            _arc(d, (x + s_ * j * F_, 0), F_, a0, a1, "q", 2.0)
    for i in range(12):
        x = Fr(2) + Fr(2 * i - 11, 30)
        _L(d, (x, -0.03), (x, Fr(1, 4)), "q", 2.6); _P(d, (x, 0), "q", 4)
    assert abs(float(Fr(2) - Fr(11, 30)) - M0) < 1e-12
    for i in range(11): _txt(d, (Fr(2) + Fr(2 * i - 10, 30), 0.205), str(i + 1), "q", 11, "middle")
    d.cote_h(float(Fr(2) - Fr(11, 30)), float(Fr(2) + Fr(11, 30)), -0.085, "11 marches × 1/15 a = 11/15 a", "q", ext=0)
    # ③ la largeur : 1/4 a depuis la face extérieure, mur compris
    _bloc(d, 1.64, float(E), 2.36, 0.25, "e", 0.14)
    d.cote_v(0, 0.25, 2.42, "1/4 a, mur compris", "e", ext=2.37, cote="d")
    d.cote_v(0, float(E), 1.56, "e", "e", ext=1.64, cote="g")
    _N(d, (2, -0.0), 1, "q", dy=-30, dx=34); _N(d, (Fr(2) + Fr(13, 30), 0), 2, "q", dy=-30); _N(d, (2.37, 0.25), 3, "e", dx=14, dy=10)


# ---- 10. la porte d'entrée (plan)
def fig_porte(d):
    c = _diagonales(d, 3, 0, 4, 1, "a")
    _L(d, (3.5, Fr(1, 2)), (4.12, Fr(1, 2)), "a", 2.0, "7 4"); _P(d, c, "a", 4.5)
    C = (Fr(4), Fr(1, 2))
    _N(d, (3.55, Fr(1, 2)), 1, "a", dy=-14)
    # ② cadre de 1/4 a : compas ouvert de 1/8 a, pointe au milieu du mur
    _arc(d, C, Fr(1, 8), -112, -68, "q", 2); _arc(d, C, Fr(1, 8), 68, 112, "q", 2)
    for y in (Fr(3, 8), Fr(5, 8)): _P(d, (Fr(4), y), "q", 5); _L(d, (Fr(4), y), (Fr(41, 10), y), "q", 1.8)
    _L(d, (Fr(41, 10), Fr(3, 8)), (Fr(41, 10), Fr(5, 8)), "q", 3.2)
    _txt(d, (4.13, Fr(1, 2) + 0.04), "cadre 1/4 a", "q", 12, "start", dy=0); _N(d, (3.97, Fr(3, 8)), 2, "q", dx=-16, dy=-4)
    # ③ passage de 4 e : le compas ouvert de e, deux pas de chaque côté du milieu
    for y in (Fr(1, 2) - 2 * E_, Fr(1, 2) - E_, Fr(1, 2) + E_, Fr(1, 2) + 2 * E_): _P(d, (Fr(4), y), "e", 3.8)
    _arc(d, C, E_, -112, -68, "e", 1.8); _arc(d, C, E_, 68, 112, "e", 1.8)
    _L(d, (Fr(4), Fr(1, 2) - 2 * E_), (Fr(4), Fr(1, 2) + 2 * E_), "e", 6)
    d.cote_v(float(Fr(1, 2) - 2 * E_), float(Fr(1, 2) + 2 * E_), 3.935, "4 e", "e", cote="g")
    _N(d, (3.92, Fr(1, 2) + 2 * E_), 3, "e", dx=-2, dy=18)


# ---- 11. la douche (plan de l'étage)
def fig_douche(d):
    yb = Fr(3, 10)
    _L(d, (3.6, yb), (4.1, yb), "g", 1.0, "4 3"); _L(d, (4, 0.26), (4, 0.74), "a", 2.2, TRAIT_PLI); _txt(d, (4, 0.742), "face extérieure", "a", 11, "end", dx=-8)
    # ① quatre pas de compas de e, depuis la face extérieure vers l'intérieur
    for j in range(4):
        _arc(d, (Fr(4) - j * E_, yb), E_, 160, 200, "e", 2.2)
    for j in range(5): _P(d, (Fr(4) - j * E_, yb), "e", 4.5)
    _L(d, (4 - 4 * E_, yb), (Fr(4), yb), "e", 5)
    _fold(d, (4 - 4 * E_, 0.32), (4 - 4 * E_, 0.68), "e")
    for j in range(4): _txt(d, (Fr(4) - j * E_ - E_ / 2, yb - 0.025), "e", "e", 12, "middle")
    d.cote_h(float(4 - 4 * E_), 4, 0.70, "4 e", "e", ext=0.67, cote="c")
    # ② la largeur : 1/4 a, de 3/8 a à 5/8 a (construction des quarts)
    _R(d, float(4 - 4 * E_), 0.375, 4, 0.625, "q", 2.4, "6 3")
    d.cote_v(0.375, 0.625, 4.07, "1/4 a", "q", ext=4, cote="d")
    _N(d, (Fr(4) - 4 * E_, yb), 1, "e", dx=-18, dy=-4); _N(d, (3.8, 0.5), 2, "q")


# ---- 10. les fenêtres du jardin (façade C)
def fig_facade_c(d):
    A_ = "q"
    ax = Fr(1, 2)
    _L(d, (ax, 0.97), (ax, 1.23), "a", 2.6, TRAIT_PLI); _txt(d, (ax, 0.985), "axe de la façade (a / 2)", "a", 11, "middle", dy=-6)
    W1, W2 = ax - Fr(1, 14) - Fr(1, 8), ax + Fr(1, 14)
    assert abs(float(W1) - 0.3035714) < 1e-6
    yb = 1.20
    _L(d, (0.2, yb), (0.8, yb), "g", 1.0, "4 3")
    # ① e puis la moitié de e, de chaque côté de l'axe : 1,5 e = 1/14 a
    for s in (-1, 1):
        x1, x2 = ax + s * E_, ax + s * Fr(3, 2) * E_
        _P(d, (x1, yb), "e", 3.6); _P(d, (x2, yb), "e", 5)
        _arc(d, (ax, yb), E_, -20 if s > 0 else 160, 20 if s > 0 else 200, "e", 1.8)
    assert ax + Fr(3, 2) * E_ == ax + Fr(1, 14) and 2 * Fr(3, 2) * E_ == 3 * E_ and 3 * E_ == Fr(1, 7)
    # ② les fenêtres : le compas ouvert de 1/8 a, depuis ces deux repères, vers l'extérieur
    for x0 in (W1, W2):
        _bloc(d, float(x0), 1.03, float(x0 + Fr(1, 8)), 1.155, "q", 0.45)
        _L(d, (x0, yb), (x0 + Fr(1, 8), yb), "q", 4)
        _P(d, (x0, yb), "q", 4.5); _P(d, (x0 + Fr(1, 8), yb), "q", 4.5)
    _arc(d, (W1 + Fr(1, 8), yb), Fr(1, 8), 160, 200, "q", 1.8); _arc(d, (W2, yb), Fr(1, 8), -20, 20, "q", 1.8)
    _L(d, (W1 + Fr(1, 8), 1.215), (W2, 1.215), "e", 4)
    _txt(d, (ax, 1.245), "écart 3 e = 1/7 a", "e", 12, "middle"); _txt(d, (W1 + Fr(1, 16), 1.245), "1/8 a", "q", 12, "middle"); _txt(d, (W2 + Fr(1, 16), 1.245), "1/8 a", "q", 12, "middle")
    _N(d, (ax, yb), 1, "e", dy=-14, dx=44); _N(d, (W2 + Fr(1, 8), yb), 2, "q", dy=-14, dx=14)


# ---- 11. le garde-corps du pont : 5 e (coupe E)
def fig_garde_corps(d):
    x = Fr(1, 2)
    _L(d, (0.2, YR), (0.8, YR), "t", 1.8, "7 4"); _txt(d, (0.745, YR), "ligne 2/3 a", "t", 11, "end", dy=-6)
    _L(d, (0.2, YP), (0.8, YP), "g", 1.0, "4 3")
    _L(d, (x, YP + 0.02), (x, YR - 0.03), "g", 1.4)
    for j in range(5):
        y = Fr(19, 21) - j * E_
        _arc(d, (x, y), E_, -112, -68, "e", 2); _P(d, (x, y), "e", 4)
        _txt(d, (x, y - E_ / 2), "e", "e", 12, "start", dx=10, dy=4)
    top = Fr(19, 21) - 5 * E_
    assert top == Fr(2, 3) and abs(float(top) - YR) < 1e-12 and abs(float(Fr(19, 21)) - YP) < 1e-12
    _P(d, (x, top), "e", 6.5); _L(d, (x, YP), (x, top), "e", 5, "", 0.45)
    d.cote_v(float(YR), float(YP), 0.755, "5 e = 95 cm", "e", cote="d")
    _txt(d, (0.5, 0.945), "dalle du pont : dessus à 19 e", "g", 11, "middle")
    _bloc(d, 1 / 3, float(YR), 1 / 3 + float(E), float(YP), "e", 0.7); _bloc(d, 2 / 3 - float(E), float(YR), 2 / 3, float(YP), "e", 0.7)
    _N(d, (x, YP), 1, "g", dx=-18, dy=2); _N(d, (x, Fr(17, 21)), 2, "e", dx=-18); _N(d, (x, top), 3, "e", dx=-18, dy=-4)


# ---- 12. l'escalier : la hauteur à monter en 12 hauteurs de marche (Thalès)
def fig_escalier(d):
    A = (Fr(2) - Fr(11, 30), Fr(13, 8) - E_); B = (A[0], A[1] - Fr(7, 10))
    P, Q = _thales(d, A, B, 12, "t", vers=(-2, -1), s_total=Fr(11, 20))
    # le profil de l'escalier : 12 hauteurs, 11 marches de 1/15 a
    pts = [(A[0], A[1])]
    for i in range(12):
        pts.append((A[0] + i * F_, Q[i + 1][1]))
        if i < 11: pts.append((A[0] + (i + 1) * F_, Q[i + 1][1]))
    for p, q in zip(pts, pts[1:]): _L(d, p, q, "t", 3.0)
    for i in range(1, 13): _txt(d, P[i], str(i), "g", 10, "end", dx=-6, dy=4)
    _txt(d, (A[0] + Fr(6, 15), Fr(1, 1) + Fr(1, 4)), "12 hauteurs égales", "t", 12, "start", dx=0)
    _L(d, (A[0], YS), (A[0] + 11 * F_, YS), "g", 1.0, "4 3")
    d.cote_h(float(A[0]), float(A[0] + 11 * F_), 1.6, "11 marches × 1/15 a", "t", ext=1.5774)
    _N(d, (A[0] - Fr(1, 10), A[1] - Fr(1, 20)), 1, "g"); _N(d, (A[0] - Fr(1, 6), A[1] - Fr(1, 12)), 2, "g", dy=14); _N(d, ((P[12][0] + B[0]) / 2, (P[12][1] + B[1]) / 2), 3, "g", dx=-12, dy=-8)
    _N(d, (A[0], Q[7][1]), 4, "t", dx=14)


CONSTRUCTIONS = [
    # (id, titre, couleur, vue de base, région (x0, x1, y0, y1), zoom, dessin, « au pli », étapes)
    ("milieu", "Le milieu : les diagonales", "a", None, (-0.15, 4.2, -0.3, 1.25), 1, fig_milieu,
     "Au pli : on plie les deux bouts l'un sur l'autre, le pli est le milieu.",
     ["Trace les 2 diagonales du grand rectangle : elles se croisent au milieu. La verticale par ce point est à <b>2 a</b> (pli 1).",
      "Même chose dans le premier carré : le croisement est à <b>1/2 a</b> (la cloison de la salle de bain)."]),
    ("quarts", "Les quarts et les huitièmes : on recommence", "q", None, (-0.1, 0.62, -0.17, 1.16), 2.4, fig_quarts,
     "Au pli : on replie en deux, encore en deux, encore en deux.",
     ["Rectangle de 1/2 a de large : ses diagonales se croisent à <b>1/4 a</b>.",
      "Rectangle de 1/4 a de large : le croisement est à <b>1/8 a</b>.",
      "Le compas ouvert de 1/8 a, pointe au milieu du côté gauche, marque <b>3/8 a</b> et <b>5/8 a</b> : c'est le cadre de la porte."]),
    ("tiers", "Le tiers : la diagonale et le milieu", "t", None, (-0.14, 1.62, -0.2, 1.16), 2.2, fig_tiers,
     "Au pli : en accordéon, on plie en 3 parts qui se superposent.",
     ["Trace la diagonale du carré, du coin bas-gauche au coin haut-droit.",
      "Repère le milieu M du côté du bas (étape précédente).",
      "Trace la droite du coin haut-gauche au point M.",
      "Elle coupe la diagonale en I : la verticale par I est à <b>1/3 a</b>, l'horizontale par I à <b>2/3 a</b>.",
      "À l'envers (diagonale haut-gauche → bas-droit, milieu du côté du haut) : on trouve la ligne à <b>1/3 a</b> de hauteur.",
      "Compas ouvert de 1/3 a, pointe en x = a : il marque <b>4/3 a</b> (pli 3). Depuis l'autre bout, il marque 8/3 a."]),
    ("thales7", "Thalès : le tiers en 7, c'est le mur e", "e", None, (0.9, 1.5, -0.12, 0.4), 5, fig_thales7,
     "Au pli : on ne peut pas plier en 7. Il faut construire.",
     ["Prends le segment AB = 1/3 a. Trace une demi-droite quelconque qui part de A.",
      "Avec le compas ouvert à volonté, reporte <b>7 pas égaux</b> sur la demi-droite.",
      "Joins le dernier point à B.",
      "Trace les parallèles à cette droite par chaque point (règle et équerre) : elles coupent AB en <b>7 parts égales</b>. Une part = <b>e = 1/21 a</b>."]),
    ("thales5", "Thalès : le tiers en 5, c'est la marche et la fente", "t", None, (0.9, 1.5, -0.12, 0.4), 5, fig_thales5,
     "Au pli : on ne peut pas plier en 5. Il faut construire.",
     ["Même construction que le tiers en 7, mais avec <b>5 pas égaux</b> sur la demi-droite.",
      "Une part = <b>1/15 a</b>. Trois parts font 1/5 a."]),
    ("neuvieme", "Le tiers du tiers : 1/9 a", "t", None, (0.9, 1.45, -0.12, 0.42), 5, fig_neuvieme,
     "Au pli : on plie le tiers en 3 (accordéon).",
     ["Dans le petit carré de 1/3 a × 1/3 a (un module de la trame), trace la diagonale bas-gauche → haut-droit.",
      "Repère le milieu du côté du bas.",
      "Trace la droite du coin haut-gauche à ce milieu.",
      "Elle coupe la diagonale en I : la verticale par I est à <b>1/9 a</b> du bord gauche.",
      "Compas ouvert de 1/9 a (de 1 à 1 + 1/9), pointe sur l'axe du mur (4/3 a) : il marque 4/3 a − 1/9 a, le <b>recul des fenêtres</b>."]),
    ("pont", "Le pont : le demi-cercle au compas", "t", "etage", (0.85, 1.75, 0.16, 0.84), 3, fig_pont,
     "Au pli : on plie la largeur du pont en deux pour trouver son axe.",
     ["L'axe de la paroi vitrée (x = 4/3 a).",
      "Les diagonales du module de 1/3 a se croisent à mi-hauteur : l'horizontale par ce croisement est la ligne <b>y = 1/2 a</b>.",
      "Cette horizontale coupe l'axe en C : c'est le centre.",
      "Compas ouvert de C jusqu'au bord du pont (rayon <b>1/6 a</b>) : demi-cercle du côté de la chambre. Pareil à l'autre bout.",
      "Contrôle : le point le plus à gauche du demi-cercle tombe sur le croisement des diagonales (7/6 a)."]),
    ("escalier_plan", "L'escalier en plan : les marches et la largeur", "q", None, (1.5, 2.72, -0.17, 0.32), 4, fig_escalier_plan,
     "Au pli : on plie le pas de 1/15 en deux pour avoir le demi-pas.",
     ["Le pli 1 (milieu du patio) passe au milieu de la 6e marche : on part d'un <b>demi-pas (1/30 a)</b> de chaque côté.",
      "Puis <b>5 pas de 1/15 a</b> de chaque côté : 12 traits, donc <b>11 marches</b> (11/15 a).",
      "La largeur : le bord de l'escalier est à <b>1/4 a</b> de la face extérieure, le mur compris. L'escalier seul fait donc <b>1/4 a − e</b> (≈ 81 cm)."]),
    ("fentes", "Les fenêtres des longs murs (plan)", "q", None, (0.99, 1.4, -0.175, 0.14), 6, fig_fentes,
     "Au pli : le recul 1/9 se plie (le tiers en 3) ; les 1/15 se construisent (Thalès).",
     ["Compas ouvert de <b>1/9 a</b>, pointe sur l'axe du mur du patio (pli 3) : il marque le bord du groupe, vers la chambre.",
      "Trois pas de compas de <b>1/15 a</b> : fente, trumeau, fente. Le groupe fait <b>1/5 a</b>. Même chose de l'autre côté du patio (à 8/3 a) et sur l'autre long mur."]),
    ("porte", "La porte d'entrée (plan)", "q", None, (3.5, 4.25, 0.12, 0.9), 3.6, fig_porte,
     "Au pli : on plie la hauteur du mur en 8 pour trouver 3/8 et 5/8.",
     ["Les diagonales du carré donnent le milieu du mur : <b>y = 1/2 a</b>.",
      "Compas ouvert de 1/8 a, pointe au milieu : le <b>cadre de 1/4 a</b> (de 3/8 a à 5/8 a).",
      "Compas ouvert de e (construit par Thalès), 2 pas de chaque côté du milieu : le <b>passage de 4 e</b> (≈ 76 cm)."]),
    ("douche", "La douche (plan de l'étage)", "e", "etage", (3.55, 4.2, 0.22, 0.78), 5, fig_douche,
     "Au pli : la largeur 1/4 a se plie ; la profondeur 4 e se construit.",
     ["Compas ouvert de e, <b>4 pas</b> depuis la face extérieure vers l'intérieur : l'axe du mur de la douche est à <b>4 e</b> (≈ 76 cm).",
      "La largeur : <b>1/4 a</b>, de 3/8 a à 5/8 a (comme le cadre de la porte, en dessous)."]),
    ("facade_c", "Les fenêtres du jardin (façade C)", "q", "facade_c", (0.18, 0.82, 0.96, 1.27), 4.6, fig_facade_c,
     "Au pli : a en 8 pour 1/8 ; l'écart 1/7 se construit (Thalès).",
     ["De chaque côté de l'axe : un pas de e, puis la moitié d'un pas : <b>1,5 e = 1/14 a</b>. L'écart entre les fenêtres fait donc <b>3 e = 1/7 a</b>.",
      "Compas ouvert de 1/8 a : chaque fenêtre fait <b>1/8 a</b> (un carré), en partant de ces repères vers l'extérieur."]),
    ("garde_corps", "Le garde-corps du pont : 5 e (coupe E)", "e", "coupe_e", (0.22, 0.8, 0.58, 1.08), 4.2, fig_garde_corps,
     "Au pli : on ne peut pas plier en 21 : on reporte e au compas.",
     ["Repère le dessus de la dalle du pont (19 e depuis le haut).",
      "Reporte <b>5 fois e</b> vers le haut avec le compas.",
      "Le haut tombe sur la ligne des <b>2/3 a</b> de la trame : le contrôle est bon. Hauteur = <b>5 e = 95 cm</b>."]),
    ("escalier", "L'escalier : la hauteur en 12 (Thalès)", "t", "coupe_longue", (1.05, 2.5, 0.78, 1.66), 1.9, fig_escalier,
     "Au pli : on ne peut pas plier en 12 pièces égales à coup sûr : on construit.",
     ["Segment AB = la hauteur à monter (du sol au plancher). Demi-droite quelconque qui part de A.",
      "Reporte <b>12 pas égaux</b> au compas.",
      "Joins le dernier point à B.",
      "Les parallèles (règle + équerre) coupent AB en <b>12 hauteurs de marche égales</b> ; chaque marche fait 1/15 a de large."]),
]
VUES_BASE = {"etage": plan_etage, "facade_c": facade_c, "coupe_e": coupe_e, "coupe_longue": coupe_longue, None: None}


def construire(i):
    """la figure i, prête à être affichée (objet avec .svg())"""
    id_, titre, k, vue, region, z, dessin, au_pli, etapes = CONSTRUCTIONS[i]
    return _zoomer(dessin, region, z, VUES_BASE[vue])


ETAPES = [
    (1, "Pli 1 · le plan plié en 2"),
    (2, "Pli 2 · encore en 2 : 4 carrés a"),
    (3, "Pli 3 · en 3 : les plis tombent sur les murs du patio"),
    (4, "Pli 4 · la largeur en 3 : la trame de 1/3 a"),
    (5, "Pli 5 · a en 2, 4, 8 : salle de bain, escalier, porte"),
]


def etape(n):
    titre = dict(ETAPES)[n]
    d = _base()
    _plis(d, n)
    if n == 1:
        _fleche(d, 3.3, 0.7, -0.12, 0.5, "a")
        d.cote_h(0, 2, 1.25, "2 a", "a", ext=1); d.cote_h(2, 4, 1.25, "2 a", "a", ext=1)
    elif n == 2:
        for i in range(4): d.zone(i, 0, i + 1, 1, "a", op=0.13 if i % 2 == 0 else 0.04, dash="2 0", w=0)
        for i in range(4): d.cote_h(i, i + 1, 1.25, "a", "a", ext=1)
        d.cote_v(0, 1, -0.14, "a", "a", ext=0)
        _pli(d, 3, 0, 4, 1, "a", w=1.6)                                    # contrôle : la diagonale du carré
        _fleche(d, 1.45, 0.55, -0.12, 0.3, "a"); _fleche(d, 3.45, 2.55, -0.12, 0.3, "a")
    elif n == 3:
        for x in (4 / 3, 8 / 3): _rond(d, x, 0.2, "t")
        for i in range(3): d.cote_h(i * 4 / 3, (i + 1) * 4 / 3, 1.25, "a + 1/3 a", "t", ext=1)
        _fleche(d, 2.1, 0.55, -0.12, 0.3, "t"); _fleche(d, 2.1, 3.45, -0.12, 0.3, "t")
    elif n == 4:
        for i in range(1, 12):
            if i % 3 and i not in (4, 8):
                d.dessus.append(("t", f'<line x1="{d.X(i/3):.1f}" y1="{d.Y(0):.1f}" x2="{d.X(i/3):.1f}" y2="{d.Y(1):.1f}" stroke="{COL["t"]}" stroke-width="1" stroke-opacity="0.45"/>'))
        _bloc(d, 4 / 3, 1 / 3, 8 / 3, 2 / 3, "t", 0.2); _bloc(d, 11 / 3, 1 / 3, 4, 2 / 3, "t", 0.3)
        for j in range(3): d.cote_v(j / 3, (j + 1) / 3, 4.14, "1/3 a", "t", ext=4, cote="d")
    elif n == 5:
        _rond(d, 0.5, 0.62, "q"); _rond(d, M1 - 0.05, 0.25, "q", 0.06)
        for y in (0.25, 0.5, 0.75): _pli(d, 3, y, 4.06, y, "q", w=1.2)
        _bloc(d, 4 - E, 0.375, 4, 0.625, "q", 0.6)
        d.cote_h(0, 0.5, 1.25, "1/2 a", "q", ext=1)
        d.cote_v(0, 0.25, 2.6, "1/4 a", "q", ext=M1, cote="g")
    return d, titre, []




# ================================================================ le tableau des mesures (réel, feuille, carnet)
def _vir(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")


MESURES = [
    ("Le plan", [
        ("a, le carré (largeur de la maison)", "a", Fr(1), "cote 650 = a + 5/8 a"),
        ("Longueur de la maison", "4 a", Fr(4), "4 carrés"),
        ("Une part : cuisine, patio ou séjour", "4/3 a", Fr(4, 3), "a + 1/3 a"),
        ("Le module de la trame", "1/3 a", Fr(1, 3), ""),
        ("Épaisseur des murs", "e = 1/21 a", E_, "1/7 du tiers"),
        ("Salle de bain (face extérieure → axe de la cloison)", "1/2 a", Fr(1, 2), ""),
        ("Sas d'entrée (un carré, aux axes de ses murs)", "1/3 a", Fr(1, 3), ""),
        ("Porte d'entrée : le cadre (façade)", "5 e", 5 * E_, "mesuré 0,380 à 0,617 a"),
        ("Porte d'entrée : le passage libre et le vantail", "4 e", 4 * E_, "montants e/2"),
        ("Porte d'entrée : l'encadrement en saillie", "1,5 e", Fr(3, 2) * E_, "mesuré 0,07 a"),
        ("Douche : largeur", "1/4 a", Fr(1, 4), "de 3/8 a à 5/8 a"),
        ("Douche : profondeur (face extérieure → axe du mur)", "4 e", 4 * E_, ""),
    ]),
    ("Le pont et son garde-corps", [
        ("Largeur du pont", "1/3 a", Fr(1, 3), "de 1/3 a à 2/3 a"),
        ("Rayon des bouts arrondis", "1/6 a", Fr(1, 6), "la moitié de 1/3 a"),
        ("Épaisseur d'un garde-corps", "e", E_, ""),
        ("Passage entre les deux garde-corps", "1/3 a − 2 e = 5 e", Fr(1, 3) - 2 * E_, ""),
        ("Hauteur du garde-corps", "5 e", 5 * E_, "cote écrite 95"),
        ("Haut du garde-corps, depuis le haut de la maison", "2/3 a", Fr(2, 3), "= 14 e"),
        ("Dalle du pont : plus basse que le plancher de l'étage de", "e", E_, "dessus à 19 e, plancher à 18 e"),
    ]),
    ("L'escalier", [
        ("Une marche (sa largeur)", "1/15 a", F_, "1/5 du tiers"),
        ("La volée : 11 marches", "11/15 a", 11 * F_, "centrée sur le milieu du patio"),
        ("Largeur, mur compris (depuis la face extérieure)", "1/4 a", Fr(1, 4), ""),
        ("Largeur de l'escalier seul", "1/4 a − e", Fr(1, 4) - E_, "≈ 1/5 a"),
        ("Hauteur à monter (sol → étage), en 12 hauteurs", "7/10 a", Fr(7, 10), "cote écrite 280"),
    ]),
    ("Les fenêtres", [
        ("Fente des longs murs", "1/15 a", F_, ""),
        ("Trumeau (le plein entre deux fentes)", "1/15 a", F_, ""),
        ("Un groupe : fente + trumeau + fente", "1/5 a", 3 * F_, ""),
        ("Recul du groupe (depuis l'axe du mur du patio)", "1/9 a", N_, "le tiers du tiers"),
        ("Fenêtre du jardin : largeur", "1/8 a", Fr(1, 8), ""),
        ("Fenêtre du jardin : hauteur", "1/7 a = 3 e", Fr(1, 7), "haut à e/2 au-dessus de la ligne a"),
        ("Écart entre les deux fenêtres du jardin", "1/7 a = 3 e", 3 * E_, "centrées sur la façade"),
        ("Fenêtres hautes de la coupe E : une fente", "1/15 a", F_, "groupe de 1/5 a"),
    ]),
    ("Les profils des portes et fenêtres (proposés)", [
        ("Montant du cadre de la porte", "e/2", E_ / 2, "proposition"),
        ("Épaisseur du vantail", "e/4", E_ / 4, "proposition"),
        ("Montant du vantail, cadre des fenêtres", "e/3", E_ / 3, "proposition"),
        ("Montant des fentes", "e/6", E_ / 6, "proposition"),
        ("Épaisseur du verre", "1 cm", Fr(1, 400), "verre simple de 10 mm, à valider"),
    ]),
    ("Les hauteurs (depuis le haut de l'acrotère)", [
        ("Hauteur totale", "13/8 a", Fr(13, 8), "cote 650"),
        ("Rez-de-chaussée sous plafond", "5/8 a", Fr(5, 8), "cote 250"),
        ("Acrotère (le muret du toit)", "1/7 a = 3 e", Fr(1, 7), ""),
        ("Dalle du toit", "≈ 1/16 a", Fr(1, 16), ""),
        ("Étage sous plafond", "≈ 2/3 a", Fr(6, 7) - Fr(1, 7) - Fr(1, 16), "cote écrite 250"),
        ("Plancher de l'étage", "2 e", 2 * E_, "cote 40 en haut de la coupe E"),
        ("Dalle du sol", "e", E_, ""),
        ("Hauteur libre sous le pont", "5/8 a − e", Fr(5, 8) - E_, "cote 230 ≈ 12 e"),
        ("Porte sous le pont (vantail)", "12 e", 12 * E_, "76 × 229 cm"),
        ("Porte de la façade B : hauteur", "5/8 a", Fr(5, 8), "= 250, comme le rez-de-chaussée"),
        ("Porte de la façade B : seuil", "3/4 e", Fr(3, 4) * E_, "≈ 14 cm"),
    ]),
]


def tableau_mesures():
    out = ['<div class="tab"><table><thead><tr><th>Mesure</th><th>en a</th><th>réel (cm)</th><th>feuille (mm)</th><th class="carnet">carnet (mm)</th></tr></thead><tbody>']
    for groupe, lignes in MESURES:
        out.append(f'<tr class="grp"><td colspan="5">{html.escape(groupe)}</td></tr>')
        for nom, txt, v, note in lignes:
            cm = float(v) * A_REEL
            fe, ca = float(v) * A_FEUILLE * 10, float(v) * A_CARNET * 10
            n = f'<span class="note"> · {html.escape(note)}</span>' if note else ""
            out.append(f'<tr><td>{html.escape(nom)}{n}</td><td class="m">{html.escape(txt)}</td><td>{_vir(cm, 1 if cm < 100 else 0)}</td><td>{_vir(fe)}</td><td class="carnet">{_vir(ca)}</td></tr>')
    out.append('</tbody></table></div>')
    return "".join(out)


RECAP = [
    ("1/2 a, 1/4 a, 1/8 a, 1/16 a", "plier en 2, puis encore en 2…", "les diagonales : leur croisement est le milieu"),
    ("1/3 a", "plier en accordéon (3 parts)", "diagonale + milieu, ou Thalès (3 pas de compas)"),
    ("1/9 a", "plier le tiers en 3", "même construction dans le petit carré de 1/3 a"),
    ("e = 1/21 a", "<b>impossible</b> (7 ne se plie pas)", "<b>Thalès</b> : le tiers en 7"),
    ("1/15 a", "<b>impossible</b> (5 ne se plie pas)", "<b>Thalès</b> : le tiers en 5"),
    ("3 e, 4 e, 5 e, 12 e", "—", "on reporte e au compas, 3, 4, 5 ou 12 fois"),
    ("r = 1/6 a (bouts du pont)", "—", "le compas, centré sur l'axe, ouvert jusqu'au bord"),
    ("12 hauteurs de marche", "—", "Thalès sur la hauteur à monter"),
]


HYPOTHESES = [
    ("a", "Où mesure-t-on le carré a ?",
     "H1 : à l'extérieur des murs. H2 : à l'intérieur (entre les faces intérieures).",
     "Rapport longueur / largeur du plan. Extérieur : 4,05 à 4,13 ≈ 4. Intérieur : (4 − 2e) / (1 − 2e) = 3,90 / 0,90 ≈ 4,3.",
     "H1 : <b>a se prend à l'extérieur</b>, épaisseur des murs comprise."),
    ("t", "Les plis tombent-ils sur la face ou sur l'axe des murs ?",
     "H1 : sur une face du mur. H2 : sur l'axe (le milieu du mur).",
     "Murs du patio mesurés à 1,34 a et 2,65 a ; 4/3 a = 1,333 et 8/3 a = 2,667. Les faces seraient à ± e/2 = ± 0,024.",
     "H2 : <b>les plis tombent sur les axes</b>."),
    ("e", "L'épaisseur du mur : 1/16, 1/18, 1/20, 1/21 ou 1/24 de a ?",
     "H1 : 1/16 a = 25 cm. H2 : 1/18 a ≈ 22 cm. H3 : 1/20 a = 20 cm. H4 : 1/21 a ≈ 19 cm (le tiers en 7). H5 : 1/24 a ≈ 17 cm.",
     "Mesures sur les plans redressés : de <b>0,046 à 0,056 a</b> (moyenne 0,051) ; sur la coupe E : 0,050 à 0,053. "
     "Trop mince pour 1/24 (0,042), trop épais pour 1/16 (0,0625). Entre 1/18, 1/20 et 1/21, la photo ne tranche pas. "
     "Contrôle avec les cotes écrites : avec 1/21, <b>95 = 5 e</b> (95,2), <b>230 = 12 e</b> (228,6), 40 ≈ 2 e (38,1) ; avec 1/20 : 95 = 4,75 e et 230 = 11,5 e (pas entiers) ; avec 1/18 : 95 = 4,3 e.",
     "H4 : <b>e = 1/21 a = 1/7 du tiers</b>. La prof a dit que ce n'est pas 1/20, et les cotes 95 et 230 tombent juste avec 1/21 (5 e et 12 e). La photo seule ne suffit pas à trancher : c'est le choix à défendre."),
    ("e", "La hauteur du garde-corps du pont ?",
     "H1 : 1/4 a = 100 cm. H2 : 5 e = 95 cm. H3 : 3/16 a = 75 cm.",
     "Cote écrite : <b>95</b> sur la coupe longitudinale et sur la coupe E ; mesurée 0,24 a (96 cm). Son sommet est mesuré à 0,67 a du haut de la maison : la ligne des 2/3 a de la trame.",
     "H2 : <b>5 e = 95 cm</b>, épaisseur e. Son sommet tombe sur 14 e = <b>2/3 a</b>. La dalle du pont est e plus bas que le plancher (mesuré : 0,04 a)."),
    ("q", "La largeur de l'escalier compte-t-elle le mur ?",
     "H1 : l'escalier seul fait 1/4 a. H2 : l'escalier + le mur font 1/4 a.",
     "Le bord de l'escalier est mesuré à <b>0,245 a</b> de la face extérieure (0,195 a de la face intérieure). Si l'escalier seul faisait 1/4 a, son bord serait à 1/4 + e = 0,30 a : trop loin de 21 px.",
     "H2 : <b>escalier + mur = 1/4 a</b>, donc l'escalier seul = <b>1/4 a − e ≈ 81 cm</b> (≈ 1/5 a)."),
    ("t", "Combien mesure une marche ?",
     "H1 : 1/16 a (25 cm). H2 : 1/15 a (27 cm). H3 : 1/14 a (29 cm).",
     "12 traits de marche : de 1,65 a à 2,375 a, soit 11 pas de <b>0,0657 a</b> en moyenne (0,0654 sur les 7 premiers). Sur la coupe, 20 px pour 300 px/a : 0,0667. 1/15 = 0,0667, 1/16 = 0,0625.",
     "H2 : <b>11 marches de 1/15 a</b>, volée de 11/15 a, centrée sur le milieu du patio (2,01 a mesuré)."),
    ("t", "Les fenêtres des longs murs ?",
     "H1 : des fentes de 1/16 a. H2 : des fentes de 1/15 a. Recul : H1 : 2 e (0,095). H2 : 1/9 a (0,111).",
     "16 fentes mesurées (4 murs × 4) : 0,062 à 0,075 a, moyenne <b>0,067</b> ; trumeaux 0,063 à 0,066 ; groupes de 0,207 et 0,192 (moyenne 0,200 = 1/5). Le groupe est à 0,093 (gauche) et 0,122 (droite) de l'axe du mur du patio, moyenne <b>0,108</b>.",
     "H2 : <b>2 fentes + 1 trumeau de 1/15 a = 1/5 a</b>, à <b>1/9 a</b> de l'axe du mur du patio, des deux côtés du patio et sur les deux longs murs."),
    ("q", "Les fenêtres du jardin (façade C) ?",
     "H1 : 3 × 1/8 a (fenêtre, écart, fenêtre). H2 : fenêtres de 1/8 a, écart de 1/7 a = 3 e.",
     "Façade C : 0,30–0,425 et 0,575–0,70 ; plan : 0,297–0,412 et 0,565–0,688. Fenêtres 0,12 ≈ 1/8 ; écart 0,15 : plus proche de 1/7 (0,143) que de 1/8 (0,125).",
     "H2 : <b>1/8 a + 1/7 a + 1/8 a</b>, centré."),
    ("e", "La porte d'entrée : cadre de 1/4 a ou de 5 e ?",
     "H1 : le cadre fait 1/4 a (0,250). H2 : le cadre fait 5 e (0,238). Le passage : 4 e ?",
     "Façade B remesurée : les traits du cadre sont à 0,380 et 0,617 a, soit <b>0,237 a</b> de large, centré (0,5 ± 0,119). 5 e = 0,238 ; 1/4 = 0,250 est 3 px trop large. Plan : passage de 0,40 à 0,59 a = 0,19 a = 4 e ; l'encadrement dépasse de 0,07 a = 1,5 e.",
     "H2 : <b>cadre 5 e</b> (montants e/2), <b>passage 4 e ≈ 76 cm</b>, vantail 4 e × 12 e. 1/4 a est l'approximation simple."),
    ("t", "Les fenêtres du jardin : combien de haut ?",
     "H1 : des carrés de 1/8 a. H2 : 1/8 a de large et 1/7 a de haut.",
     "Façade C remesurée avec la hauteur totale de 13/8 a comme étalon : largeur entre les traits 0,126 a ; hauteur <b>0,139 a</b> ; de 0,972 à 1,110 a. (Avant, j'avais oublié que la photo était étirée de 7 % en hauteur.)",
     "H2 : <b>1/8 a × 1/7 a = 3 e</b>, le haut à <b>e/2 au-dessus</b> de la ligne a."),
    ("e", "L'épaisseur du vitrage ?",
     "H1 : verre simple de 1 cm. H2 : double vitrage de 2,4 cm. H3 : un trait, sans épaisseur.",
     "Aucune des feuilles ne donne l'épaisseur du verre : à 1/72, 1 cm ne fait que 0,14 mm, bien moins qu'un trait. Sur le plan original, la paroi vitrée du patio fait 0,033 a (13 cm) avec le cadre.",
     "<b>Convention proposée</b> : verre simple de <b>1 cm</b>, dessiné en <b>un trait fin</b> à 1/72 et avec son épaisseur sur les détails au 1/10. À valider avec la prof."),
    ("e", "La profondeur de la douche et les dalles ?",
     "Douche : 1/5 a ou 4 e ? Acrotère : 1/8 a ou 1/7 a ? Plancher : 1/16 a ou 2 e ?",
     "Douche : 0,19 a (1/5 = 0,20 : trop). Acrotère mesuré 0,140 à 0,143 (1/7 = 0,143, 1/8 = 0,125). Plancher de l'étage : 0,095 à 0,10 = 2 e (0,095). Dalle du toit : 0,063 ≈ 1/16.",
     "<b>douche 1/4 a × 4 e</b> ; <b>acrotère 1/7 a = 3 e</b> ; <b>plancher 2 e</b> ; dalle du sol <b>e</b> ; dalle du toit ≈ <b>1/16 a</b>."),
]


def blocs_ajout():
    import trait
    plis = "".join(
        f'<figure class="pas"><figcaption><span class="n">{n}</span>{html.escape(t)}</figcaption><div class="dessin">{etape(n)[0].svg(t)}</div></figure>'
        for n, t in ETAPES)
    cons = []
    for i, (id_, titre, k, vue, region, z, dessin, au_pli, etapes) in enumerate(CONSTRUCTIONS):
        fig = construire(i)
        li = "".join(f'<li><span class="num" style="background:{COL["g"] if j not in () else COL[k]}">{j+1}</span><span>{t}</span></li>' for j, t in enumerate(etapes))
        zoom = f' <span class="zoomtag">zoom × {z:g}</span>' if z != 1 else ""
        cons.append(f'<article class="cons{" large" if id_ in ("milieu", "escalier_plan") else ""}" style="border-color:{COL[k]}"><h3><span class="n" style="color:{COL[k]}">{i+1}</span>{html.escape(titre)}{zoom}</h3>'
                    f'<div class="dessin zoom">{fig.svg(titre)}</div><ol class="etapes">{li}</ol><p class="aupli">{au_pli}</p></article>')
    recap = "".join(f'<tr><td class="m">{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in RECAP)
    hyps = "".join(
        f'<article class="hyp" style="border-color:{COL[k]}"><h3><span style="color:{COL[k]}">Q{i+1}</span> {html.escape(q)}</h3>'
        f'<dl><dt>Hypothèses</dt><dd>{h}</dd><dt>Test</dt><dd>{test}</dd><dt>Réponse</dt><dd class="rep" style="color:{COL[k]}">{rep}</dd></dl></article>'
        for i, (k, q, h, test, rep) in enumerate(HYPOTHESES))
    d, nom, _ = trame()
    carnet = (f'<div class="echelle"><div><b>{A_REEL} cm</b><span>a, en vrai</span></div><div class="fl">→</div>'
              f'<div><b>{_vir(A_FEUILLE)} cm</b><span>a sur la feuille<br>(≈ 1/{A_REEL/A_FEUILLE:.0f})</span></div><div class="fl">× {_vir(K_CARNET)} →</div>'
              f'<div class="cn"><b>{_vir(A_CARNET, 2)} cm</b><span>a dans le carnet<br>(≈ 1/{A_REEL/A_CARNET:.0f})</span></div></div>')
    return f"""
  <section class="bloc" aria-labelledby="t-carnet">
    <div class="surtitre">Pour le carnet · tout × 1,5</div>
    <h2 id="t-carnet">a = {_vir(A_CARNET, 2)} cm dans le carnet</h2>
    {carnet}
    <p class="intro">Sur la feuille, a mesure {_vir(A_FEUILLE)} cm. Dans le carnet on agrandit par {_vir(K_CARNET)} : <b>a = {_vir(A_CARNET, 2)} cm</b>, donc le plan fait <b>4 a = {_vir(4 * A_CARNET, 1)} cm</b> de long et <b>{_vir(A_CARNET, 2)} cm</b> de large, et la coupe fait <b>{_vir(13 / 8 * A_CARNET, 1)} cm</b> de haut. Il faut une page de plus de 23 cm de large : une page A4 en paysage. Le tableau plus bas donne chaque mesure en millimètres, déjà multipliée.</p>
  </section>

  <section class="bloc" aria-labelledby="t-trame">
    <div class="surtitre">La logique · la trame</div>
    <h2 id="t-trame">Une trame de modules de 1/3 a</h2>
    <p class="intro">Hypothèse de départ : <b>la structure suit les tiers, les ouvertures suivent les quarts</b>. On pose sur le plan une trame de carrés de <b>1/3 a</b> : la largeur fait 3 modules, la longueur <b>12 modules</b>, chaque part (cuisine, patio, séjour) <b>4 modules</b>. Les murs du patio tombent sur les lignes 4 et 8, le pont occupe le rang du milieu, le sas est 1 module. Les hauteurs suivent aussi un module : <b>e = 1/21 a</b> (le tiers en 7).</p>
    <div class="dessin">{d.svg("Le rez-de-chaussée sur la trame de 1/3 a")}</div>
    <p class="intro">Puis on divise le module : <b>le tiers en 7</b> donne le mur <b>e = 1/21 a</b> ; <b>le tiers en 5</b> donne <b>1/15 a</b> (les marches, les fentes) ; <b>le tiers en 3</b> donne <b>1/9 a</b> ; <b>a en 2, 4, 8</b> donne les quarts et les huitièmes. Les trois règles :</p>
    <div class="dessin regles">{regles_svg()}</div>
  </section>

  <section class="bloc" aria-labelledby="t-plis">
    <div class="surtitre">Méthode 1 · le pli · trait mixte = le pli · en gras : le pli de l'étape, en pâle : les plis d'avant</div>
    <h2 id="t-plis">Les plis, dessinés sur le plan</h2>
    <div class="pas-liste">{plis}</div>
    <p class="intro">Le pli ne marche que pour diviser en 2 ou en 3. Pour le mur (1/7 du tiers) et les marches (1/5 du tiers), il faut la construction géométrique.</p>
  </section>

  <section class="bloc" aria-labelledby="t-cons">
    <div class="surtitre">Méthode 2 · la construction géométrique · règle, équerre, compas</div>
    <h2 id="t-cons">Chaque mesure se construit, sur le plan</h2>
    <p class="intro">Les traits gris sont les traits de construction (diagonales, demi-droites, arcs de compas). Les traits mixtes de couleur sont les lignes obtenues. Les ronds numérotés suivent les étapes écrites dessous. Les points sont calculés en fractions exactes : chaque construction tombe pile sur sa fraction.</p>
    <div class="cons-liste">{"".join(cons)}</div>
    <div class="tab recap"><table><thead><tr><th>Mesure</th><th>Au pli</th><th>À la règle et au compas</th></tr></thead><tbody>{recap}</tbody></table></div>
  </section>

  {trait.blocs_web()}

  <section class="bloc" aria-labelledby="t-tab">
    <div class="surtitre">Toutes les mesures · réel, feuille et carnet</div>
    <h2 id="t-tab">Le tableau des mesures</h2>
    <p class="intro">Réel : a = {A_REEL} cm. Feuille : a = {_vir(A_FEUILLE)} cm. Carnet : a = {_vir(A_CARNET, 2)} cm (× {_vir(K_CARNET)}). Les mesures du carnet sont en millimètres : pour les petites (e = {_vir(float(E_) * A_CARNET * 10)} mm), construis-les en grand par Thalès puis reporte-les.</p>
    {tableau_mesures()}
  </section>

  <section class="bloc" aria-labelledby="t-hyp">
    <div class="surtitre">Hypothèses · test · réponse</div>
    <h2 id="t-hyp">Les questions qu'on s'est posées</h2>
    <p class="intro">Pour chaque mesure douteuse, on écrit plusieurs hypothèses, on mesure, et on garde celle qui tombe juste (les mesures sont en fractions de a, relevées sur les dessins redressés).</p>
    <div class="hyps">{hyps}</div>
  </section>
"""


def page():
    cartes = []
    for i, (titre, ou, f) in enumerate(VUES):
        d, nom, notes = f(); svg = d.svg(nom)
        large = i < 4
        li = "".join(f'<li><i style="background:{COL[k]}"></i><span>{t}</span></li>' for k, t in notes)
        cartes.append(f'<section class="vue{" large" if large else ""}" id="v{i+1}"><header><span class="n">{i+1}</span><div><h2>{html.escape(titre)}</h2>'
                      f'<p class="ou">{html.escape(ou)}</p></div></header><div class="dessin">{svg}</div><ul class="notes">{li}</ul></section>')
    leg = "".join(f'<li><i style="background:{COL[k]}"></i>{html.escape(v)}</li>' for k, v in NOMS.items())
    ajout = blocs_ajout()
    return f"""<title>Azuma House · le carré a</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&family=IBM+Plex+Mono:wght@400;500;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<style>
/* Planche d'analyse : légende et chaîne des mesures en tête, puis une carte par vue (dessin coloré + lecture). */
:root {{ --papier: #f1f2ee; --feuille: #fbfbf8; --encre: #1c2120; --encre-2: #5a615d; --ligne: #d4d7d0;
  --c-a: {COL["a"]}; --c-t: {COL["t"]}; --c-q: {COL["q"]}; --c-e: {COL["e"]};
  --f-titre: "Archivo", "Arial Narrow", system-ui, sans-serif; --f-texte: "Source Serif 4", Georgia, serif; --f-tech: "IBM Plex Mono", ui-monospace, monospace; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --papier: #141716; --feuille: #1b1f1d; --encre: #e5e8e3; --encre-2: #a3aaa5; --ligne: #2e3430; color-scheme: dark; }} }}
:root[data-theme="dark"] {{ --papier: #141716; --feuille: #1b1f1d; --encre: #e5e8e3; --encre-2: #a3aaa5; --ligne: #2e3430; color-scheme: dark; }}
* {{ box-sizing: border-box; }}
body {{ background: var(--papier); color: var(--encre); font-family: var(--f-texte); font-size: 1.02rem; line-height: 1.55; margin: 0;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 24px 48px; }}
.planche {{ max-width: 1180px; margin-inline: auto; display: grid; gap: 18px; }}
.surtitre {{ font-family: var(--f-tech); font-size: .74rem; letter-spacing: .07em; text-transform: uppercase; color: var(--encre-2); }}
header.cartouche {{ border: 1.5px solid var(--encre); background: var(--feuille); padding: 20px 22px; display: grid; gap: 10px; }}
h1 {{ font-family: var(--f-titre); font-stretch: 125%; font-weight: 800; font-size: clamp(1.8rem, 5vw, 2.9rem); line-height: 1; margin: 4px 0 0; text-wrap: balance; }}
.cartouche p {{ margin: 0; max-width: 72ch; }}
.legende {{ list-style: none; margin: 4px 0 0; padding: 0; display: flex; flex-wrap: wrap; gap: 8px 18px; font-family: var(--f-tech); font-size: .82rem; font-weight: 700; }}
.legende i, .notes i {{ width: 14px; height: 14px; display: inline-block; vertical-align: -2px; margin-right: 7px; border-radius: 2px; flex: none; }}
.bloc {{ border: 1.5px solid var(--encre); background: var(--feuille); padding: 18px 22px; display: grid; gap: 12px; min-width: 0; }}
.bloc h2, .vue h2 {{ font-family: var(--f-titre); font-stretch: 112%; font-size: 1.3rem; margin: 0; line-height: 1.15; text-wrap: balance; }}
.chaine {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; }}
.etape {{ border-top: 4px solid; padding-top: 8px; min-width: 0; }}
.etape > b {{ font-family: var(--f-tech); font-size: 1.15rem; display: block; }}
.etape span {{ font-size: .95rem; }}
.regle {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; }}
.regle div {{ border-left: 3px solid var(--encre); padding-left: 12px; min-width: 0; }}
.regle div > b:first-child {{ font-family: var(--f-titre); display: block; }}
.vues {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }}
.vue {{ border: 1.5px solid var(--encre); background: var(--feuille); padding: 16px 18px 18px; display: grid; gap: 12px; align-content: start; min-width: 0; }}
.vue.large {{ grid-column: 1 / -1; }}
.vue header {{ display: flex; gap: 12px; align-items: baseline; }}
.vue .n {{ font-family: var(--f-titre); font-stretch: 62%; font-weight: 800; font-size: 2.2rem; line-height: .8; color: var(--c-a); }}
.ou {{ margin: 2px 0 0; font-family: var(--f-tech); font-size: .74rem; color: var(--encre-2); }}
.dessin {{ overflow-x: auto; border: 1px solid var(--ligne); }}
.dessin svg {{ display: block; width: 100%; height: auto; min-width: 520px; }}
.vue:not(.large) .dessin svg {{ min-width: 300px; max-height: 560px; }}
.notes {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 8px; }}
.notes li {{ display: flex; align-items: flex-start; }}
.notes li i {{ margin-top: 5px; }}
.intro {{ margin: 0; max-width: 80ch; }}
.regles svg {{ min-width: 560px; }}
.pas-liste {{ display: grid; gap: 18px; }}
.pas {{ margin: 0; display: grid; gap: 8px; min-width: 0; }}
.pas figcaption {{ font-family: var(--f-titre); font-weight: 700; font-size: 1.05rem; display: flex; gap: 10px; align-items: baseline; }}
.pas .n {{ font-stretch: 62%; font-weight: 800; font-size: 1.9rem; line-height: .8; color: var(--c-a); }}
.dessin.zoom svg {{ max-width: 820px; min-width: 300px; margin-inline: auto; }}
.cons-liste {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; }}
.cons {{ border-top: 4px solid; padding-top: 8px; display: grid; gap: 10px; align-content: start; min-width: 0; }}
.cons.large {{ grid-column: 1 / -1; }}
.cons h3 {{ font-family: var(--f-titre); font-size: 1.08rem; margin: 0; line-height: 1.2; display: flex; gap: 10px; align-items: baseline; flex-wrap: wrap; }}
.cons h3 .n {{ font-stretch: 62%; font-weight: 800; font-size: 1.9rem; line-height: .8; }}
.zoomtag {{ font-family: var(--f-tech); font-size: .7rem; font-weight: 500; color: var(--encre-2); border: 1px solid var(--ligne); padding: 0 6px; border-radius: 9px; }}
.cons .dessin svg {{ min-width: 0; }}
.etapes {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; font-size: .95rem; }}
.etapes li {{ display: flex; gap: 9px; align-items: flex-start; }}
.num {{ flex: none; width: 21px; height: 21px; border-radius: 50%; color: #fff; font-family: var(--f-tech); font-size: .78rem; font-weight: 700; display: inline-grid; place-items: center; margin-top: 2px; }}
.aupli {{ margin: 0; font-family: var(--f-tech); font-size: .8rem; color: var(--encre-2); border-top: 1px dashed var(--ligne); padding-top: 6px; }}
.tab {{ overflow-x: auto; }}
.tab table {{ border-collapse: collapse; width: 100%; font-size: .93rem; }}
.tab th {{ text-align: left; font-family: var(--f-tech); font-size: .7rem; letter-spacing: .06em; text-transform: uppercase; color: var(--encre-2); border-bottom: 1.5px solid var(--encre); padding: 6px 10px 6px 0; white-space: nowrap; }}
.tab td {{ border-bottom: 1px solid var(--ligne); padding: 5px 10px 5px 0; vertical-align: top; }}
.tab td:nth-child(n+3), .tab th:nth-child(n+3) {{ text-align: right; white-space: nowrap; }}
.tab td.m {{ font-family: var(--f-tech); font-size: .85rem; white-space: nowrap; }}
.tab tr.grp td {{ font-family: var(--f-titre); font-weight: 700; padding-top: 14px; border-bottom: 1.5px solid var(--encre); }}
.tab .note {{ color: var(--encre-2); font-size: .85rem; }}
.tab .carnet {{ font-weight: 700; background: color-mix(in srgb, var(--c-a) 9%, transparent); padding-right: 8px; padding-left: 8px; }}
.tab.recap {{ margin-top: 6px; }}
.tab.traits td, .tab.traits th {{ text-align: left !important; white-space: normal !important; }}
.tab.traits td:first-child {{ width: 50mm; }}
.tab.recap td:nth-child(n+3), .tab.recap th:nth-child(n+3) {{ text-align: left; white-space: normal; }}
.tab.recap td:nth-child(2), .tab.recap td:nth-child(3) {{ white-space: normal; }}
.echelle {{ display: flex; flex-wrap: wrap; gap: 8px 14px; align-items: center; }}
.echelle > div {{ display: grid; gap: 2px; text-align: center; }}
.echelle b {{ font-family: var(--f-tech); font-size: 1.5rem; }}
.echelle span {{ font-size: .82rem; color: var(--encre-2); }}
.echelle .fl {{ font-family: var(--f-tech); font-size: 1.1rem; color: var(--encre-2); }}
.echelle .cn {{ border: 2px solid var(--c-a); border-radius: 6px; padding: 6px 14px; }}
.echelle .cn b {{ color: var(--c-a); }}
.hyps {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }}
.hyp {{ border-left: 4px solid; padding: 2px 0 2px 12px; min-width: 0; }}
.hyp h3 {{ font-family: var(--f-titre); font-size: 1.05rem; margin: 0 0 6px; line-height: 1.2; }}
.hyp h3 span {{ font-family: var(--f-tech); margin-right: 4px; }}
.hyp dl {{ margin: 0; display: grid; gap: 2px; font-size: .93rem; }}
.hyp dt {{ font-family: var(--f-tech); font-size: .7rem; letter-spacing: .06em; text-transform: uppercase; color: var(--encre-2); margin-top: 4px; }}
.hyp dd {{ margin: 0; }}
.hyp dd.rep {{ font-weight: 600; }}
footer {{ font-family: var(--f-tech); font-size: .74rem; color: var(--encre-2); }}
@media (max-width: 820px) {{ .vues, .cons-liste {{ grid-template-columns: 1fr; }} .cons.large {{ grid-column: auto; }} .chaine {{ grid-template-columns: 1fr 1fr; }} }}
</style>
<main class="planche">
  <header class="cartouche">
    <div class="surtitre">Atelier · Séance 5 · représentation conventionnelle · Tadao Ando, Azuma House (Osaka, 1976)</div>
    <h1>Azuma House · le carré a</h1>
    <p>Toutes les mesures des 8 vues partent d'une seule référence, le carré de côté <b>a</b>. On la plie en tiers (la trame), puis en quarts (les ouvertures). Le tiers divisé en 7 donne le mur, divisé en 5 donne les marches : cela se <b>construit</b> à la règle et au compas (Thalès). Chaque mesure se trouve donc <b>de deux façons : le pli et la construction géométrique</b>. Une couleur par mesure :</p>
    <ul class="legende">{leg}</ul>
  </header>

  <section class="bloc" aria-labelledby="t-chaine">
    <div class="surtitre">La chaîne des mesures</div>
    <h2 id="t-chaine">Du carré jusqu'au mur, en 4 étapes</h2>
    <div class="chaine">
      <div class="etape" style="border-color:var(--c-a)"><b style="color:var(--c-a)">a</b><span>Le côté du carré. Le plan en contient <b>4</b>. a = 400 cm.</span></div>
      <div class="etape" style="border-color:var(--c-t)"><b style="color:var(--c-t)">1/3 a</b><span>On plie le grand rectangle en 3 : chaque part vaut <b>a + 1/3 a</b>. ≈ 133 cm. Le tiers en 5 : <b>1/15 a</b> (la marche) ; en 3 : <b>1/9 a</b>.</span></div>
      <div class="etape" style="border-color:var(--c-q)"><b style="color:var(--c-q)">1/4 a</b><span>On plie a en 4 (deux fois en deux) : porte, escalier + mur. 100 cm. En 8 : 1/8 a, 50 cm.</span></div>
      <div class="etape" style="border-color:var(--c-e)"><b style="color:var(--c-e)">e = 1/21 a</b><span>On divise le tiers en 7 (Thalès) : c'est <b>l'épaisseur du mur</b>. ≈ 19 cm. (Pas 1/20 : voir la question Q3.)</span></div>
    </div>
  </section>

  <section class="bloc" aria-labelledby="t-regle">
    <div class="surtitre">Pour ne pas se tromper</div>
    <h2 id="t-regle">Où l'on mesure, et l'échelle</h2>
    <div class="regle">
      <div><b>a se prend à l'extérieur</b>De la face extérieure d'un mur de façade à la face extérieure de l'autre : l'épaisseur des deux murs est comprise dans a.</div>
      <div><b>Les plis tombent sur les axes</b>Les tiers et les quarts se comptent depuis la face extérieure, et chaque pli tombe sur <b>l'axe</b> (le milieu) d'un mur intérieur ou d'une cloison.</div>
      <div><b>Les combinaisons</b>Une mesure peut en combiner plusieurs : 4/3 a = a + 1/3 a, 1/2 a = 2 × 1/4 a, 1/8 a = ½ × 1/4 a, 5/8 a = 1/4 + 1/4 + 1/8 a, 1/7 a = 3 e, 4/7 a = 12 e, 1/5 a = 3 × 1/15 a, 5 e = 95 cm, escalier = 1/4 a − e.</div>
      <div><b>L'échelle des vues</b>Les cotes écrites donnent a : 650 cm = a + 5/8 a, et 250 cm = 5/8 a, donc <b>a = 400 cm</b>. Sur ta feuille, a mesure <b>3,7 cm</b> à la règle : l'échelle est d'environ <b>1/108</b>. Dans le carnet, tout est multiplié par 1,5 : <b>a = 5,55 cm</b>, échelle d'environ <b>1/72</b>.</div>
    </div>
  </section>

{ajout}
  <div class="vues">{"".join(cartes)}</div>
  <footer>Positions relevées sur les photos des deux feuilles (chaque dessin redressé, puis mesuré en fractions de a). Sur les photos, le plan fait un peu plus de 4 carrés (≈ 4,1) : on retient 4, l'écart est plus petit que la précision d'un pliage. Les mesures marquées ≈ sont arrondies à la fraction la plus proche.</footer>
</main>"""


if __name__ == "__main__":
    import importlib
    open(os.path.join(ICI, "index.html"), "w", encoding="utf-8").write(importlib.import_module("build").page())
    print("index.html écrit")

"""Azuma House (Tadao Ando) : analyse des proportions de chaque vue à partir du carré a.

Toutes les positions sont en unités de a (a = largeur extérieure de la maison, face extérieure à face extérieure),
relevées sur les photos des deux feuilles (plans redressés, puis mesurés).
Quatre couleurs, une par mesure de la chaîne : a (bleu) -> 1/3 a (rouge) -> 1/4 a (vert) -> e = 1/21 a (violet).
Trame : modules de 1/3 a ; le tiers plié en 7 donne e, plié en 5 donne 1/15 a (marches, fentes).
Lancer : python3 build.py  ->  index.html
"""
import html, os

ICI = os.path.dirname(os.path.abspath(__file__))
S = 200                       # px par a dans les dessins
E = 1 / 21                    # épaisseur des murs : 1/21 a = le tiers plié en 7 (≈ 19 cm)
F = 1 / 15                    # la marche et la fente : le tiers plié en 5 (≈ 27 cm)
M0, M1 = 2 - 11 * F / 2, 2 + 11 * F / 2      # l'escalier : 11 marches de 1/15 a, centrées sur le patio
G1, G2 = 4 / 3 - 2 * E - 3 * F, 8 / 3 + 2 * E  # groupes de fentes (2 fentes + 1 trumeau = 1/5 a), à 2 e des murs du patio
XD = 4 - 4 * E                # la douche et les lanterneaux : 4 e depuis la face extérieure
COL = {"a": "#1f5fd1", "t": "#d9342b", "q": "#14965a", "e": "#8a3cc4", "g": "#6b6e70"}
GRIS, TRAIT = "#3b3d3f", "#6b6e70"
IMPRESSION = False            # True : marges serrées et cotes courtes (planches A4 pour les calques, calques.py)
MARGES_A4 = {(4, 1): (0.42, 0.55, 0.5, 0.55), (4, 13 / 8): (0.55, 0.3, 0.45, 0.62), (1, 13 / 8): (0.6, 0.6, 0.45, 0.6)}
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

    def _t(self, t): return COURT.get(t, t) if IMPRESSION else t

    def X(self, x): return (x + self.mg) * S
    def Y(self, y): return (y + self.mh) * S

    # --- le bâtiment (gris) ---
    def mur(self, x0, y0, x1, y1):
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
            if vitre: self.ligne(x0, (y0 + y1) / 2, x1, (y0 + y1) / 2, 0.9)
        else:
            self.ligne(x0, y0, x0, y1, 0.9); self.ligne(x1, y0, x1, y1, 0.9)
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

    def svg(self, titre, couche=None, mm=None):
        """couche None : la page web (tout) ; "base" : le bâtiment seul ; ensemble de couleurs : un calque
        (le bâtiment en fantôme pâle, puis les formes et les cotes de ces couleurs). mm : mm par px pour l'impression."""
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
    """les fenêtres des deux longs murs : 2 fentes de 1/15 a + 1 trumeau de 1/15 a = 1/5 a, à 2 e de l'axe du mur du patio"""
    for g in (G1, G2):
        for x in (g, g + 2 * F):
            for y0, y1 in ((0, E), (1 - E, 1)):
                d.fenetre(x, y0, x + F, y1)
                d.forme(x, y0, x + F, y1, "t", op=0.75, w=0)
    d.forme(G1 + 3 * F, 1 - E, 4 / 3, 1, "e", op=0.55, w=0); d.forme(8 / 3, 1 - E, G2, 1, "e", op=0.55, w=0)
    if cotes:
        d.cote_h(G1, G1 + 3 * F, 1.12, "3 × 1/15 a", "t", ext=1); d.cote_h(G2, G2 + 3 * F, 1.12, "3 × 1/15 a", "t", ext=1)
        d.cote_h(G1 + 3 * F, 4 / 3, 1.3, "2 e", "e", ext=1, cote="d"); d.cote_h(8 / 3, G2, 1.3, "2 e", "e", ext=1, cote="g")


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
        ("t", "Les fenêtres des deux longs murs sont des <b>fentes de 1/15 a</b> (le tiers plié en 5, ≈ 27 cm) : 2 fentes et 1 trumeau de 1/15 a, soit un groupe de <b>1/5 a</b>. Chaque groupe est posé à <b>2 e</b> de l'axe d'un mur du patio, côté cuisine et côté séjour."),
        ("q", "Au bout gauche (côté jardin), deux fenêtres de <b>1/8 a</b>, séparées de <b>1/7 a = 3 e</b> et centrées : ce sont celles de la façade C."),
        ("t", "L'escalier a <b>11 marches de 1/15 a</b> (≈ 27 cm), et la volée est centrée sur le milieu du patio (x = 2 a)."),
        ("q", "Sa largeur : <b>escalier + mur = 1/4 a</b> depuis la face extérieure. L'escalier seul fait donc <b>1/4 a − e ≈ 81 cm</b>."),
        ("e", "Les murs ont une épaisseur <b>e = 1/21 a ≈ 19 cm</b> : c'est le tiers plié en 7 (1/3 × 1/7 = 1/21)."),
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
        ("e", "Ses deux garde-corps ont chacun l'épaisseur d'un mur, <b>e</b>. Le passage entre eux fait donc <b>1/3 a − 2e</b>."),
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
    d.mur(0, 0.14, 4 / 3 + E / 2, 0.21); d.mur(8 / 3 - E / 2, 0.14, 4, 0.21)   # toitures
    d.mur(4 / 3 - E / 2, 0.10, 4 / 3 + E / 2, 0.21); d.mur(8 / 3 - E / 2, 0.10, 8 / 3 + E / 2, 0.21)
    d.mur(0, 0.87, 4, 0.945)                                           # plancher + pont
    for x in (4 / 3, 8 / 3): d.vitrage(x, 0.21, x, 0.87); d.vitrage(x, 0.945, x, H - 0.05)
    d.mur(0.5 - E / 2, 0.945, 0.5 + E / 2, H - 0.05)                 # cloison salle de bain
    d.mur(11 / 3 - E / 2, 0.945, 11 / 3 + E / 2, H - 0.05)           # cloison du sas
    d.mur(XD - E / 2, 0.21, XD + E / 2, 0.87)                        # mur de la douche
    d.rect(1.36, 0.63, 2.36, 0.87, 1.2)                               # garde-corps du pont
    x, y = M0, H - 0.05; pts = [(x, y)]                              # escalier : 11 marches de 1/15 a, 12 hauteurs
    h = (H - 0.05 - 0.87) / 12
    for i in range(12):
        y -= h; pts.append((x, y))
        if i < 11: x += F; pts.append((x, y))
    d.fond.append('<polyline points="' + " ".join(f"{d.X(p):.1f},{d.Y(q):.1f}" for p, q in pts) + f'" fill="none" stroke="{TRAIT}" stroke-width="1.3"/>')
    d.mur(0, H - 0.05, 4, H); d.sol(H)
    for x, t in ((0.66, "chambre"), (3.2, "chambre"), (0.25, "bain"), (0.92, "cuisine"), (2.0, "patio"), (3.15, "séjour")):
        d.texte(x, 0.55 if t == "chambre" else (1.38 if t != "patio" else 0.4), t, taille=11)
    for i in range(4): d.cote_h(i, i + 1, -0.14, "a", "a", ext=0)
    for i in range(3): d.cote_h(i * 4 / 3, (i + 1) * 4 / 3, -0.36, "a + 1/3 a", "t", ext=0)
    for x in (4 / 3, 8 / 3): d.axe(x, -0.04, x, H + 0.04, "t")
    d.zone(0, 0, 4 / 3, 1, "a", op=0.07, dash="8 4")
    d.cote_v(0, 1, -0.16, "a", "a", ext=0); d.cote_v(1, H, -0.16, "5/8 a", "q", ext=0)
    d.cote_v(0, 0.14, -0.38, "≈ 1/8 a", "q", ext=0)
    d.cote_v(0.63, 0.87, 2.5, "95 = 5 e", "e", cote="d")
    d.cote_h(0, 0.5, H + 0.25, "1/2 a", "q", ext=H)
    d.cote_h(11 / 3, 4, H + 0.25, "1/3 a", "t", ext=H)
    d.cote_h(XD, 4, H + 0.47, "4 e", "e", ext=H, cote="g")
    d.cote_h(M0, M1, H + 0.25, "11 marches de 1/15 a", "t", ext=H - 0.05)
    d.cote_h(0, E, H + 0.47, "e", "e", ext=H, cote="d")
    d.forme(0, 0, 4 / 3, 1, "a", op=0.16, w=2.4)                                          # le carré a
    for i in range(3): d.forme(i * 4 / 3, 0.02, (i + 1) * 4 / 3, H - 0.02, "t", op=0, w=2.6, dash="10 5")
    d.forme(11 / 3, 0.945, 4 - E, H - 0.05, "t", op=0.40)                                 # sas 1/3 a
    d.forme(0, 1, 4, H, "q", op=0.10, w=2.2)                                              # 5/8 a
    d.forme(0, 0, 4, 0.14, "q", op=0.30, w=0)                                             # acrotère 1/8 a
    d.forme(E, 0.945, 0.5, H - 0.05, "q", op=0.30)                                        # salle de bain 1/2 a
    d.forme(1.36, 0.63, 2.36, 0.87, "e", op=0.25)                                         # garde-corps 5 e
    d.forme(0, 0, E, H, "e", op=0.65, w=0); d.forme(4 - E, 0, 4, H, "e", op=0.65, w=0)
    d.forme(XD, 0.21, 4, 0.87, "e", op=0, w=2.2, dash="5 3")                               # douche 4 e
    for i in range(12): d.trait_c(M0 + i * F, H - 0.05 - i * h - h, M0 + i * F, H - 0.05, "t", w=1.2, dash="3 2")
    return d, "Coupe longitudinale", [
        ("t", "En long, on retrouve <b>les trois parts de a + 1/3 a</b> : le patio du milieu n'a pas de toit, seul le pont le traverse."),
        ("a", "En hauteur, la coupe fait <b>a + 5/8 a</b> (du haut des murs jusqu'au sol). Le carré a (bleu) monte du haut du mur jusqu'au plancher de l'étage, environ."),
        ("q", "Les petites mesures sont des quarts : <b>1/2 a</b> pour la salle de bain et un acrotère de <b>≈ 1/8 a</b> (la moitié d'un quart)."),
        ("e", "Le garde-corps du pont fait <b>95 cm = 5 e</b> (5 × 19 = 95, juste ; avec 1/20 a on aurait 100)."),
        ("t", "L'escalier : <b>11 marches de 1/15 a</b>, de 1,63 a à 2,37 a, centrées sur le milieu du patio. Il monte en 12 hauteurs jusqu'au plancher de l'étage."),
        ("t", "Le sas d'entrée fait <b>1/3 a</b> de long, comme sur le plan."),
        ("e", "La douche fait <b>4 e</b>, et les murs <b>e</b>. Les dalles sont un peu plus épaisses que les murs, environ <b>1,5 e ≈ 28 cm</b>."),
    ]


def coupe_c():
    H = 13 / 8
    d = Dessin(1, H, mg=1.0, md=1.0, mh=0.45, mb=0.55)
    d.mur(0, 0, E, H); d.mur(1 - E, 0, 1, H)
    d.mur(0, 0.14, 1, 0.207); d.mur(0, 0.87, 1, 0.947); d.mur(0, H - 0.05, 1, H); d.sol(H)
    d.rect(0.37, 0.02, 0.62, 0.14, 1.1)                                # lanterneau en toiture
    d.texte(0.5, 0.6, "chambre", taille=11); d.texte(0.5, 1.3, "cuisine", taille=11)
    d.cote_h(0, 1, -0.16, "a", "a", ext=0)
    d.zone(0, 0, 1, 1, "a", op=0.08, dash="8 4")
    d.cote_v(0, 1, -0.18, "a", "a", ext=0); d.cote_v(1, H, -0.18, "5/8 a", "q", ext=0)
    d.cote_v(0.947, H - 0.05, 1.18, "250 = 5/8 a", "q", ext=1, cote="d")
    d.cote_v(0.207, 0.87, 1.18, "≈ 2/3 a", "t", ext=1, cote="d")
    d.cote_v(0, 0.14, 1.18, "≈ 1/8 a", "q", ext=1, cote="d")
    d.cote_h(0, E, H + 0.3, "e = 1/21 a", "e", ext=H, cote="d")
    d.cote_v(0, H, -0.42, "650 = a + 5/8 a", "a", ext=0)
    d.forme(0, 0, 1, 1, "a", op=0.16, w=2.4)
    d.forme(0, 0.207, 1, 0.87, "t", op=0, w=2.4, dash="10 5")                               # chambre 2/3 a
    d.trait_c(0, 0.207 + 0.33, 1, 0.207 + 0.33, "t", w=1.4, dash="4 4")
    d.forme(0, 1, 1, H, "q", op=0.15, w=2.2)                                              # 5/8 a
    d.forme(0, 0, 1, 0.14, "q", op=0.30, w=0)                                             # acrotère
    d.forme(0, 0, E, H, "e", op=0.65, w=0); d.forme(1 - E, 0, 1, H, "e", op=0.65, w=0)
    return d, "Coupe C", [
        ("a", "La coupe est large de <b>a</b> et haute de <b>a + 5/8 a</b>. Avec la cote de 650 cm, on trouve <b>a = 400 cm</b>."),
        ("q", "Le rez-de-chaussée fait <b>250 cm = 5/8 a</b> sous plafond. C'est la deuxième cote qui donne a = 400 cm."),
        ("t", "La chambre de l'étage fait environ <b>2/3 a</b> de haut (2 tiers)."),
        ("q", "L'acrotère, au-dessus de la toiture, fait environ <b>1/8 a</b>."),
        ("e", "Les murs font <b>e = 1/21 a ≈ 19 cm</b> (400 / 21 = 19,05)."),
    ]


def facade_b():
    H = 13 / 8
    d = Dessin(1, H, mg=1.0, md=1.0, mh=0.45, mb=0.55)
    d.rect(0, 0, 1, H, 1.8, c=GRIS); d.sol(H)
    d.rect(0.375, 1.0, 0.625, H - 0.035, 1.4, c=GRIS); d.ligne(0.375, H - 0.035, 0.625, H - 0.035, 1.2)
    d.cote_h(0, 1, -0.16, "a", "a", ext=0)
    d.zone(0, 0, 1, 1, "a", op=0.10, dash="8 4")
    d.etiquette(0.5, 0.52, "1 carré a × a", "a", 13)
    d.cote_v(0, 1, -0.18, "a", "a", ext=0); d.cote_v(1, H, -0.18, "5/8 a", "q", ext=0)
    d.cote_h(0.375, 0.625, H + 0.3, "porte 1/4 a", "q", ext=H)
    d.cote_v(1.0, H, 1.18, "porte 5/8 a", "q", ext=0.625, cote="d")
    d.forme(0, 0, 1, 1, "a", op=0.16, w=2.4)
    d.forme(0.375, 1.0, 0.625, H - 0.035, "q", op=0.40)                                   # porte 1/4 × 5/8
    for x in (0.25, 0.5, 0.75): d.trait_c(x, 1.0, x, H, "q", w=1.2, dash="4 4")          # les quarts de a
    return d, "Façade B, sur la rue", [
        ("a", "La façade sur la rue est un rectangle de <b>a</b> par <b>a + 5/8 a</b>. Au-dessus de la porte, le mur est <b>exactement un carré a × a</b>."),
        ("q", "La seule ouverture, la porte, fait <b>1/4 a</b> de large (son cadre), au milieu (de 3/8 a à 5/8 a). Son haut tombe pile au bas du carré, donc elle fait <b>5/8 a</b> de haut."),
        ("e", "Sur le plan, le passage dans ce cadre fait <b>4 e ≈ 76 cm</b>."),
    ]


def coupe_e():
    H = 13 / 8
    d = Dessin(1, H, mg=1.0, md=1.0, mh=0.45, mb=0.55)
    d.mur(0, 0, E, H); d.mur(1 - E, 0, 1, H)
    d.ligne(E, 0.12, 1 - E, 0.12, 1.2); d.ligne(E, 0.22, 1 - E, 0.22, 1.1, dash="6 4")      # rives des toitures, au fond
    d.mur(1 / 3, 0.70, 1 / 3 + E, 0.95); d.mur(2 / 3 - E, 0.70, 2 / 3, 0.95)              # garde-corps du pont
    d.mur(1 / 3, 0.92, 2 / 3, 1.0)
    d.fond.append(f'<polygon points="{d.X(1/3):.1f},{d.Y(1.0):.1f} {d.X(2/3):.1f},{d.Y(1.0):.1f} {d.X(0.61):.1f},{d.Y(1.06):.1f} {d.X(0.39):.1f},{d.Y(1.06):.1f}" fill="{GRIS}"/>')
    d.rect(0.42, 1.07, 0.6, H - 0.05, 1.3)                             # porte sous le pont
    d.rect(0.40, 0.27, 0.48, 0.70, 1.1); d.rect(0.52, 0.27, 0.60, 0.70, 1.1)
    d.rect(E, 0.90, 0.25, H - 0.05, 1.2)                               # escalier
    for i in range(1, 11): d.ligne(E, 0.90 + i * 0.0675, 0.25, 0.90 + i * 0.0675, 0.9)
    d.mur(0, H - 0.05, 1, H); d.sol(H)
    d.cote_h(0, 1, -0.16, "a", "a", ext=0)
    d.cote_h(1 / 3, 2 / 3, -0.34, "pont 1/3 a", "t", ext=0)
    d.cote_v(0.70, 0.95, 1.18, "95 = 5 e", "e", ext=2 / 3, cote="d")
    d.cote_v(0.12, 0.22, 1.18, "40 = 2 e", "e", ext=1, cote="d")
    d.cote_h(E, 0.25, H + 0.28, "escalier 1/4 a − e", "e", ext=H, cote="d")
    d.cote_h(0, 0.25, H + 0.48, "avec le mur : 1/4 a", "q", ext=H, cote="d")
    d.cote_h(1 / 3, 1 / 3 + E, 0.6, "e", "e", cote="g"); d.cote_h(2 / 3 - E, 2 / 3, 0.6, "e", "e", cote="d")
    d.cote_v(1.07, H - 0.05, -0.18, "porte 230 = 12 e", "e", ext=0.42)
    d.forme(1 / 3, 0.70, 2 / 3, 1.06, "t", op=0.30)                                       # pont 1/3 a
    for x in (1 / 3, 2 / 3): d.trait_c(x, 0, x, H, "t", w=1.4, dash="4 4")
    d.forme(1 / 3, 0.70, 2 / 3, 0.95, "e", op=0, w=2.2, dash="6 3")                        # garde-corps 5 e
    d.forme(1 / 3, 0.70, 1 / 3 + E, 0.95, "e", op=0.7, w=0); d.forme(2 / 3 - E, 0.70, 2 / 3, 0.95, "e", op=0.7, w=0)
    d.forme(E, 0.90, 0.25, H - 0.05, "e", op=0.25)                                        # escalier 1/4 a − e
    d.forme(0, 0.90, 0.25, H - 0.05, "q", op=0, w=2.2, dash="6 3")                         # + le mur = 1/4 a
    d.forme(0.42, 1.07, 0.6, H - 0.05, "e", op=0.2)                                       # porte 12 e
    d.forme(E, 0.12, 1 - E, 0.22, "e", op=0.25, w=0)                                      # 40 = 2 e
    d.forme(0, 0, E, H, "e", op=0.65, w=0); d.forme(1 - E, 0, 1, H, "e", op=0.65, w=0)
    return d, "Coupe E, à travers le patio", [
        ("t", "Coupé à travers le patio, le pont fait <b>1/3 a</b> de large, pile au milieu (de 1/3 a à 2/3 a), comme sur le plan de l'étage."),
        ("e", "Ses garde-corps ont l'épaisseur <b>e</b> d'un mur."),
        ("e", "Leur hauteur est de <b>95 cm = 5 e</b>."),
        ("q", "L'escalier, contre le mur : <b>escalier + mur = 1/4 a</b>. Sans le mur, l'escalier fait <b>1/4 a − e ≈ 81 cm</b>."),
        ("e", "La cote de 40 cm en haut vaut <b>2 e</b> (38 cm)."),
        ("e", "La porte sous le pont fait 230 cm = <b>12 e</b> (12 × 19 = 228,6), soit <b>4/7 a</b> (4 septièmes de a)."),
    ]


def facade_c():
    H = 13 / 8
    d = Dessin(1, H, mg=1.0, md=1.0, mh=0.45, mb=0.55)
    d.rect(0, 0, 1, H, 1.8, c=GRIS); d.sol(H)
    W1, W2 = 0.5 - 1 / 14 - 1 / 8, 0.5 + 1 / 14                      # 2 fenêtres de 1/8 a, écart 1/7 a = 3 e, centrées
    for x0 in (W1, W2):
        d.rect(x0, 1.03, x0 + 0.125, 1.155, 1.4, c=GRIS); d.rect(x0 + 0.012, 1.042, x0 + 0.113, 1.143, 1)
    d.cote_h(0, 1, -0.16, "a", "a", ext=0)
    d.zone(0, 0, 1, 1, "a", op=0.10, dash="8 4")
    d.etiquette(0.5, 0.52, "1 carré a × a", "a", 13)
    d.cote_v(0, 1, -0.18, "a", "a", ext=0); d.cote_v(1, H, -0.18, "5/8 a", "q", ext=0)
    d.cote_h(W1, W1 + 0.125, H + 0.25, "1/8", "q", ext=1.155, cote="g"); d.cote_h(W2, W2 + 0.125, H + 0.25, "1/8", "q", ext=1.155, cote="d")
    d.cote_h(W1 + 0.125, W2, H + 0.45, "1/7 a = 3 e", "e", ext=1.155, cote="d")
    d.cote_v(1.03, 1.155, 1.18, "≈ 1/8 a", "q", ext=0.69, cote="d")
    d.forme(0, 0, 1, 1, "a", op=0.16, w=2.4)
    for x0 in (W1, W2): d.forme(x0, 1.03, x0 + 0.125, 1.155, "q", op=0.45)
    d.forme(W1 + 0.125, 1.03, W2, 1.155, "e", op=0.3, w=0)
    for i in range(1, 3): d.trait_c(W1 + 0.125 + i * E, 1.03, W1 + 0.125 + i * E, 1.155, "e", w=1.2, dash="2 2")
    return d, "Façade C, sur le jardin", [
        ("a", "Même rectangle que la façade B : <b>a</b> par <b>a + 5/8 a</b>, avec <b>un carré a × a</b> au-dessus des ouvertures."),
        ("q", "Les deux petites fenêtres sont des carrés d'environ <b>1/8 a = moitié de 1/4 a</b>. Leur haut est juste sous le carré a."),
        ("e", "Elles sont séparées de <b>1/7 a = 3 e</b> (≈ 57 cm) et centrées. On avait d'abord supposé 1/8 a : la mesure (0,15 a) est plus proche de 1/7 (0,143) que de 1/8 (0,125)."),
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

NOMS = {"a": "a · le carré", "t": "1/3 a · le tiers (et 1/15 a)", "q": "1/4 a · le quart (et 1/8 a)", "e": "e = 1/21 a · le mur (1/7 du tiers)"}


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


def _regle_biais(d, xa, ya, xb, yb, n, k, y_proj=None):
    """la règle posée en biais : 0 sur un bord, n sur l'autre ; on descend chaque graduation (Thalès)"""
    ep = 14
    d.dessus.append((k, f'<polygon points="{d.X(xa):.1f},{d.Y(ya)-ep:.1f} {d.X(xb):.1f},{d.Y(yb)-ep:.1f} {d.X(xb):.1f},{d.Y(yb)+3:.1f} {d.X(xa):.1f},{d.Y(ya)+3:.1f}" '
                        f'fill="#f4e7b5" stroke="#8a7a3a" stroke-width="1"/>'))
    for i in range(n + 1):
        x, y = xa + (xb - xa) * i / n, ya + (yb - ya) * i / n
        X, Y = d.X(x), d.Y(y)
        d.dessus.append((k, f'<line x1="{X:.1f}" y1="{Y-ep:.1f}" x2="{X:.1f}" y2="{Y+3:.1f}" stroke="#5a4a1a" stroke-width="1.3"/>'
                            f'<text x="{X + (5 if i == 0 else 0):.1f}" y="{Y-ep-4:.1f}" fill="#5a4a1a" font-size="11" text-anchor="middle">{i}</text>'))
        if y_proj is not None and 0 < i < n:
            d.dessus.append((k, f'<line x1="{X:.1f}" y1="{Y+3:.1f}" x2="{X:.1f}" y2="{d.Y(y_proj):.1f}" stroke="{COL[k]}" stroke-width="1.6" stroke-dasharray="5 4"/>'))


def _base():
    d, _, _ = plan_rdc()
    d.par, d.dessus, d.cal = [], [], []
    d.fond = ['<g opacity="0.5">'] + d.fond + ['</g>']
    return d


class Zoom:
    """un morceau du plan agrandi (le plan est redessiné à l'échelle z, puis recadré)"""
    mg, n = 0, 0

    def __init__(self, W, H, corps, ox, oy):
        self.W, self.H, self.corps, self.ox, self.oy = W, H, corps, ox, oy
        Zoom.n += 1; self.id = f"zc{Zoom.n}"           # un clipPath par zoom (les id sont partagés dans la page)

    def svg(self, titre, couche=None, mm=None):
        return (f'<svg viewBox="0 0 {self.W:.0f} {self.H:.0f}" role="img" aria-label="{html.escape(titre)}" font-family="IBM Plex Mono, ui-monospace, monospace">'
                f'<rect width="100%" height="100%" fill="#fbfbf8"/><defs><clipPath id="{self.id}"><rect width="{self.W:.0f}" height="{self.H:.0f}"/></clipPath></defs>'
                f'<g clip-path="url(#{self.id})"><g transform="translate({-self.ox:.1f} {-self.oy:.1f})">{self.corps}</g></g>'
                f'<rect x="0.75" y="0.75" width="{self.W-1.5:.0f}" height="{self.H-1.5:.0f}" fill="none" stroke="#1c2120" stroke-width="1.5"/></svg>')


def _zoomer(dessine, region, z):
    """redessine le plan à l'échelle z (× S), ajoute les tracés de dessine(d), puis recadre sur region (x0, x1, y0, y1)"""
    global S
    s0 = S
    S = s0 * z
    try:
        d = _base()
        dessine(d)
        x0, x1, y0, y1 = region
        ox, oy, W, H = d.X(x0), d.Y(y0), (x1 - x0) * S, (y1 - y0) * S
        corps = "".join(x for _, x in d.par) + "".join(d.fond) + "".join(x for _, x in d.dessus)
    finally:
        S = s0
    return Zoom(W, H, corps, ox, oy)


def _trace_mur(d):
    """pli 6 : le module 1/3 a (contre le mur du patio) plié en 7 avec la règle en biais"""
    _pli(d, 1, -0.1, 1, 0.45, "a", actif=False); _pli(d, 4 / 3, -0.1, 4 / 3, 0.45, "t", actif=False)
    _pli(d, 0.9, 1 / 3, 1.6, 1 / 3, "t", actif=False)
    for k in range(1, 7):
        _pli(d, 1 + k / 21, 0, 1 + k / 21, 1 / 3, "e", w=1.8)
        _pli(d, 1, k / 21, 4 / 3, k / 21, "e", w=1.0)
    _bloc(d, 1, 0, 4 / 3, E, "e", 0.4)                                 # 1 part sur 7 = le mur de façade
    _bloc(d, 4 / 3 - E / 2, E, 4 / 3 + E / 2, 1 / 3, "e", 0.35)         # le mur du patio : e, centré sur le pli 3
    _regle_biais(d, 1, 0.285, 4 / 3, 0.175, 7, "e")
    d.cote_v(0, E, 0.97, "e", "e", cote="g")
    d.cote_h(4 / 3 - 2 * E, 4 / 3, 0.11, "2 e", "e", ext=E, cote="g")
    d.cote_h(4 / 3 - E / 2, 4 / 3 + E / 2, 0.3, "e", "e", cote="d")
    d.cote_h(1, 4 / 3, 0.36, "1/3 a = 7 e", "t", ext=1 / 3)
    _tag(d, 1 + 1 / 6, -0.035, "pli 6 : le tiers en 7", "e")


def _trace_marches(d):
    """pli 7 : le tiers en 5 = 1/15 a, reporté depuis le recul de 2 e (fenêtres) et depuis le milieu du patio (marches)"""
    _plis(d, 6)
    _pli(d, 2, -0.2, 2, 0.5, "a", w=2.4)                               # le pli 1 = le milieu du patio
    r0, r1 = 4 / 3 - 2 * E - 5 * F, 4 / 3 - 2 * E
    _regle_biais(d, r0, 0.36, r1, 0.25, 5, "t", y_proj=0)
    for x in (G1, G1 + 2 * F): _bloc(d, x, 0, x + F, E, "t", 0.75)
    for i in range(12):
        d.dessus.append(("t", f'<line x1="{d.X(M0+i*F):.1f}" y1="{d.Y(-0.03):.1f}" x2="{d.X(M0+i*F):.1f}" y2="{d.Y(0.25):.1f}" stroke="{COL["t"]}" stroke-width="2.4"/>'))
    for i in range(11): d.etiquette(M0 + (i + 0.5) * F, 0.2, str(i + 1), "t", 11)
    d.cote_h(M0, M1, -0.1, "11 marches × 1/15 a, centrées sur le pli 1", "t", ext=0)
    d.cote_h(G1, G1 + 3 * F, -0.1, "3 × 1/15", "t", ext=0)
    d.cote_h(G1 + 3 * F, 4 / 3, 0.1, "2 e", "e", ext=E, cote="g")
    _tag(d, (r0 + r1) / 2, 0.43, "pli 7 : le tiers en 5", "t")


ETAPES = [
    (1, "Pli 1 · le plan plié en 2"),
    (2, "Pli 2 · encore en 2 : 4 carrés a"),
    (3, "Pli 3 · en 3 : les plis tombent sur les murs du patio"),
    (4, "Pli 4 · la largeur en 3 : la trame de 1/3 a"),
    (5, "Pli 5 · a en 2, 4, 8 : salle de bain, escalier, porte"),
    (6, "Pli 6 · zoom × 5 : le tiers en 7 = le mur e"),
    (7, "Pli 7 · zoom × 2,5 : le tiers en 5 = 1/15 a, fenêtres et marches"),
]


def etape(n):
    titre = dict(ETAPES)[n]
    if n == 6: return _zoomer(_trace_mur, (0.92, 1.52, -0.065, 0.385), 5), titre, []
    if n == 7: return _zoomer(_trace_marches, (0.85, 2.45, -0.2, 0.5), 2.5), titre, []
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


HYPOTHESES = [
    ("a", "Où mesure-t-on le carré a ?",
     "H1 : à l'extérieur des murs. H2 : à l'intérieur (entre les faces intérieures).",
     "Rapport longueur / largeur du plan. Extérieur : 4,05 à 4,13 ≈ 4. Intérieur : (4 − 2e) / (1 − 2e) = 3,90 / 0,90 ≈ 4,3.",
     "H1 : <b>a se prend à l'extérieur</b>, épaisseur des murs comprise."),
    ("t", "Les plis tombent-ils sur la face ou sur l'axe des murs ?",
     "H1 : sur une face du mur. H2 : sur l'axe (le milieu du mur).",
     "Murs du patio mesurés à 1,34 a et 2,65 a ; 4/3 a = 1,333 et 8/3 a = 2,667. Les faces seraient à ± e/2 = ± 0,024.",
     "H2 : <b>les plis tombent sur les axes</b>."),
    ("e", "L'épaisseur du mur : 1/20, 1/21 ou 1/24 de a ?",
     "H1 : 1/20 a = 20 cm (le quart en 5). H2 : 1/21 a ≈ 19 cm (le tiers en 7). H3 : 1/24 a ≈ 17 cm (le tiers en 8).",
     "Mesures : 0,045 / 0,049 / 0,050 / 0,049 a (moyenne 0,048). Contrôle par les cotes écrites : avec 1/20, garde-corps 95 = 4,75 e et porte 230 = 11,5 e (pas entiers). Avec 1/21 : <b>95 = 5 e</b>, <b>230 = 12 e</b>, 40 ≈ 2 e. Avec 1/24 : 95 = 5,7 e.",
     "H2 : <b>e = 1/21 a = 1/7 du tiers</b>. Ce n'est pas 1/20 : 1/20 ne donne pas des nombres entiers."),
    ("q", "La largeur de l'escalier compte-t-elle le mur ?",
     "H1 : l'escalier seul fait 1/4 a. H2 : l'escalier + le mur font 1/4 a.",
     "Le bord de l'escalier est mesuré à 0,25 a de la <b>face extérieure</b> (sur les plans et sur la coupe E), pas de la face intérieure (ce serait 0,30).",
     "H2 : <b>escalier + mur = 1/4 a</b>, donc l'escalier seul = <b>1/4 a − e ≈ 81 cm</b>."),
    ("t", "Combien mesure une marche ?",
     "H1 : 1/16 a (25 cm). H2 : 1/15 a (27 cm). H3 : 1/14 a (29 cm).",
     "12 traits de marche de 1,645 a à 2,378 a : 11 marches de 0,0667 a. 1/15 = 0,0667.",
     "H2 : <b>11 marches de 1/15 a</b> (le tiers en 5), volée de 11/15 a centrée sur le milieu du patio."),
    ("t", "Les fenêtres des longs murs ?",
     "H1 : des fentes de 1/16 a (un demi-huitième). H2 : des fentes de 1/15 a.",
     "Fentes mesurées de 1,03 à 1,10 et de 1,165 à 1,235 a (0,067 et 0,070), trumeau 0,065. Le groupe finit à 0,095 a de l'axe du mur du patio = 2 e.",
     "H2 : <b>2 fentes + 1 trumeau de 1/15 a = 1/5 a</b>, à <b>2 e</b> du mur du patio, des deux côtés du patio et sur les deux longs murs."),
    ("q", "Les fenêtres du jardin (façade C) ?",
     "H1 : 3 × 1/8 a (fenêtre, écart, fenêtre). H2 : fenêtres de 1/8 a, écart de 1/7 a = 3 e.",
     "Façade C : 0,30–0,425 et 0,575–0,70 ; plan : 0,297–0,412 et 0,565–0,688. Fenêtres 0,12 ≈ 1/8 ; écart 0,15 : plus proche de 1/7 (0,143) que de 1/8 (0,125).",
     "H2 : <b>1/8 a + 1/7 a + 1/8 a</b>, centré."),
    ("q", "La porte d'entrée : 1/4 a ou moins ?",
     "H1 : l'ouverture fait 1/4 a. H2 : le cadre fait 1/4 a, le passage est plus petit.",
     "Façade B : cadre de 3/8 a à 5/8 a = 1/4 a. Plan : passage de 0,40 à 0,59 a = 0,19 a = 4 e.",
     "H2 : <b>cadre 1/4 a × 5/8 a</b>, <b>passage 4 e ≈ 76 cm</b>."),
    ("e", "La douche et le garde-corps du pont ?",
     "Douche : 1/5 a ou 4 e de profondeur ? Garde-corps : 1/4 a ou 5 e de haut ?",
     "Douche : 0,19 a de la face extérieure à l'axe de son mur = 4 e (1/5 = 0,20 est un peu trop). Garde-corps : cote écrite 95 cm (1/4 a = 100).",
     "<b>douche 1/4 a × 4 e</b> ; <b>garde-corps 5 e = 95 cm</b>, épais de e, sur un pont de 1/3 a. Les dalles ≈ 1,5 e."),
]


def blocs_ajout():
    plis = "".join(
        f'<figure class="pas"><figcaption><span class="n">{n}</span>{html.escape(t)}</figcaption><div class="dessin{" zoom" if n in (6, 7) else ""}">{etape(n)[0].svg(t)}</div></figure>'
        for n, t in ETAPES)
    hyps = "".join(
        f'<article class="hyp" style="border-color:{COL[k]}"><h3><span style="color:{COL[k]}">Q{i+1}</span> {html.escape(q)}</h3>'
        f'<dl><dt>Hypothèses</dt><dd>{h}</dd><dt>Test</dt><dd>{test}</dd><dt>Réponse</dt><dd class="rep" style="color:{COL[k]}">{rep}</dd></dl></article>'
        for i, (k, q, h, test, rep) in enumerate(HYPOTHESES))
    d, nom, _ = trame()
    return f"""
  <section class="bloc" aria-labelledby="t-trame">
    <div class="surtitre">La logique · la trame</div>
    <h2 id="t-trame">Une trame de modules de 1/3 a</h2>
    <p class="intro">Hypothèse de départ : <b>la structure suit les tiers, les ouvertures suivent les quarts</b>. On pose sur le plan une trame de carrés de <b>1/3 a</b> : la largeur fait 3 modules, la longueur <b>12 modules</b>, chaque part (cuisine, patio, séjour) <b>4 modules</b>. Les murs du patio tombent sur les lignes 4 et 8, le pont occupe le rang du milieu, le sas est 1 module.</p>
    <div class="dessin">{d.svg("Le rez-de-chaussée sur la trame de 1/3 a")}</div>
    <p class="intro">Puis on redivise le module. <b>Le tiers en 7</b> donne le mur <b>e = 1/21 a</b> ; <b>le tiers en 5</b> donne <b>1/15 a</b> (les marches, les fentes) ; <b>a en 2, 4, 8</b> donne les quarts et les huitièmes (portes, douche, fenêtres du jardin). Les trois règles :</p>
    <div class="dessin regles">{regles_svg()}</div>
  </section>

  <section class="bloc" aria-labelledby="t-plis">
    <div class="surtitre">Étape par étape · trait mixte = le pli · en gras : le pli de l'étape, en pâle : les plis d'avant</div>
    <h2 id="t-plis">Les plis, dessinés sur le plan</h2>
    <div class="pas-liste">{plis}</div>
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
.hyps {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }}
.hyp {{ border-left: 4px solid; padding: 2px 0 2px 12px; min-width: 0; }}
.hyp h3 {{ font-family: var(--f-titre); font-size: 1.05rem; margin: 0 0 6px; line-height: 1.2; }}
.hyp h3 span {{ font-family: var(--f-tech); margin-right: 4px; }}
.hyp dl {{ margin: 0; display: grid; gap: 2px; font-size: .93rem; }}
.hyp dt {{ font-family: var(--f-tech); font-size: .7rem; letter-spacing: .06em; text-transform: uppercase; color: var(--encre-2); margin-top: 4px; }}
.hyp dd {{ margin: 0; }}
.hyp dd.rep {{ font-weight: 600; }}
footer {{ font-family: var(--f-tech); font-size: .74rem; color: var(--encre-2); }}
@media (max-width: 820px) {{ .vues {{ grid-template-columns: 1fr; }} .chaine {{ grid-template-columns: 1fr 1fr; }} }}
</style>
<main class="planche">
  <header class="cartouche">
    <div class="surtitre">Atelier · Séance 5 · représentation conventionnelle · Tadao Ando, Azuma House (Osaka, 1976)</div>
    <h1>Azuma House · le carré a</h1>
    <p>Toutes les mesures des 8 vues partent d'une seule référence, le carré de côté <b>a</b>. On la plie en tiers (la trame), puis en quarts (les ouvertures), puis le tiers en 7 (le mur) et en 5 (les marches). Une couleur par mesure :</p>
    <ul class="legende">{leg}</ul>
  </header>

  <section class="bloc" aria-labelledby="t-chaine">
    <div class="surtitre">La chaîne des mesures</div>
    <h2 id="t-chaine">Du carré jusqu'au mur, en 4 pliages</h2>
    <div class="chaine">
      <div class="etape" style="border-color:var(--c-a)"><b style="color:var(--c-a)">a</b><span>Le côté du carré. Le plan en contient <b>4</b>. a = 400 cm.</span></div>
      <div class="etape" style="border-color:var(--c-t)"><b style="color:var(--c-t)">1/3 a</b><span>On plie le grand rectangle en 3 : chaque part vaut <b>a + 1/3 a</b>. ≈ 133 cm. Plié en 5 : <b>1/15 a</b>, la marche.</span></div>
      <div class="etape" style="border-color:var(--c-q)"><b style="color:var(--c-q)">1/4 a</b><span>On plie a en 4 (deux fois en deux) : porte, douche, escalier + mur. 100 cm. En 8 : 1/8 a, 50 cm.</span></div>
      <div class="etape" style="border-color:var(--c-e)"><b style="color:var(--c-e)">e = 1/21 a</b><span>On plie le tiers en 7 : c'est <b>l'épaisseur du mur</b>. ≈ 19 cm. (Pas 1/20 : voir la question Q3.)</span></div>
    </div>
  </section>

  <section class="bloc" aria-labelledby="t-regle">
    <div class="surtitre">Pour ne pas se tromper</div>
    <h2 id="t-regle">Où l'on mesure, et l'échelle</h2>
    <div class="regle">
      <div><b>a se prend à l'extérieur</b>De la face extérieure d'un mur de façade à la face extérieure de l'autre : l'épaisseur des deux murs est comprise dans a.</div>
      <div><b>Les plis tombent sur les axes</b>Les tiers et les quarts se comptent depuis la face extérieure, et chaque pli tombe sur <b>l'axe</b> (le milieu) d'un mur intérieur ou d'une cloison.</div>
      <div><b>Les combinaisons</b>Une mesure peut en combiner plusieurs : 4/3 a = a + 1/3 a, 1/2 a = 2 × 1/4 a, 1/8 a = ½ × 1/4 a, 5/8 a = 1/4 + 1/4 + 1/8 a, 1/7 a = 3 e, 4/7 a = 12 e, 1/5 a = 3 × 1/15 a, escalier = 1/4 a − e.</div>
      <div><b>L'échelle des vues</b>Les cotes écrites donnent a : 650 cm = a + 5/8 a, et 250 cm = 5/8 a, donc <b>a = 400 cm</b>. Mesure a à la règle sur ta feuille : l'échelle vaut a (en cm) / 400. Les photos donnent a ≈ 4 cm, soit <b>1/100</b> pour les 8 vues (les deux barres de 5 m le confirment).</div>
    </div>
  </section>

{ajout}
  <div class="vues">{"".join(cartes)}</div>
  <footer>Positions relevées sur les photos des deux feuilles (chaque dessin redressé, puis mesuré en fractions de a). Sur les photos, le plan fait un peu plus de 4 carrés (≈ 4,1) : on retient 4, l'écart est plus petit que la précision d'un pliage. Les mesures marquées ≈ sont arrondies à la fraction la plus proche.</footer>
</main>"""


if __name__ == "__main__":
    open(os.path.join(ICI, "index.html"), "w", encoding="utf-8").write(page())
    print("index.html écrit")

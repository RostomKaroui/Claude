"""Azuma House (Tadao Ando) : analyse des proportions de chaque vue à partir du carré a.

Toutes les positions sont en unités de a (a = largeur extérieure de la maison, face extérieure à face extérieure),
relevées sur les photos des deux feuilles (plans redressés, puis mesurés).
Quatre couleurs, une par mesure de la chaîne : a (bleu) -> 1/3 a (rouge) -> 1/4 a (vert) -> e = 1/20 a (violet).
Lancer : python3 build.py  ->  index.html
"""
import html, os

ICI = os.path.dirname(os.path.abspath(__file__))
S = 200                       # px par a dans les dessins
E = 0.05                      # épaisseur des murs : 1/20 a
COL = {"a": "#1f5fd1", "t": "#d9342b", "q": "#14965a", "e": "#8a3cc4", "g": "#6b6e70"}
GRIS, TRAIT = "#3b3d3f", "#6b6e70"
IMPRESSION = False            # True : marges serrées et cotes courtes (planches A4 pour les calques, calques.py)
MARGES_A4 = {(4, 1): (0.42, 0.42, 0.5, 0.55), (4, 13 / 8): (0.55, 0.3, 0.45, 0.62), (1, 13 / 8): (0.6, 0.6, 0.45, 0.6)}
COURT = {"650 = a + 5/8 a": "650", "250 = 5/8 a": "5/8 a", "porte 1/4 a": "1/4 a", "porte 5/8 a": "5/8 a", "40 = 2 e": "2 e",
         "95 ≈ 1/4 a": "≈ 1/4 a", "escalier 1/5 a = 4 e": "1/5 a = 4 e", "1/2 a = 2 × 1/4 a": "1/2 a", "e = 1/20 a": "e",
         "1/5 a = 4 e": "1/5 a", "3/8 a, centrés": "3/8 a", "porte 230": "230", "≈ 1/8 a": "1/8 a", "≈ 2/3 a": "2/3 a",
         "pont 1/3 a": "1/3 a", "sas : 1/3 a × 1/3 a": "1/3 a", "pont = 1/3 a": "1/3 a", "1/3 a − 2e": "1/3 a − 2e",
         "r = 1/6 a": "r = 1/6 a", "1 carré a × a": "a × a"}


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


# ================================================================ les vues
def plan_rdc():
    d = Dessin(4, 1, md=1.0)
    d.anneau(0, 0, 4, 1)
    for x in (4 / 3, 8 / 3):                                         # murs du patio : pleins en haut, vitrés en bas
        d.mur(x - E / 2, E, x + E / 2, 0.42); d.vitrage(x, 0.42, x, 1 - E)
    d.mur(0.5 - E / 2, E, 0.5 + E / 2, 0.72)                         # salle de bain
    d.rect(1.62, E, 8 / 3 - E / 2, 0.24)                             # escalier
    for i in range(1, 14): d.ligne(1.62 + i * 0.07, E, 1.62 + i * 0.07, 0.24, 0.9)
    for y in (1 / 3, 2 / 3): d.ligne(4 / 3 + E / 2, y, 8 / 3 - E / 2, y, 1, dash="5 4")     # passerelle au-dessus
    d.mur(11 / 3 - E / 2, 1 / 3 - E / 2, 11 / 3 + E / 2, 2 / 3 + E / 2)                      # sas d'entrée
    d.mur(11 / 3, 1 / 3 - E / 2, 4 - E, 1 / 3 + E / 2); d.mur(11 / 3, 2 / 3 - E / 2, 4 - E, 2 / 3 + E / 2)
    d.fond.append(f'<rect x="{d.X(4-E):.1f}" y="{d.Y(0.375):.1f}" width="{E*S:.1f}" height="{0.25*S:.1f}" fill="#fbfbf8"/>')  # porte d'entrée
    for x, t in ((0.25, "bain"), (0.92, "cuisine"), (2.0, "patio"), (3.15, "séjour"), (3.83, "sas")):
        d.texte(x, 0.88 if t != "sas" else 0.52, t, taille=11)
    carres_et_tiers(d)
    d.zone(11 / 3, 1 / 3, 4, 2 / 3, "t", op=0.16)
    d.etiquette(3.5, 0.2, "sas : 1/3 a × 1/3 a", "t", 11.5)
    d.cote_h(0, 0.5, 1.2, "1/2 a = 2 × 1/4 a", "q", ext=1)
    d.cote_v(0.375, 0.625, 4.2, "porte 1/4 a", "q", ext=4, cote="d")
    d.cote_h(0, E, 1.42, "e = 1/20 a", "e", ext=1, cote="d")
    d.forme(11 / 3, 1 / 3, 4, 2 / 3, "t", op=0.45)                                        # sas 1/3 × 1/3
    d.forme(E, E, 0.5, 0.72, "q", op=0.30)                                                 # salle de bain 1/2 a
    d.trait_c(0.25, E, 0.25, 0.72, "q", w=1.6, dash="4 4")                                 # = 2 quarts
    d.forme(4 - E, 0.375, 4, 0.625, "q", op=0.8, w=0)                                      # porte 1/4 a
    for x in (4 / 3, 8 / 3): d.forme(x - E / 2, E, x + E / 2, 0.42, "e", op=0.6, w=0)     # murs du patio, e
    d.forme(0.5 - E / 2, E, 0.5 + E / 2, 0.72, "e", op=0.6, w=0)
    return d, "Plan du rez-de-chaussée", [
        ("a", "Le grand rectangle fait <b>4 carrés</b> de côté <b>a</b>. On mesure <b>a d'une face extérieure à l'autre</b> (épaisseur des murs de façade comprise), en largeur comme en longueur."),
        ("t", "Plié en trois, il donne <b>3 parts égales de 4/3 a, soit 1 carré + 1/3 de carré</b> : cuisine et salle de bain, patio, séjour. Les plis à 4/3 a et 8/3 a (mesurés depuis la face extérieure) tombent <b>sur l'axe des murs du patio</b>."),
        ("t", "La largeur se plie aussi en trois : les pointillés de la passerelle (au-dessus du patio) sont à <b>1/3 a et 2/3 a</b>. Le sas d'entrée est un petit carré de <b>1/3 a × 1/3 a</b> (aux axes de ses murs)."),
        ("q", "La salle de bain fait <b>1/2 a = 2 × 1/4 a</b> (de la face extérieure à l'axe de sa cloison). La porte d'entrée fait <b>1/4 a</b>, au milieu du mur (de 3/8 a à 5/8 a)."),
        ("e", "Les murs ont une épaisseur <b>e = 1/20 a</b> (pliage : a en 4, puis le quart en 5)."),
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
    d.rect(1.64, E + 0.01, 2.36, 0.25)                                # escalier
    for i in range(1, 12): d.ligne(1.64 + i * 0.06, E + 0.01, 1.64 + i * 0.06, 0.25, 0.9)
    d.mur(3.8 - E / 2, 0.375 - E / 2, 3.8 + E / 2, 0.625 + E / 2)   # douche
    d.mur(3.8, 0.375 - E / 2, 4 - E, 0.375 + E / 2); d.mur(3.8, 0.625 - E / 2, 4 - E, 0.625 + E / 2)
    for x, t in ((0.66, "chambre"), (2.0, "pont"), (3.2, "chambre")): d.texte(x, 0.52 if t == "pont" else 0.9, t, taille=11)
    d.texte(2.0, 0.17, "vide", taille=11); d.texte(2.0, 0.86, "vide", taille=11)
    carres_et_tiers(d)
    d.zone(4 / 3, 1 / 3, 8 / 3, 2 / 3, "t", op=0.14)
    d.etiquette(2.0, 0.44, "pont = 1/3 a", "t", 11.5)
    d.cote_v(1 / 3, 1 / 3 + E, 2.75, "e", "e", cote="d"); d.cote_v(2 / 3 - E, 2 / 3, 2.75, "e", "e", cote="d")
    d.cote_v(1 / 3 + E, 2 / 3 - E, 2.62, "1/3 a − 2e", "e", cote="g")
    for x, s in ((4 / 3, -1),):
        d.axe(x, 0.5, x - 1 / 6, 0.5, "t", w=1.4, dash="3 3"); d.etiquette(x - 0.3, 0.52, "r = 1/6 a", "t", 10.5)
    d.cote_v(0.375, 0.625, 4.2, "1/4 a", "q", ext=4, cote="d")
    d.cote_h(3.8, 4, 1.2, "1/5 a = 4 e", "e", ext=1)
    d.cote_h(0, E, 1.42, "e = 1/20 a", "e", ext=1, cote="d")
    d.forme(4 / 3, 1 / 3, 8 / 3, 2 / 3, "t", op=0.40)                                     # pont 1/3 a
    for x, sw in ((4 / 3, 0), (8 / 3, 1)):
        r = 1 / 6
        d.cal.append(("t", f'<path d="M{d.X(x):.1f} {d.Y(0.5-r):.1f} A {r*S:.1f} {r*S:.1f} 0 0 {sw} {d.X(x):.1f} {d.Y(0.5+r):.1f} Z" fill="{COL["t"]}" fill-opacity="0.25" stroke="{COL["t"]}" stroke-width="2.2"/>'))
    d.forme(4 / 3, 1 / 3, 8 / 3, 1 / 3 + E, "e", op=0.7, w=0); d.forme(4 / 3, 2 / 3 - E, 8 / 3, 2 / 3, "e", op=0.7, w=0)
    d.forme(3.8, 0.375, 4, 0.625, "q", op=0.35)                                           # douche 1/4 a
    d.forme(3.8, 0.33, 4, 0.67, "e", op=0, w=2.2, dash="5 3")                              # profondeur 1/5 a = 4 e
    for i in range(1, 4): d.trait_c(4 - i * E, 0.33, 4 - i * E, 0.67, "e", w=1.2, dash="2 2")
    return d, "Plan de l'étage", [
        ("a", "Même rectangle : <b>4 carrés a</b>, mesurés aux faces extérieures."),
        ("t", "Mêmes trois parts de <b>a + 1/3 a</b> : chambre, vide du patio avec le pont, chambre. Les façades vitrées sur le patio sont sur les plis à 4/3 a et 8/3 a."),
        ("t", "Le pont occupe <b>le tiers du milieu de la largeur</b> (de 1/3 a à 2/3 a, faces extérieures de ses garde-corps). Ses bouts arrondis sont des demi-cercles de rayon <b>1/6 a = moitié de 1/3 a</b>."),
        ("e", "Ses deux garde-corps ont chacun l'épaisseur d'un mur, <b>e</b>. Le passage entre eux fait donc <b>1/3 a − 2e</b>."),
        ("q", "La douche (à droite) fait <b>1/4 a</b> de large, au milieu (axes de ses murs à 3/8 a et 5/8 a)."),
        ("e", "Elle fait <b>1/5 a = 4 e</b> de profondeur (de la face extérieure à l'axe de son mur)."),
    ]


def plan_toit():
    d = Dessin(4, 1, md=1.0)
    d.rect(0, 0, 4, 1, 1.4); d.rect(E, E, 4 - E, 1 - E, 1.2)          # acrotère : deux traits
    for x in (4 / 3, 8 / 3):
        d.ligne(x - E / 2, E, x - E / 2, 1 - E, 1.2); d.ligne(x + E / 2, E, x + E / 2, 1 - E, 1.2)
    d.rect(4 / 3 + E / 2, 1 / 3, 8 / 3 - E / 2, 2 / 3, 1.1); d.ligne(4 / 3 + E / 2, 1 / 3 + E, 8 / 3 - E / 2, 1 / 3 + E, 1); d.ligne(4 / 3 + E / 2, 2 / 3 - E, 8 / 3 - E / 2, 2 / 3 - E, 1)
    d.rect(1.64, E + 0.01, 2.36, 0.25, 1); [d.ligne(1.64 + i * 0.06, E + 0.01, 1.64 + i * 0.06, 0.25, 0.9) for i in range(1, 12)]
    for y0, y1 in ((E, 1 / 3), (0.375, 0.625), (2 / 3, 1 - E)):     # lanterneaux à droite
        d.rect(3.8, y0 + 0.01, 4 - E, y1 - 0.01, 1.2)
    d.ligne(3.8, 0.385, 4 - E, 0.615, 1); d.ligne(3.8, 0.615, 4 - E, 0.385, 1)
    d.rect(E, 0.37, 0.21, 0.63, 1.2); d.rect(E, 0.42, 0.17, 0.58, 1)  # lanterneau gauche
    d.texte(0.66, 0.9, "toiture", taille=11); d.texte(2.0, 0.52, "pont (vu d'en haut)", taille=11); d.texte(3.2, 0.9, "toiture", taille=11)
    carres_et_tiers(d)
    d.zone(3.8, E, 4 - E, 1 / 3, "t", op=0.12); d.zone(3.8, 2 / 3, 4 - E, 1 - E, "t", op=0.12)
    d.zone(3.8, 0.375, 4 - E, 0.625, "q", op=0.16)
    d.cote_v(0.375, 0.625, 4.2, "1/4 a", "q", ext=4, cote="d")
    d.cote_h(0, E, 1.2, "e = 1/20 a", "e", ext=1, cote="d")
    d.cote_h(3.8, 4, 1.2, "1/5 a", "e", ext=1)
    d.forme(3.8, E, 4 - E, 1 / 3, "t", op=0.35); d.forme(3.8, 2 / 3, 4 - E, 1 - E, "t", op=0.35)
    d.forme(3.8, 0.375, 4 - E, 0.625, "q", op=0.40)
    d.forme(3.8, 0, 4, 1, "e", op=0, w=2.2, dash="5 3")
    return d, "Plan de toiture", [
        ("a", "Toujours <b>4 carrés a</b>. Le double trait du bord est l'acrotère (le muret du toit) : son épaisseur est <b>e</b>."),
        ("t", "Les trois parts de <b>a + 1/3 a</b> : toiture, patio ouvert (on voit le pont et l'escalier d'en haut), toiture."),
        ("t", "La colonne de lanterneaux à droite reprend <b>les tiers de la largeur</b> : deux cases de 1/3 a (rouge) de part et d'autre."),
        ("q", "La case du milieu, au-dessus de la douche, fait <b>1/4 a</b> (de 3/8 a à 5/8 a)."),
        ("e", "La colonne fait <b>1/5 a = 4 e</b> de profondeur, comme la douche en dessous."),
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
    d.mur(3.8 - E / 2, 0.21, 3.8 + E / 2, 0.87)                      # mur de la douche
    d.rect(1.36, 0.63, 2.36, 0.87, 1.2)                               # garde-corps du pont
    pts = []                                                          # escalier
    x, y = 1.6, H - 0.05
    for i in range(10):
        pts += [(x, y), (x, y - 0.0675)]; y -= 0.0675; x += 0.068
        pts.append((x, y))
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
    d.cote_v(0.63, 0.87, 2.5, "95 ≈ 1/4 a", "q", cote="d")
    d.cote_h(0, 0.5, H + 0.25, "1/2 a", "q", ext=H)
    d.cote_h(11 / 3, 4, H + 0.25, "1/3 a", "t", ext=H)
    d.cote_h(3.8, 4, H + 0.47, "1/5 a = 4 e", "e", ext=H)
    d.cote_h(0, E, H + 0.47, "e", "e", ext=H, cote="d")
    d.forme(0, 0, 4 / 3, 1, "a", op=0.16, w=2.4)                                          # le carré a
    for i in range(3): d.forme(i * 4 / 3, 0.02, (i + 1) * 4 / 3, H - 0.02, "t", op=0, w=2.6, dash="10 5")
    d.forme(11 / 3, 0.945, 4 - E, H - 0.05, "t", op=0.40)                                 # sas 1/3 a
    d.forme(0, 1, 4, H, "q", op=0.10, w=2.2)                                              # 5/8 a
    d.forme(0, 0, 4, 0.14, "q", op=0.30, w=0)                                             # acrotère 1/8 a
    d.forme(E, 0.945, 0.5, H - 0.05, "q", op=0.30)                                        # salle de bain 1/2 a
    d.forme(1.36, 0.63, 2.36, 0.87, "q", op=0.35)                                         # garde-corps 1/4 a
    d.forme(0, 0, E, H, "e", op=0.65, w=0); d.forme(4 - E, 0, 4, H, "e", op=0.65, w=0)
    d.forme(3.8, 0.21, 4, 0.87, "e", op=0, w=2.2, dash="5 3")                              # douche 1/5 a = 4 e
    return d, "Coupe longitudinale", [
        ("t", "En long, on retrouve <b>les trois parts de a + 1/3 a</b> : le patio du milieu n'a pas de toit, seul le pont le traverse."),
        ("a", "En hauteur, la coupe fait <b>a + 5/8 a</b> (du haut des murs jusqu'au sol). Le carré a (bleu) monte du haut du mur jusqu'au plancher de l'étage, environ."),
        ("q", "Les petites mesures sont des quarts : <b>1/2 a</b> pour la salle de bain, un garde-corps de <b>95 cm ≈ 1/4 a</b> sur le pont, et un acrotère de <b>≈ 1/8 a</b> (la moitié d'un quart)."),
        ("t", "Le sas d'entrée fait <b>1/3 a</b> de long, comme sur le plan."),
        ("e", "La douche fait <b>1/5 a = 4 e</b>, et les murs <b>e</b>. Les dalles sont dessinées un peu plus épaisses que les murs, environ 1,5 e."),
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
    d.cote_h(0, E, H + 0.3, "e = 1/20 a", "e", ext=H, cote="d")
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
        ("e", "Les murs font <b>e = 1/20 a = 20 cm</b>."),
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
        ("q", "La seule ouverture, la porte, fait <b>1/4 a</b> de large, au milieu (de 3/8 a à 5/8 a). Son haut tombe pile au bas du carré, donc elle fait <b>5/8 a</b> de haut."),
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
    d.cote_v(0.70, 0.95, 1.18, "95 ≈ 1/4 a", "q", ext=2 / 3, cote="d")
    d.cote_v(0.12, 0.22, 1.18, "40 = 2 e", "e", ext=1, cote="d")
    d.cote_h(E, 0.25, H + 0.3, "escalier 1/5 a = 4 e", "e", ext=H)
    d.cote_h(1 / 3, 1 / 3 + E, 0.6, "e", "e", cote="g"); d.cote_h(2 / 3 - E, 2 / 3, 0.6, "e", "e", cote="d")
    d.cote_v(1.07, H - 0.05, -0.18, "porte 230", "g", ext=0.42)
    d.forme(1 / 3, 0.70, 2 / 3, 1.06, "t", op=0.30)                                       # pont 1/3 a
    for x in (1 / 3, 2 / 3): d.trait_c(x, 0, x, H, "t", w=1.4, dash="4 4")
    d.forme(1 / 3, 0.70, 2 / 3, 0.95, "q", op=0, w=2.2, dash="6 3")                        # garde-corps 1/4 a
    d.forme(1 / 3, 0.70, 1 / 3 + E, 0.95, "e", op=0.7, w=0); d.forme(2 / 3 - E, 0.70, 2 / 3, 0.95, "e", op=0.7, w=0)
    d.forme(E, 0.90, 0.25, H - 0.05, "e", op=0.25)                                        # escalier 1/5 a = 4 e
    d.forme(E, 0.12, 1 - E, 0.22, "e", op=0.25, w=0)                                      # 40 = 2 e
    d.forme(0, 0, E, H, "e", op=0.65, w=0); d.forme(1 - E, 0, 1, H, "e", op=0.65, w=0)
    return d, "Coupe E, à travers le patio", [
        ("t", "Coupé à travers le patio, le pont fait <b>1/3 a</b> de large, pile au milieu (de 1/3 a à 2/3 a), comme sur le plan de l'étage."),
        ("e", "Ses garde-corps ont l'épaisseur <b>e</b> d'un mur."),
        ("q", "Leur hauteur est de <b>95 cm ≈ 1/4 a</b>."),
        ("e", "L'escalier, contre le mur, fait <b>1/5 a = 4 e</b> de large. La cote de 40 cm en haut vaut <b>1/10 a = 2 e</b>."),
        ("g", "La porte sous le pont fait 230 cm de haut, soit environ 0,58 a : ce n'est pas une fraction simple, on la donne en cm."),
    ]


def facade_c():
    H = 13 / 8
    d = Dessin(1, H, mg=1.0, md=1.0, mh=0.45, mb=0.55)
    d.rect(0, 0, 1, H, 1.8, c=GRIS); d.sol(H)
    for x0 in (0.3125, 0.5625):
        d.rect(x0, 1.03, x0 + 0.125, 1.155, 1.4, c=GRIS); d.rect(x0 + 0.012, 1.042, x0 + 0.113, 1.143, 1)
    d.cote_h(0, 1, -0.16, "a", "a", ext=0)
    d.zone(0, 0, 1, 1, "a", op=0.10, dash="8 4")
    d.etiquette(0.5, 0.52, "1 carré a × a", "a", 13)
    d.cote_v(0, 1, -0.18, "a", "a", ext=0); d.cote_v(1, H, -0.18, "5/8 a", "q", ext=0)
    d.cote_h(0.3125, 0.4375, H + 0.25, "1/8", "q", ext=1.155); d.cote_h(0.4375, 0.5625, H + 0.25, "1/8", "q", ext=1.155); d.cote_h(0.5625, 0.6875, H + 0.25, "1/8", "q", ext=1.155)
    d.cote_h(0.3125, 0.6875, H + 0.45, "3/8 a, centrés", "q")
    d.cote_v(1.03, 1.155, 1.18, "≈ 1/8 a", "q", ext=0.69, cote="d")
    d.forme(0, 0, 1, 1, "a", op=0.16, w=2.4)
    for x0 in (0.3125, 0.5625): d.forme(x0, 1.03, x0 + 0.125, 1.155, "q", op=0.45)
    d.forme(0.3125, 1.0, 0.6875, 1.185, "q", op=0, w=1.6, dash="4 3")
    return d, "Façade C, sur le jardin", [
        ("a", "Même rectangle que la façade B : <b>a</b> par <b>a + 5/8 a</b>, avec <b>un carré a × a</b> au-dessus des ouvertures."),
        ("q", "Les deux petites fenêtres sont des carrés d'environ <b>1/8 a = moitié de 1/4 a</b>, séparés par 1/8 a. À trois, elles font <b>3/8 a</b>, centrés sur la façade. Leur haut est juste sous le carré a."),
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

NOMS = {"a": "a · le carré", "t": "1/3 a · le tiers", "q": "1/4 a · le quart", "e": "e = 1/20 a · le mur"}


def page():
    cartes = []
    for i, (titre, ou, f) in enumerate(VUES):
        d, nom, notes = f(); svg = d.svg(nom)
        large = i < 4
        li = "".join(f'<li><i style="background:{COL[k]}"></i><span>{t}</span></li>' for k, t in notes)
        cartes.append(f'<section class="vue{" large" if large else ""}" id="v{i+1}"><header><span class="n">{i+1}</span><div><h2>{html.escape(titre)}</h2>'
                      f'<p class="ou">{html.escape(ou)}</p></div></header><div class="dessin">{svg}</div><ul class="notes">{li}</ul></section>')
    leg = "".join(f'<li><i style="background:{COL[k]}"></i>{html.escape(v)}</li>' for k, v in NOMS.items())
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
footer {{ font-family: var(--f-tech); font-size: .74rem; color: var(--encre-2); }}
@media (max-width: 820px) {{ .vues {{ grid-template-columns: 1fr; }} .chaine {{ grid-template-columns: 1fr 1fr; }} }}
</style>
<main class="planche">
  <header class="cartouche">
    <div class="surtitre">Atelier · Séance 5 · représentation conventionnelle · Tadao Ando, Azuma House (Osaka, 1976)</div>
    <h1>Azuma House · le carré a</h1>
    <p>Toutes les mesures des 8 vues partent d'une seule référence, le carré de côté <b>a</b>. On la plie en tiers, puis en quarts, jusqu'à trouver l'épaisseur du mur. Une couleur par mesure :</p>
    <ul class="legende">{leg}</ul>
  </header>

  <section class="bloc" aria-labelledby="t-chaine">
    <div class="surtitre">La chaîne des mesures</div>
    <h2 id="t-chaine">Du carré jusqu'au mur, en 4 pliages</h2>
    <div class="chaine">
      <div class="etape" style="border-color:var(--c-a)"><b style="color:var(--c-a)">a</b><span>Le côté du carré. Le plan en contient <b>4</b>. a = 400 cm.</span></div>
      <div class="etape" style="border-color:var(--c-t)"><b style="color:var(--c-t)">1/3 a</b><span>On plie le grand rectangle en 3 : chaque part vaut <b>a + 1/3 a</b>. ≈ 133 cm.</span></div>
      <div class="etape" style="border-color:var(--c-q)"><b style="color:var(--c-q)">1/4 a</b><span>On plie a en 4 (deux fois en deux) : porte, douche, garde-corps. 100 cm.</span></div>
      <div class="etape" style="border-color:var(--c-e)"><b style="color:var(--c-e)">e = 1/20 a</b><span>On plie le quart en 5 : c'est <b>l'épaisseur du mur</b>. 20 cm.</span></div>
    </div>
  </section>

  <section class="bloc" aria-labelledby="t-regle">
    <div class="surtitre">Pour ne pas se tromper</div>
    <h2 id="t-regle">Où l'on mesure, et l'échelle</h2>
    <div class="regle">
      <div><b>a se prend à l'extérieur</b>De la face extérieure d'un mur de façade à la face extérieure de l'autre : l'épaisseur des deux murs est comprise dans a.</div>
      <div><b>Les plis tombent sur les axes</b>Les tiers et les quarts se comptent depuis la face extérieure, et chaque pli tombe sur <b>l'axe</b> (le milieu) d'un mur intérieur ou d'une cloison.</div>
      <div><b>Les combinaisons</b>Une mesure peut en combiner plusieurs : 4/3 a = a + 1/3 a, 1/2 a = 2 × 1/4 a, 1/8 a = ½ × 1/4 a, 1/5 a = 4 e, 5/8 a = 1/4 + 1/4 + 1/8 a.</div>
      <div><b>L'échelle des vues</b>Les cotes écrites donnent a : 650 cm = a + 5/8 a, et 250 cm = 5/8 a, donc <b>a = 400 cm</b>. Mesure a à la règle sur ta feuille : l'échelle vaut a (en cm) / 400. Les photos donnent a ≈ 4 cm, soit <b>1/100</b> pour les 8 vues (les deux barres de 5 m le confirment).</div>
    </div>
  </section>

  <div class="vues">{"".join(cartes)}</div>
  <footer>Positions relevées sur les photos des deux feuilles (chaque dessin redressé, puis mesuré en fractions de a). Sur les photos, le plan fait un peu plus de 4 carrés (≈ 4,1) : on retient 4, l'écart est plus petit que la précision d'un pliage. Les mesures marquées ≈ sont arrondies à la fraction la plus proche.</footer>
</main>"""


if __name__ == "__main__":
    open(os.path.join(ICI, "index.html"), "w", encoding="utf-8").write(page())
    print("index.html écrit")

"""Coupes et façades : les constructions géométriques, le rendu au trait (fort / moyen / fin) et les détails des portes et fenêtres.

Les constructions sont dessinées sur les vues elles-mêmes (le bâtiment en gris pâle, les traits de construction par-dessus), avec des
points calculés en fractions exactes : chaque construction tombe pile sur la fraction annoncée (vérifiée par un assert).
Les détails (1/10 et 1/20) sont dessinés en cm réels : 1 cm réel = 1 mm sur la feuille à 1/10.
"""
import html, math
from fractions import Fraction as Fr
import build
from build import (COL, E_, F_, N_, TRAIT_PLI, _L, _P, _N, _arc, _txt, _fold, _R, _bloc, _tag, _thales, _diagonales,
                   _tiers_dans_rect, _zoomer, plan_rdc, plan_etage, plan_toit, coupe_longue, coupe_c, coupe_e, facade_b, facade_c)

# les niveaux, en fractions exactes (ils doivent égaler les constantes de build.py)
YT_, YT2_, YR_ = Fr(1, 7), Fr(1, 7) + Fr(1, 16), Fr(2, 3)
YF_, YD_, YP_, YS_ = Fr(6, 7), Fr(20, 21), Fr(19, 21), Fr(13, 8) - E_
H_ = Fr(13, 8)
for a, b in ((YT_, build.YT), (YT2_, build.YT2), (YR_, build.YR), (YF_, build.YF), (YD_, build.YD), (YP_, build.YP), (YS_, build.YS)):
    assert abs(float(a) - b) < 1e-12, (a, b)


def _pas(d, A, sens, r, n, k, w=2.0, pts=True):
    """n pas de compas de rayon r à partir de A, dans la direction sens ('x+', 'x-', 'y+', 'y-') ; renvoie les points marqués"""
    ang = {"x+": 0, "x-": 180, "y+": 90, "y-": -90}[sens]
    dx, dy = {"x+": (1, 0), "x-": (-1, 0), "y+": (0, 1), "y-": (0, -1)}[sens]
    P = [(Fr(A[0]), Fr(A[1]))]
    for j in range(n):
        _arc(d, P[-1], r, ang - 24, ang + 24, k, w)
        P.append((P[-1][0] + dx * r, P[-1][1] + dy * r))
    if pts:
        for p in P: _P(d, p, k, 3.6)
    return P


def _niveau(d, y, t, k="e", x0=-0.03, x1=None, ancre="start", dx=6):
    """une ligne de niveau (rappel) sur toute la largeur de la vue, avec son étiquette à droite (t vide : pas d'étiquette)"""
    x1 = x1 if x1 is not None else d.w + 0.03
    _L(d, (x0, y), (x1, y), k, 1.0, "7 4", 0.85)
    if t: _txt(d, (x1, y), t, k, 10.5, ancre, dx=dx, dy=-3)


def _niveaux_e(d, x1, avec_pont=True):
    """les lignes 3 e, 18 e, 19 e, 20 e (étiquette unique pour les trois derniers, trop serrés)"""
    _niveau(d, YT_, "3 e", "e", x1=x1)
    for y in (YF_, YP_ if avec_pont else None, YD_):
        if y is not None: _niveau(d, y, "", "e", x1=x1)
    _txt(d, (x1, YP_), "18 · 19 · 20 e" if avec_pont else "18 · 20 e", "e", 10.5, "start", dx=6, dy=4)


def _sol(d, x1, H):
    """le sol : 13/8 a ; la dalle du sol (e) au-dessus"""
    _niveau(d, YS_, "", "q", x1=x1); _L(d, (-0.03, H), (x1, H), "q", 1.2, "7 4", 0.8)
    _txt(d, (x1, H), "13/8 a", "q", 10.5, "start", dx=6, dy=4)


def _echelle_e(d, x, k="e", s=Fr(3, 5), lab=True):
    """l'échelle des e : Thalès en 7 sur le tiers du haut (→ 3 e) et sur le tiers du bas (→ 18, 19, 20 e), dans la marge de gauche"""
    P1, Q1 = _thales(d, (x, Fr(0)), (x, Fr(1, 3)), 7, k, vers=(-2, 1), s_total=s)
    P2, Q2 = _thales(d, (x, Fr(2, 3)), (x, Fr(1)), 7, k, vers=(-2, 1), s_total=s)
    assert Q1[3][1] == YT_ and Q2[4][1] == YF_ and Q2[5][1] == YP_ and Q2[6][1] == YD_
    return Q1, Q2


# ================================================================ la coupe longitudinale
def cons_coupe_longue(d):
    H = H_
    yb = Fr(-3, 20)
    # ① a, quatre fois, au compas
    _L(d, (0, yb), (4, yb), "g", 1.0, "4 3")
    for i in range(4): _arc(d, (i, yb), 1, -12, 12, "a", 1.8)
    for i in range(5): _P(d, (i, yb), "a", 4)
    _txt(d, (4, yb), "4 × a", "a", 11, "start", dx=8, dy=4); _N(d, (0, yb), 1, "a", dx=-16, dy=-2)
    # ② 2 a : les diagonales du rectangle 4 a × a
    c = _diagonales(d, 0, 0, 4, 1, "a", 1.0, 0.7)
    assert c == (2, Fr(1, 2))
    _fold(d, (2, -0.1), (2, H + 0.04), "a"); _P(d, c, "a", 5); _N(d, (2, -0.1), 2, "a", dy=-15)
    # ③ le tiers dans le premier carré : 1/3 a et 2/3 a de hauteur ; 4/3 a et 8/3 a au compas
    I, I2 = _tiers_dans_rect(d, 0, 0, 1, 1, "g", "t")
    for y in (Fr(1, 3), Fr(2, 3)): _L(d, (-0.03, y), (4.03, y), "t", 1.3, TRAIT_PLI, 0.8)
    _arc(d, (1, yb), Fr(1, 3), -26, 26, "t", 2.0); _arc(d, (3, yb), Fr(1, 3), 154, 206, "t", 2.0)
    for x in (Fr(4, 3), Fr(8, 3)): _fold(d, (x, yb - 0.02), (x, H + 0.04), "t"); _P(d, (x, yb), "t", 5)
    _N(d, (Fr(4, 3), yb), 3, "t", dx=16, dy=-4)
    # ④ l'échelle des e : Thalès en 7 sur le tiers du haut et sur le tiers du bas (dans la marge de gauche)
    Q1, Q2 = _echelle_e(d, Fr(0))
    _niveaux_e(d, 4.03)
    _txt(d, (4.03, Fr(2, 3)), "14 e = 2/3 a", "t", 10.5, "start", dx=6, dy=-3)
    _txt(d, (4.03, Fr(1)), "21 e = a", "a", 10.5, "start", dx=6, dy=-3)
    _N(d, Q1[3], 4, "e", dx=-20, dy=-2); _N(d, Q2[5], 5, "e", dx=-22, dy=-4)
    # ⑤ le sol : 13/8 a ; la dalle du sol : e
    _sol(d, 4.03, H)
    _N(d, (Fr(1, 2), H), 6, "q", dy=14)
    # ⑥ la cloison à 1/2 a (le croisement des diagonales), le sas à 1/3 a du bout, la douche à 4 e, l'escalier
    _fold(d, (Fr(1, 2), YD_), (Fr(1, 2), YS_), "q")
    yb2 = H + Fr(1, 10)
    _L(d, (3, yb2), (4, yb2), "g", 1.0, "4 3")
    _arc(d, (4, yb2), Fr(1, 3), 154, 206, "t", 2.0); _P(d, (Fr(11, 3), yb2), "t", 4.5); _fold(d, (Fr(11, 3), YD_), (Fr(11, 3), YS_), "t")
    yb3 = H + Fr(1, 4)
    _pas(d, (4, yb3), "x-", E_, 4, "e", 1.8)
    _fold(d, (4 - 4 * E_, YT2_), (4 - 4 * E_, YF_), "e")
    _L(d, (4 - 4 * E_, yb3), (4 - 4 * E_, YF_), "e", 0.8, "3 3", 0.7)
    for i in range(12):
        x = Fr(2) + Fr(2 * i - 11, 30)
        _L(d, (x, YS_), (x, H + 0.1), "q", 1.0, "3 3", 0.9)
    _txt(d, (2, H + 0.11), "11 marches de 1/15 a", "q", 10.5, "middle", dy=13)
    _N(d, (Fr(11, 3), yb2), 7, "t", dx=14, dy=-12)


# ================================================================ la coupe C
def cons_coupe_c(d):
    H = H_
    _R(d, 0, 0, 1, 1, "a", 1.6)
    c = _diagonales(d, 0, 0, 1, 1, "a", 1.1, 0.9)
    _fold(d, (Fr(1, 2), -0.06), (Fr(1, 2), H + 0.04), "a"); _P(d, c, "a", 5)
    _N(d, (Fr(1, 2), -0.06), 1, "a", dy=-14)
    I, I2 = _tiers_dans_rect(d, 0, 0, 1, 1, "g", "t")
    for y in (Fr(1, 3), Fr(2, 3)): _L(d, (-0.03, y), (1.03, y), "t", 1.3, TRAIT_PLI, 0.8)
    _N(d, I, 2, "t", dx=16, dy=14)
    Q1, Q2 = _echelle_e(d, Fr(0))
    _niveau(d, YT_, "3 e", "e", x1=1.03); _niveau(d, YF_, "", "e", x1=1.03); _niveau(d, YD_, "", "e", x1=1.03)
    _txt(d, (1.03, YF_), "18 · 20 e", "e", 10.5, "start", dx=6, dy=4)
    _txt(d, (1.03, Fr(2, 3)), "2/3 a", "t", 10.5, "start", dx=6, dy=-3); _txt(d, (1.03, Fr(1)), "a", "a", 10.5, "start", dx=6, dy=-3)
    _N(d, Q1[3], 3, "e", dx=-20, dy=-2); _N(d, Q2[5], 4, "e", dx=-22, dy=-4)
    _sol(d, 1.03, H)
    _P(d, (0, YS_), "q", 4); _N(d, (Fr(1, 2), H), 5, "q", dy=14)
    _arc(d, (Fr(1, 2), H), Fr(1, 21), -112, -68, "e", 1.8)
    d.cote_v(float(YD_), float(YS_), 0.72, "5/8 a = 250", "q", ext=0.5, cote="d")


# ================================================================ la coupe E
def cons_coupe_e(d):
    H = H_
    _R(d, 0, 0, 1, 1, "a", 1.6)
    c = _diagonales(d, 0, 0, 1, 1, "a", 1.1, 0.9)
    _fold(d, (Fr(1, 2), -0.06), (Fr(1, 2), H + 0.04), "a"); _P(d, c, "a", 5); _N(d, (Fr(1, 2), -0.06), 1, "a", dy=-14)
    I, I2 = _tiers_dans_rect(d, 0, 0, 1, 1, "g", "t")
    yb = Fr(-1, 8)
    _arc(d, (1, 0), Fr(1, 3), 154, 206, "t", 2.0)
    for x in (Fr(1, 3), Fr(2, 3)): _fold(d, (x, -0.05), (x, YP_ + 0.03), "t"); _P(d, (x, 0), "t", 4.5)
    for y in (Fr(1, 3), Fr(2, 3)): _L(d, (-0.03, y), (1.03, y), "t", 1.3, TRAIT_PLI, 0.8)
    _N(d, I, 2, "t", dx=16, dy=14)
    Q1, Q2 = _echelle_e(d, Fr(0))
    _niveau(d, YT_, "3 e", "e", x1=1.03); _niveau(d, YP_, "19 e", "e", x1=1.03)
    _txt(d, (1.03, Fr(2, 3)), "14 e = 2/3 a", "t", 10.5, "start", dx=6, dy=-3)
    _N(d, Q1[3], 3, "e", dx=-20, dy=-2); _N(d, Q2[5], 4, "e", dx=-22, dy=-4)
    # les garde-corps : e d'épaisseur ; la porte : 4 e de large (2 pas de chaque côté de l'axe)
    yp = Fr(13, 10)
    _pas(d, (Fr(1, 3), Fr(7, 10)), "x+", E_, 1, "e", 2.0)
    P = _pas(d, (Fr(1, 2), YS_ + Fr(1, 14)), "x+", E_, 2, "e", 1.8); Pm = _pas(d, (Fr(1, 2), YS_ + Fr(1, 14)), "x-", E_, 2, "e", 1.8)
    assert P[2][0] - Pm[2][0] == 4 * E_
    _L(d, (Fr(1, 2) - 2 * E_, YS_ + Fr(1, 14)), (Fr(1, 2) + 2 * E_, YS_ + Fr(1, 14)), "e", 4)
    _fold(d, (Fr(1, 2) - 2 * E_, YS_ - 12 * E_), (Fr(1, 2) - 2 * E_, YS_), "e"); _fold(d, (Fr(1, 2) + 2 * E_, YS_ - 12 * E_), (Fr(1, 2) + 2 * E_, YS_), "e")
    _N(d, (Fr(1, 2) + 2 * E_, YS_ + Fr(1, 14)), 5, "e", dx=16, dy=2)
    # l'escalier : 1/4 a depuis la face extérieure (les diagonales d'un rectangle de 1/2 a), mur compris
    c4 = _diagonales(d, 0, 0, Fr(1, 2), 1, "q", 1.0, 0.8)
    assert c4 == (Fr(1, 4), Fr(1, 2))
    _fold(d, (Fr(1, 4), YS_ - Fr(7, 10) - 0.03), (Fr(1, 4), YS_ + 0.03), "q"); _P(d, c4, "q", 5); _N(d, (Fr(1, 4), YS_ - Fr(7, 10)), 6, "q", dy=-14)
    # les fentes hautes : un groupe de 1/5 a centré (3 pas de 1/15 a)
    _pas(d, (Fr(2, 5), Fr(1, 5)), "x+", F_, 3, "t", 1.6)
    _N(d, (Fr(1, 2), Fr(1, 5)), 7, "t", dy=-14)
    _sol(d, 1.03, H)


# ================================================================ la façade B
def cons_facade_b(d):
    H = H_
    _R(d, 0, 0, 1, 1, "a", 1.6)
    c = _diagonales(d, 0, 0, 1, 1, "a", 1.1, 0.9)
    _fold(d, (Fr(1, 2), -0.06), (Fr(1, 2), H + 0.04), "a"); _P(d, c, "a", 5); _N(d, (Fr(1, 2), -0.06), 1, "a", dy=-14)
    # ② 5/8 a sous la ligne a : 1/2 a (les diagonales du carré du dessous) puis 1/8 a
    c2 = _diagonales(d, 0, 1, 1, 2, "q", 0.9, 0.55)
    _L(d, (-0.03, Fr(3, 2)), (1.03, Fr(3, 2)), "q", 1.3, TRAIT_PLI, 0.9); _txt(d, (1.03, Fr(3, 2)), "1/2 a", "q", 10.5, "start", dx=6, dy=-3)
    _arc(d, (Fr(1, 10), Fr(3, 2)), Fr(1, 8), 68, 112, "q", 1.8); _P(d, (Fr(1, 10), H), "q", 4.5)
    _L(d, (-0.03, H), (1.03, H), "q", 1.4, "7 4", 0.9); _txt(d, (1.03, H), "5/8 a sous a", "q", 10.5, "start", dx=6, dy=-3)
    _N(d, (Fr(1, 10), Fr(3, 2)), 2, "q", dx=-16, dy=-2)
    # ③ la porte : l'axe, puis des pas de compas de e sur la ligne de la tête (a) : 4 e = vantail, 5 e = cadre
    _L(d, (0, 1), (1, 1), "a", 1.0, "4 3")
    R_ = _pas(d, (Fr(1, 2), 1), "x+", E_, 2, "e", 1.8); L_ = _pas(d, (Fr(1, 2), 1), "x-", E_, 2, "e", 1.8)
    assert R_[2][0] - L_[2][0] == 4 * E_
    for s in (-1, 1):
        x = Fr(1, 2) + s * Fr(5, 2) * E_
        _arc(d, (Fr(1, 2) + s * 2 * E_, 1), E_ / 2, -26 if s > 0 else 154, 26 if s > 0 else 206, "e", 1.6); _P(d, (x, 1), "e", 4.5)
    _fold(d, (Fr(1, 2) - Fr(5, 2) * E_, 1), (Fr(1, 2) - Fr(5, 2) * E_, H), "e"); _fold(d, (Fr(1, 2) + Fr(5, 2) * E_, 1), (Fr(1, 2) + Fr(5, 2) * E_, H), "e")
    _L(d, (Fr(1, 2) - 2 * E_, 1), (Fr(1, 2) - 2 * E_, H), "e", 1.3, "5 3"); _L(d, (Fr(1, 2) + 2 * E_, 1), (Fr(1, 2) + 2 * E_, H), "e", 1.3, "5 3")
    _N(d, (Fr(1, 2) + 2 * E_, 1), 3, "e", dx=16, dy=-10)
    # ④ la tête du vantail : e/2 sous la ligne a ; le seuil : 3/4 e au-dessus du sol
    _arc(d, (Fr(1, 2) - 2 * E_ - Fr(1, 20), 1), E_ / 2, 68, 112, "e", 1.6); _P(d, (Fr(1, 2) - 2 * E_ - Fr(1, 20), 1 + E_ / 2), "e", 4)
    _N(d, (Fr(1, 2) - 2 * E_ - Fr(1, 20), 1 + E_ / 2), 4, "e", dx=-16, dy=6)
    _L(d, (Fr(1, 2) - 3 * E_, H - Fr(7, 200)), (Fr(1, 2) + 3 * E_, H - Fr(7, 200)), "e", 1.0, "3 2")


# ================================================================ la façade C
def cons_facade_c(d):
    H = H_
    _R(d, 0, 0, 1, 1, "a", 1.6)
    c = _diagonales(d, 0, 0, 1, 1, "a", 1.1, 0.9)
    _fold(d, (Fr(1, 2), -0.06), (Fr(1, 2), H + 0.04), "a"); _P(d, c, "a", 5); _N(d, (Fr(1, 2), -0.06), 1, "a", dy=-14)
    yb = Fr(6, 5)
    _L(d, (Fr(1, 5), yb), (Fr(4, 5), yb), "g", 1.0, "4 3")
    # ② l'écart : e, puis la moitié de e, de chaque côté de l'axe (1,5 e = 1/14 a)
    for s in (-1, 1):
        _arc(d, (Fr(1, 2), yb), E_, -24 if s > 0 else 156, 24 if s > 0 else 204, "e", 1.8)
        _P(d, (Fr(1, 2) + s * E_, yb), "e", 3.6); _P(d, (Fr(1, 2) + s * Fr(3, 2) * E_, yb), "e", 5)
    # ③ les fenêtres : 1/8 a de large, vers l'extérieur
    W1, W2 = Fr(1, 2) - Fr(1, 14) - Fr(1, 8), Fr(1, 2) + Fr(1, 14)
    for x0 in (W1, W2):
        _L(d, (x0, yb), (x0 + Fr(1, 8), yb), "q", 4); _P(d, (x0, yb), "q", 4.5); _P(d, (x0 + Fr(1, 8), yb), "q", 4.5)
    _arc(d, (W1 + Fr(1, 8), yb), Fr(1, 8), 160, 200, "q", 1.8); _arc(d, (W2, yb), Fr(1, 8), -20, 20, "q", 1.8)
    for x in (W1, W1 + Fr(1, 8), W2, W2 + Fr(1, 8)): _L(d, (x, yb), (x, 1 - E_ / 2), "q", 1.0, "3 3", 0.8)
    _N(d, (Fr(1, 2), yb), 2, "e", dy=16); _N(d, (W2 + Fr(1, 8), yb), 3, "q", dx=14, dy=-8)
    # ④ la hauteur : e/2 au-dessus de la ligne a, puis 3 pas de compas de e
    xv = Fr(1, 7)
    _L(d, (xv, 1 - Fr(1, 20)), (xv, Fr(5, 4)), "g", 1.0, "4 3")
    _L(d, (0, 1), (1, 1), "a", 1.0, "4 3")
    P = _pas(d, (xv, 1 - E_ / 2), "y+", E_, 3, "e", 1.8)
    assert P[3][1] == 1 - E_ / 2 + 3 * E_ == build.WT + build.WH or abs(float(P[3][1]) - (build.WT + build.WH)) < 1e-12
    _arc(d, (xv, 1), E_ / 2, -112, -68, "e", 1.6)
    _L(d, (W1, 1 - E_ / 2), (W2 + Fr(1, 8), 1 - E_ / 2), "e", 1.0, "5 3", 0.9); _L(d, (W1, P[3][1]), (W2 + Fr(1, 8), P[3][1]), "e", 1.0, "5 3", 0.9)
    _N(d, (xv, 1 - E_ / 2), 4, "e", dx=-16, dy=-2)


CONSTR = [
    # (id, titre, couleur, vue, dessin, marges (gauche, droite) pour tenir à l'échelle du carnet, étapes)
    ("coupe_longue", "La coupe longitudinale : la trame en hauteur", "a", coupe_longue, cons_coupe_longue, (0.75, 0.42),
     ["Sur une ligne au-dessus de la coupe, reporte <b>a quatre fois</b> au compas : la longueur fait 4 a.",
      "Les <b>diagonales</b> du rectangle 4 a × a se croisent au milieu : la verticale est à <b>2 a</b> (pli 1).",
      "Dans le premier carré : <b>diagonale + milieu</b> (construction du tiers) donnent les lignes à <b>1/3 a</b> et <b>2/3 a</b> de hauteur. Le compas ouvert de 1/3 a, pointe en a, marque <b>4/3 a</b> ; pointe en 3 a, vers la gauche : <b>8/3 a</b>.",
      "<b>L'échelle des e</b> : Thalès en 7 sur le tiers du haut. Le 3e repère est à <b>3 e = 1/7 a</b> : le haut de la dalle du toit (l'acrotère).",
      "Thalès en 7 sur le tiers du bas : <b>18 e</b> = le plancher de l'étage, <b>19 e</b> = le dessus de la dalle du pont (e plus bas), <b>20 e</b> = le dessous du plancher, <b>21 e = a</b>. Le haut du garde-corps est sur la ligne <b>2/3 a</b> (14 e) : 5 e au-dessus de la dalle du pont.",
      "Sous la ligne a : 1/2 a puis 1/8 a (diagonales) donnent le sol, à <b>13/8 a</b>. La dalle du sol fait <b>e</b> : reporte-la au compas vers le haut.",
      "Cloison de la salle de bain à <b>1/2 a</b> (croisement des diagonales du carré) ; sas à <b>1/3 a</b> du bout (compas) ; douche à <b>4 e</b> (4 pas de compas de e) ; escalier : <b>11 marches de 1/15 a</b> (construction 8 du plan)."]),
    ("coupe_c", "La coupe C : les niveaux", "a", coupe_c, cons_coupe_c, (0.8, 0.5),
     ["Les <b>diagonales</b> du carré a donnent l'axe. <b>Diagonale + milieu</b> : les lignes à <b>1/3 a</b> et <b>2/3 a</b>.",
      "<b>L'échelle des e</b> : Thalès en 7 sur le tiers du haut (→ <b>3 e</b> : le haut de la dalle du toit) et sur le tiers du bas (→ <b>18 e</b> : dessus du plancher de l'étage, <b>20 e</b> : son dessous).",
      "Le sol : 1/2 a + 1/8 a sous la ligne a, soit <b>13/8 a</b> ; la dalle du sol fait <b>e</b>. Le rez-de-chaussée fait alors exactement <b>5/8 a = 250 cm</b> sous plafond (de 20 e à 13/8 a − e)."]),
    ("coupe_e", "La coupe E : le pont, la porte, l'escalier", "a", coupe_e, cons_coupe_e, (0.8, 0.5),
     ["Les <b>diagonales</b> du carré a donnent l'axe ; <b>diagonale + milieu</b> donne 1/3 a ; le compas ouvert de 1/3 a, pointe en a, marque <b>2/3 a</b> : le pont fait 1/3 a, de 1/3 à 2/3.",
      "<b>L'échelle des e</b> (Thalès en 7, tiers du haut et du bas) : la dalle du pont est à <b>19 e</b> ; le haut des garde-corps est sur la ligne <b>2/3 a</b> (14 e) : hauteur <b>5 e = 95 cm</b>. Les garde-corps font <b>e</b> d'épaisseur (1 pas de compas).",
      "La porte sous le pont : <b>2 pas de e de chaque côté de l'axe</b> = <b>4 e</b> de large ; sa hauteur est de <b>12 e</b> (230 cm) à partir du sol.",
      "L'escalier : les diagonales d'un rectangle de 1/2 a donnent <b>1/4 a</b> depuis la face extérieure, mur compris (donc 1/4 a − e pour l'escalier).",
      "Les fentes hautes : un groupe de <b>1/5 a</b> centré sur l'axe, soit 3 pas de compas de <b>1/15 a</b>."]),
    ("facade_b", "La façade B : la porte", "e", facade_b, cons_facade_b, (0.8, 0.5),
     ["Les <b>diagonales</b> du carré a donnent l'axe de la porte.",
      "Sous la ligne a : les diagonales du carré du dessous donnent <b>1/2 a</b> ; le compas ouvert de 1/8 a ajoute <b>1/8 a</b> : le sol, à <b>13/8 a</b> (la porte fait 5/8 a de haut).",
      "Sur la ligne de la tête (a) : <b>2 pas de e</b> de chaque côté de l'axe = le vantail de <b>4 e</b> ; puis <b>e/2</b> de plus = le cadre de <b>5 e</b> (montants de e/2).",
      "La tête du vantail est à <b>e/2</b> sous la ligne a ; le seuil fait environ <b>3/4 e</b> (14 cm) au-dessus du sol."]),
    ("facade_c", "La façade C : les fenêtres", "q", facade_c, cons_facade_c, (0.8, 0.5),
     ["Les <b>diagonales</b> du carré a donnent l'axe de la façade.",
      "De chaque côté de l'axe : <b>e</b>, puis <b>la moitié de e</b> : 1,5 e = 1/14 a. L'écart entre les fenêtres fait donc <b>3 e = 1/7 a</b>.",
      "Le compas ouvert de <b>1/8 a</b> donne la largeur de chaque fenêtre, vers l'extérieur.",
      "Hauteur : le haut est <b>e/2 au-dessus</b> de la ligne a ; puis <b>3 pas de compas de e</b> : la fenêtre fait <b>1/7 a = 3 e</b> de haut."]),
]


def construire_vue(i):
    """la construction i : le bâtiment en gris pâle et les traits de construction (marges ajustées pour tenir sur la page)"""
    id_, titre, k, vue, dessin, marges, etapes = CONSTR[i]
    cle = (4, H_) if id_ == "coupe_longue" else (1, H_)
    ancien = build.MARGES_A4.get((cle[0], float(cle[1])))
    key = (cle[0], float(cle[1]))
    gm, dm = marges
    build.MARGES_A4[key] = (gm, dm, 0.55 if id_ == "coupe_longue" else 0.45, 0.62 if id_ == "coupe_longue" else 0.6)
    try:
        w = cle[0]
        d0 = vue()[0]
        region = (-d0.mg, d0.w + (d0.W / build.S - d0.w - d0.mg), -d0.mh, d0.h + (d0.H / build.S - d0.h - d0.mh))
        return _zoomer(dessin, region, 1, vue)
    finally:
        if ancien is not None: build.MARGES_A4[key] = ancien


# ================================================================ les détails des portes et fenêtres (cm réels)
ECM = 400 / 21          # e en cm = 19,05
U = 10                  # px par cm dans le dessin du détail


class Det:
    """un détail dessiné en cm réels ; imprimé à 1/10 (1 cm = 1 mm) ou à 1/20, avec les mêmes épaisseurs de trait sur le papier"""

    def __init__(self, w, h, echelle=10):
        self.w, self.h, self.ech, self.o = w, h, echelle, []
        self.mm = 0.1 * 10 / echelle                 # mm de papier par px
        pt = lambda mm: mm / self.mm                  # une épaisseur voulue sur le papier (mm) en px
        self.FORT, self.MOY, self.FIN = pt(0.55), pt(0.30), pt(0.14)
        self.T = pt(3.0)                              # hauteur de texte : 3 mm

    def X(self, x): return x * U

    def rect(self, x, y, w, h, tr=None, fill="none", hach=False, dash=""):
        tr = tr or self.MOY
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.o.append(f'<rect x="{x*U:.1f}" y="{y*U:.1f}" width="{w*U:.1f}" height="{h*U:.1f}" fill="{fill}" stroke="#151515" stroke-width="{tr:.2f}"{da}/>')
        if hach: self.o.append(f'<rect x="{x*U:.1f}" y="{y*U:.1f}" width="{w*U:.1f}" height="{h*U:.1f}" fill="url(#hd)"/>')

    def ligne(self, x0, y0, x1, y1, tr=None, dash="", c="#151515"):
        tr = tr or self.MOY
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.o.append(f'<line x1="{x0*U:.1f}" y1="{y0*U:.1f}" x2="{x1*U:.1f}" y2="{y1*U:.1f}" stroke="{c}" stroke-width="{tr:.2f}"{da}/>')

    def arc(self, cx, cy, r, a0, a1, tr=None, dash=""):
        tr = tr or self.FIN
        x0, y0 = (cx + r * math.cos(math.radians(a0))) * U, (cy + r * math.sin(math.radians(a0))) * U
        x1, y1 = (cx + r * math.cos(math.radians(a1))) * U, (cy + r * math.sin(math.radians(a1))) * U
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.o.append(f'<path d="M{x0:.1f} {y0:.1f} A {r*U:.1f} {r*U:.1f} 0 0 {1 if a1 > a0 else 0} {x1:.1f} {y1:.1f}" fill="none" stroke="#151515" stroke-width="{tr:.2f}"{da}/>')

    def txt(self, x, y, t, anc="middle", c="#151515", f=1.0, gras=False):
        g = ' font-weight="700"' if gras else ""
        self.o.append(f'<text x="{x*U:.1f}" y="{y*U:.1f}" fill="{c}" font-size="{self.T*f:.1f}" text-anchor="{anc}"{g} paint-order="stroke" stroke="#fbfbf8" stroke-width="{self.FIN*3:.1f}">{html.escape(t)}</text>')

    def cote_h(self, x0, x1, y, t, ext=None, dy=-1.2, col="#6b2a96"):
        tk = 1.2
        self.ligne(x0, y, x1, y, self.FIN, c=col)
        for x in (x0, x1):
            self.ligne(x, y - tk, x, y + tk, self.FIN, c=col)
            if ext is not None: self.ligne(x, y, x, ext, self.FIN * 0.7, c=col)
        self.txt((x0 + x1) / 2, y + dy, t, "middle", col, 0.95)

    def cote_v(self, y0, y1, x, t, ext=None, dx=1.2, anc="start", col="#6b2a96"):
        tk = 1.2
        self.ligne(x, y0, x, y1, self.FIN, c=col)
        for y in (y0, y1):
            self.ligne(x - tk, y, x + tk, y, self.FIN, c=col)
            if ext is not None: self.ligne(x, y, ext, y, self.FIN * 0.7, c=col)
        self.txt(x + dx, (y0 + y1) / 2 + 0.4, t, anc, col, 0.95)

    def svg(self, titre, mm=True):
        defs = (f'<defs><pattern id="hd" width="{2.2*U:.0f}" height="{2.2*U:.0f}" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                f'<line x1="0" y1="0" x2="0" y2="{2.2*U:.0f}" stroke="#151515" stroke-width="{self.FIN*0.8:.2f}"/></pattern></defs>')
        taille = f' width="{self.w*U*self.mm:.2f}mm" height="{self.h*U*self.mm:.2f}mm"' if mm else ""
        return (f'<svg viewBox="0 0 {self.w*U:.0f} {self.h*U:.0f}"{taille} role="img" aria-label="{html.escape(titre)}" '
                f'font-family="IBM Plex Mono, ui-monospace, monospace">{defs}<rect width="100%" height="100%" fill="#fbfbf8"/>{"".join(self.o)}</svg>')


def _num(D, x, y, n):
    """un repère numéroté sur le détail"""
    r = D.T * 0.62
    D.o.append(f'<circle cx="{x*U:.1f}" cy="{y*U:.1f}" r="{r:.1f}" fill="#6b2a96" stroke="#fbfbf8" stroke-width="{D.FIN*2:.1f}"/>'
               f'<text x="{x*U:.1f}" y="{y*U+D.T*0.35:.1f}" fill="#fff" font-size="{D.T*0.85:.1f}" font-weight="700" text-anchor="middle">{n}</text>')


def _legende(D, x, y, lignes, pas=7.0):
    for i, t in enumerate(lignes):
        _num(D, x, y + i * pas, i + 1)
        D.txt(x + 4, y + i * pas + 1.0, t, "start", "#151515", 0.82)


def det_porte_plan():
    """la porte d'entrée en plan (coupe horizontale à 1,20 m), 1/10 : l'extérieur est à droite"""
    e = ECM
    L, ox, oy = 18.0, 80.0, 12.0
    D = Det(ox + e + 1.5 * e + 150, oy + L + 5 * e + L + 22, 10)
    X0, Y0 = ox, oy
    yo, yf = Y0 + L, Y0 + L + 5 * e
    D.rect(X0, Y0, e, L, D.FORT, "#efefef", hach=True); D.rect(X0, yf, e, L, D.FORT, "#efefef", hach=True)       # le mur coupé
    D.rect(X0 + e, yo, 1.5 * e, 5 * e, D.MOY)                                                                 # l'encadrement en saillie (vu)
    px0 = X0 + e / 4
    D.rect(px0, yo, e / 2, e / 2, D.FORT, "#d4d4d4"); D.rect(px0, yf - e / 2, e / 2, e / 2, D.FORT, "#d4d4d4")   # les montants du cadre
    ym0, ym1 = yo + e / 2, yf - e / 2
    xm, ep = X0 + e / 2, e / 4
    D.rect(xm - ep / 2, ym0, ep, e / 3, D.FORT, "#d4d4d4"); D.rect(xm - ep / 2, ym1 - e / 3, ep, e / 3, D.FORT, "#d4d4d4")   # montants du vantail
    D.rect(xm - 0.5, ym0 + e / 3, 1.0, (ym1 - ym0) - 2 * e / 3, D.MOY, "#ffffff")                             # le verre : 1 cm
    hx, hy = xm, ym1
    D.rect(hx - (ym1 - ym0), hy - ep / 2, ym1 - ym0, ep, D.MOY, "#ffffff")                                     # vantail ouvert à 90°
    D.arc(hx, hy, ym1 - ym0, -90, -180, D.FIN, "5 4")
    xr = X0 + e + 1.5 * e
    D.cote_v(yo, yf, xr + 10, "cadre 5 e = 95,2", ext=xr, dx=2)
    D.cote_v(ym0, ym1, xr + 62, "passage 4 e = 76,2", ext=X0 + e, dx=2)
    D.cote_h(X0, X0 + e, Y0 - 5, "e = 19,05", ext=Y0, dy=-1.6)
    D.cote_h(X0 + e, xr, yo - 8, "1,5 e = 28,6", ext=yo, dy=-1.6)
    _num(D, px0 + e / 4, yo + e / 4, 1); _num(D, xm + 9, ym0 + e / 6, 2); _num(D, xm + 6, (ym0 + ym1) / 2, 3); _num(D, xm - 30, hy + 7, 4)
    _num(D, xr - 9, yo + 14, 5); _num(D, X0 + e / 2, Y0 + L / 2, 6); _num(D, xm - 45, ym0 + 25, 7)
    _legende(D, X0 + e + 1.5 * e + 84, oy + 8, [
        "montant du cadre : e/2 = 9,5 cm", "montant du vantail : e/3 = 6,35 cm", "verre : 1 cm d'épaisseur",
        "vantail ouvert à 90° : trait moyen", "encadrement en saillie : 1,5 e", "mur coupé : trait fort, hachuré",
        "arc d'ouverture : trait fin pointillé"], 8.0)
    D.txt(X0 + e / 2, yf + L + 14, "intérieur ← → extérieur", "middle", "#555", 0.95)
    return D


def det_porte_elevation():
    """la porte d'entrée en élévation, 1/20"""
    e = ECM
    W, Hh = 5 * e, 250.0
    ox, oy = 80.0, 20.0
    D = Det(ox + W + 150, oy + Hh + 40, 20)
    seuil, tete = 3 * e / 4, e / 2
    D.ligne(ox - 30, oy + Hh, ox + W + 30, oy + Hh, D.FORT)
    for i in range(0, int(W + 60), 6): D.ligne(ox - 30 + i, oy + Hh, ox - 30 + i - 6, oy + Hh + 6, D.FIN)
    D.rect(ox, oy, W, Hh - seuil, D.MOY)
    D.rect(ox, oy + Hh - seuil, W, seuil, D.MOY)
    D.rect(ox + e / 2, oy + tete, 4 * e, Hh - seuil - tete, D.MOY)
    D.rect(ox + e / 2 + e / 3, oy + tete + e / 3, 4 * e - 2 * e / 3, Hh - seuil - tete - 2 * e / 3, D.FIN, "#fdfdf9")
    D.rect(ox + W - e / 2 - e / 3 - 4, oy + 100, 3, 12, D.MOY)
    xc = ox + W + 12
    D.cote_v(oy, oy + Hh, xc, "5/8 a = 250", ext=ox + W, dx=2)
    D.cote_v(oy + tete, oy + Hh - seuil, xc + 62, "vantail ≈ 12 e = 226", ext=ox + W - e / 2, dx=2)
    D.cote_h(ox, ox + W, oy - 6, "cadre 5 e = 95,2", ext=oy, dy=-3)
    D.cote_h(ox + e / 2, ox + e / 2 + 4 * e, oy + Hh + 18, "vantail 4 e = 76,2", ext=oy + Hh, dy=8)
    D.cote_v(oy + Hh - seuil, oy + Hh, ox - 12, "seuil 3/4 e = 14,3", ext=ox, dx=-2, anc="end")
    D.cote_v(oy, oy + tete, ox - 12, "tête e/2 = 9,5", ext=ox, dx=-2, anc="end")
    return D


def det_fente_plan():
    """une fente des longs murs en plan, 1/10 : 2 fentes et 1 trumeau de 1/15 a (le groupe fait 1/5 a)"""
    e, F = ECM, 400 / 15
    ox, oy = 40.0, 36.0
    Lg = 3 * F + 2 * 18
    D = Det(Lg + 2 * ox, oy + e + 64, 10)
    xs = ox + 18
    D.rect(ox, oy, 18, e, D.FORT, "#efefef", hach=True)
    D.rect(xs + F, oy, F, e, D.FORT, "#efefef", hach=True)
    D.rect(xs + 3 * F, oy, 18, e, D.FORT, "#efefef", hach=True)
    ym = oy + e / 2
    for x0 in (xs, xs + 2 * F):
        D.rect(x0, ym - e / 8, e / 6, e / 4, D.FORT, "#d4d4d4"); D.rect(x0 + F - e / 6, ym - e / 8, e / 6, e / 4, D.FORT, "#d4d4d4")
        D.rect(x0 + e / 6, ym - 0.5, F - e / 3, 1.0, D.MOY, "#ffffff")
    D.cote_h(xs, xs + F, oy - 6, "fente 1/15 a = 26,7", ext=oy, dy=-1.6)
    D.cote_h(xs + F, xs + 2 * F, oy - 14, "trumeau 26,7", ext=oy, dy=-1.6)
    D.cote_h(xs, xs + 3 * F, oy - 22, "groupe 1/5 a = 80", ext=oy, dy=-1.6)
    D.cote_v(oy, oy + e, ox - 8, "e = 19,05", ext=ox, dx=-1.5, anc="end")
    D.txt(xs + F / 2, oy + e + 9, "montant e/6 = 3,2", "middle", "#6b2a96", 0.95)
    D.txt(xs + F / 2, oy + e + 14, "verre 1 cm", "middle", "#6b2a96", 0.95)
    D.txt(xs + 1.5 * F, oy + e + 26, "extérieur en haut · vu d'en haut", "middle", "#555", 0.95)
    return D


def det_fenetre_jardin():
    """une fenêtre du jardin : élévation et coupe horizontale, 1/10 (50 × 57 cm)"""
    e, Wd, Hd = ECM, 50.0, 400 / 7
    ox, oy = 42.0, 22.0
    D = Det(ox + Wd + 70 + Wd + 40, oy + Hd + 44, 10)
    D.rect(ox, oy, Wd, Hd, D.MOY)
    D.rect(ox + e / 3, oy + e / 3, Wd - 2 * e / 3, Hd - 2 * e / 3, D.FIN, "#fdfdf9")
    D.ligne(ox - 6, oy + Hd, ox + Wd + 6, oy + Hd, D.FORT)
    D.cote_h(ox, ox + Wd, oy - 6, "1/8 a = 50", ext=oy, dy=-1.6)
    D.cote_v(oy, oy + Hd, ox - 10, "1/7 a = 57,1", ext=ox, dx=-1.5, anc="end")
    D.cote_h(ox, ox + e / 3, oy + Hd + 10, "cadre e/3 = 6,35", ext=oy + Hd, dy=6)
    D.txt(ox + Wd / 2, oy + Hd / 2, "vitrage", "middle", "#555", 0.95)
    px, wy, Lm = ox + Wd + 66, oy + 18, 24
    D.rect(px - Lm, wy, Lm, e, D.FORT, "#efefef", hach=True); D.rect(px + Wd, wy, Lm, e, D.FORT, "#efefef", hach=True)
    ym = wy + e / 2
    for x0 in (px, px + Wd - e / 3): D.rect(x0, ym - e / 8, e / 3, e / 4, D.FORT, "#d4d4d4")
    D.rect(px + e / 3, ym - 0.5, Wd - 2 * e / 3, 1.0, D.MOY, "#ffffff")
    D.cote_h(px, px + Wd, wy - 6, "ouverture 50", ext=wy, dy=-1.6)
    D.cote_v(wy, wy + e, px - Lm - 8, "e = 19,05", ext=px - Lm, dx=-1.5, anc="end")
    D.txt(px + Wd / 2, wy + e + 10, "montant e/3 × e/4, verre 1 cm", "middle", "#6b2a96", 0.95)
    D.txt(px + Wd / 2, wy + e + 15, "coupe horizontale (vu d'en haut)", "middle", "#555", 0.95)
    return D


DETAILS = [
    ("porte_plan", "La porte d'entrée en plan", "1/10", det_porte_plan,
     ["Le mur est coupé : <b>trait fort</b>, hachuré. Son épaisseur est <b>e = 19 cm</b>. L'ouverture du mur fait <b>5 e = 95 cm</b>.",
      "Les montants du cadre font <b>e/2 = 9,5 cm</b> : il reste un <b>passage de 4 e = 76 cm</b>. Le cadre fait 5 e sur la façade B (mesuré : 0,380 à 0,617 a).",
      "Le vantail fait <b>4 e</b> de large et <b>e/4 = 4,8 cm</b> d'épaisseur. Ses montants font e/3 = 6,35 cm. Le <b>verre</b> est entre les montants : <b>1 cm</b> d'épaisseur (verre simple de 10 mm, proposition à valider).",
      "L'encadrement qui dépasse du mur fait <b>1,5 e = 28,6 cm</b> (mesuré 0,07 a sur la feuille). Le vantail ouvert à 90° et son arc sont dessinés en moyen et en fin pointillé."]),
    ("porte_elev", "La porte d'entrée en élévation", "1/20", det_porte_elevation,
     ["Le cadre dormant fait <b>5 e</b> de large, avec la tête sur la ligne <b>a</b> : il fait <b>5/8 a = 250 cm</b> de haut jusqu'au sol.",
      "Le vantail fait <b>4 e × ≈ 12 e</b> (76 × 226 cm). Entre la tête (e/2) et le seuil (3/4 e ≈ 14 cm). Le vitrage est inscrit dans le cadre du vantail (e/3 = 6,35 cm).",
      "Traits : le sol en fort, le cadre et le vantail en moyen, le vitrage en fin."]),
    ("fente", "Les fentes des longs murs en plan", "1/10", det_fente_plan,
     ["Le mur est coupé : trait fort. Chaque fente fait <b>1/15 a = 26,7 cm</b>, le trumeau aussi ; le groupe fait <b>1/5 a = 80 cm</b>.",
      "La fenêtre est posée au milieu de l'épaisseur du mur : montants de <b>e/6 = 3,2 cm</b> sur <b>e/4 = 4,8 cm</b>, verre de <b>1 cm</b> (proposition à valider)."]),
    ("fenetre_jardin", "La fenêtre du jardin : élévation et coupe", "1/10", det_fenetre_jardin,
     ["La fenêtre fait <b>1/8 a = 50 cm</b> de large et <b>1/7 a = 57 cm</b> de haut. Le cadre fait <b>e/3 = 6,35 cm</b> ; le vitrage est à l'intérieur.",
      "Dans la coupe horizontale : le mur (e = 19 cm) est coupé en trait fort ; les montants du cadre sont coupés aussi ; le verre de 1 cm est au milieu."]),
]


# ================================================================ les agrandissements des façades, la page web et les pages du PDF
ZOOMS = [
    # (id de la construction, titre, région, zoom)
    ("facade_b", "La façade B : la porte, agrandie", (0.27, 0.73, 0.92, 1.66), 3),
    ("facade_c", "La façade C : les fenêtres, agrandies", (0.2, 0.8, 0.92, 1.3), 4.6),
]


def construire_zoom(j):
    id_, titre, region, z = ZOOMS[j]
    i = [c[0] for c in CONSTR].index(id_)
    return _zoomer(CONSTR[i][4], region, z, CONSTR[i][3])


TRAITS = [
    ("trait fort", build.FORT, "#151515", "tout ce qui est <b>coupé</b> par le plan de coupe : murs, dalles, garde-corps et escalier coupés, montants coupés. Le contour est fort, l'intérieur reste clair (ou hachuré).", "2B bien taillé, appuyé"),
    ("trait moyen", build.MOYEN, "#151515", "ce que l'on <b>voit</b> au-delà de la coupe : arêtes des ouvertures, cadres, vantail, escalier au fond, garde-corps vu, limites de la façade.", "HB"),
    ("trait fin", build.FIN, "#151515", "le reste : <b>vitrage</b>, hachures du sol, arcs d'ouverture (pointillés), lignes cachées, noms des pièces, cotes.", "H, léger"),
    ("construction", 0.4, "#8a8a8a", "les traits de <b>construction géométrique</b> (diagonales, arcs de compas, parallèles de Thalès) : très légers, on les laisse visibles.", "2H, à peine appuyé"),
]


def legende_traits_html(mm=False):
    """les 4 épaisseurs de trait avec un échantillon (à l'échelle du papier du carnet)"""
    k = build.S and (build.A_CARNET * 10 / 200)
    lignes = []
    for nom, w, c, quoi, crayon in TRAITS:
        mmw = w * k
        lignes.append(f'<tr><td><svg width="46mm" height="4mm" viewBox="0 0 46 4"><line x1="1" y1="2" x2="45" y2="2" stroke="{c}" stroke-width="{mmw:.3f}"/></svg></td>'
                      f'<td><b>{nom}</b><br><span class="note">{mmw:.2f} mm · {crayon}</span></td><td>{quoi}</td></tr>')
    return '<div class="tab traits"><table><thead><tr><th>Échantillon</th><th>Trait</th><th>Où</th></tr></thead><tbody>' + "".join(lignes) + "</tbody></table></div>"


def blocs_web():
    """les sections de la page web : le trait, les constructions des coupes et façades, les détails"""
    cons = []
    for i, (id_, titre, k, vue, dessin, marges, etapes) in enumerate(CONSTR):
        fig = construire_vue(i)
        li = "".join(f'<li><span class="num" style="background:{COL["g"]}">{j+1}</span><span>{t}</span></li>' for j, t in enumerate(etapes))
        cons.append(f'<article class="cons large" style="border-color:{COL[k]}"><h3><span class="n" style="color:{COL[k]}">{i+1}</span>{html.escape(titre)}</h3>'
                    f'<div class="dessin zoom">{fig.svg(titre)}</div><ol class="etapes">{li}</ol></article>')
        for j, (zid, zt, zr, z) in enumerate(ZOOMS):
            if zid == id_:
                fz = construire_zoom(j)
                cons.append(f'<article class="cons large" style="border-color:{COL[k]}"><h3><span class="n" style="color:{COL[k]}">{i+1}\'</span>{html.escape(zt)} <span class="zoomtag">zoom × {z:g}</span></h3>'
                            f'<div class="dessin zoom">{fz.svg(zt)}</div></article>')
    det = []
    for i, (id_, titre, ech, f, steps) in enumerate(DETAILS):
        D = f()
        li = "".join(f'<li><span class="num" style="background:{COL["g"]}">{j+1}</span><span>{t}</span></li>' for j, t in enumerate(steps))
        det.append(f'<article class="cons large" style="border-color:{COL["e"]}"><h3><span class="n" style="color:{COL["e"]}">{i+1}</span>{html.escape(titre)} <span class="zoomtag">échelle {ech}</span></h3>'
                   f'<div class="dessin zoom">{D.svg(titre, mm=False)}</div><ol class="etapes">{li}</ol></article>')
    return f"""
  <section class="bloc" aria-labelledby="t-trait">
    <div class="surtitre">La qualité du trait · fort, moyen, fin</div>
    <h2 id="t-trait">Doser les traits : le fort là où l'on coupe</h2>
    <p class="intro">Règle de la prof : <b>trait fort là où il y a la coupe</b>, plus fin pour le reste, et bien doser. Quatre épaisseurs, de la plus appuyée à la plus légère (épaisseurs sur le papier du carnet, a = {build._vir(build.A_CARNET, 2)} cm) :</p>
    {legende_traits_html()}
    <p class="intro"><b>Dans l'ordre :</b> 1) les traits de construction, très légers ; 2) les traits fins (vitrages, hachures) ; 3) les traits moyens (ce qu'on voit) ; 4) en dernier, les traits forts sur tout ce qui est coupé. Ainsi la coupe ressort sans qu'on ait à repasser plusieurs fois.</p>
  </section>

  <section class="bloc" aria-labelledby="t-cvues">
    <div class="surtitre">Méthode 2 · les coupes et les façades</div>
    <h2 id="t-cvues">La construction géométrique des coupes et des façades</h2>
    <p class="intro">Même méthode que sur le plan : le bâtiment en gris pâle, les traits de construction par-dessus. <b>Les hauteurs se lisent sur l'échelle des e</b> : le tiers de a se construit par diagonale + milieu, puis chaque tiers se divise en 7 par Thalès (7 × 3 = 21 e = a). Toutes les hauteurs de la coupe tombent sur cette échelle.</p>
    <div class="cons-liste">{"".join(cons)}</div>
  </section>

  <section class="bloc" aria-labelledby="t-det">
    <div class="surtitre">Plus de détails · portes et fenêtres, en cm réels</div>
    <h2 id="t-det">Les détails : la porte, les fentes, les fenêtres</h2>
    <p class="intro"><b>Mesuré sur les feuilles :</b> le cadre de la porte (5 e), le passage (4 e), l'encadrement en saillie (0,07 a), les fentes (1/15 a), les fenêtres du jardin (1/8 a × 1/7 a). <b>Proposé (à valider avec la prof) :</b> les profils des cadres (e/2, e/3, e/6) et l'épaisseur du verre (1 cm). À l'échelle du carnet (1/72), 1 cm de verre ne fait que 0,14 mm : on dessine le vitrage en <b>un trait fin</b> ; l'épaisseur se montre sur ces détails à 1/10.</p>
    <div class="cons-liste">{"".join(det)}</div>
  </section>
"""

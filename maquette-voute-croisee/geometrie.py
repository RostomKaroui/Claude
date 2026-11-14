"""Maquette d'une voûte croisée (voûte d'arêtes) : géométrie exacte de toutes les pièces à découper.

Une voûte croisée = deux voûtes en berceau (demi-cylindres de rayon A) qui se croisent à angle droit.
Elle se compose de 4 « voûtains » (les 4 triangles courbes), de 2 arêtes diagonales qui se rejoignent
à la clef (le point le plus haut), de 4 arcs au bord et de 4 piliers aux angles.

Chaque voûtain est un morceau de CYLINDRE : une surface qui se déplie à plat sans déformation. Les 4
voûtains sont identiques ; chacun se découpe dans une seule feuille (avec la bande de l'arc, d'épaisseur B).

Repère (cm) : x vers l'est, y vers le nord, z vers le haut, centre de la voûte en (0, 0), dessus du socle z = 0.
Repère du patron (cm) : X vers la droite (le long de l'arc), Y vers le haut (depuis la clef vers le bord de l'arc),
on regarde la FACE INTÉRIEURE (la face imprimée = le dessous de la voûte).

Lancer :  python3 geometrie.py   ->  vérifie tout et écrit pieces.json
"""
import json, math, os, sys
import numpy as np

# ------------------------------------------------------------------ les choix de dimensions (cm)
A = 4.5            # demi-portée libre : rayon de chaque arc (portée libre entre piliers = 2A = 9 cm)
B = 1.5            # côté carré d'un pilier = profondeur (épaisseur) de chaque arc
H = 8.0            # hauteur des piliers = hauteur de la naissance des arcs
SOCLE = 14.0       # côté du socle carré
EP_SOCLE = 0.2     # épaisseur du socle (carton gris de 2 mm)
LANGUETTE_ARETE = 0.5   # largeur des languettes de colle le long des arêtes
LANGUETTE_PILIER = 1.0  # longueur des languettes posées sur la tête des piliers
COLLE_PILIER = 0.6      # languette de recouvrement d'un pilier
HAUT_TOTAL = EP_SOCLE + H + A          # 12,7 cm : sommet de la clef au-dessus de la table
L = math.pi * A / 2                    # demi-longueur de l'arc d'un voûtain (7,07 cm)

ICI = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------ le voûtain, plié et à plat
def w0(s):
    """bord de l'arête dans le patron : w = A |sin(s/A)|  (s = abscisse le long de l'arc, 0 à la clef)"""
    return A * np.abs(np.sin(np.asarray(s) / A))


def rot(k, x, y):
    """rotation de -90° x k autour de l'axe vertical : voûtain k (0 = est, 1 = sud, 2 = ouest, 3 = nord)"""
    c, s = [(1, 0), (0, -1), (-1, 0), (0, 1)][k % 4]    # cos, sin de -90°·k
    return x * c - y * s, x * s + y * c


def voutain_3d(k, s, w, kappa=None):
    """Point 3D (cm, z = 0 sur le socle) du voûtain k au point (s, w) de son patron.
    kappa = courbure du patron (1/A = voûtain en place ; 0 = patron à plat) : sert à l'animation."""
    s = np.asarray(s, float); w = np.asarray(w, float)
    if kappa is None:
        kappa = 1.0 / A
    if kappa < 1e-9:
        y = -s
        z = EP_SOCLE + H + A + 0 * s
    else:
        y = -np.sin(kappa * s) / kappa
        z = EP_SOCLE + H + A + (np.cos(kappa * s) - 1.0) / kappa
    x, y = rot(k, w, y)
    return np.array([x, y, z])


def contour_voutain():
    """contour du patron d'un voûtain (cm), sens trigonométrique, sans les languettes"""
    L = math.pi * A / 2
    s = np.linspace(0, L, 121)
    droite = [(float(si), float(w0(si))) for si in s]
    gauche = [(-float(si), float(w0(si))) for si in s[::-1]]
    haut = [(L, A + B), (-L, A + B)]
    return droite + haut + gauche


def languette_arete(n=60):
    """languette de colle le long de la demi-arête droite (s > 0) : bande de largeur LANGUETTE_ARETE,
    du côté du vide (sous la courbe). Renvoie la courbe, la courbe décalée et les entailles."""
    L = math.pi * A / 2
    s = np.linspace(0, L, n)
    w = w0(s)
    dw = np.cos(s / A)                               # pente de la courbe
    nx, ny = dw, -1.0                                # normale, vers le bas
    nn = np.hypot(nx, ny)
    nx, ny = nx / nn, ny / nn
    ex = s + LANGUETTE_ARETE * nx
    ey = w + LANGUETTE_ARETE * ny
    # entailles : tous les ~1 cm de courbe, de l'extérieur jusqu'à 1,5 mm du pli
    ds = np.hypot(np.diff(s), np.diff(w))
    cum = np.concatenate([[0], np.cumsum(ds)])
    entailles = []
    for t in np.arange(0.9, cum[-1] - 0.5, 0.9):
        i = int(np.argmin(abs(cum - t)))
        p_ext = (float(ex[i]), float(ey[i]))
        p_int = (float(s[i] + 0.15 * nx[i]), float(w[i] + 0.15 * ny[i]))
        entailles.append((p_ext, p_int))
    return list(zip(map(float, s), map(float, w))), list(zip(map(float, ex), map(float, ey))), entailles, float(cum[-1])


def patron_pilier():
    """patron d'un pilier (cm) : 4 faces B x H, languette de recouvrement, couvercle (haut) et fond (bas) sur la face 1"""
    faces = [(i * B, 0.0, (i + 1) * B, H) for i in range(4)]
    return dict(faces=faces, colle=[(4 * B, 0.0), (4 * B + COLLE_PILIER, 0.3), (4 * B + COLLE_PILIER, H - 0.3), (4 * B, H)],
                haut=(0.0, H, B, H + B), bas=(0.0, -B, B, 0.0), largeur=4 * B + COLLE_PILIER, hauteur=H + 2 * B)


# ------------------------------------------------------------------ les piliers dans la maquette
PILIERS = [(sx * (A + B / 2), sy * (A + B / 2)) for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1))]   # centres


# ------------------------------------------------------------------ vérifications
def verifier():
    res = {}
    L = math.pi * A / 2

    # 1. les 4 voûtains se touchent exactement le long des arêtes : bord droit de k = bord gauche de k+1
    s = np.linspace(0, L, 400)
    pire = 0.0
    for k in range(4):
        droit = voutain_3d(k, s, w0(s)).T                      # bord droit (s > 0) du voûtain k
        gauche = voutain_3d((k + 1) % 4, -s, w0(s)).T          # bord gauche (s < 0) du voûtain k+1
        pire = max(pire, float(np.max(np.linalg.norm(droit - gauche, axis=1))))
    res["ecart_aretes_cm"] = pire
    assert pire < 1e-9, pire

    # 2. la clef : les 4 voûtains se rejoignent au même point, à HAUT_TOTAL
    clefs = [voutain_3d(k, 0.0, 0.0) for k in range(4)]
    assert all(np.allclose(c, clefs[0]) for c in clefs)
    res["clef"] = [round(float(v), 4) for v in clefs[0]]
    assert abs(clefs[0][2] - HAUT_TOTAL) < 1e-9

    # 3. le patron est exact : le dépliage conserve toutes les longueurs (surface développable)
    ss = np.linspace(-L, L, 41)
    pire_iso = 0.0
    for k in (0,):
        for i in range(len(ss) - 1):
            for w in (w0(ss[i]) + 0.01, 3.0, A + B):
                p = voutain_3d(k, ss[i], w); q = voutain_3d(k, ss[i + 1], w)
                d3 = float(np.linalg.norm(p - q))
                # longueur de l'arc de cercle entre ss[i] et ss[i+1] : A * dtheta = dss exactement
                pire_iso = max(pire_iso, abs(d3 - 2 * A * math.sin((ss[i + 1] - ss[i]) / (2 * A))))
    res["ecart_isometrie_cm"] = pire_iso
    assert pire_iso < 1e-9

    # 4. longueur de l'arête (courbe) : même valeur dans le patron et dans la maquette, et pour les deux voûtains voisins
    sc = np.linspace(0, L, 4001)
    pat = np.hypot(np.diff(sc), np.diff(w0(sc))).sum()
    p3 = voutain_3d(0, sc, w0(sc)).T
    long3 = float(np.linalg.norm(np.diff(p3, axis=0), axis=1).sum())
    res["longueur_arete_cm"] = round(float(pat), 4)
    res["longueur_arete_3d_cm"] = round(long3, 4)
    assert abs(pat - long3) < 1e-4, (pat, long3)

    # 5. les dimensions annoncées
    res["longueur_arc_cm"] = round(math.pi * A, 4)
    res["portee_libre_cm"] = 2 * A
    res["diagonale_libre_cm"] = round(2 * A * math.sqrt(2), 3)
    res["emprise_cm"] = 2 * (A + B)
    res["hauteur_totale_cm"] = round(HAUT_TOTAL, 3)
    assert SOCLE >= 2 * (A + B) + 1.99
    # languette sur la tête d'un pilier : elle doit tenir dans le carré B x B
    assert LANGUETTE_PILIER <= B and B <= B

    # 6. les arcs sont en continuité avec les faces intérieures des piliers (tangente verticale à la naissance)
    p0 = voutain_3d(0, L, A); p1 = voutain_3d(0, L - 1e-6, A)
    assert abs(p0[2] - (EP_SOCLE + H)) < 1e-9 and abs(p0[1] + A) < 1e-9 and abs((p1 - p0)[1]) < 1e-5
    res["naissance_des_arcs_cm"] = round(EP_SOCLE + H, 3)
    return res


def table_points():
    """points pour tracer à la main l'arête du patron : s (cm depuis la clef), w (cm)"""
    L = math.pi * A / 2
    pts = [(float(s), round(float(w0(s)), 2)) for s in range(0, 8) if s <= L] + [(round(L, 2), round(float(w0(L)), 2))]
    return pts


if __name__ == "__main__":
    res = verifier()
    cont = contour_voutain()
    c, e, ent, lg = languette_arete()
    pil = patron_pilier()
    surf = float(np.trapezoid(np.maximum(A + B - w0(np.linspace(-L, L, 20001)), 0), np.linspace(-L, L, 20001)))
    pieces = [
        dict(id="socle", nom="Socle", nb=1, matiere="carton gris 2 mm", dim="14,0 × 14,0 cm (épaisseur 0,2 cm)"),
        dict(id="pilier", nom="Pilier", nb=4, matiere="bristol 200 g", dim=f"1,5 × 1,5 × {H:.1f} cm (patron {pil['largeur']:.1f} × {pil['hauteur']:.1f} cm)"),
        dict(id="voutain", nom="Voûtain", nb=4, matiere="bristol 200 g",
             dim=f"patron {math.pi * A + 2 * LANGUETTE_PILIER:.2f} × {A + B + 0.4:.2f} cm (arc {math.pi * A:.2f} cm)"),
        dict(id="cintre", nom="Gabarit de contrôle (facultatif)", nb=1, matiere="carton gris 2 mm", dim=f"demi-disque de rayon {A:.1f} cm ({2 * A:.1f} × {A:.1f} cm)"),
    ]
    data = dict(A=A, B=B, H=H, SOCLE=SOCLE, EP_SOCLE=EP_SOCLE, HAUT_TOTAL=HAUT_TOTAL, L=L,
                languette_arete=LANGUETTE_ARETE, languette_pilier=LANGUETTE_PILIER, colle_pilier=COLLE_PILIER,
                piliers=PILIERS, contour_voutain=cont, languette=dict(courbe=c, decalee=e, entailles=ent, longueur=lg),
                patron_pilier=pil, points_arete=table_points(), surface_voutain_cm2=round(surf, 2),
                pieces=pieces, verifications=res)
    json.dump(data, open(os.path.join(ICI, "pieces.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Vérifications :")
    for k, v in res.items():
        print(f"  {k:26s} {v}")
    print(f"surface d'un voûtain (patron, sans languettes) : {surf:.2f} cm²")
    print("points de l'arête (s, w) :", data["points_arete"])
    print("pieces.json écrit")

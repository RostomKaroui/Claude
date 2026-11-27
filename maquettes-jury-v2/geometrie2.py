"""Trois autres propositions : toutes les pièces travaillent (aucune n'est posée à plat sur le sol).
Même repère que geometrie.py. Lancer : python3 geometrie2.py -> maquettes2.json"""
import json, math, os, itertools
from geometrie import P2T, NOMS, sub, cross, dot, d
R = math.sqrt(2); S3 = math.sqrt(3); H = 0.8

# ---------- 4 · Le Miroir (symétrie) ----------
L30 = 2 * R * S3 / 2       # 2,45 : pied des ailes
MIROIR = {
    # la colonne dans le plan de symétrie : le carré, puis le parallélogramme penché ; dessous, un passage
    "C":  [(0, 0, 0), (R, 0, 0), (R, 0, R), (0, 0, R)],
    "Pa": [(R, 0, R), (2 * R, 0, R), (3 * R, 0, 0), (2 * R, 0, 0)],
    # les deux ailes, symétriques : un petit côté collé sur le faîtage, inclinées à 30°
    "G1": [(0, 0, R), (2 * R, 0, R), (0, L30, 0)],
    "G2": [(0, 0, R), (2 * R, 0, R), (0, -L30, 0)],
    # le porche est : deux poteaux symétriques et l'auvent posé dessus
    "P1": [(3 * R, R, 0), (3 * R, R, R), (2 * R, R, 0)],
    "P2": [(3 * R, -R, 0), (3 * R, -R, R), (2 * R, -R, 0)],
    "M":  [(2 * R, 0, R), (3 * R, R, R), (3 * R, -R, R)],
}
# ---------- 5 · Le Tipi des deux soleils (pliage) ----------
TIPI = {
    # le carré des deux grands triangles plié en toit : le faîtage est leur grand côté commun
    "G1": [(0, 0, R), (4, 0, R), (2, R, 0)],
    "G2": [(0, 0, R), (4, 0, R), (2, -R, 0)],
    # au milieu, le triangle moyen remplit exactement la coupe du toit : il sépare la chambre du matin et celle du soir
    "M":  [(2, -R, 0), (2, R, 0), (2, 0, R)],
    # aux deux bouts du faîtage, un poteau et son contrefort ; le second est le premier tourné d'un demi-tour
    "P1": [(0, 0, 0), (0, 0, R), (-R, 0, 0)],
    "P2": [(4, 0, 0), (4, 0, R), (4 + R, 0, 0)],
    # deux auvents en porte-à-faux au bout du faîtage : le carré à l'ouest, le parallélogramme à l'est
    "C":  [(0, -R / 2, R), (0, R / 2, R), (-R, R / 2, R), (-R, -R / 2, R)],
    "Pa": [(4, -R / 2, R), (4, R / 2, R), (4 + R, R / 2 + R, R), (4 + R, -R / 2 + R, R)],
}
# ---------- 6 · Le Belvédère (rampe) ----------
ZM = 2.0
BELVEDERE = {
    # deux murs-triangles en équerre, au nord et à l'est : l'un est l'autre tourné d'un quart de tour
    "G1": [(0, 4, 0), (4, 4, 0), (2, 4, 2)],
    "G2": [(4, 0, 0), (4, 4, 0), (4, 2, 2)],
    # l'auvent : son grand côté va d'une pointe à l'autre
    "M":  [(2, 4, 2), (4, 2, 2), (2, 2, 2)],
    # la plateforme à 3,75 cm, sur deux petits triangles croisés à angle droit
    "C":  [(2, 2, 1), (2 + R, 2, 1), (2 + R, 2 + R, 1), (2, 2 + R, 1)],
    "P1": [(2 + R / 2 - 1, 2.0, 0), (2 + R / 2 + 1, 2.0, 0), (2 + R / 2, 2.0, 1)],
    "P2": [(2.0, 2 + R / 2 - 1, 0), (2.0, 2 + R / 2 + 1, 0), (2.0, 2 + R / 2, 1)],
    # la rampe : le parallélogramme monte du sol jusqu'au bord ouest de la plateforme
}
# rampe : petit côté haut le long du bord ouest de la plateforme (x = 2, z = 1), grands côtés de 2 qui descendent vers l'ouest
_u = (0, R, 0)                              # bord ouest, 1,41
_w = (-1, -R, -1)                           # pente : 2 de long, à 45° du bord, descend de 1 vers le sud-ouest
_t0 = (2, 2, 1); _t1 = (2, 2 + R, 1)
BELVEDERE["Pa"] = [_t0, _t1, tuple(_t1[i] + _w[i] for i in range(3)), tuple(_t0[i] + _w[i] for i in range(3))]

CHEMINS = {
    "miroir": [(5.2, 0.6, 0), (1.85, 0.6, 0), (1.85, -0.6, 0), (-0.9, -0.6, 0)],
    "tipi": [(-1.9, 0.35, 0), (1.6, 0.35, 0)],
    "belvedere": None,   # calculé : pied de la rampe -> plateforme
}

def verifier(nom, P3, chemin):
    def plane(k):
        p = P3[k]; n = cross(sub(p[1], p[0]), sub(p[2], p[0])); m = math.sqrt(dot(n, n)); n = [x / m for x in n]
        assert all(abs(dot(n, sub(q, p[0]))) < 1e-6 for q in p), nom + " " + k + " non plane"
        return n, dot(n, p[0])
    def dedans(k, q, marge=1e-6):
        p = P3[k]; n, _ = plane(k)
        s = [dot(cross(sub(p[(i + 1) % len(p)], p[i]), sub(q, p[i])), n) for i in range(len(p))]
        return all(x > marge for x in s) or all(x < -marge for x in s)
    def traverse(a, b):
        n, c = plane(b); pa = P3[a]
        for i in range(len(pa)):
            u, v = pa[i], pa[(i + 1) % len(pa)]
            du, dv = dot(n, u) - c, dot(n, v) - c
            if du * dv < -1e-9:
                t = du / (du - dv); q = [u[j] + t * (v[j] - u[j]) for j in range(3)]
                if dedans(b, q): return True
        return False
    def dessus(x, y, z0):
        """hauteur libre au-dessus de z0 (sol de marche) au point (x, y)"""
        h = math.inf
        for k in P3:
            n, c = plane(k)
            if abs(n[2]) < 1e-9: continue
            z = (c - n[0] * x - n[1] * y) / n[2]
            if z > z0 + 0.02 and dedans(k, (x, y, z)): h = min(h, z - z0)
        return h
    def obstacle(x, y, z0):
        for k in P3:
            n, c = plane(k)
            if abs(n[2]) > 0.3: continue           # seules les pièces debout peuvent barrer le passage
            dist = n[0] * x + n[1] * y - c
            if abs(dist) < 0.1:
                for dz in (0.1, 0.4, 0.75):
                    q = (x - dist * n[0], y - dist * n[1], z0 + dz)
                    q = (q[0], q[1], (c - n[0] * q[0] - n[1] * q[1]) / n[2]) if abs(n[2]) > 1e-9 else q
                    if abs(n[2]) < 1e-9 and dedans(k, q, -1e-9): return k
        return None
    p2 = {}
    for k in P3:
        a, b = P3[k], P2T[k]; n = len(a)
        for s, sens in itertools.product(range(n), (1, -1)):
            c = [b[(s + sens * i) % n] for i in range(n)]
            if all(abs(d(a[i], a[j]) - d(c[i], c[j])) < 1e-6 for i in range(n) for j in range(n)): p2[k] = c; break
        else: raise AssertionError(f"{nom} {k} : pas la forme du tangram")
        assert max(v[2] for v in a) > 0.05, f"{nom} : {k} est posé à plat sur le sol"
    for a, b in itertools.permutations(P3, 2):
        assert not traverse(a, b), f"{nom} : {a} traverse {b}"
    assert min(v[2] for p in P3.values() for v in p) >= -1e-9
    mini, couvert, n = math.inf, 0, 0
    for p, q in zip(chemin, chemin[1:]):
        L = math.dist(p[:2], q[:2])
        for i in range(int(L / 0.02) + 1):
            t = i * 0.02 / L
            x, y, z = (p[j] + (q[j] - p[j]) * t for j in range(3))
            h = dessus(x, y, z); o = obstacle(x, y, z); n += 1
            assert o is None, f"{nom} : {o} barre le chemin en ({x:.2f}, {y:.2f})"
            if h < math.inf: mini = min(mini, h); couvert += 1
    assert mini >= H - 1e-9, f"{nom} : hauteur libre {mini:.2f}"
    print(f"{nom:10s} OK · aucune pièce au sol · hauteur libre mini {mini * 3.75:.1f} cm · chemin abrité sur {100 * couvert // n} %")
    return {k: {"nom": NOMS[k][0], "couleur": NOMS[k][1], "p3": [list(v) for v in P3[k]], "p2": [list(v) for v in p2[k]]} for k in P3}

if __name__ == "__main__":
    pied = BELVEDERE["Pa"][3]; pied2 = BELVEDERE["Pa"][2]
    bas = ((pied[0] + pied2[0]) / 2, (pied[1] + pied2[1]) / 2, 0.0)
    haut = (2.0, 2 + R / 2, 1.0)
    CHEMINS["belvedere"] = [(bas[0] - 0.9, bas[1] - 0.5, 0), bas, haut, (2.75, 2.75, 1.0)]
    out = {}
    for nom, P3 in [("miroir", MIROIR), ("tipi", TIPI), ("belvedere", BELVEDERE)]:
        out[nom] = {"pieces": verifier(nom, P3, CHEMINS[nom]), "chemin": CHEMINS[nom]}
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "maquettes2.json"), "w"), ensure_ascii=False)

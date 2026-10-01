"""Genere les schemas SVG des 5 formes de tangram et verifie la geometrie.

Unite : 1 carreau = 1/4 du cote du carre de depart (carre 4 x 4).
Verifications : chaque piece a la bonne forme, aucune superposition,
chaque forme est d'un seul tenant (pieces en contact par un cote).
"""
import json
import math
from itertools import combinations

# ---------- pieces de reference (carre 4x4) ----------
STD = {
    "G1": [(0, 0), (4, 0), (2, 2)],
    "G2": [(0, 0), (2, 2), (0, 4)],
    "M":  [(4, 4), (2, 4), (4, 2)],
    "P1": [(4, 0), (4, 2), (3, 1)],
    "C":  [(2, 2), (3, 1), (4, 2), (3, 3)],
    "P2": [(2, 2), (3, 3), (1, 3)],
    "Pa": [(0, 4), (1, 3), (3, 3), (2, 4)],
}
KIND = {"G1": "G", "G2": "G", "M": "M", "P1": "P", "P2": "P", "C": "C", "Pa": "Pa"}
B = ["M", "P1", "C", "P2", "Pa"]  # les 5 petites pieces


def tr(poly, dx, dy):
    return [(x + dx, y + dy) for x, y in poly]


def rot(poly, cx, cy, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(round(cx + c * (x - cx) - s * (y - cy), 9),
             round(cy + s * (x - cx) + c * (y - cy), 9)) for x, y in poly]


# ---------- les 5 formes ----------
F = {}

# 1. Translation : la moitie haute glisse le long de la diagonale de (2,-2)
F["faille"] = {k: (tr(v, 2, -2) if k in B else v) for k, v in STD.items()}

# 2. Rotation : G1 pivote de 90 deg autour du coin O(0,0)
F["porche"] = dict(STD, G1=rot(STD["G1"], 0, 0, 90))

# 3/4. Le carre des 5 petites pieces, pose sur la pointe, centre en O
LOSANGE = {
    "M":  [(0, -2), (2, 0), (0, 0)],
    "C":  [(-1, -1), (0, 0), (-1, 1), (-2, 0)],
    "P1": [(0, -2), (0, 0), (-1, -1)],
    "Pa": [(0, 0), (2, 0), (1, 1), (-1, 1)],
    "P2": [(1, 1), (0, 2), (-1, 1)],
}
G_GAUCHE = [(-2, 0), (0, 2), (-2, 4)]
F["chevron"] = dict(LOSANGE, G1=G_GAUCHE,
                    G2=[(-x, y) for x, y in G_GAUCHE])  # reflet axe vertical
G_HAUT = [(-1, 1), (1, 3), (-3, 3)]
F["torsion"] = dict(LOSANGE, G1=G_HAUT, G2=rot(G_HAUT, 0, 0, 180))

# 5. Symetrie glissee : reflet / axe horizontal y=0 puis glissement de 2
def vers_bas(p):  # sommet droit (4,4)->(2,0), quart de tour
    return [(-(y - 4) + 2, (x - 4)) for x, y in p]
F["pas"] = {"G1": STD["G1"], "G2": STD["G2"], **{k: vers_bas(STD[k]) for k in B}}


# ---------- verifications ----------
def area(p):
    return abs(sum(p[i][0] * p[i - 1][1] - p[i - 1][0] * p[i][1]
                   for i in range(len(p)))) / 2


def sides(p):
    return sorted(round(math.dist(p[i], p[i - 1]), 6) for i in range(len(p)))


def inside(pt, poly):
    x, y = pt
    n, ok = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            ok = not ok
    return ok


def contact(p, q):
    """longueur de cote commun entre deux pieces"""
    tot = 0.0
    for i in range(len(p)):
        a, b = p[i - 1], p[i]
        for j in range(len(q)):
            c, d = q[j - 1], q[j]
            ux, uy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(ux, uy)
            cr1 = ux * (c[1] - a[1]) - uy * (c[0] - a[0])
            cr2 = ux * (d[1] - a[1]) - uy * (d[0] - a[0])
            if abs(cr1) > 1e-6 or abs(cr2) > 1e-6:
                continue
            t1 = (ux * (c[0] - a[0]) + uy * (c[1] - a[1])) / L
            t2 = (ux * (d[0] - a[0]) + uy * (d[1] - a[1])) / L
            lo, hi = max(0, min(t1, t2)), min(L, max(t1, t2))
            tot += max(0, hi - lo)
    return tot


for name, fig in F.items():
    for k, p in fig.items():
        assert sides(p) == sides(STD[k]), (name, k)
    tot = sum(area(p) for p in fig.values())
    assert abs(tot - 16) < 1e-9, (name, tot)
    xs = [x for p in fig.values() for x, _ in p]
    ys = [y for p in fig.values() for _, y in p]
    step = 0.05
    n_over = 0
    y = min(ys) + step / 2 + 0.0123
    while y < max(ys):
        x = min(xs) + step / 2 + 0.0071
        while x < max(xs):
            if sum(inside((x, y), p) for p in fig.values()) > 1:
                n_over += 1
            x += step
        y += step
    assert n_over == 0, (name, "superposition", n_over)
    # connexite par cotes communs
    keys = list(fig)
    seen, todo = {keys[0]}, [keys[0]]
    while todo:
        a = todo.pop()
        for b in keys:
            if b not in seen and contact(fig[a], fig[b]) > 1e-6:
                seen.add(b)
                todo.append(b)
    assert len(seen) == 7, (name, "non connexe", seen)
    print(f"OK  {name:8s} aire={tot}  7 pieces, sans superposition, d'un seul tenant")

with open(__file__.replace("generer.py", "formes.json"), "w") as fh:
    json.dump({"std": STD, "formes": F, "kind": KIND}, fh)

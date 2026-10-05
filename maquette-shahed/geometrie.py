"""Geometrie 3D de la maquette de Shahed (reconstitution d'apres photos).

x : le long du pignon, y : profondeur, z : hauteur. Table = plan z = 0.
Verifie : formes exactes des pieces, aretes collees de meme longueur,
aucune piece ne traverse une autre. Ecrit pieces.json pour la page.
"""
import itertools
import json
import math
import os

R = math.sqrt(2)
H = R  # demi-diagonale utile

# 3D final (reconstitution d'après les 4 photos), 2D tangram (image en couleurs)
# x : le long du pignon du fond, y : vers l'avant (négatif), z : hauteur.
PIECES = {
    "G1": dict(nom="Grand triangle orange", couleur="#f4a93a",
               p3=[(0, 0, 0), (4, 0, 0), (2, 0, 2)],
               p2=[(0, 4), (4, 4), (2, 2)]),
    "G2": dict(nom="Grand triangle turquoise", couleur="#8fcfc3",
               p3=[(0, 0, 0), (2, 0, 2), (0, -2 * R, 0)],
               p2=[(2, 2), (0, 4), (0, 0)]),
    "M":  dict(nom="Triangle moyen jaune", couleur="#f5dc2a",
               p3=[(0, -R, 0), (2 * R, -R, 0), (R, -R, R)],
               p2=[(2, 0), (4, 2), (4, 0)]),
    "C":  dict(nom="Carré rouge", couleur="#e04b30",
               p3=[(R, -R, R), (R + 1, -R, R - 1), (R + 1, 0, R - 1), (R, 0, R)],
               p2=[(2, 2), (3, 3), (4, 2), (3, 1)]),
    "P1": dict(nom="Petit triangle bleu clair", couleur="#3cb2e4",
               p3=[(R, 0, R), (2 * R, -R, R), (R, -R, R)],
               p2=[(4, 4), (4, 2), (3, 3)]),
    "P2": dict(nom="Petit triangle vert", couleur="#16984a",
               p3=[(R, -R - 1, 0), (R + 1, -R, 0), (R - 1, -R, 0)],
               p2=[(2, 2), (3, 1), (1, 1)]),
    "Pa": dict(nom="Parallélogramme bleu", couleur="#1f5aa6",
               p3=[(4 - R, 0, R), (4, 0, 0), (4 - 1 / R, -1, 1 / R), (4 - R - 1 / R, -1, R + 1 / R)],
               p2=[(2, 0), (0, 0), (1, 1), (3, 1)]),
}

def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def norm(a): return math.sqrt(dot(a, a))
def L(p): return [round(math.dist(p[i], p[i - 1]), 6) for i in range(len(p))]
def ang(p, i): 
    a, b = sub(p[i - 1], p[i]), sub(p[(i + 1) % len(p)], p[i])
    return round(math.degrees(math.acos(dot(a, b) / norm(a) / norm(b))), 4)

# 1. chaque piece 3D est congruente a sa piece 2D (memes cotes, memes angles, plane)
for k, d in PIECES.items():
    p3, p2 = d["p3"], [(x, y, 0) for x, y in d["p2"]]
    assert L(p3) == L(p2), (k, L(p3), L(p2))
    assert [ang(p3, i) for i in range(len(p3))] == [ang(p2, i) for i in range(len(p2))], k
    n = cross(sub(p3[1], p3[0]), sub(p3[2], p3[0]))
    for q in p3[3:]:
        assert abs(dot(n, sub(q, p3[0]))) < 1e-9, (k, "non plane")
    assert all(q[2] >= -1e-9 for q in p3), (k, "sous la table")

# 2. aucune interpenetration
def frame(p):
    o = p[0]; e1 = sub(p[1], o); e1 = tuple(x / norm(e1) for x in e1)
    n = cross(sub(p[1], o), sub(p[2], o)); n = tuple(x / norm(n) for x in n)
    e2 = cross(n, e1)
    return o, e1, e2, n

def inside2(pt, poly, m):
    # strictement a l'interieur, a plus de m des bords (polygone convexe)
    s = 0
    for i in range(len(poly)):
        a, b = poly[i - 1], poly[i]
        c = (b[0]-a[0])*(pt[1]-a[1]) - (b[1]-a[1])*(pt[0]-a[0])
        c /= math.dist(a, b)
        if s == 0: s = 1 if c > 0 else -1
        if c * s < m: return False
    return True

def local(p, fr):
    o, e1, e2, n = fr
    return [(dot(sub(q, o), e1), dot(sub(q, o), e2)) for q in p]

def samples(p, k=40):
    out = []
    o = p[0]
    for i in range(1, len(p) - 1):
        a, b, c = p[0], p[i], p[i + 1]
        for u in range(1, k):
            for v in range(1, k - u):
                w = 1 - u / k - v / k
                out.append(tuple(a[j]*w + b[j]*u/k + c[j]*v/k for j in range(3)))
    return out

for (ka, A), (kb, B) in itertools.permutations(PIECES.items(), 2):
    fb = frame(B["p3"]); pb = local(B["p3"], fb)
    pa = A["p3"]
    # aretes de A coupant le plan de B -> points de la coupe
    d = [dot(sub(q, fb[0]), fb[3]) for q in pa]
    if max(d) > 1e-6 and min(d) < -1e-6:
        cuts = []
        for i in range(len(pa)):
            a, b, da, db = pa[i - 1], pa[i], d[i - 1], d[i]
            if (da > 1e-9 and db < -1e-9) or (da < -1e-9 and db > 1e-9):
                t = da / (da - db)
                cuts.append(tuple(a[j] + t * (b[j] - a[j]) for j in range(3)))
            elif abs(db) <= 1e-9:
                cuts.append(b)
        for s in range(len(cuts)):
            for t in range(len(cuts)):
                for k in range(1, 50):
                    q = tuple(cuts[s][j] + (cuts[t][j] - cuts[s][j]) * k / 50 for j in range(3))
                    assert not inside2(local([q], fb)[0], pb, 1e-3), (ka, kb, "se traversent")
    elif max(abs(x) for x in d) < 1e-9:
        for q in samples(pa):
            assert not inside2(local([q], fb)[0], pb, 1e-3), (ka, kb, "superposees")

# 3. collages : aretes communes
def edges(p): return [(p[i - 1], p[i]) for i in range(len(p))]
def on_seg(q, a, b):
    ab, aq = sub(b, a), sub(q, a)
    return norm(cross(ab, aq)) < 1e-9 and -1e-9 <= dot(ab, aq) <= dot(ab, ab) + 1e-9
contacts = {}
for (ka, A), (kb, B) in itertools.combinations(PIECES.items(), 2):
    tot = 0
    for a, b in edges(A["p3"]):
        for c, e in edges(B["p3"]):
            if on_seg(c, a, b) and on_seg(e, a, b): tot += math.dist(c, e)
            elif on_seg(a, c, e) and on_seg(b, c, e): tot += math.dist(a, b)
    # arete posee sur une face (C contre G1, C sous M)
    for X, Y in ((A, B), (B, A)):
        fb = frame(Y["p3"]); pb = local(Y["p3"], fb)
        for a, b in edges(X["p3"]):
            if abs(dot(sub(a, fb[0]), fb[3])) < 1e-9 and abs(dot(sub(b, fb[0]), fb[3])) < 1e-9:
                mid = tuple((a[j] + b[j]) / 2 for j in range(3))
                if inside2(local([mid], fb)[0], pb, 1e-6): tot = max(tot, math.dist(a, b))
    if tot > 1e-6: contacts[f"{ka}-{kb}"] = round(tot, 3)
print("contacts :", contacts)

ici = os.path.dirname(os.path.abspath(__file__))
json.dump({k: dict(nom=d["nom"], couleur=d["couleur"], p3=d["p3"], p2=d["p2"])
           for k, d in PIECES.items()}, open(os.path.join(ici, "pieces.json"), "w"))
print("OK : 7 pieces exactes, aucune ne traverse une autre")

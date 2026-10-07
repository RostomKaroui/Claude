"""Trois propositions pour le jury (séance 4), un tangram de 15 cm en double épaisseur.

Repère : x vers l'est, y vers le nord, z vers le haut. Le côté du carré vaut 4 unités
(1 unité = 3,75 cm) ; le personnage mesure 3 cm = 0,8 unité.
Lancer : python3 geometrie.py  ->  vérifie les 3 maquettes et écrit maquettes.json
"""
import json, math, os, itertools
R = math.sqrt(2); S3 = math.sqrt(3)
H = 0.8

# ---------- 1 · Le Papillon (pliage) ----------
V = R                      # le pli (noue) à 5,3 cm
PAPILLON = {
    # le carré des deux grands triangles, plié en V le long de leur grand côté commun
    "G1": [(0, 0, V), (4, 0, V), (2, S3, V + 1)],      # aile nord, relevée à 30°
    "G2": [(0, 0, V), (4, 0, V), (2, -S3, V + 1)],     # aile sud = aile nord tournée d'un demi-tour autour du pli
    # la colonne vertébrale sous le pli : le carré à l'est, le parallélogramme penché à l'ouest ; entre les deux, le passage
    "C":  [(4 - R, 0, 0), (4, 0, 0), (4, 0, V), (4 - R, 0, V)],
    "Pa": [(-R, 0, 0), (0, 0, 0), (R, 0, V), (0, 0, V)],
    # le pignon est, perpendiculaire au carré
    "M":  [(4, -R, 0), (4, R, 0), (4, 0, V)],
    # le bassin : deux petits triangles qui forment un carré, au pied du parallélogramme
    "P1": [(-R, -R / 2, 0), (-R, R / 2, 0), (-2 * R, -R / 2, 0)],
    "P2": [(-2 * R, R / 2, 0), (-2 * R, -R / 2, 0), (-R, R / 2, 0)],
}
# ---------- 2 · Les Sheds (translation) ----------
SHEDS = {
    # trois toits inclinés à 45°, translatés vers le nord : grand, grand, moyen
    "G1": [(0, 0, R), (4, 0, R), (2, -R, 0)],
    "G2": [(0, R, R), (4, R, R), (2, 0, 0)],
    "M":  [(2 - R, R + 1, 1), (2 + R, R + 1, 1), (2, R, 0)],
    # sous le haut de chaque toit, un appui ; entre les appuis, la fenêtre au nord
    "C":  [(2 - R / 2, 0, 0), (2 + R / 2, 0, 0), (2 + R / 2, 0, R), (2 - R / 2, 0, R)],
    "P1": [(0, R, 0), (0, R, R), (R, R, 0)],
    "P2": [(4, R, 0), (4, R, R), (4 - R, R, 0)],
    "Pa": [(R - 1, R + 1, 0), (R + 1, R + 1, 0), (R + 2, R + 1, 1), (R, R + 1, 1)],
}
# ---------- 3 · Le Kiosque (rotation) ----------
A, B, Cq, D = (-1.5, -0.5), (0.5, -0.5), (1.5, 0.5), (-0.5, 0.5)
KIOSQUE = {
    # le toit : le parallélogramme, seule pièce qui se retrouve elle-même après un demi-tour
    "Pa": [(*A, R), (*B, R), (*Cq, R), (*D, R)],
    # deux poteaux-contreforts : un petit triangle et le même tourné d'un demi-tour
    "P1": [(B[0], B[1], 0), (B[0], B[1], R), (B[0] + R, B[1], 0)],
    "P2": [(D[0], D[1], 0), (D[0], D[1], R), (D[0] - R, D[1], 0)],
    # deux grandes ailes à 45° qui portent les deux autres coins : sud-ouest et, tournée d'un demi-tour, nord-est
    "G1": [(A[0] - 2, A[1] - R, 0), (A[0] + 2, A[1] - R, 0), (*A, R)],
    "G2": [(Cq[0] + 2, Cq[1] + R, 0), (Cq[0] - 2, Cq[1] + R, 0), (*Cq, R)],
    # le sol du kiosque, tourné de 45°, au centre de la rotation
    "C":  [(1, 0, 0), (0, 1, 0), (-1, 0, 0), (0, -1, 0)],
    # la seule pièce sans paire : la terrasse face au couchant
    "M":  [(-2, -R, 0), (-2, R, 0), (-2 - R, 0, 0)],
}
P2T = {"G1": [(0, 4), (4, 4), (2, 2)], "G2": [(2, 2), (0, 4), (0, 0)], "M": [(2, 0), (4, 2), (4, 0)],
       "C": [(2, 2), (3, 3), (4, 2), (3, 1)], "P1": [(4, 4), (4, 2), (3, 3)], "P2": [(2, 2), (3, 1), (1, 1)],
       "Pa": [(2, 0), (0, 0), (1, 1), (3, 1)]}
NOMS = {"G1": ("Grand triangle orange", "#f4a93a"), "G2": ("Grand triangle turquoise", "#8fcfc3"),
        "M": ("Triangle moyen jaune", "#f5dc2a"), "C": ("Carré rouge", "#e04b30"),
        "P1": ("Petit triangle bleu clair", "#3cb2e4"), "P2": ("Petit triangle vert", "#16984a"),
        "Pa": ("Parallélogramme bleu", "#1f5aa6")}
CHEMINS = {"papillon": [(1.7, -2.7), (1.7, -0.3), (-1.0, -0.3)],
           "sheds": [(4.6, 1.1), (-0.9, 1.1)],
           "kiosque": [(3.0, 0.0), (-2.6, 0.0)]}

d = math.dist
def sub(a, b): return [a[i] - b[i] for i in range(len(a))]
def cross(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def dot(a, b): return sum(x * y for x, y in zip(a, b))


def verifier(nom, P3):
    def plane(k):
        p = P3[k]; n = cross(sub(p[1], p[0]), sub(p[2], p[0])); m = math.sqrt(dot(n, n)); n = [x / m for x in n]
        assert all(abs(dot(n, sub(q, p[0]))) < 1e-9 for q in p), nom + " " + k + " non plane"
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
            if du * dv < -1e-12:
                t = du / (du - dv); q = [u[j] + t * (v[j] - u[j]) for j in range(3)]
                if dedans(b, q): return True
        return False
    def hauteur(x, y):
        h = math.inf
        for k in P3:
            n, c = plane(k)
            if abs(n[2]) < 1e-9: continue
            z = (c - n[0] * x - n[1] * y) / n[2]
            if z > 1e-6 and dedans(k, (x, y, z)): h = min(h, z)
        return h
    def obstacle(x, y):
        """une pièce verticale coupe-t-elle le personnage (cylindre de rayon 0,1) ?"""
        for k in P3:
            n, c = plane(k)
            if abs(n[2]) > 1e-9: continue
            dist = n[0] * x + n[1] * y - c
            if abs(dist) < 0.1:
                for z in (0.05, 0.4, 0.75):
                    q = (x - dist * n[0], y - dist * n[1], z)
                    if dedans(k, q, -1e-9): return k
        return None
    p2 = {}
    for k in P3:
        a, b = P3[k], P2T[k]; n = len(a)
        for s, sens in itertools.product(range(n), (1, -1)):
            c = [b[(s + sens * i) % n] for i in range(n)]
            if all(abs(d(a[i], a[j]) - d(c[i], c[j])) < 1e-6 for i in range(n) for j in range(n)): p2[k] = c; break
        else: raise AssertionError(f"{nom} {k} : pas la forme du tangram")
    for a, b in itertools.permutations(P3, 2):
        assert not traverse(a, b), f"{nom} : {a} traverse {b}"
    assert min(v[2] for p in P3.values() for v in p) >= -1e-9
    ch = CHEMINS[nom]; mini = math.inf; couvert = 0; n = 0
    for (x0, y0), (x1, y1) in zip(ch, ch[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        for i in range(int(L / 0.02) + 1):
            x, y = x0 + (x1 - x0) * i * 0.02 / L, y0 + (y1 - y0) * i * 0.02 / L
            h = hauteur(x, y); o = obstacle(x, y); n += 1
            assert o is None, f"{nom} : {o} barre le chemin en ({x:.2f}, {y:.2f})"
            if h < math.inf: mini = min(mini, h); couvert += 1
    assert mini >= H - 1e-9, f"{nom} : hauteur libre {mini:.2f} < 3 cm"
    print(f"{nom:9s} OK · hauteur libre mini {mini * 3.75:.1f} cm · chemin abrité sur {100 * couvert // n} %")
    return {k: {"nom": NOMS[k][0], "couleur": NOMS[k][1], "p3": [list(v) for v in P3[k]], "p2": [list(v) for v in p2[k]]} for k in P3}


if __name__ == "__main__":
    out = {}
    for nom, P3 in [("papillon", PAPILLON), ("sheds", SHEDS), ("kiosque", KIOSQUE)]:
        out[nom] = {"pieces": verifier(nom, P3), "chemin": CHEMINS[nom]}
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "maquettes.json"), "w"), ensure_ascii=False)

"""Maquette du jury (séance 4) : un seul tangram de 15 cm, en double épaisseur (2 tangrams collés).

Repère : x vers l'est, y vers le nord, z vers le haut ; le côté du carré vaut 4 unités
(1 unité = 3,75 cm). Le personnage mesure 3 cm = 0,8 unité.
Lancer : python3 geometrie.py  ->  vérifie tout et écrit pieces.json
"""
import json, math, os, itertools
R = math.sqrt(2)
H = 0.8   # personnage de 3 cm

# Position finale (3D) de chaque pièce
P3 = {
    # deux murs pignons parallèles, debout sur leur grand côté : le mur sud est le mur nord translaté de 5,3 cm
    "G1": [(0, R, 0), (4, R, 0), (2, R, 2)],            # mur nord
    "G2": [(0, 0, 0), (4, 0, 0), (2, 0, 2)],            # mur sud
    # versant ouest (45°) : le carré, du faîtage jusqu'à mi-pente ; dessous, le cadrage vers le couchant
    "C":  [(1, 0, 1), (2, 0, 2), (2, R, 2), (1, R, 1)],
    # versant est (45°) : deux petits triangles qui forment le même carré, tourné d'un demi-tour
    "P1": [(2, 0, 2), (3, 0, 1), (2, R, 2)],
    "P2": [(3, R, 1), (2, R, 2), (3, 0, 1)],
    # casquette horizontale à 3,75 cm, sous le bas du carré, tournée de 45° vers le sud-ouest
    "Pa": [(1, 0, 1), (1, R, 1), (1 - R, 0, 1), (1 - R, -R, 1)],
    # terrasse du couchant, à plat sur le sol devant le cadrage ouest
    "M":  [(0, -R, 0), (0, R, 0), (-R, 0, 0)],
}
# Position dans le carré du tangram (même tangram que les séances précédentes)
P2 = {"G1": [(0, 4), (4, 4), (2, 2)], "G2": [(2, 2), (0, 4), (0, 0)], "M": [(2, 0), (4, 2), (4, 0)],
      "C": [(2, 2), (3, 3), (4, 2), (3, 1)], "P1": [(4, 4), (4, 2), (3, 3)], "P2": [(2, 2), (3, 1), (1, 1)],
      "Pa": [(2, 0), (0, 0), (1, 1), (3, 1)]}
NOMS = {"G1": ("Grand triangle orange", "#f4a93a"), "G2": ("Grand triangle turquoise", "#8fcfc3"),
        "M": ("Triangle moyen jaune", "#f5dc2a"), "C": ("Carré rouge", "#e04b30"),
        "P1": ("Petit triangle bleu clair", "#3cb2e4"), "P2": ("Petit triangle vert", "#16984a"),
        "Pa": ("Parallélogramme bleu", "#1f5aa6")}

d = lambda a, b: math.dist(a, b)
def sub(a, b): return [a[i] - b[i] for i in range(len(a))]
def cross(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def dot(a, b): return sum(x * y for x, y in zip(a, b))


def apparier(k):
    """ordonne p2 pour que chaque sommet corresponde au sommet 3D (mêmes distances), miroir permis"""
    a, b = P3[k], P2[k]; n = len(a)
    for s in range(n):
        for sens in (1, -1):
            c = [b[(s + sens * i) % n] for i in range(n)]
            if all(abs(d(a[i], a[j]) - d(c[i], c[j])) < 1e-9 for i in range(n) for j in range(n)):
                return c
    raise AssertionError(k + " : la forme 3D n'est pas celle du tangram")


def plane(k):
    p = P3[k]; n = cross(sub(p[1], p[0]), sub(p[2], p[0])); m = math.sqrt(dot(n, n)); n = [x / m for x in n]
    assert all(abs(dot(n, sub(q, p[0]))) < 1e-9 for q in p), k + " non plane"
    return n, dot(n, p[0])


def dedans(k, q, marge=1e-6):
    """q (dans le plan de k) est-il strictement à l'intérieur du polygone convexe k ?"""
    p = P3[k]; n, _ = plane(k)
    s = [dot(cross(sub(p[(i + 1) % len(p)], p[i]), sub(q, p[i])), n) for i in range(len(p))]
    return all(x > marge for x in s) or all(x < -marge for x in s)


def traverse(a, b):
    """une arête de a perce-t-elle l'intérieur de b ?"""
    n, c = plane(b)
    pa = P3[a]
    for i in range(len(pa)):
        u, v = pa[i], pa[(i + 1) % len(pa)]
        du, dv = dot(n, u) - c, dot(n, v) - c
        if du * dv < -1e-12:
            t = du / (du - dv); q = [u[j] + t * (v[j] - u[j]) for j in range(3)]
            if dedans(b, q): return True
    return False


def hauteur_libre(x, y):
    """hauteur libre au-dessus du point (x, y) du sol, sous la pièce la plus basse qui le couvre"""
    h = math.inf
    for k in P3:
        n, c = plane(k)
        if abs(n[2]) < 1e-9: continue
        z = (c - n[0] * x - n[1] * y) / n[2]
        if z > 1e-6 and dedans(k, (x, y, z)): h = min(h, z)
    return h


if __name__ == "__main__":
    for k in P3: plane(k)
    p2 = {k: apparier(k) for k in P3}
    for a, b in itertools.permutations(P3, 2):
        assert not traverse(a, b), f"{a} traverse {b}"
    assert min(v[2] for p in P3.values() for v in p) >= 0
    # promenade : de l'entrée est (x = 3,5) à la terrasse (x = -0,7), sur l'axe du passage
    y0 = R / 2
    for i in range(0, 61):
        x = 3.5 - i * 4.2 / 60
        assert hauteur_libre(x, y0) >= H - 1e-9 or hauteur_libre(x, y0) == math.inf, f"trop bas en x={x:.2f}"
    couvert = [x / 20 for x in range(-14, 80) if hauteur_libre(x / 20, y0) < math.inf]
    print("hauteur sous faîtage :", round(hauteur_libre(1.98, y0), 3), " sous casquette :", round(hauteur_libre(-0.2, 0.0), 3),
          " parcours abrité de x =", min(couvert), "à", max(couvert))
    out = {k: {"nom": NOMS[k][0], "couleur": NOMS[k][1], "p3": [list(v) for v in P3[k]], "p2": [list(v) for v in p2[k]]} for k in P3}
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pieces.json"), "w"), ensure_ascii=False)
    print("OK : 7 pièces exactes, aucune ne traverse une autre, le personnage de 3 cm passe partout")

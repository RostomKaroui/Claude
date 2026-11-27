"""Maquette commune : Le Pli (Rostom), la maquette de Shahed et celle de Yassmine sur un même socle.

Les trois maquettes gardent leur géométrie exacte (fichiers pieces.json de chaque dossier),
à la même échelle : le côté du carré du tangram vaut 4 unités. Chacune est tournée pour que
son ouverture regarde la cour centrale. Lancer : python3 geometrie.py  ->  pieces.json
"""
import json, math, os

ici = os.path.dirname(os.path.abspath(__file__))
racine = os.path.dirname(ici)
lire = lambda d: json.load(open(os.path.join(racine, d, "pieces.json"), encoding="utf-8"))

R2 = math.sqrt(2)
# polygones 3D (x est, y nord, z haut) de chaque maquette, dans son propre repère
pli = [p["p3"] for p in lire("maquette").values()]
shahed = [p["p3"] for p in lire("maquette-shahed").values() if p["p3"]]
yas = [[[c * R2 for c in v] for v in p["p3"]] for p in lire("maquette-yassmine")["pieces"].values()]  # a -> carré de côté 4

MAQUETTES = {
    # ouverture : direction (dans le repère de la maquette) du côté qui doit regarder la cour
    # porte : point d'arrivée du chemin, dans le repère de la maquette
    "pli": dict(nom="Le Pli", auteur="Rostom", couleur="#e0a43a", polys=pli, ouverture=(0, 1), porte=(2.7, 1.9),
                lumiere="lumière rasante dans le couloir"),
    "shahed": dict(nom="Maquette de Shahed", auteur="Shahed", couleur="#3d7fc4", polys=shahed, ouverture=(0, -1), porte=(-2.6, -0.3),
                   lumiere="lumière basse sous la tablette"),
    "yassmine": dict(nom="Maquette de Yassmine", auteur="Yassmine", couleur="#c8503d", polys=yas, ouverture=(1, 1), porte=(1.0 * R2, 1.9 * R2),
                     lumiere="lumière par l'encoche"),
}
PLACE = {"pli": (-5.0, 4.4), "shahed": (5.0, 4.4), "yassmine": (0.0, -5.5)}   # centre de chaque maquette sur le socle
COUR = dict(centre=(0.0, 0.7), rayon=2.4)
SOCLE = 20.0
ENTREE = (-10.0, -6.5)   # le chemin arrive par le coin sud-ouest du socle


def centre(polys):
    xs = [v[0] for p in polys for v in p]; ys = [v[1] for p in polys for v in p]
    return ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)


def placer(k):
    m = MAQUETTES[k]
    cx, cy = centre(m["polys"])
    px, py = PLACE[k]
    vers_cour = math.atan2(COUR["centre"][1] - py, COUR["centre"][0] - px)
    th = vers_cour - math.atan2(m["ouverture"][1], m["ouverture"][0])
    c, s = math.cos(th), math.sin(th)
    f = lambda v: [round(px + (v[0] - cx) * c - (v[1] - cy) * s, 4), round(py + (v[0] - cx) * s + (v[1] - cy) * c, 4)] + ([round(v[2], 4)] if len(v) > 2 else [])
    return [[f(v) for v in p] for p in m["polys"]], f(m["porte"]), th


def emprise(polys):
    """enveloppe convexe de l'emprise au sol (monotone chain)"""
    pts = sorted({(v[0], v[1]) for p in polys for v in p})
    def cr(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cr(hi[-2], hi[-1], p) <= 0: hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def dist_cour(poly):
    cx, cy = COUR["centre"]
    return min(math.hypot(x - cx, y - cy) for x, y in poly)


if __name__ == "__main__":
    out = {"socle": SOCLE, "cour": COUR, "maquettes": {}}
    emps = {}
    for k, m in MAQUETTES.items():
        polys, porte, th = placer(k)
        emps[k] = emprise(polys)
        h = max(v[2] for p in polys for v in p)
        out["maquettes"][k] = dict(nom=m["nom"], auteur=m["auteur"], couleur=m["couleur"], lumiere=m["lumiere"],
                                   polys=polys, porte=porte, hauteur=round(h, 3))
        print(f"{m['nom']:22s} rotation {math.degrees(th):7.1f}°  hauteur {h:.2f}  distance à la cour {dist_cour(emps[k]) - COUR['rayon']:.2f}")
    # chemins : entrée -> cour, puis cour -> chaque porte
    cx, cy = COUR["centre"]
    out["chemins"] = [[list(ENTREE), [cx - 1.6, cy - 1.7]]] + [[[cx, cy], out["maquettes"][k]["porte"][:2]] for k in ("pli", "shahed", "yassmine")]
    # contrôles : emprises dans le socle et sans chevauchement (test des sommets)
    def dedans(p, poly):
        n, ins = len(poly), False
        for i in range(n):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
            if (y1 > p[1]) != (y2 > p[1]) and p[0] < x1 + (p[1] - y1) * (x2 - x1) / (y2 - y1): ins = not ins
        return ins
    for k, e in emps.items():
        assert all(abs(x) < SOCLE / 2 - 0.3 and abs(y) < SOCLE / 2 - 0.3 for x, y in e), k + " déborde du socle"
        for j, f in emps.items():
            if j != k: assert not any(dedans(p, f) for p in e), k + " chevauche " + j
        assert dist_cour(e) > COUR["rayon"] + 0.3, k + " touche la cour"
    json.dump(out, open(os.path.join(ici, "pieces.json"), "w"), ensure_ascii=False)
    print("OK : pieces.json écrit")

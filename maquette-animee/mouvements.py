"""Maquette du jury : le montage animé, du tangram posé à plat jusqu'à la maquette finie.

Chaque pièce ne bouge que par TRANSLATION (glisse sur la table ou le long du pli), ROTATION
(tourne à plat sur la table, autour d'un de ses coins) ou PLIAGE (se relève autour d'un de ses
côtés, qui reste posé). Aucune pièce n'est enlevée du tangram puis reposée ailleurs.

Le script :
  1. part du tangram posé en losange, sa diagonale dans l'axe est–ouest (axe de la vue) ;
  2. applique les mouvements et vérifie que chaque pièce arrive exactement à sa place
     dans la maquette finale (geometrie2.py, MIROIR) ;
  3. vérifie à chaque instant (pas de 1/60) qu'aucune pièce n'en traverse une autre et
     qu'une pièce qui glisse à plat passe bien sous les pentes (épaisseur du carton comprise) ;
  4. écrit mouvements.json pour la page.

Repère : x vers l'est, y vers le nord, z vers le haut, table en z = 0 ; 1 unité = 3,75 cm.
Lancer : python3 mouvements.py
"""
import json, math, os, sys, itertools
import numpy as np

ici = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ici, "..", "maquettes-jury-v2"))
from geometrie import P2T, NOMS          # noqa: E402
from geometrie2 import MIROIR, CHEMINS, verifier as verifier_final  # noqa: E402

R = math.sqrt(2)
EP = 0.08            # double épaisseur de carton : 3 mm
CM = 3.75            # 1 unité = 3,75 cm
H = 0.8              # personnage de 3 cm


def cm(u):
    return f"{u * CM:.1f}".replace(".", ",")


# ---------- 1 · le tangram posé en losange ----------
def losange(u, v):
    s = math.sqrt(0.5)
    return (s * (-(u - 2) + (v - 2)), -s * ((u - 2) + (v - 2)))


# Les deux grands triangles ont leur face de référence en haut (z = EP) : leur carton est sous
# cette face. Ainsi, une fois pliés, le dessus du pli est exactement à 5,3 cm.
DEPART = {k: [(*losange(*p), EP if k in ("G1", "G2") else 0.0) for p in P2T[k]] for k in P2T}

# Place finale : la maquette choisie. G1 (orange) et P1 (bleu clair) sont au sud dans le
# tangram, ils vont au sud ; G2 (turquoise) et P2 (vert) vont au nord.
FINAL = dict(MIROIR)
FINAL["G1"], FINAL["G2"] = MIROIR["G2"], MIROIR["G1"]
FINAL["P1"], FINAL["P2"] = MIROIR["P2"], MIROIR["P1"]


# ---------- 2 · les mouvements ----------
def T(v):
    return {"type": "T", "v": list(v)}


def Rot(c, axe, angle, leve=(0, 0, 0), glisse=(0, 0, 0)):
    """Rotation de `angle` degrés autour de la droite (c, axe) ; en plus, une translation
    leve * sin(angle parcouru) + glisse * t (pour le pli : la ligne de pli monte pendant
    que les pieds glissent sur la table)."""
    return {"type": "R", "c": list(c), "axe": list(axe), "angle": angle, "leve": list(leve), "glisse": list(glisse)}


E, N, S, O = "vers l'est", "vers le nord", "vers le sud", "vers l'ouest"
X = (1, 0, 0)
Z = (0, 0, 1)
L = 4 * R / 2        # 2,83 : demi-diagonale du carré = côté de l'angle droit d'un grand triangle

ETAPES = [
    {"titre": "Le tangram", "pieces": [],
     "texte": "Deux tangrams de 15 cm collés : 7 pièces en double épaisseur. Le carré est posé en losange : sa diagonale suit l'axe est–ouest, l'axe de la vue vers le coucher du soleil.",
     "logique": "Toutes les pièces partent d'ici et ne quittent jamais la table d'un coup : elles glissent, tournent ou se relèvent.",
     "mouvements": []},
    {"titre": "Le pli", "pieces": ["G1", "G2"],
     "texte": "Les deux grands triangles se relèvent ensemble autour de leur côté commun : la ligne de pli monte à 5,3 cm, les deux pointes glissent sur la table vers l'axe.",
     "logique": "Un seul pli donne la couverture : deux pentes à 30°, l'une vers le nord, l'autre vers le sud. Le pli est l'axe de symétrie de toute la maquette.",
     "mouvements": [
         {"type": "PLIAGE", "texte": "30° chacun : la ligne de pli monte à 5,3 cm",
          "ops": {"G2": Rot((0, 0, EP), X, -30, leve=(0, 0, L), glisse=(0, 0, -EP)),
                  "G1": Rot((0, 0, EP), X, 30, leve=(0, 0, L), glisse=(0, 0, -EP))}}]},
    {"titre": "L'appui nord", "pieces": ["P2"],
     "texte": "Le petit triangle vert glisse vers l'est sous la pente nord, puis vers le nord, et se relève.",
     "logique": "Debout, il tient un coin du toit de l'entrée. Son grand côté descend vers l'intérieur : l'entrée s'ouvre en biais.",
     "mouvements": [
         {"type": "TRANSLATION", "texte": f"{cm(3 * R)} cm {E}, sous la pente nord", "ops": {"P2": T((3 * R, 0, 0))}, "voir": True},
         {"type": "TRANSLATION", "texte": f"{cm(R)} cm {N}", "ops": {"P2": T((0, R, 0))}},
         {"type": "PLIAGE", "texte": "90° : il se relève autour de son petit côté", "ops": {"P2": Rot((0, R, 0), X, 90)}}]},
    {"titre": "L'appui sud", "pieces": ["P1"],
     "texte": "Le petit triangle bleu clair contourne le pied de la pente sud, glisse vers l'est, revient vers le nord et se relève.",
     "logique": "C'est l'appui nord renversé de l'autre côté de l'axe : la même pièce, le même geste, en symétrie.",
     "mouvements": [
         {"type": "TRANSLATION", "texte": f"{cm(1.2)} cm {S}, pour contourner le pied de la pente", "ops": {"P1": T((0, -1.2, 0))}},
         {"type": "TRANSLATION", "texte": f"{cm(3 * R)} cm {E}", "ops": {"P1": T((3 * R, 0, 0))}},
         {"type": "TRANSLATION", "texte": f"{cm(1.2)} cm {N}", "ops": {"P1": T((0, 1.2, 0))}},
         {"type": "PLIAGE", "texte": "90° : il se relève autour de son petit côté", "ops": {"P1": Rot((0, -R, 0), X, -90)}}]},
    {"titre": "Le toit de l'entrée", "pieces": ["M"],
     "texte": "Le triangle moyen monte à la hauteur du pli, puis glisse le long du pli jusqu'aux deux appuis.",
     "logique": "Il continue la ligne de pli à l'horizontale : l'entrée est couverte, à 5,3 cm, à l'est.",
     "mouvements": [
         {"type": "TRANSLATION", "texte": f"{cm(R)} cm vers le haut, à la hauteur du pli", "ops": {"M": T((0, 0, R))}},
         {"type": "TRANSLATION", "texte": f"{cm(4 * R)} cm {E}, le long du pli", "ops": {"M": T((4 * R, 0, 0))}}]},
    {"titre": "La paroi penchée", "pieces": ["Pa"],
     "texte": "Le parallélogramme tourne d'un quart de tour sur la table autour de son coin, se relève, puis glisse vers l'est sous le pli.",
     "logique": "Il tient le pli par en dessous. Penché, il laisse sous lui un passage pour le personnage, d'un côté de l'axe à l'autre.",
     "mouvements": [
         {"type": "ROTATION", "texte": "90°, sens inverse des aiguilles d'une montre, autour de son coin", "ops": {"Pa": Rot((-R, 0, 0), Z, 90)}},
         {"type": "PLIAGE", "texte": "90° : il se relève autour de son petit côté", "ops": {"Pa": Rot((0, 0, 0), X, 90)}},
         {"type": "TRANSLATION", "texte": f"{cm(4 * R)} cm {E}, sous le pli", "ops": {"Pa": T((4 * R, 0, 0))}, "voir": True}]},
    {"titre": "La paroi de la vue", "pieces": ["C"],
     "texte": "Le carré se relève autour de son côté nord, puis glisse vers l'est sous le pli.",
     "logique": "Debout dans l'axe, à l'ouest, il partage la vue en deux cadrages sur le coucher du soleil.",
     "mouvements": [
         {"type": "PLIAGE", "texte": "90° : il se relève autour de son côté nord", "ops": {"C": Rot((0, 0, 0), X, -90)}},
         {"type": "TRANSLATION", "texte": f"{cm(R)} cm {E}, sous le pli", "ops": {"C": T((R, 0, 0))}, "voir": True}]},
]


def matrice(op, t):
    """Matrice 4x4 (repère maths) du mouvement `op` arrivé à la fraction t."""
    M = np.eye(4)
    if op["type"] == "T":
        M[:3, 3] = np.array(op["v"]) * t
        return M
    a = math.radians(op["angle"] * t)
    k = np.array(op["axe"], float); k /= np.linalg.norm(k)
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    Rm = np.eye(3) + math.sin(a) * K + (1 - math.cos(a)) * K @ K
    c = np.array(op["c"], float)
    M[:3, :3] = Rm
    M[:3, 3] = c - Rm @ c + np.array(op["leve"]) * abs(math.sin(a)) + np.array(op["glisse"]) * t
    return M


def appliquer(M, pts):
    P = np.c_[np.array(pts, float), np.ones(len(pts))]
    return (M @ P.T).T[:, :3]


# ---------- 3 · vérifications ----------
def normale(P):
    n = np.cross(P[1] - P[0], P[2] - P[0])
    return n / np.linalg.norm(n)


def dedans(P, q, marge=1e-6):
    n = normale(P)
    s = [np.dot(np.cross(P[(i + 1) % len(P)] - P[i], q - P[i]), n) for i in range(len(P))]
    return all(x > marge for x in s) or all(x < -marge for x in s)


def traverse(A, B):
    """Une arête de A passe-t-elle à travers l'intérieur de B ?"""
    n = normale(B); c = np.dot(n, B[0])
    for i in range(len(A)):
        u, v = A[i], A[(i + 1) % len(A)]
        du, dv = np.dot(n, u) - c, np.dot(n, v) - c
        if du * dv < -1e-9:
            q = u + du / (du - dv) * (v - u)
            if dedans(B, q, 1e-4): return True
    return False


def a_plat(P):
    return max(p[2] for p in P) < EP + 0.03


def chevauche_2d(A, B, marge=1e-4, plan=None):
    """Deux pièces convexes dans un même plan se recouvrent-elles ? (axes séparateurs).
    Par défaut le plan est la table ; sinon `plan` = deux vecteurs qui le portent."""
    if plan is not None:
        A = np.array([[np.dot(p, plan[0]), np.dot(p, plan[1])] for p in A])
        B = np.array([[np.dot(p, plan[0]), np.dot(p, plan[1])] for p in B])
    for P in (A, B):
        for i in range(len(P)):
            e = P[(i + 1) % len(P)][:2] - P[i][:2]
            ax = np.array([-e[1], e[0]]) / np.linalg.norm(e)
            a = [np.dot(ax, p[:2]) for p in A]; b = [np.dot(ax, p[:2]) for p in B]
            if max(a) <= min(b) + marge or max(b) <= min(a) + marge: return False
    return True


def meme_plan(A, B):
    na, nb = normale(A), normale(B)
    if abs(abs(np.dot(na, nb)) - 1) > 1e-6 or abs(np.dot(na, B[0] - A[0])) > 1e-6: return None
    u = (A[1] - A[0]) / np.linalg.norm(A[1] - A[0])
    return u, np.cross(na, u)


def hauteur_sous(P, x, y):
    """Hauteur de la face de dessous de la pièce inclinée P au point (x, y), ou None."""
    n = normale(P)
    if abs(n[2]) < 1e-6 or abs(n[2]) > 0.999: return None
    z = (np.dot(n, P[0]) - n[0] * x - n[1] * y) / n[2]
    if not dedans(P, np.array([x, y, z]), 1e-6): return None
    return z - EP / abs(n[2])        # le carton des grands triangles est sous la face de référence


def points(P, pas=0.08):
    """Points d'une pièce à plat : sommets, bords et intérieur."""
    out = [p for p in P]
    for i in range(len(P)):
        u, v = P[i], P[(i + 1) % len(P)]
        k = int(np.linalg.norm(v - u) / pas) + 1
        out += [u + (v - u) * j / k for j in range(k)]
    c = sum(P) / len(P)
    out += [c + (p - c) * f for p in out for f in (0.33, 0.66)]
    return out


def verifier():
    pose = {k: np.eye(4) for k in DEPART}
    pires = {"jeu": math.inf}
    for e in ETAPES[1:]:
        for m in e["mouvements"]:
            for t in np.linspace(0, 1, 61):
                cur = {k: pose[k] if k not in m["ops"] else matrice(m["ops"][k], t) @ pose[k] for k in DEPART}
                P = {k: appliquer(cur[k], DEPART[k]) for k in DEPART}
                for a, b in itertools.permutations(P, 2):
                    if a_plat(P[a]) and a_plat(P[b]):
                        assert not chevauche_2d(P[a], P[b]), f"{e['titre']} · {m['texte']} · t={t:.2f} : {a} recouvre {b} sur la table"
                    elif meme_plan(P[a], P[b]) is not None:
                        assert not chevauche_2d(P[a], P[b], plan=meme_plan(P[a], P[b])), f"{e['titre']} · {m['texte']} · t={t:.2f} : {a} recouvre {b}"
                    else:
                        assert not traverse(P[a], P[b]), f"{e['titre']} · {m['texte']} · t={t:.2f} : {a} traverse {b}"
                # une pièce qui glisse à plat doit passer sous les pentes, carton compris
                for k in m["ops"]:
                    if not a_plat(P[k]): continue
                    dessus = (EP if k == "M" else EP / 2) + max(p[2] for p in P[k])
                    for g in ("G1", "G2"):
                        if g in m["ops"]: continue
                        for q in points(P[k]):
                            h = hauteur_sous(P[g], q[0], q[1])
                            if h is not None:
                                pires["jeu"] = min(pires["jeu"], h - dessus)
                                assert h - dessus > 0.02, f"{e['titre']} · {m['texte']} · t={t:.2f} : {k} touche {g} ({h - dessus:.3f})"
                # aucune pièce sous la table
                for k in P:
                    assert min(p[2] for p in P[k]) > -1e-6, f"{e['titre']} · {k} passe sous la table"
            for k in m["ops"]:
                pose[k] = matrice(m["ops"][k], 1) @ pose[k]
    # arrivée : chaque pièce exactement à sa place dans la maquette choisie
    for k in DEPART:
        A = appliquer(pose[k], DEPART[k]); B = np.array(FINAL[k], float)
        ok = all(min(np.linalg.norm(a - b) for b in B) < 1e-6 for a in A)
        assert ok, f"{k} n'arrive pas à sa place :\n{A.round(3)}\n{B.round(3)}"
    return pires


if __name__ == "__main__":
    pires = verifier()
    n = sum(len(e["mouvements"]) for e in ETAPES)
    print(f"OK · {n} mouvements, contrôlés à chaque 1/60 : aucune collision ; "
          f"chaque pièce arrive à sa place. Jeu mini sous les pentes : {pires['jeu'] * CM * 10:.1f} mm")
    pieces = verifier_final("miroir", FINAL, CHEMINS["miroir"])
    out = {"depart": DEPART, "pieces": {k: {"nom": NOMS[k][0], "couleur": NOMS[k][1]} for k in DEPART},
           "etapes": ETAPES, "chemin": CHEMINS["miroir"], "ep": EP}
    json.dump(out, open(os.path.join(ici, "mouvements.json"), "w"), ensure_ascii=False)
    print("mouvements.json écrit")

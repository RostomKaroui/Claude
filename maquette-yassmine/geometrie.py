"""Maquette de Yassmine : géométrie des 5 panneaux, reconstituée à partir de ses 5 photos.

Méthode : chaque panneau a une forme connue (relevée sur les photos grâce aux lignes
tracées au crayon). On a recalé les 4 points de vue (photos 1, 2, 3 et 5 ; la 4 est la
même que la 5) sur les sommets visibles, en imposant les arêtes collées. Erreur moyenne
de recalage : environ 5 px sur des photos de 540 px de large. La verticale vient des
4 appareils photo, tous tenus droits : la maquette touche la table par le bas du grand
plan incliné, le grand côté du triangle ouest, le bas du triangle nord et le bas du trapèze.

Unité : a = petit côté du petit triangle du tangram = c / (2*racine(2)), c = côté du carré.
Repère : x vers l'est, y vers le nord, z vers le haut, table en z = 0.
Lancer : python3 geometrie.py  ->  vérifie les formes et écrit pieces.json
"""
import json, math, os

R2 = math.sqrt(2)
H = R2 / 2

# Formes à plat (unités a) : sommets du contour, puis points des lignes tracées.
FORMES = {
    # grand triangle rectangle isocèle, côtés de l'angle droit 2*R2 (= c), angle droit en C
    "tri": {"T": (-2, 0), "BL": (2, 0), "C": (0, 2), "M": (0, 0), "R": (-1, 1), "B": (1, 1), "sT": (-1, 0), "sB": (1, 0)},
    # hexagone à encoche
    "hex": {"NW": (0, 0), "NE": (2, 0), "E": (3, 1), "O": (1, 1), "SE": (2, 2), "SW": (0, 2), "N1": (1, 0), "W1": (0, 1)},
    # trapèze rectangle : deux triangles moyens et deux petits autour de Q
    "trap": {"A": (-R2, 0), "B": (-R2, R2), "Cc": (0, R2), "D": (R2, 0), "Q": (0, 0), "mid": (H, H)},
    # triangle moyen coupé par sa hauteur
    "moy": {"V": (0, 0), "P1": (R2, 0), "P2": (0, R2), "H": (H, H)},
}

# Position finale (unités a), issue du recalage sur les photos.
FINAL = {
    "Br": {"M": [-1.595, -0.256, 0.023], "T": [-1.764, 1.736, 0.046], "BL": [-1.426, -2.249, 0.0], "C": [-1.452, -0.267, 2.018],
           "R": [-1.608, 0.735, 1.032], "B": [-1.439, -1.258, 1.009], "sT": [-1.679, 0.74, 0.035], "sB": [-1.51, -1.253, 0.012]},
    "W": {"M": [-0.22, 0.969, 1.037], "T": [-1.44, -0.31, 1.972], "BL": [1.0, 2.249, 0.102], "C": [-1.783, 1.743, 0.057],
          "R": [-1.611, 0.716, 1.015], "B": [-0.391, 1.996, 0.079], "sT": [-0.83, 0.329, 1.504], "sB": [0.39, 1.609, 0.569]},
    "N": {"NW": [-1.462, -0.839, 1.466], "N1": [-0.462, -0.839, 1.466], "NE": [0.538, -0.839, 1.466], "E": [1.538, -1.541, 0.755],
          "O": [-0.462, -1.541, 0.755], "SE": [0.538, -2.244, 0.044], "SW": [-1.462, -2.244, 0.044], "W1": [-1.462, -1.541, 0.755]},
    "Z1": {"Q": [0.753, 0.316, 0.776], "A": [0.533, -0.877, 1.503], "B": [1.562, -1.513, 0.771], "Cc": [1.783, -0.32, 0.044],
           "D": [0.973, 1.509, 0.05], "mid": [1.378, 0.594, 0.047]},
    "WT": {"V": [-0.867, 0.22, 1.595], "P1": [0.1, -0.797, 1.418], "P2": [-0.032, 1.133, 0.91], "H": [0.034, 0.168, 1.164]},
}

# Points de vue des photos (même repère) : position, point visé, champ vertical en degrés.
PHOTOS = {
    "photo-1": {"pos": [3.841, 1.851, 7.781], "cible": [0.673, 0.479, 0.516], "fov": 54.0},
    "photo-2": {"pos": [-1.188, 4.745, 6.264], "cible": [-0.426, 0.317, 0.595], "fov": 56.3},
    "photo-3": {"pos": [-3.864, -1.515, 6.792], "cible": [-0.414, -0.676, 0.579], "fov": 58.9},
    "photo-5": {"pos": [0.23, -4.587, 6.766], "cible": [-0.099, -0.765, 0.443], "fov": 60.6},
}

PANNEAUX = {
    "Br": dict(nom="Grand triangle ouest", couleur="#d9822b", forme="tri", contour=["C", "T", "BL"],
               lignes=[("M", "C"), ("M", "R"), ("M", "B"), ("R", "B")],
               plat=dict(o=(5.6, 1.15), rot=0)),
    "W": dict(nom="Grand triangle nord", couleur="#2f6db5", forme="tri", contour=["T", "C", "BL"],
              lignes=[("M", "R"), ("M", "C"), ("M", "B"), ("R", "sT"), ("B", "sB")],
              plat=dict(o=(5.6, -1.6), rot=0)),
    "N": dict(nom="Grand plan incliné", couleur="#e7b93a", forme="hex", contour=["NW", "NE", "E", "O", "SE", "SW"],
              lignes=[("O", "NW"), ("O", "N1"), ("O", "NE"), ("O", "W1"), ("O", "SW")],
              plat=dict(o=(8.4, 1.7), rot=0)),
    "Z1": dict(nom="Trapèze est", couleur="#3a9b72", forme="trap", contour=["A", "B", "Cc", "D"],
               lignes=[("Q", "B"), ("Q", "Cc"), ("Q", "mid")],
               plat=dict(o=(9.9, -2.4), rot=0)),
    "WT": dict(nom="Triangle de liaison", couleur="#c8463a", forme="moy", contour=["V", "P1", "P2"],
               lignes=[("V", "H")],
               plat=dict(o=(12.0, -0.9), rot=0)),
}
ORDRE = ["Br", "W", "N", "Z1", "WT"]


def d3(a, b):
    return math.dist(a, b)


def verifier():
    """Chaque panneau 3D doit avoir exactement la forme du gabarit (distances conservées)."""
    pire = 0
    for k, p in PANNEAUX.items():
        F, X = FORMES[p["forme"]], FINAL[k]
        cles = list(F)
        for i in range(len(cles)):
            for j in range(i + 1, len(cles)):
                e = abs(d3(F[cles[i]], F[cles[j]]) - d3(X[cles[i]], X[cles[j]]))
                pire = max(pire, e)
    # arêtes collées : écart entre les points qui doivent coïncider
    paires = [(("Br", "C"), ("W", "T")), (("Br", "T"), ("W", "C")), (("Br", "BL"), ("N", "SW")),
              (("Z1", "A"), ("N", "NE")), (("Z1", "B"), ("N", "E"))]
    ecart = max(d3(FINAL[a][b], FINAL[c][d]) for (a, b), (c, d) in paires)
    sol = min(v[2] for X in FINAL.values() for v in X.values())
    return pire, ecart, sol


def plat(k):
    """Contour et points à plat sur la table (à droite de la maquette)."""
    p = PANNEAUX[k]
    ox, oy = p["plat"]["o"]
    a = math.radians(p["plat"]["rot"])
    out = {}
    for n, (u, v) in FORMES[p["forme"]].items():
        out[n] = (round(ox + u * math.cos(a) - v * math.sin(a), 4), round(oy + u * math.sin(a) + v * math.cos(a), 4))
    return out


if __name__ == "__main__":
    pire, ecart, sol = verifier()
    print(f"forme : écart max {pire:.3f} a · arêtes collées : écart max {ecart:.3f} a · point le plus bas z = {sol:.3f}")
    assert pire < 0.01 and ecart < 0.1 and sol > -0.01
    out = {}
    for k in ORDRE:
        p = PANNEAUX[k]
        P2 = plat(k)
        out[k] = {
            "nom": p["nom"], "couleur": p["couleur"],
            "p3": [FINAL[k][n] for n in p["contour"]],
            "p2": [P2[n] for n in p["contour"]],
            "l3": [[FINAL[k][a], FINAL[k][b]] for a, b in p["lignes"]],
        }
    ici = os.path.dirname(os.path.abspath(__file__))
    json.dump({"pieces": out, "photos": PHOTOS}, open(os.path.join(ici, "pieces.json"), "w"), ensure_ascii=False)
    print("OK : pieces.json écrit,", len(out), "panneaux")

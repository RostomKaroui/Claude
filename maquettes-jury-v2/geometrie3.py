"""Trois variantes dans l'esprit du Miroir (symétrie, colonne, ailes, passage), sans étage.
Toutes les pièces travaillent. Lancer : python3 geometrie3.py -> maquettes3.json"""
import json, math, os
from geometrie2 import verifier
R = math.sqrt(2); L30 = R * math.sqrt(3)     # 2,45 : pied d'une aile à 30°
G = R / 2                                     # demi-largeur de la fente

# ---------- 7 · La Fente : deux demi-toits symétriques séparés par un puits de lumière ----------
FENTE = {
    "G1": [(0, G, R), (2 * R, G, R), (0, G + L30, 0)],
    "G2": [(0, -G, R), (2 * R, -G, R), (0, -G - L30, 0)],
    # le linteau relie les deux faîtages à l'ouest ; le parallélogramme le porte dans l'axe
    "C":  [(0, -G, R), (R, -G, R), (R, G, R), (0, G, R)],
    "Pa": [(0, 0, R), (R, 0, R), (0, 0, 0), (-R, 0, 0)],
    # à l'est, deux poteaux symétriques et l'auvent qui pointe vers le soleil levant
    "P1": [(2 * R, G, 0), (2 * R, G, R), (3 * R, G, 0)],
    "P2": [(2 * R, -G, 0), (2 * R, -G, R), (3 * R, -G, 0)],
    "M":  [(2 * R, -R, R), (2 * R, R, R), (3 * R, 0, R)],
}
# ---------- 8 · L'Oiseau : les ailes se relèvent, une tête vers le couchant, une queue vers le levant ----------
OISEAU = {
    "C":  [(0, 0, 0), (R, 0, 0), (R, 0, R), (0, 0, R)],
    "Pa": [(R, 0, R), (2 * R, 0, R), (3 * R, 0, 0), (2 * R, 0, 0)],
    "G1": [(0, 0, R), (2 * R, 0, R), (0, L30, R + R)],
    "G2": [(0, 0, R), (2 * R, 0, R), (0, -L30, R + R)],
    # la queue : deux petits triangles symétriques, à plat à 5,3 cm, au bout est du pli
    "P1": [(2 * R, 0, R), (3 * R, 0, R), (2 * R, R, R)],
    "P2": [(2 * R, 0, R), (3 * R, 0, R), (2 * R, -R, R)],
    # la tête : le triangle moyen, à plat, pointe vers l'ouest
    "M":  [(0, -R, R), (0, R, R), (-R, 0, R)],
}
# ---------- 9 · Le Miroir tourné : l'aile sud est l'aile nord tournée d'un demi-tour ----------
TOURNE = {
    "C":  [(0, 0, 0), (R, 0, 0), (R, 0, R), (0, 0, R)],
    "Pa": [(R, 0, R), (2 * R, 0, R), (3 * R, 0, 0), (2 * R, 0, 0)],
    "G1": [(0, 0, R), (2 * R, 0, R), (0, L30, 0)],
    "G2": [(0, 0, R), (2 * R, 0, R), (2 * R, -L30, 0)],
    # le porche du couchant, à l'ouest
    "P1": [(-R, R, 0), (-R, R, R), (0, R, 0)],
    "P2": [(-R, -R, 0), (-R, -R, R), (0, -R, 0)],
    "M":  [(0, 0, R), (-R, R, R), (-R, -R, R)],
}
CHEMINS = {
    "fente":  [(4.7, 0.0, 0), (1.6, 0.0, 0), (1.0, 0.35, 0), (0.15, 0.35, 0)],
    "oiseau": [(4.6, 0.5, 0), (-0.9, 0.5, 0)],
    "tourne": [(4.6, 0.8, 0), (1.85, 0.8, 0), (1.85, -0.6, 0), (-0.9, -0.6, 0)],
}
if __name__ == "__main__":
    out = {}
    for nom, P3 in [("fente", FENTE), ("oiseau", OISEAU), ("tourne", TOURNE)]:
        out[nom] = {"pieces": verifier(nom, P3, CHEMINS[nom]), "chemin": CHEMINS[nom]}
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "maquettes3.json"), "w"), ensure_ascii=False)

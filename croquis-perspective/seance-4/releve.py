"""Relevé des détails sur la photo redressée : joints des pavés, fer forgé bleu, taches d'enduit.

Chaque fonction rend une liste de polylignes en px (cadre 720 x 960) ; croquis4.py les repasse au crayon.
Les zones (sol, mur...) sont des polygones en px ; la végétation, la moto et la main sont retirées par masque.
"""
import cv2, numpy as np
from skimage.morphology import skeletonize

VOISINS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def masque_poly(polys, forme=(960, 720)):
    m = np.zeros(forme, np.uint8)
    for p in polys:
        cv2.fillPoly(m, [np.array(p, np.int32)], 255)
    return m


def squelette_en_lignes(sq, lmin=8, eps=1.2):
    """suit le squelette (pixels à 1) et le découpe en polylignes entre les bouts et les croisements"""
    sq = sq.astype(bool).copy()
    H, W = sq.shape
    pad = np.pad(sq, 1)
    deg = sum(np.roll(np.roll(pad, dy, 0), dx, 1) for dy, dx in VOISINS)[1:-1, 1:-1] * sq
    vu = np.zeros_like(sq)
    lignes = []

    def voisins(y, x):
        for dy, dx in VOISINS:
            yy, xx = y + dy, x + dx
            if 0 <= yy < H and 0 <= xx < W and sq[yy, xx]:
                yield yy, xx

    def suivre(y, x):
        chemin = [(x, y)]; vu[y, x] = True
        while True:
            nxt = [(yy, xx) for yy, xx in voisins(y, x) if not vu[yy, xx]]
            if not nxt: break
            y, x = nxt[0]; chemin.append((x, y)); vu[y, x] = True
            if deg[y, x] != 2: break
        return chemin

    depart = list(zip(*np.where(sq & (deg != 2))))
    for y, x in depart:
        for yy, xx in voisins(y, x):
            if not vu[yy, xx]:
                vu[y, x] = True
                ch = [(x, y)] + suivre(yy, xx)
                lignes.append(ch)
    for y, x in zip(*np.where(sq & ~vu)):          # les boucles fermées
        if not vu[y, x]: lignes.append(suivre(y, x))
    out = []
    for ch in lignes:
        a = np.array(ch, np.float32)
        if len(a) < 2: continue
        L = np.sum(np.hypot(*np.diff(a, axis=0).T))
        if L < lmin: continue
        a = cv2.approxPolyDP(a.reshape(-1, 1, 2), eps, False).reshape(-1, 2)
        out.append(a)
    return out


def joints_paves(img, zone, bloc=35, C=10, ouvre=3, lmin=10, echelle=2):
    """les joints sombres entre les pavés -> squelette -> traits"""
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    g = cv2.resize(g, None, fx=echelle, fy=echelle, interpolation=cv2.INTER_CUBIC)
    cl = cv2.createCLAHE(2.5, (6, 6)).apply(g)
    b = cv2.GaussianBlur(cl, (7, 7), 0)
    th = cv2.adaptiveThreshold(b, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, bloc, C)
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, np.ones((ouvre, ouvre), np.uint8))
    z = cv2.resize(zone, (th.shape[1], th.shape[0]), interpolation=cv2.INTER_NEAREST)
    th &= z
    sq = skeletonize(th > 0)
    return [l / echelle for l in squelette_en_lignes(sq, lmin * echelle, 1.5)]


def fer_bleu(hi, zone, lmin=6, echelle=2, s_min=70, eps=1.3):
    """le fer forgé bleu (grilles, balcons) sur la photo 2x -> squelette -> traits en px du cadre"""
    im = hi
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    m = cv2.inRange(hsv, (92, s_min, 60), (128, 255, 255))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    z = cv2.resize(zone, (m.shape[1], m.shape[0]), interpolation=cv2.INTER_NEAREST)
    m &= z
    sq = skeletonize(m > 0)
    return [l / echelle for l in squelette_en_lignes(sq, lmin * echelle, eps * echelle)]


def taches(hi, zone, bloc=121, C=9, aire_min=60, eps=1.8, echelle=2):
    """les plaques d'enduit tombé (plus sombres que le mur blanc) sur la photo 2x -> contours en px du cadre"""
    g = cv2.cvtColor(hi, cv2.COLOR_BGR2GRAY)
    zone = cv2.resize(zone, (g.shape[1], g.shape[0]), interpolation=cv2.INTER_NEAREST)
    b = cv2.GaussianBlur(g, (9, 9), 0)
    th = cv2.adaptiveThreshold(b, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, bloc, C)
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    th &= zone
    cs, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    out = []
    for c in cs:
        if cv2.contourArea(c) < aire_min * echelle**2: continue
        a = cv2.approxPolyDP(c, eps * echelle, True).reshape(-1, 2).astype(float) / echelle
        out.append(np.vstack([a, a[:1]]))
    return out


def vert(hi):
    """masque de la végétation (en px du cadre)"""
    hsv = cv2.cvtColor(hi, cv2.COLOR_BGR2HSV)
    m = cv2.inRange(hsv, (33, 35, 25), (92, 255, 255))
    m = cv2.resize(cv2.dilate(m, np.ones((9, 9), np.uint8)), (720, 960), interpolation=cv2.INTER_AREA)
    return np.where(m > 40, 255, 0).astype(np.uint8)

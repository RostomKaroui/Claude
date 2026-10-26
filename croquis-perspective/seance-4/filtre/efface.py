"""Efface les personnes de la photo d'origine, sans modèle externe : remplissage par exemples (Criminisi et al., 2004).
On remplit le masque morceau par morceau, en commençant par le bord ; chaque morceau est recopié depuis l'endroit voisin
de la photo qui lui ressemble le plus (pavés, mur, portes). Les arêtes qui entrent dans le masque sont prolongées en priorité.
Seule la zone masquée change ; tout le reste de la photo est identique à l'original.
Lancer : python3 efface.py <photo> <masque-personnes.png> -> photo-sans-personnes.png"""
import sys
import cv2
import numpy as np

R = 6                 # demi-côté du morceau recopié (13 x 13 px)
FENETRE = 170         # on cherche le modèle à moins de 170 px


def remplir(img, trou, source, wx=1.0, wy=2.0):
    """remplit trou ; les modèles ne sont pris que là où source est vrai ; wx, wy : coût d'un décalage horizontal / vertical"""
    img = img.astype(np.float32).copy()
    trou = trou.copy()
    H, W = trou.shape
    conf = (~trou).astype(np.float32)
    lab = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2Lab).astype(np.float32)
    k = 2 * R + 1
    while trou.any():
        # le front : pixels du trou qui touchent le connu
        t8 = trou.astype(np.uint8)
        front = np.argwhere((t8 - cv2.erode(t8, np.ones((3, 3), np.uint8))) > 0)
        # priorité = confiance x terme de données (isophote . normale)
        cs = cv2.boxFilter(conf, -1, (k, k), normalize=False) / (k * k)
        g = cv2.cvtColor(np.clip(img, 0, 255).astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
        g[trou] = 0
        gx, gy = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3), cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3)
        connu = cv2.erode((~trou).astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
        gx[~connu] = 0; gy[~connu] = 0
        gx = cv2.dilate(np.abs(gx), np.ones((5, 5), np.uint8)) * np.sign(cv2.GaussianBlur(gx, (5, 5), 0))
        gy = cv2.dilate(np.abs(gy), np.ones((5, 5), np.uint8)) * np.sign(cv2.GaussianBlur(gy, (5, 5), 0))
        mf = cv2.GaussianBlur(trou.astype(np.float32), (5, 5), 0)
        nx, ny = cv2.Sobel(mf, cv2.CV_32F, 1, 0, ksize=3), cv2.Sobel(mf, cv2.CV_32F, 0, 1, ksize=3)
        nn = np.hypot(nx, ny) + 1e-6
        fy, fx = front[:, 0], front[:, 1]
        data = np.abs(-gy[fy, fx] * nx[fy, fx] / nn[fy, fx] + gx[fy, fx] * ny[fy, fx] / nn[fy, fx]) / 255 + 0.001
        # on traite plusieurs points du front par tour (les plus prioritaires, assez éloignés entre eux)
        ordre = np.argsort(-(cs[fy, fx] * data))
        pris = []
        for i in ordre[:60]:
            y, x = front[i]
            if any(abs(y - py) <= 2 * R and abs(x - px) <= 2 * R for py, px in pris): continue
            pris.append((y, x))
            y0, y1, x0, x1 = max(0, y - R), min(H, y + R + 1), max(0, x - R), min(W, x + R + 1)
            cible = lab[y0:y1, x0:x1]; inc = trou[y0:y1, x0:x1]
            if inc.all(): continue
            # fenêtre de recherche
            sy0, sy1 = max(0, y - FENETRE), min(H, y + FENETRE + 1)
            sx0, sx1 = max(0, x - FENETRE), min(W, x + FENETRE + 1)
            src = lab[sy0:sy1, sx0:sx1]
            ph, pw = cible.shape[:2]
            masque_m = np.repeat((~inc).astype(np.float32)[..., None], 3, 2)
            ssd = cv2.matchTemplate(src, cible, cv2.TM_SQDIFF, mask=masque_m)
            # interdit : les morceaux qui touchent le trou ou sortent de la source
            bad = cv2.boxFilter((trou | ~source)[sy0:sy1, sx0:sx1].astype(np.float32), -1, (pw, ph), normalize=False,
                                anchor=(0, 0), borderType=cv2.BORDER_CONSTANT)[:ssd.shape[0], :ssd.shape[1]]
            ssd[bad > 0] = np.inf
            # léger avantage aux modèles proches (et à la même hauteur : pavés en rangs)
            yy, xx = np.mgrid[0:ssd.shape[0], 0:ssd.shape[1]]
            ssd = ssd * (1 + 0.0009 * np.hypot((yy + sy0 - y0) * wy, (xx + sx0 - x0) * wx))
            if not np.isfinite(ssd).any(): continue
            by, bx = np.unravel_index(np.argmin(ssd), ssd.shape)
            sy, sx = sy0 + by, sx0 + bx
            img[y0:y1, x0:x1][inc] = img[sy:sy + ph, sx:sx + pw][inc]
            lab[y0:y1, x0:x1][inc] = lab[sy:sy + ph, sx:sx + pw][inc]
            conf[y0:y1, x0:x1][inc] = cs[y, x]
            trou[y0:y1, x0:x1][inc] = False
    return np.clip(img, 0, 255).astype(np.uint8)


def pied(x):
    """pied de la façade sur la photo d'origine : au-dessus la façade, en dessous les pavés"""
    return 1640 - 0.064 * (x - 600)


if __name__ == "__main__":
    im = cv2.imread(sys.argv[1])
    m = cv2.imread(sys.argv[2], cv2.IMREAD_GRAYSCALE) > 127
    Hh, Ww = m.shape
    yy, xx = np.mgrid[0:Hh, 0:Ww]
    facade = yy < pied(xx)
    exclu = np.zeros_like(m)
    exclu[:, 1425:] = True                                   # le mur de droite tout proche (autre plan)
    exclu[1760:1920, 1320:1480] = True                       # le sac poubelle
    out = im.copy()
    # 1. la façade : on prolonge à la verticale (portes, montants, mur), modèles pris sur la façade seulement
    # 2. le sol : on prolonge les rangées de pavés à l'horizontale, modèles pris sur le sol seulement
    for nom, zone, src_zone, wx, wy in (("façade", facade, facade & (yy < pied(xx) - 4), 5.0, 0.6),
                                        ("sol", ~facade, ~facade & (yy > pied(xx) + 4), 0.6, 5.0)):
        trou = m & zone
        n, comp, st, _ = cv2.connectedComponentsWithStats(trou.astype(np.uint8))
        for i in range(1, n):                       # chaque zone séparément, dans sa boîte avec du contexte
            x, y, w, h = st[i, :4]
            a = FENETRE + 60
            y0, y1, x0, x1 = max(0, y - a), min(Hh, y + h + a), max(0, x - a), min(Ww, x + w + a)
            src = src_zone[y0:y1, x0:x1] & ~m[y0:y1, x0:x1] & ~exclu[y0:y1, x0:x1]
            out[y0:y1, x0:x1] = remplir(out[y0:y1, x0:x1], comp[y0:y1, x0:x1] == i, src, wx, wy)
            print(nom, i, "rempli", flush=True)
    cv2.imwrite("photo-sans-personnes.png", out)
    print("photo-sans-personnes.png écrit")

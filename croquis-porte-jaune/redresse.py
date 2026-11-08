"""Redresse la photo de la porte jaune : verticales verticales, horizon horizontal.

Méthode (la photo a des données EXIF : 24 mm équivalent 35 mm -> focale ~1400 px quand la photo est réduite à 1500 x 2000) :
  1. point de fuite des verticales VV = (650 ; -7279) mesuré sur 107 droites quasi verticales ;
  2. on fait « tourner » l'appareil virtuellement pour le remettre d'aplomb (rotation pure, sans déformation inventée) :
     plus d'inclinaison vers le haut (~9,5 deg) ni de roulis (~1 deg) ;
  3. petit réglage final : le roulis est ajusté pour que les verticales ET les longues horizontales de la façade
     soient le plus droites possible ;
  4. on recadre au plus grand rectangle sans bords vides.
Sorties : photo_redressee.jpg (pleine résolution), redresse.json (matrice, position de l'horizon, etc.).
"""
import cv2, numpy as np, json, math, sys
from PIL import Image, ImageOps

SRC = sys.argv[1] if len(sys.argv) > 1 else "photo.jpg"
OUT = sys.argv[2] if len(sys.argv) > 2 else "photo_redressee.jpg"
F = 1400.0                          # focale (px, photo réduite à 1500 x 2000)
VV = np.array([650.0, -7279.0])     # point de fuite des verticales (photo 1500 x 2000)
C = np.array([750.0, 1000.0])

pil = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB")
full = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
Hf, Wf = full.shape[:2]
s = Wf / 1500.0                     # facteur photo pleine résolution / photo de travail
K = np.array([[F, 0, C[0]], [0, F, C[1]], [0, 0, 1]])
Ki = np.linalg.inv(K)


def rotation(roulis_deg=0.0):
    up = Ki @ np.array([VV[0], VV[1], 1.0]); up /= np.linalg.norm(up)
    if up[1] > 0: up = -up                         # « haut » : y négatif dans l'image
    ey = -up                                       # axe y de l'appareil redressé = le bas
    ez = np.array([0, 0, 1.0]) - (np.array([0, 0, 1.0]) @ ey) * ey; ez /= np.linalg.norm(ez)
    ex = np.cross(ey, ez)
    R = np.vstack([ex, ey, ez])
    a = math.radians(roulis_deg)                    # roulis supplémentaire autour de l'axe optique
    Rz = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
    return Rz @ R


def homographie(roulis_deg, cx2, cy2):
    K2 = np.array([[F, 0, cx2], [0, F, cy2], [0, 0, 1]])
    return K2 @ rotation(roulis_deg) @ Ki


def mesure(img_bgr):
    """pentes médianes des quasi-verticales (en degrés) et des longues quasi-horizontales (en degrés)"""
    g = cv2.createCLAHE(2.0, (8, 8)).apply(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY))
    L = cv2.createLineSegmentDetector(0).detect(cv2.GaussianBlur(g, (3, 3), 0))[0].reshape(-1, 4)
    d = L[:, 2:] - L[:, :2]; l = np.hypot(d[:, 0], d[:, 1])
    ang = np.degrees(np.arctan2(d[:, 1], d[:, 0]))          # -180..180
    ang = (ang + 90) % 180 - 90                              # -90..90 ; 0 = horizontale, ±90 = verticale
    hor = (np.abs(ang) < 6) & (l > 140)
    ver = (np.abs(np.abs(ang) - 90) < 6) & (l > 140)
    av = np.where(ang[ver] > 0, ang[ver] - 90, ang[ver] + 90)   # écart à la verticale
    # médiane pondérée par la longueur
    def med(a, w):
        i = np.argsort(a); c = np.cumsum(w[i]); return a[i][np.searchsorted(c, c[-1] / 2)]
    return med(ang[hor], l[hor]), med(av, l[ver]), hor.sum(), ver.sum()


def rect_inscrit(H, w, h, cx2, cy2):
    """plus grand rectangle (axes alignés) dans l'image transformée"""
    pts = np.array([[0, 0], [w, 0], [w, h], [0, h]], np.float64)
    q = (H @ np.c_[pts, np.ones(4)].T).T; q = q[:, :2] / q[:, 2:]
    # haut/bas/gauche/droite : bords du quadrilatère convexe (haut, bas, gauche, droite)
    ys0 = max(q[0][1], q[1][1]); ys1 = min(q[2][1], q[3][1])
    def x_gauche(y):   # bord gauche : segment q[3] -> q[0]
        t = (y - q[3][1]) / (q[0][1] - q[3][1]); return q[3][0] + t * (q[0][0] - q[3][0])
    def x_droit(y):
        t = (y - q[2][1]) / (q[1][1] - q[2][1]); return q[2][0] + t * (q[1][0] - q[2][0])
    xs0 = max(x_gauche(ys0), x_gauche(ys1)); xs1 = min(x_droit(ys0), x_droit(ys1))
    return xs0, ys0, xs1, ys1, q


# 1) première passe à la résolution de travail (1500 x 2000) pour régler le roulis
work = cv2.resize(full, (1500, 2000), interpolation=cv2.INTER_AREA)
best = None
for roulis in np.arange(-2.0, 2.01, 0.05):
    H0 = homographie(roulis, 750, 1237)
    xs0, ys0, xs1, ys1, q = rect_inscrit(H0, 1500, 2000, 750, 1237)
    off = np.array([[1, 0, -xs0], [0, 1, -ys0], [0, 0, 1]])
    out = cv2.warpPerspective(work, off @ H0, (int(xs1 - xs0), int(ys1 - ys0)), flags=cv2.INTER_AREA)
    ah, av, nh, nv = mesure(out)
    cout = ah ** 2 + av ** 2
    if best is None or cout < best[0]: best = (cout, roulis, ah, av, nh, nv)
cout, roulis, ah, av, nh, nv = best
print(f"roulis ajouté {roulis:+.2f} deg ; écart restant : horizontales {ah:+.3f} deg ({nh} droites), verticales {av:+.3f} deg ({nv} droites)")

# 2) rendu pleine résolution
H1 = homographie(roulis, 750, 1237)
xs0, ys0, xs1, ys1, q = rect_inscrit(H1, 1500, 2000, 750, 1237)
S = np.diag([s, s, 1.0]); Si = np.diag([1 / s, 1 / s, 1.0])
Hfull = S @ H1 @ Si                                   # même transformation, en pixels pleine résolution
offf = np.array([[1, 0, -xs0 * s], [0, 1, -ys0 * s], [0, 0, 1]])
wout, hout = int((xs1 - xs0) * s), int((ys1 - ys0) * s)
res = cv2.warpPerspective(full, offf @ Hfull, (wout, hout), flags=cv2.INTER_CUBIC)
cv2.imwrite(OUT, res, [cv2.IMWRITE_JPEG_QUALITY, 95])
# position de l'horizon et du point principal dans l'image redressée (px pleine résolution)
cy_h = (1237 - ys0) * s; cx_p = (750 - xs0) * s
info = dict(roulis_deg=float(roulis), reste_horizontales_deg=float(ah), reste_verticales_deg=float(av),
            largeur=wout, hauteur=hout, echelle=float(s), horizon_y=float(cy_h), point_principal_x=float(cx_p),
            rect=[float(xs0), float(ys0), float(xs1), float(ys1)], H_travail=H1.tolist(), focale_travail=F)
json.dump(info, open("redresse.json", "w"), indent=1)
print(f"photo redressée : {wout} x {hout} px ; horizon à y = {cy_h:.0f} ({cy_h / hout * 100:.0f} % de la hauteur) ; point principal x = {cx_p:.0f}")

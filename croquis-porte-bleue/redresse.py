"""Redresse la photo de la porte bleue : verticales verticales, horizon horizontal.

Pas de données EXIF sur cette photo : on suppose le même téléphone que les autres photos (équivalent 24 mm en 35 mm,
soit une focale de 24 / 43,27 x diagonale = 1386 px sur la photo 1500 x 2000). C'est une hypothèse.

Méthode :
  1. point de fuite des verticales VV (vv.json) mesuré sur les droites quasi verticales ;
  2. rotation pure de l'appareil virtuel (sans déformation inventée) pour effacer l'inclinaison haut/bas et le roulis ;
  3. réglage fin du roulis pour que verticales ET longues horizontales de la façade soient le plus droites possible ;
  4. recadrage au plus grand rectangle sans bords vides.
Sorties : photo_redressee.jpg et redresse.json.
"""
import cv2, numpy as np, json, math, sys
from PIL import Image, ImageOps

SRC = sys.argv[1] if len(sys.argv) > 1 else "photo.jpg"
OUT = sys.argv[2] if len(sys.argv) > 2 else "photo_redressee.jpg"
vv = json.load(open("vv.json"))["VV"]
pil = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB")
full = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
Hf, Wf = full.shape[:2]
s = Wf / 1500.0
F = 1386.0
C = np.array([750.0, 1000.0])
VV = np.array(vv)
K = np.array([[F, 0, C[0]], [0, F, C[1]], [0, 0, 1]])
Ki = np.linalg.inv(K)
YH0 = C[1] + F * F / (C[1] - VV[1])        # horizon (avant redressement), au centre de la photo
print(f"horizon avant redressement : y = {YH0:.0f} au centre")


def rotation(roulis_deg):
    up = Ki @ np.array([VV[0], VV[1], 1.0]); up /= np.linalg.norm(up)
    if up[1] > 0: up = -up
    ey = -up
    ez = np.array([0, 0, 1.0]) - (np.array([0, 0, 1.0]) @ ey) * ey; ez /= np.linalg.norm(ez)
    ex = np.cross(ey, ez)
    R = np.vstack([ex, ey, ez])
    a = math.radians(roulis_deg)
    Rz = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
    return Rz @ R


def homographie(roulis, cx2, cy2):
    return np.array([[F, 0, cx2], [0, F, cy2], [0, 0, 1]]) @ rotation(roulis) @ Ki


def mesure(img):
    g = cv2.createCLAHE(2.0, (8, 8)).apply(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    L = cv2.createLineSegmentDetector(0).detect(cv2.GaussianBlur(g, (3, 3), 0))[0].reshape(-1, 4)
    d = L[:, 2:] - L[:, :2]; l = np.hypot(d[:, 0], d[:, 1])
    ang = (np.degrees(np.arctan2(d[:, 1], d[:, 0])) + 90) % 180 - 90
    hor = (np.abs(ang) < 6) & (l > 120); ver = (np.abs(np.abs(ang) - 90) < 6) & (l > 120)
    av = np.where(ang[ver] > 0, ang[ver] - 90, ang[ver] + 90)
    def med(a, w):
        i = np.argsort(a); c = np.cumsum(w[i]); return a[i][np.searchsorted(c, c[-1] / 2)]
    # verticales : moyenne pondérée par la longueur des droites, sans les 20 % les plus écartées (pierre taillée à la main)
    wv = l[ver]; k = np.abs(av - np.median(av)) <= np.percentile(np.abs(av - np.median(av)), 80)
    moy_v = np.sum(av[k] * wv[k]) / np.sum(wv[k])
    return med(ang[hor], l[hor]), moy_v, hor.sum(), ver.sum()


def rect_inscrit(H, w, h):
    pts = np.array([[0, 0], [w, 0], [w, h], [0, h]], np.float64)
    q = (H @ np.c_[pts, np.ones(4)].T).T; q = q[:, :2] / q[:, 2:]
    ys0 = max(q[0][1], q[1][1]); ys1 = min(q[2][1], q[3][1])
    xg = lambda y: q[3][0] + (y - q[3][1]) / (q[0][1] - q[3][1]) * (q[0][0] - q[3][0])
    xd = lambda y: q[2][0] + (y - q[2][1]) / (q[1][1] - q[2][1]) * (q[1][0] - q[2][0])
    return max(xg(ys0), xg(ys1)), ys0, min(xd(ys0), xd(ys1)), ys1


work = cv2.resize(full, (1500, 2000), interpolation=cv2.INTER_AREA)
cx2, cy2 = 750.0, float(YH0)
best = None
for roulis in np.arange(-2.0, 2.01, 0.05):
    H0 = homographie(roulis, cx2, cy2)
    xs0, ys0, xs1, ys1 = rect_inscrit(H0, 1500, 2000)
    off = np.array([[1, 0, -xs0], [0, 1, -ys0], [0, 0, 1]])
    out = cv2.warpPerspective(work, off @ H0, (int(xs1 - xs0), int(ys1 - ys0)), flags=cv2.INTER_AREA)
    ah, av, nh, nv = mesure(out)
    c = (3 * av) ** 2 + ah ** 2                  # les verticales comptent plus : elles doivent être verticales
    if best is None or c < best[0]: best = (c, roulis, ah, av, nh, nv)
_, roulis, ah, av, nh, nv = best
print(f"roulis ajouté {roulis:+.2f} deg ; reste : horizontales {ah:+.3f} deg ({nh}), verticales {av:+.3f} deg ({nv})")

H1 = homographie(roulis, cx2, cy2)
xs0, ys0, xs1, ys1 = rect_inscrit(H1, 1500, 2000)
S = np.diag([s, s, 1.0]); Si = np.diag([1 / s, 1 / s, 1.0])
offf = np.array([[1, 0, -xs0 * s], [0, 1, -ys0 * s], [0, 0, 1]])
wout, hout = int((xs1 - xs0) * s), int((ys1 - ys0) * s)
res = cv2.warpPerspective(full, offf @ S @ H1 @ Si, (wout, hout), flags=cv2.INTER_CUBIC)
cv2.imwrite(OUT, res, [cv2.IMWRITE_JPEG_QUALITY, 95])
info = dict(roulis_deg=float(roulis), reste_horizontales_deg=float(ah), reste_verticales_deg=float(av),
            largeur=wout, hauteur=hout, echelle=float(s), horizon_y=float((cy2 - ys0) * s),
            point_principal_x=float((cx2 - xs0) * s), rect=[float(xs0), float(ys0), float(xs1), float(ys1)],
            H_travail=H1.tolist(), focale_travail=F)
json.dump(info, open("redresse.json", "w"), indent=1)
print(f"photo redressée : {wout} x {hout} ; horizon y = {(cy2 - ys0) * s:.0f} ({(cy2 - ys0) / (ys1 - ys0) * 100:.0f} % de la hauteur) ; point principal x = {(cx2 - xs0) * s:.0f}")

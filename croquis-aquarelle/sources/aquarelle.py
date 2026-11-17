# Aquarelle numerique d'apres le croquis a la main (tes traits de crayon sont conserves).
# Style calque sur ton aquarelle d'exemple : papier blanc, ciel laisse blanc avec quelques taches,
# bords qui se dissolvent, ocres chauds, ombres lilas, verts profonds, reserves blanches.
# Usage : python aquarelle.py  ->  ../Avenue_HB_aquarelle.png + ../Avenue_HB_traits_a_peindre.png
import cv2, numpy as np, os, sys
rng = np.random.default_rng(11)
HERE = os.path.dirname(os.path.abspath(__file__))
im = cv2.imread(os.path.join(HERE, "croquis_original.jpg"))
W, H = 1900, 2606
SRC = np.float32([[156,168],[1419,174],[1452,1955],[55,1955]])
M = cv2.getPerspectiveTransform(SRC, np.float32([[0,0],[W,0],[W,H],[0,H]]))
rect = cv2.warpPerspective(im, M, (W, H), flags=cv2.INTER_CUBIC)

# ---------- traits de crayon (ton dessin) ----------
gray = cv2.cvtColor(rect, cv2.COLOR_BGR2GRAY).astype(np.float32)
ratio = gray / np.maximum(cv2.GaussianBlur(gray, (0,0), 40), 1)
dark = np.clip((0.972 - ratio) / 0.17, 0, 1)
dark = cv2.GaussianBlur(dark, (0,0), 0.7)
def P(pts):
    a = np.float32(pts).reshape(-1,1,2)
    return cv2.perspectiveTransform(a, M).reshape(-1,2)
def Y(y): return float(P([(700, y)])[0][1])
dark[: int(Y(640) - 40), :] = 0
dark[:, :14] = 0; dark[:, -14:] = 0; dark[-14:, :] = 0
b = (dark > 0.3).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(b, 8)
keep = np.zeros(n, bool); keep[1:] = st[1:, cv2.CC_STAT_AREA] > 90
dark *= cv2.dilate(keep[lab].astype(np.uint8), np.ones((9,9), np.uint8)).astype(np.float32)

# ---------- papier, bruits, textures de pinceau ----------
def noise(sig, amp=1.0):
    n = rng.standard_normal((H, W)).astype(np.float32)
    n = cv2.GaussianBlur(n, (0,0), sig); n /= n.std() + 1e-6
    return n * amp
tooth = noise(1.1) * 0.5 + noise(3.0) * 0.5
PAPER = np.array([0.990, 0.978, 0.950], np.float32)
paper = np.ones((H, W, 3), np.float32) * PAPER
paper *= (1 + 0.010 * tooth)[..., None]
canvas = paper.copy()
lo1, lo2, lo3 = noise(40), noise(90), noise(160)
fleck = noise(1.7)
def streaks(deg, L=41):
    k = np.zeros((L, L), np.float32); c = L // 2; a = np.deg2rad(deg)
    cv2.line(k, (int(c - np.cos(a) * c), int(c - np.sin(a) * c)), (int(c + np.cos(a) * c), int(c + np.sin(a) * c)), 1.0, 1)
    k /= k.sum(); n0 = cv2.GaussianBlur(rng.standard_normal((H, W)).astype(np.float32), (0, 0), 2.5)
    s = cv2.filter2D(n0, -1, k); return s / (s.std() + 1e-6)
STK = {a: streaks(a, 61) for a in (0, 35, -35, 80)}
VIG = np.ones((H, W), np.float32)

# ---------- moteur d'aquarelle ----------
def poly(pts):
    m = np.zeros((H, W), np.uint8)
    cv2.fillPoly(m, [np.round(P(pts)).astype(np.int32)], 255)
    return m.astype(np.float32) / 255
def ellipse(c, ax, ang=0):
    m = np.zeros((H, W), np.uint8)
    (cx, cy) = P([c])[0]
    cv2.ellipse(m, (int(cx), int(cy)), (int(ax[0] * 1.5), int(ax[1] * 1.5)), ang, 0, 360, 255, -1)
    return m.astype(np.float32) / 255
def roughen(m, amp=7, sig=18):
    hh, ww = m.shape
    dx = cv2.GaussianBlur(rng.standard_normal((hh, ww)).astype(np.float32), (0,0), sig); dx *= amp / (dx.std() + 1e-6)
    dy = cv2.GaussianBlur(rng.standard_normal((hh, ww)).astype(np.float32), (0,0), sig); dy *= amp / (dy.std() + 1e-6)
    gx, gy = np.meshgrid(np.arange(ww, dtype=np.float32), np.arange(hh, dtype=np.float32))
    return cv2.remap(m, gx + dx, gy + dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
def _roi(mask, pad):
    ys, xs = np.nonzero(mask > 0.004)
    if len(xs) == 0: return None
    return max(xs.min() - pad, 0), min(xs.max() + pad + 1, W), max(ys.min() - pad, 0), min(ys.max() + pad + 1, H)
def wash(mask, color, k=0.8, edge=0.5, var=0.35, rough=7, soft=1.4, gran=0.35, brush=None, bstr=0.25, dry=0.0, vig=True):
    """Lavis transparent. color = transmittance du pigment ; k = intensite ; brush = angle des traces de pinceau ;
    dry = taches blanches de pinceau sec (surtout sur les bords)."""
    global canvas
    r = _roi(mask, int(rough * 3 + soft * 4 + 24))
    if r is None: return
    x0, x1, y0, y1 = r
    m = mask[y0:y1, x0:x1]
    m = roughen(m, rough) if rough else m
    m = cv2.GaussianBlur(m, (0,0), soft)
    inner = cv2.GaussianBlur(m, (0,0), 7)
    ridge = np.clip(m - inner, 0, 1) * edge * 3.2
    v = 1 + var * (0.6 * lo1[y0:y1, x0:x1] + 0.3 * lo2[y0:y1, x0:x1] + 0.2 * lo3[y0:y1, x0:x1])
    if brush is not None: v = v * (1 + 0.7 * bstr * STK[brush][y0:y1, x0:x1])
    gg = 1 + gran * 0.45 * tooth[y0:y1, x0:x1]
    a = np.clip(m * k * v * gg + ridge * k, 0, 1)
    if dry > 0:
        edgez = np.clip(4 * m * (1 - m), 0, 1)
        a *= 1 - dry * (fleck[y0:y1, x0:x1] > (2.3 - 1.4 * edgez))
    if vig: a *= VIG[y0:y1, x0:x1]
    col = np.array(color, np.float32) if np.ndim(color) == 1 else color
    if col.ndim == 1: col = col[None, None, :]
    elif col.ndim == 3 and col.shape[0] == H: col = col[y0:y1, x0:x1]
    canvas[y0:y1, x0:x1] = canvas[y0:y1, x0:x1] * (1 - a[..., None] * (1 - col))
def lift(mask, amt=0.8, soft=0.8):
    """Reserve / rehaut : on enleve la peinture (le papier blanc revient)."""
    global canvas
    r = _roi(mask, 6)
    if r is None: return
    x0, x1, y0, y1 = r
    a = np.clip(cv2.GaussianBlur(mask[y0:y1, x0:x1], (0,0), soft) * amt, 0, 1)[..., None]
    canvas[y0:y1, x0:x1] = canvas[y0:y1, x0:x1] * (1 - a) + paper[y0:y1, x0:x1] * a
def grad_v(y0, y1, c0, c1):
    t = np.clip((np.arange(H, dtype=np.float32)[:, None] - Y(y0)) / (Y(y1) - Y(y0)), 0, 1)[..., None]
    return np.array(c0, np.float32) * (1 - t) + np.array(c1, np.float32) * t
def box(x0, y0, x1, y1): return poly([(x0,y0),(x1,y0),(x1,y1),(x0,y1)])
def lignes(x0, y0, x1, y1, d=5):
    b = np.zeros((H, W), np.uint8); b[(dark > 0.38)] = 255
    b = cv2.dilate(b, np.ones((d, d), np.uint8)).astype(np.float32) / 255
    return b * box(x0, y0, x1, y1)

# ---------- crayon + projection en perspective ----------
exec(open(os.path.join(HERE, "crayon.py")).read())

# ---------- on efface l'ancien mobilier (bancs ; a droite bancs + lampadaires + poubelles emmeles) ----------
ERASE = [[(140,1412),(240,1405),(308,1498),(304,1532),(208,1612),(140,1594)],
         [(394,1258),(470,1203),(512,1238),(508,1258),(440,1322),(396,1302)],
         [(536,1150),(605,1076),(637,1098),(634,1116),(570,1188),(538,1178)],
         [(605,1005),(700,940),(750,975),(745,1000),(690,1048),(640,1050),(605,1030)],
         [(952,1048),(1096,1048),(1096,1258),(1045,1260),(952,1112)],
         [(1062,1262),(1232,1250),(1234,1394),(1196,1394),(1194,1548),(1144,1548),(1144,1374),(1062,1374)],
         [(1185,1512),(1252,1512),(1252,1640),(1185,1640)]]
erase_m = np.zeros((H, W), np.float32)
for pts in ERASE: erase_m = np.maximum(erase_m, poly(pts))
dark *= 1 - cv2.GaussianBlur(erase_m, (0,0), 1.5)

# ---------- zones ----------
tower_pts = [(815,636),(826,672),(832,700),(832,815),(846,870),(866,908),(760,908),(786,870),(797,815),(797,700),(805,672)]
tower = poly(tower_pts)
blobs = [((225,935),(128,150)), ((450,925),(88,112)), ((585,940),(72,62)), ((685,930),(52,50)), ((340,1175),(62,58)), ((525,1105),(52,52)),
         ((940,940),(62,66)), ((1030,962),(56,72)), ((1140,992),(92,132)), ((1322,1010),(128,192)), ((1168,1288),(66,50))]
bl = np.zeros((H, W), np.float32)
for c, ax in blobs: bl = np.maximum(bl, ellipse(c, ax))
bl = cv2.GaussianBlur(bl, (0,0), 18)
leafy = bl + 0.30 * (0.6 * noise(14) + 0.4 * noise(6)) + 0.35 * np.clip(cv2.GaussianBlur(dark, (0,0), 10) * 6, 0, 1) * (bl > 0.15)
fol = (leafy > 0.52).astype(np.float32) * cv2.dilate((bl > 0.12).astype(np.uint8), np.ones((9,9), np.uint8)).astype(np.float32)
fol = cv2.morphologyEx(fol, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25,25)))
fol = cv2.morphologyEx(fol, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11)))
fol = cv2.GaussianBlur(fol, (0,0), 2.5)
ground = poly([(728,935),(892,935),(1010,1095),(1100,1235),(1240,1560),(1452,1955),(55,1955),(95,1665),(280,1420),(520,1185)])
stripL = poly([(55,1040),(300,1075),(520,1185),(280,1420),(95,1665),(55,1955)])
stripR = poly([(1100,1235),(1240,1560),(1452,1955),(1452,1130),(1230,1130)])
sky = poly([(156,168),(1419,174),(1419,935),(156,935)]) * (1 - tower)
FONT_NEAR = ellipse((752,1858), (205,102)); FONT_FAR = ellipse((812,1208), (128,56))

# ---------- skatepark : emprise (partagee par la peinture de base et les ajouts) ----------
SK_C, SK_RIN, SK_ROUT, SK_H, SK_DECK = (3.6, 14.2), 2.0, 2.9, 1.2, 0.7
TH_SK = np.deg2rad(np.linspace(25, 155, 60))
deck_out = [(SK_C[0] + (SK_ROUT + SK_DECK) * np.cos(t), SK_C[1] + (SK_ROUT + SK_DECK) * np.sin(t)) for t in TH_SK]
hull_pts = np.array(deck_out + [(1.2, 11.3), (7.8, 11.3), (7.8, 13.0)], np.float32)
hull = cv2.convexHull(hull_pts).reshape(-1, 2)
SLAB_W = [tuple(p) for p in hull]
slab_m = polyR(SL([(X, 0, Z) for X, Z in SLAB_W]))
_cx, _cz = SK_C
SK_BOT = SL([(_cx + SK_RIN * np.cos(t), 0, _cz + SK_RIN * np.sin(t)) for t in TH_SK])
SK_TOP = SL([(_cx + SK_ROUT * np.cos(t), SK_H, _cz + SK_ROUT * np.sin(t)) for t in TH_SK])
SK_DO = SL([(_cx + (SK_ROUT + SK_DECK) * np.cos(t), SK_H, _cz + (SK_ROUT + SK_DECK) * np.sin(t)) for t in TH_SK])
ramp_m = polyR(SK_BOT + SK_TOP[::-1]); deck_m = polyR(SK_TOP + SK_DO[::-1])
SK_WALLS = []
for t_end in (TH_SK[0], TH_SK[-1]):
    SK_WALLS.append(SL([(_cx + SK_RIN * np.cos(t_end), 0, _cz + SK_RIN * np.sin(t_end)), (_cx + SK_ROUT * np.cos(t_end), SK_H, _cz + SK_ROUT * np.sin(t_end)),
                        (_cx + (SK_ROUT + SK_DECK) * np.cos(t_end), SK_H, _cz + (SK_ROUT + SK_DECK) * np.sin(t_end)), (_cx + (SK_ROUT + SK_DECK) * np.cos(t_end), 0, _cz + (SK_ROUT + SK_DECK) * np.sin(t_end))]))
SK_OCC = np.clip(ramp_m + deck_m + sum(polyR(w_) for w_ in SK_WALLS), 0, 1)     # ce qui cache ce qu'il y a derriere
SK_SCREEN = np.clip(slab_m + SK_OCC, 0, 1)
dark *= 1 - cv2.dilate(SK_OCC, np.ones((5, 5), np.uint8))                          # traits caches par la rampe (tronc, etc.)

# ---------- coordonnees du sol (inverse de la perspective) : pour les dalles et les ombres tachetees ----------
Minv = np.linalg.inv(M)
gy_, gx_ = np.mgrid[0:H, 0:W].astype(np.float32)
pts = np.stack([gx_.ravel(), gy_.ravel()], 1).reshape(-1, 1, 2)
orig = cv2.perspectiveTransform(pts, Minv).reshape(H, W, 2); del pts
dyv = np.maximum(orig[..., 1] - VPY, 2.0)
Zw = (f_cam * hc_cam / dyv).astype(np.float32); Xw = ((orig[..., 0] - VPX) * Zw / f_cam).astype(np.float32); del orig, dyv

# ---------- vignette : la peinture se dissout vers les bords (comme ton exemple) ----------
dxn = (gx_ - W * 0.5) / (W * 0.53); dyn = (gy_ - H * 0.57) / (H * 0.49)
rr = (np.abs(dxn) ** 4.0 + np.abs(dyn) ** 4.0) ** (1 / 4.0)
thr = 1 + 0.07 * noise(55) + 0.06 * STK[0] * (dyn > 0.5) + 0.05 * STK[80] * (np.abs(dxn) > 0.7) + 0.04 * STK[35]
VIG = np.clip((thr - rr) / 0.09, 0, 1).astype(np.float32)
VIG = cv2.GaussianBlur(VIG, (0,0), 2)
del gx_, gy_, dxn, dyn, rr, thr

STEP = int(sys.argv[1]) if len(sys.argv) > 1 else 99
exec(open(os.path.join(HERE, "peinture.py")).read())

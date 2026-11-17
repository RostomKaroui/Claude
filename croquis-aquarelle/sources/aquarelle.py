# Aquarelle numerique d'apres le croquis a la main (tes traits de crayon sont conserves).
# Usage : python aquarelle.py  ->  ../Avenue_HB_aquarelle.png
import cv2, numpy as np, os, sys
rng = np.random.default_rng(11)
HERE = os.path.dirname(os.path.abspath(__file__))
im = cv2.imread(os.path.join(HERE, "croquis_original.jpg"))
W, H = 1900, 2606
SRC = np.float32([[156,168],[1419,174],[1452,1955],[55,1955]])
M = cv2.getPerspectiveTransform(SRC, np.float32([[0,0],[W,0],[W,H],[0,H]]))
rect = cv2.warpPerspective(im, M, (W, H), flags=cv2.INTER_CUBIC)

# ---------- traits de crayon ----------
gray = cv2.cvtColor(rect, cv2.COLOR_BGR2GRAY).astype(np.float32)
ratio = gray / np.maximum(cv2.GaussianBlur(gray, (0,0), 40), 1)
dark = np.clip((0.972 - ratio) / 0.17, 0, 1)
dark = cv2.GaussianBlur(dark, (0,0), 0.7)
def P(pts):
    a = np.float32(pts).reshape(-1,1,2)
    return cv2.perspectiveTransform(a, M).reshape(-1,2)
def Y(y):  # y original -> y rectifie
    return float(P([(700, y)])[0][1])
ytop = Y(640) - 40
dark[: int(ytop), :] = 0           # parasites du papier au-dessus de la tour
dark[:, :14] = 0; dark[:, -14:] = 0; dark[-14:, :] = 0
# supprime les petites taches isolees
b = (dark > 0.3).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(b, 8)
keep = np.zeros(n, bool); keep[1:] = st[1:, cv2.CC_STAT_AREA] > 90
dark *= cv2.dilate(keep[lab].astype(np.uint8), np.ones((9,9), np.uint8)).astype(np.float32)

# ---------- papier ----------
def noise(sig, amp=1.0):
    n = rng.standard_normal((H, W)).astype(np.float32)
    n = cv2.GaussianBlur(n, (0,0), sig); n /= n.std() + 1e-6
    return n * amp
tooth = noise(1.1) * 0.5 + noise(3.0) * 0.5
paper = np.ones((H, W, 3), np.float32) * np.array([0.985, 0.966, 0.925], np.float32)
paper *= (1 + 0.012 * tooth)[..., None]
canvas = paper.copy()
lo1, lo2, lo3 = noise(40), noise(90), noise(160)

# ---------- moteur d'aquarelle ----------
def poly(pts, jit=0):
    m = np.zeros((H, W), np.uint8)
    cv2.fillPoly(m, [np.round(P(pts)).astype(np.int32)], 255)
    return m.astype(np.float32) / 255
def ellipse(c, ax, ang=0):
    m = np.zeros((H, W), np.uint8)
    (cx, cy) = P([c])[0]; sx = W / 1263.0
    cv2.ellipse(m, (int(cx), int(cy)), (int(ax[0] * 1.5), int(ax[1] * 1.5)), ang, 0, 360, 255, -1)
    return m.astype(np.float32) / 255
def roughen(m, amp=7, sig=18):
    dx = cv2.GaussianBlur(rng.standard_normal((H, W)).astype(np.float32), (0,0), sig); dx *= amp / (dx.std() + 1e-6)
    dy = cv2.GaussianBlur(rng.standard_normal((H, W)).astype(np.float32), (0,0), sig); dy *= amp / (dy.std() + 1e-6)
    gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    return cv2.remap(m, gx + dx, gy + dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
def wash(mask, color, k=0.8, edge=0.5, var=0.35, rough=7, soft=1.4, gran=0.35):
    """color = transmittance du pigment (rgb 0..1) ; k = intensite."""
    m = roughen(mask, rough) if rough else mask
    m = cv2.GaussianBlur(m, (0,0), soft)
    inner = cv2.GaussianBlur(m, (0,0), 7)
    ridge = np.clip(m - inner, 0, 1) * edge * 3.2          # pigment qui se depose au bord
    v = 1 + var * (0.6 * lo1 + 0.3 * lo2 + 0.2 * lo3)
    g = 1 + gran * 0.45 * tooth
    a = np.clip(m * k * v * g + ridge * k, 0, 1)
    col = np.array(color, np.float32) if np.ndim(color) == 1 else color
    if col.ndim == 1: col = col[None, None, :]
    global canvas
    canvas = canvas * (1 - a[..., None] * (1 - col))
def grad_v(y0, y1, c0, c1):
    t = np.clip((np.arange(H, dtype=np.float32)[:, None] - Y(y0)) / (Y(y1) - Y(y0)), 0, 1)[..., None]
    return np.array(c0, np.float32) * (1 - t) + np.array(c1, np.float32) * t
def box(x0, y0, x1, y1): return poly([(x0,y0),(x1,y0),(x1,y1),(x0,y1)])
def lignes(x0, y0, x1, y1, d=5):
    b = np.zeros((H, W), np.uint8); b[(dark > 0.38)] = 255
    b = cv2.dilate(b, np.ones((d, d), np.uint8)).astype(np.float32) / 255
    return b * box(x0, y0, x1, y1)

# ---------- zones ----------
tower_pts = [(815,636),(826,672),(832,700),(832,815),(846,870),(866,908),(760,908),(786,870),(797,815),(797,700),(805,672)]
tower = poly(tower_pts)
dens = cv2.GaussianBlur(dark, (0,0), 16)
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
horizon_orig = 935
sky = poly([(156,168),(1419,174),(1419,horizon_orig),(156,horizon_orig)]) * (1 - tower)

np.save(os.path.join(HERE, "_dark.npy"), dark)
STEP = int(sys.argv[1]) if len(sys.argv) > 1 else 99
exec(open(os.path.join(HERE, "peinture.py")).read())

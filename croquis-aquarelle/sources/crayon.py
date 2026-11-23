# ===== Moteur de crayon : traits graphite tremblés, pression variable, hachures, grain =====
D1 = np.zeros((H, W), np.float32)          # couche de crayon ajoutee (fusionnee avec tes traits)
f_cam, hc_cam = 1500.0, 7.35               # focale (px) et hauteur de l'oeil (m) deduites de ton croquis
VPX, VPY = 800.0, 925.0                    # point de fuite (pied de la tour)
def S(X, Y, Z):
    x = VPX + f_cam * X / Z; y = VPY + f_cam * (hc_cam - Y) / Z
    return tuple(P([(x, y)])[0])
def SL(pts): return [S(*p) for p in pts]
def px_m(Z): return f_cam / Z * 1.5       # pixels rectifies par metre (largeur) a la profondeur Z
def resample(pts, step=6.0):
    pts = np.asarray(pts, np.float32); out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        d = float(np.hypot(*(b - a))); n = max(1, int(d / step))
        for i in range(1, n + 1): out.append(a + (b - a) * i / n)
    return np.array(out, np.float32)
def spline(pts, n=14):
    p = np.asarray(pts, np.float32); p = np.vstack([p[0], p, p[-1]]); out = []
    for i in range(1, len(p) - 2):
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t ** 3
            out.append(0.5 * ((2 * p[i]) + (-p[i-1] + p[i+1]) * t + (2*p[i-1] - 5*p[i] + 4*p[i+1] - p[i+2]) * t2 + (-p[i-1] + 3*p[i] - 3*p[i+1] + p[i+2]) * t3))
    out.append(p[-2]); return np.array(out, np.float32)
def _merge(temp, x0, y0, x1, y1, mask=None, gain=1.0):
    roi = temp[y0:y1, x0:x1]
    if mask is not None: roi = roi * mask[y0:y1, x0:x1]
    D1[y0:y1, x0:x1] = np.maximum(D1[y0:y1, x0:x1], roi * gain)
def stroke(pts, p=0.8, w=2.3, wob=0.9, over=2.0, mask=None):
    d = resample(pts, 5.0)
    if len(d) < 2: return
    t = d[1] - d[0]; t /= (np.hypot(*t) + 1e-6); d[0] = d[0] - t * over
    t = d[-1] - d[-2]; t /= (np.hypot(*t) + 1e-6); d[-1] = d[-1] + t * over
    n = len(d); knots = rng.standard_normal(max(3, n // 8 + 2)) * wob
    off = np.interp(np.linspace(0, len(knots) - 1, n), np.arange(len(knots)), knots)
    nrm = np.gradient(d, axis=0); nrm = np.stack([-nrm[:, 1], nrm[:, 0]], 1); nrm /= (np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-6)
    d = d + nrm * off[:, None]
    x0, y0 = np.floor(d.min(0) - 5).astype(int); x1, y1 = np.ceil(d.max(0) + 6).astype(int)
    x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, W), min(y1, H)
    if x1 <= x0 or y1 <= y0: return
    temp = np.zeros((y1 - y0, x1 - x0), np.uint8); base = (d - [x0, y0])
    pr = p * (0.80 + 0.20 * np.sin(np.linspace(0, rng.uniform(2, 6), n) + rng.uniform(0, 6)))
    for i in range(n - 1):
        cv2.line(temp, tuple(np.round(base[i] * 16).astype(int)), tuple(np.round(base[i + 1] * 16).astype(int)), int(255 * pr[i]), max(1, int(round(w))), cv2.LINE_AA, shift=4)
    T = np.zeros((H, W), np.float32) if False else None
    roi = temp.astype(np.float32) / 255
    if mask is not None: roi = roi * mask[y0:y1, x0:x1]
    D1[y0:y1, x0:x1] = np.maximum(D1[y0:y1, x0:x1], cv2.GaussianBlur(roi, (0, 0), 0.7))
def poly_stroke(pts, closed=True, **k):
    pts = list(pts); 
    if closed: pts = pts + [pts[0]]
    stroke(pts, **k)
def hatch(mask, ang=-45, gap=9, p=0.5, w=1.4, jit=0.12):
    ys, xs = np.nonzero(mask > 0.3)
    if len(xs) == 0: return
    x0, x1, y0, y1 = xs.min() - 4, xs.max() + 4, ys.min() - 4, ys.max() + 4
    x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, W), min(y1, H)
    hh, ww = y1 - y0, x1 - x0
    temp = np.zeros((hh, ww), np.uint8); a = np.deg2rad(ang); dx, dy = np.cos(a), np.sin(a); nx, ny = -dy, dx
    diag = int(np.hypot(hh, ww)); cx, cy = ww / 2, hh / 2
    for s in np.arange(-diag, diag, gap * (1 + rng.uniform(-0.2, 0.2))):
        aa = a + rng.normal(0, jit * 0.1)
        ddx, ddy = np.cos(aa), np.sin(aa)
        ox, oy = cx + nx * s, cy + ny * s
        cv2.line(temp, (int(ox - ddx * diag), int(oy - ddy * diag)), (int(ox + ddx * diag), int(oy + ddy * diag)), int(255 * p * rng.uniform(0.7, 1.0)), max(1, int(w)), cv2.LINE_AA)
    roi = temp.astype(np.float32) / 255 * cv2.GaussianBlur(mask, (0, 0), 1.0)[y0:y1, x0:x1]
    D1[y0:y1, x0:x1] = np.maximum(D1[y0:y1, x0:x1], roi)
def polyR(pts):
    m = np.zeros((H, W), np.uint8); cv2.fillPoly(m, [np.round(np.array(pts, np.float32)).astype(np.int32)], 255); return m.astype(np.float32) / 255
def circ_pts(cx, cz, r, Y, n=48, a0=0.0, a1=2 * np.pi):
    return [S(cx + r * np.cos(t), Y, cz + r * np.sin(t)) for t in np.linspace(a0, a1, n)]

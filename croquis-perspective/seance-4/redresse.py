"""Redresse chaque photo : les verticales du bâti deviennent verticales (comme sur un croquis),
puis la vue est mise au format de la fenêtre de dessin (18 x 24 cm, 40 px = 1 cm)."""
import cv2, numpy as np, sys
src = "/tmp/claude-0/-home-user-Claude/0095011d-962b-595a-b8c6-2625d1aef2e9/images/"
S, W, H = 40, 720, 960
def vp_vertical(g):
    L = cv2.createLineSegmentDetector(cv2.LSD_REFINE_STD).detect(g)[0].reshape(-1, 4)
    d = L[:, 2:] - L[:, :2]; lg = np.hypot(*d.T); ang = np.degrees(np.arctan2(d[:, 1], d[:, 0])) % 180
    V = L[(abs(ang - 90) < 12) & (lg > 120)]
    A = np.array([np.cross([x1, y1, 1.], [x2, y2, 1.]) for x1, y1, x2, y2 in V])
    A = A / np.linalg.norm(A[:, :2], axis=1)[:, None] * np.hypot(V[:,2]-V[:,0], V[:,3]-V[:,1])[:, None]
    v = np.linalg.svd(A)[2][-1]; return v, len(V)
for n, nom in ((32, "voute"), (33, "rue")):
    im = cv2.imread(src + f"{n}.jpg"); h, w = im.shape[:2]
    g = cv2.GaussianBlur(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY), (3, 3), 0)
    v, nb = vp_vertical(g)
    vy = v[:2] / v[2] if abs(v[2]) > 1e-9 else None
    print(nom, "verticales", nb, "point de fuite vertical", None if vy is None else vy.round(0))
    # homographie qui envoie le point de fuite vertical à l'infini (verticales parallèles), centre conservé
    cx, cy = w / 2, h / 2
    T = np.array([[1, 0, -cx], [0, 1, -cy], [0, 0, 1.]])
    p = T @ np.array([*vy, 1.]); 
    Hm = np.array([[1, 0, 0], [0, 1, 0], [-p[0] / (p[0]**2 + p[1]**2) * 0, -1 / p[1], 1.]])   # recul de la verticale
    M = np.linalg.inv(T) @ Hm @ T
    # cisaillement pour rendre l'axe vertical exactement vertical
    q = M @ np.array([*vy, 1.]); sh = q[0] / q[1] if abs(q[2]) < 1e-9 or True else 0
    Sh = np.array([[1, -sh, 0], [0, 1, 0], [0, 0, 1.]]) if abs(q[2]) < 1e-6 else np.eye(3)
    M = Sh @ M
    c = cv2.perspectiveTransform(np.float32([[[0, 0], [w, 0], [w, h], [0, h]]]), M)[0]
    # cadre : la plus grande zone utile, au format 3:4, dans l'image redressée
    x0, x1 = max(c[0, 0], c[3, 0]), min(c[1, 0], c[2, 0]); y0, y1 = max(c[0, 1], c[1, 1]), min(c[2, 1], c[3, 1])
    bw, bh = x1 - x0, y1 - y0
    if bw / bh > 0.75: x0 += (bw - 0.75 * bh) / 2; bw = 0.75 * bh
    else: bh = bw / 0.75
    D = np.array([[W / bw, 0, -x0 * W / bw], [0, H / bh, -y0 * H / bh], [0, 0, 1]]) @ M
    out = cv2.warpPerspective(im, D, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    cv2.imwrite(f"redresse_{nom}.png", out); np.save(f"D_{nom}.npy", D)
    g2 = cv2.GaussianBlur(cv2.cvtColor(out, cv2.COLOR_BGR2GRAY), (3, 3), 0)
    v2, _ = vp_vertical(g2); print("   après :", (v2[:2] / v2[2]).round(0) if abs(v2[2]) > 1e-9 else "à l'infini")

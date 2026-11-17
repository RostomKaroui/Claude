# ===== Details de crayon sur ton croquis : pavés en perspective, branches, tour, fontaines, ombrage du feuillage =====
def oP(pts): return [tuple(P([p])[0]) for p in pts]
def orig_ellipse(c, ax, ay, n=60, a0=0, a1=360):
    return oP([(c[0] + ax * np.cos(np.deg2rad(t)), c[1] + ay * np.sin(np.deg2rad(t))) for t in np.linspace(a0, a1, n)])
# --- 1) pavés en perspective (légers), hors fontaines / banc / plateforme
occ = np.zeros((H, W), np.float32)
occ = np.maximum(occ, cv2.dilate(np.clip(FONT_NEAR + FONT_FAR + VEG_OCC, 0, 1), np.ones((9, 9), np.uint8)))
occ = np.maximum(occ, cv2.dilate(SK_SCREEN, np.ones((9, 9), np.uint8))); occ = np.maximum(occ, cv2.dilate(BENCH_OCC, np.ones((9, 9), np.uint8)))
allow = ground * (1 - np.clip(occ, 0, 1)); allow = cv2.GaussianBlur(allow, (0, 0), 2)
for X in np.arange(-13, 13.1, 1.4):
    stroke(SL([(X, 0, Z) for Z in np.geomspace(8.2, 80, 26)]), p=0.17, w=1.5, wob=0.9, over=0, mask=allow)
Zk = 8.8
while Zk < 85:
    stroke(SL([(-14, 0, Zk), (14, 0, Zk)]), p=0.17, w=1.5, wob=1.1, over=0, mask=allow); Zk *= 1.145
# --- 2) branches et ecorce des arbres
def branches(base_o, cibles_o, p=0.55):
    for c in cibles_o:
        a = np.array(base_o, float); b = np.array(c, float); mid = (a + b) / 2 + [rng.uniform(-8, 8), rng.uniform(-8, 4)]
        stroke(oP([tuple(a), tuple(mid), tuple(b)]), p=p, w=2.0, wob=0.8)
branches((236, 1035), [(190, 962), (214, 905), (262, 930), (290, 985)])
branches((444, 1040), [(412, 975), (440, 930), (480, 968)])
branches((1122, 1088), [(1090, 1030), (1120, 990), (1162, 1030)])
branches((1268, 1132), [(1230, 1052), (1272, 992), (1332, 1040), (1380, 1105)])
for (x0, y0, x1, y1) in ((226, 1060, 258, 1390), (1255, 1160, 1285, 1520), (1112, 1110, 1130, 1245)):
    for k in range(3):
        o = rng.uniform(0.2, 0.8); xa = x0 + (x1 - x0) * 0 + (x1 - x0 + 1e-6) * 0
        stroke(oP([(x0 + (k + 1) * 7, y0), (x0 + (k + 1) * 7 + rng.uniform(-4, 4), (y0 + y1) / 2), (x1 - (3 - k) * 4, y1)]), p=0.32, w=1.4, wob=1.2, over=0)
for xl in (1107, 1136): stroke(oP([(xl, 1235), (xl - 1, 1268)]), p=0.7, w=2.0, wob=0.4, over=0)
# ombrage graphite du feuillage (côté ombre) : hachures courtes obliques
hatch(np.clip(ombre_f, 0, 1) * (ombre_f > 0.45), ang=-62, gap=8, p=0.30, w=1.3)
# --- 3) tour de l'horloge : cadran, joints de pierre, fenetres
ck = (820, 697)
stroke(orig_ellipse(ck, 17, 17, 28), p=0.85, w=2.2, wob=0.4, over=0)
stroke(orig_ellipse(ck, 12, 12, 24), p=0.4, w=1.2, wob=0.3, over=0)
for t in range(12):
    a = np.deg2rad(t * 30); stroke(oP([(ck[0] + 12 * np.cos(a), ck[1] + 12 * np.sin(a)), (ck[0] + 15 * np.cos(a), ck[1] + 15 * np.sin(a))]), p=0.7, w=1.4, wob=0.1, over=0)
stroke(oP([ck, (ck[0] + 1, ck[1] - 10)]), p=0.85, w=2.0, wob=0.1, over=0); stroke(oP([ck, (ck[0] + 8, ck[1] + 3)]), p=0.85, w=2.0, wob=0.1, over=0)
for y in (730, 750, 772, 794): stroke(oP([(795, y), (832, y + 1)]), p=0.30, w=1.3, wob=0.5, over=0)
for y in (738, 782):
    wx = 806
    stroke(oP([(wx, y + 18), (wx, y + 4), (wx + 5, y - 2), (wx + 10, y + 4), (wx + 10, y + 18)]), p=0.5, w=1.5, wob=0.3, over=0)
stroke(oP([(790, 713), (835, 713)]), p=0.7, w=2.0, wob=0.4); stroke(oP([(792, 718), (833, 718)]), p=0.45, w=1.4, wob=0.4)
for y in (840, 862, 884): stroke(oP([(776 - (y - 840) * 0.5, y), (860 + (y - 840) * 0.5, y)]), p=0.28, w=1.3, wob=0.6, over=0)
# --- 5) fusion du crayon ajouté et du tien (avec le grain du papier)
D1 = D1 * np.clip(0.80 + 0.22 * tooth, 0.45, 1.05)
dark = np.maximum(dark, np.clip(D1, 0, 1))

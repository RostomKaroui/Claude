# ===== Base : ciel, sol, feuillage, tour, fontaines ... (style de ton aquarelle d'exemple) =====
# Lumiere : le soleil vient de la DROITE -> ombres lilas a gauche des objets.
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
nofont = (1 - np.clip(FONT_NEAR + FONT_FAR, 0, 1))
noslab = 1 - cv2.dilate(SK_SCREEN, np.ones((5, 5), np.uint8))

# 1) CIEL : laisse blanc (papier). Seulement deux ou trois grands lavis libres autour de la tour et des arbres.
band = np.clip((yy - Y(540)) / (Y(760) - Y(540)), 0, 1) * np.clip((Y(960) - yy) / 60, 0, 1)
sky_m = sky * band * (1 - cv2.dilate(fol, np.ones((5, 5), np.uint8))) * np.clip((W * 0.42 - np.abs(xx - W * 0.48)) / (W * 0.10), 0, 1)
big = np.clip((0.75 * noise(75) + 0.25 * noise(30) + 0.25) / 0.45, 0, 1)
wash(sky_m * big, (0.76, 0.77, 0.93), k=0.48, edge=0.7, var=0.45, rough=16, soft=1.6, brush=-35, bstr=0.15, dry=0.25)
wash(sky_m * np.clip((noise(80) - 0.35) / 0.4, 0, 1) * (xx > W * 0.56), (0.97, 0.86, 0.66), k=0.38, edge=0.6, var=0.4, rough=14, soft=1.6, brush=35, bstr=0.15, dry=0.25)
wash(sky_m * np.clip((noise(60) - 0.7) / 0.4, 0, 1) * (xx < W * 0.42), (0.84, 0.78, 0.93), k=0.35, edge=0.6, var=0.4, rough=14, soft=1.6, brush=-35, bstr=0.15, dry=0.25)

# 2) DALLES DE LA PROMENADE : ocre chaud, chaque dalle un peu differente, quelques dalles laissees claires
ix = np.floor((Xw + 13) / 1.4); iz = np.floor(np.log(np.maximum(Zw, 1) / 8.8) / np.log(1.145))
hsh = np.mod(np.sin(ix * 12.9898 + iz * 78.233) * 43758.5453, 1.0).astype(np.float32)
tnear = np.clip((Zw - 10) / 38, 0, 1)[..., None]; tfar = np.clip((Zw - 32) / 70, 0, 1)[..., None]
cN, cM, cF = np.array([0.92, 0.68, 0.46], np.float32), np.array([0.97, 0.83, 0.60], np.float32), np.array([0.95, 0.90, 0.87], np.float32)
colp = (cN * (1 - tnear) + cM * tnear) * (1 - tfar) + cF * tfar
colp = np.clip(colp * (1 - 0.07 * (hsh[..., None] - 0.5)), 0, 1).astype(np.float32)
kf = (0.66 + 0.16 * hsh) * np.where(hsh > 0.9, 0.45, 1.0)
gm = ground * nofont * noslab
wash(gm * kf, colp, k=1.0, edge=0.35, var=0.35, rough=4, soft=1.2, brush=0, bstr=0.3, dry=0.2)
fx = np.mod((Xw + 13) / 1.4, 1.0); fz = np.mod(np.log(np.maximum(Zw, 1) / 8.8) / np.log(1.145), 1.0)
joint = ((np.minimum(fx, 1 - fx) < 0.035) | (np.minimum(fz, 1 - fz) < 0.05)).astype(np.float32) * np.clip((40 - Zw) / 25, 0, 1)
wash(gm * joint, (0.78, 0.58, 0.46), k=0.30, edge=0.0, var=0.3, rough=1.2, soft=0.9)

# 3) BANDES DE TERRE/HERBE SOUS LES ARBRES
for strip in (stripL, stripR):
    sm = strip * noslab
    wash(sm, (0.84, 0.89, 0.58), k=0.60, edge=0.4, var=0.5, rough=8, brush=0, dry=0.45)
    wash(sm * np.clip(noise(20) - 0.2, 0, 1), (0.95, 0.82, 0.58), k=0.40, edge=0.3, var=0.4, rough=8, dry=0.4)
    wash(sm * np.clip(noise(9) - 0.6, 0, 1), (0.52, 0.72, 0.46), k=0.45, edge=0.3, var=0.4, rough=4, dry=0.4)

# 4) OMBRES TACHETEES DES ARBRES (lilas) sur le sol : le soleil vient de la droite
T = cv2.GaussianBlur(rng.standard_normal((1024, 1024)).astype(np.float32), (0, 0), 9); T /= T.std()
mu = np.mod(Xw * 26, 1023).astype(np.float32); mv = np.mod(Zw * 26, 1023).astype(np.float32)
dap = cv2.remap(T, mu, mv, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP); del mu, mv
dapm = np.clip((dap - 0.05) / 0.35, 0, 1)
wR = np.clip((Xw - 0.4) / 2.2, 0, 1) * (Xw < 7.6); wL = 0.45 * (Xw < -6.0).astype(np.float32)
zon = ((Zw > 14) & (Zw < 140)).astype(np.float32)
om = np.clip(ground + stripL + stripR, 0, 1) * np.clip(wR + wL, 0, 1) * zon * dapm * noslab * nofont
wash(om, (0.74, 0.68, 0.90), k=0.50, edge=0.45, var=0.35, rough=3, soft=1.6, dry=0.15)

# 5) FEUILLAGE : vert-jaune lumineux, emeraude, ombres sarcelle profondes, eclats blancs (comme ton exemple)
sh = cv2.warpAffine(fol, np.float32([[1, 0, 30], [0, 1, -44]]), (W, H))
ombre_f = np.clip(np.clip(fol - sh, 0, 1) + 0.30 * fol * np.clip(noise(20), 0, 1), 0, 1)
wash(fol, (0.84, 0.91, 0.50), k=0.80, edge=0.45, var=0.5, rough=5, brush=35, bstr=0.3, dry=0.25)
wash(fol * np.clip(0.6 * noise(6) + 0.6 * noise(14) - 0.15, 0, 1), (0.40, 0.70, 0.48), k=0.85, edge=0.5, var=0.5, rough=3, brush=-35, dry=0.5)
wash(ombre_f, (0.10, 0.44, 0.42), k=0.90, edge=0.55, var=0.5, rough=4, brush=35, dry=0.5)
wash(fol * ombre_f * (noise(4) > 0.5), (0.07, 0.28, 0.30), k=0.75, edge=0.4, var=0.4, rough=2, dry=0.4)
wash(fol * (noise(5) > 1.2) * (1 - ombre_f), (0.98, 0.93, 0.45), k=0.55, edge=0.2, var=0.3, rough=2)
lift(fol * (fleck > 2.6) * (1 - 0.6 * ombre_f), 0.75, soft=1.2)

# 6) TRONCS
for pts in ([(220,1040),(252,1035),(275,1405),(243,1415)], [(430,1040),(458,1040),(462,1215),(436,1215)],
            [(1105,1090),(1140,1085),(1132,1262),(1106,1268)], [(1245,1135),(1290,1130),(1284,1562),(1243,1532)]):
    tm = poly(pts) * (1 - SK_OCC); cxp = P([(np.mean([p[0] for p in pts]), np.mean([p[1] for p in pts]))])[0][0]
    wash(tm, (0.70, 0.55, 0.46), k=0.85, edge=0.5, var=0.3, rough=3, brush=80, dry=0.3)
    wash(tm * (xx < cxp), (0.70, 0.62, 0.84), k=0.55, edge=0.2, var=0.3, rough=2)

# 7) TOUR DE L'HORLOGE : terre cuite, cote gauche a l'ombre (lilas), cote droit chaud, sommet dore
tcx = P([(815, 760)])[0][0]
wash(tower, (0.86, 0.56, 0.40), k=0.95, edge=0.55, var=0.35, rough=2, brush=80, bstr=0.3, dry=0.3)
wash(tower * (xx < tcx), (0.66, 0.54, 0.70), k=0.60, edge=0.2, var=0.3, rough=1.5)
wash(tower * (xx >= tcx), (0.99, 0.86, 0.60), k=0.30, edge=0.0, var=0.3, rough=1.5)
wash(tower * (yy < Y(692)), (0.96, 0.76, 0.24), k=0.95, edge=0.5, var=0.2, rough=1.5)
wash(tower * (yy > Y(862)), (0.95, 0.88, 0.74), k=0.75, edge=0.4, var=0.3, rough=2)
lift(ellipse((820, 697), (15, 15)), 0.9)

# 8) FONTAINES : pierre claire, eau turquoise vive, reflets blancs, voile des jets
def fontaine(ring, water, bowl, stem, top, veil):
    rc_ = P([ring[0]])[0][0]
    wash(ellipse(*ring), (0.96, 0.90, 0.80), k=0.70, edge=0.55, var=0.3, rough=3, dry=0.3)
    wash(ellipse(*ring) * (xx < rc_), (0.78, 0.74, 0.90), k=0.45, edge=0.1, var=0.3, rough=3)
    wash(ellipse(*water), (0.42, 0.78, 0.80), k=0.85, edge=0.55, var=0.4, rough=3, brush=0, dry=0.35)
    wash(ellipse(*water) * (yy < P([(0, water[0][1])])[0][1]), (0.30, 0.62, 0.72), k=0.45, edge=0.1, var=0.3, rough=3)
    lift(ellipse(*water) * (fleck > 2.2) * (noise(3) > 0.3), 0.85)
    for m_ in (poly(stem), ellipse(*bowl), ellipse(*top)):
        wash(m_, (0.95, 0.89, 0.80), k=0.75, edge=0.5, var=0.2, rough=2)
        wash(m_ * (xx < rc_), (0.78, 0.74, 0.90), k=0.45, edge=0.1, var=0.2, rough=2)
    wash(ellipse(bowl[0], (bowl[1][0] * 0.82, bowl[1][1] * 0.7)), (0.45, 0.80, 0.82), k=0.8, edge=0.4, var=0.2, rough=2)
    wash(ellipse(*veil), (0.82, 0.93, 0.97), k=0.38, edge=0.35, var=0.5, rough=8)
fontaine(((812,1208),(124,53)), ((812,1203),(108,42)), ((805,1148),(54,18)), [(797,1170),(816,1170),(818,1205),(795,1205)], ((812,1056),(26,9)), ((812,1105),(88,72)))
fontaine(((752,1858),(200,98)), ((752,1850),(176,80)), ((745,1778),(90,42)), [(716,1818),(776,1818),(782,1895),(712,1895)], ((765,1668),(52,22)), ((755,1705),(118,98)))

# 9) PERGOLA FLEURIE (bougainvillier) et POUBELLES restantes (bleu tunisien)
pergola = poly([(95,1288),(245,1285),(248,1405),(95,1405)])
wash(pergola, (0.55, 0.78, 0.48), k=0.80, edge=0.45, var=0.5, rough=9, brush=35, dry=0.4)
wash(pergola * np.clip(noise(8) - 0.3, 0, 1), (0.12, 0.45, 0.42), k=0.7, edge=0.3, var=0.4, rough=4)
fl = np.zeros((H, W), np.float32)
for _ in range(170):
    fl = np.maximum(fl, ellipse((rng.uniform(100, 242), rng.uniform(1292, 1400)), (rng.uniform(4, 8), rng.uniform(3, 6))))
wash(fl * pergola, (0.93, 0.42, 0.66), k=0.85, edge=0.35, var=0.4, rough=2.5, soft=0.9)
for pts in ([(305,1310),(360,1305),(362,1385),(330,1398),(308,1385)], [(495,1148),(525,1146),(525,1205),(497,1212)]):
    wash(poly(pts), (0.40, 0.56, 0.84), k=0.85, edge=0.5, var=0.3, rough=2)

# 10) LAMPADAIRES restants (a gauche et au fond) : tes traits colores en bleu, vasques lumineuses
for bx_ in [(95,1180,255,1330), (95,1300,140,1672), (355,1112,480,1200), (365,1190,402,1372), (535,1033,612,1100), (725,888,768,932), (878,890,920,945)]:
    wash(lignes(*bx_, d=5), (0.30, 0.42, 0.76), k=0.75, edge=0.0, var=0.15, rough=0, soft=1.0, gran=0.15)
for c, ax in (((228,1270),(24,9)), ((446,1172),(22,8)), ((588,1048),(15,6))):
    wash(ellipse(c, ax), (0.99, 0.86, 0.42), k=0.95, edge=0.2, var=0.1, rough=1)

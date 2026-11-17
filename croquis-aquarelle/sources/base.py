# ===== Base : ciel, sol, feuillage, tour, fontaines, bancs ... =====
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
def paint_if(n): return STEP >= n

# 1) CIEL : degrade bleu -> chaud a l'horizon, nuages reserves (laisses blancs)
cl = noise(70) * 0.6 + noise(35) * 0.4
nuage = np.clip((cl - 0.15) / 0.6, 0, 1)
fade = np.clip(np.minimum(xx, W - xx) / 140, 0, 1) * np.clip((yy - 30) / 120, 0, 1)
sky_m = sky * (1 - cv2.dilate(fol, np.ones((5,5), np.uint8))) * fade
c_sky = grad_v(168, 935, (0.60, 0.73, 0.88), (0.96, 0.90, 0.80))
wash(sky_m * (1 - 0.78 * nuage), c_sky, k=0.95, edge=0.25, var=0.3, rough=10)
wash(sky_m * np.clip(nuage * 0.9, 0, 1) * (yy > Y(380)), (0.80, 0.80, 0.89), k=0.40, edge=0.1, var=0.4, rough=12)
wash(sky_m * np.clip((yy - Y(800)) / (Y(935) - Y(800)), 0, 1), (0.97, 0.84, 0.70), k=0.30, edge=0.0, var=0.3, rough=14)

# 2) SOL : promenade pavee (gris chaud, pale au loin), bandes laterales ombragees
c_gr = grad_v(935, 1955, (0.91, 0.89, 0.88), (0.84, 0.76, 0.67))
wash(ground, c_gr, k=0.75, edge=0.35, var=0.30, rough=9)
wash(ground * np.clip(noise(26) - 0.2, 0, 1), (0.84, 0.82, 0.86), k=0.35, edge=0.0, var=0.2, rough=10)
for strip in (stripL, stripR):
    wash(strip, (0.66, 0.76, 0.56), k=0.55, edge=0.35, var=0.45, rough=10)
    wash(strip * np.clip(noise(25), 0, 1), (0.66, 0.64, 0.74), k=0.40, edge=0.1, var=0.4, rough=10)

# 3) FEUILLAGE : jaune-vert clair, vert profond cote ombre, touches bleutees et soleil
wash(fol, (0.68, 0.83, 0.44), k=0.80, edge=0.45, var=0.55, rough=5)
sh = cv2.warpAffine(fol, np.float32([[1,0,-30],[0,1,-44]]), (W, H))
ombre_f = np.clip(np.clip(fol - sh, 0, 1) + 0.30 * fol * np.clip(noise(20), 0, 1), 0, 1)
wash(ombre_f, (0.32, 0.54, 0.32), k=0.85, edge=0.5, var=0.5, rough=5)
wash(fol * np.clip(noise(14) - 0.25, 0, 1), (0.48, 0.65, 0.64), k=0.45, edge=0.2, var=0.5, rough=4)
wash(fol * np.clip(noise(10) - 0.55, 0, 1), (0.85, 0.80, 0.36), k=0.50, edge=0.0, var=0.4, rough=3)

# 4) TRONCS
for pts in ([(220,1040),(252,1035),(275,1405),(243,1415)], [(430,1040),(458,1040),(462,1215),(436,1215)],
            [(1105,1090),(1140,1085),(1132,1262),(1106,1268)], [(1245,1135),(1290,1130),(1284,1562),(1243,1532)]):
    wash(poly(pts), (0.55, 0.44, 0.37), k=0.85, edge=0.5, var=0.3, rough=3)

# 5) TOUR DE L'HORLOGE
wash(tower, (0.70, 0.46, 0.34), k=0.9, edge=0.5, var=0.3, rough=2)
wash(tower * (xx > P([(815, 700)])[0][0]), (0.55, 0.36, 0.30), k=0.7, edge=0.2, var=0.2, rough=2)
wash(tower * (yy < Y(692)), (0.90, 0.72, 0.22), k=0.95, edge=0.4, var=0.2, rough=1.5)
wash(tower * (yy > Y(862)), (0.88, 0.82, 0.70), k=0.8, edge=0.3, var=0.2, rough=2)
wash(ellipse((818, 705), (14, 14)), (0.95, 0.93, 0.85), k=0.8, edge=0.1, var=0.1, rough=1)

# 6) FONTAINES : pierre chaude, eau bleu-vert, jets en voile
def fontaine(ring, water, bowl, stem, top, veil):
    wash(ellipse(*ring), (0.82, 0.78, 0.72), k=0.80, edge=0.5, var=0.3, rough=3)
    wash(ellipse(*water), (0.62, 0.82, 0.89), k=0.70, edge=0.5, var=0.35, rough=3)
    wash(ellipse(*water) * (yy > (P([(0, water[0][1])])[0][1])), (0.55, 0.74, 0.84), k=0.30, edge=0.1, var=0.3, rough=3)
    wash(poly(stem), (0.80, 0.76, 0.70), k=0.8, edge=0.4, var=0.2, rough=2)
    wash(ellipse(*bowl), (0.80, 0.76, 0.70), k=0.8, edge=0.5, var=0.2, rough=2)
    wash(ellipse(bowl[0], (bowl[1][0] * 0.82, bowl[1][1] * 0.7)), (0.58, 0.78, 0.86), k=0.8, edge=0.3, var=0.2, rough=2)
    wash(ellipse(*top), (0.80, 0.76, 0.70), k=0.8, edge=0.4, var=0.2, rough=2)
    wash(ellipse(*veil), (0.78, 0.88, 0.95), k=0.55, edge=0.35, var=0.5, rough=8)
fontaine(((812,1208),(124,53)), ((812,1203),(108,42)), ((805,1148),(54,18)), [(797,1170),(816,1170),(818,1205),(795,1205)], ((812,1056),(26,9)), ((812,1105),(88,72)))
fontaine(((752,1858),(200,98)), ((752,1850),(176,80)), ((745,1778),(90,42)), [(716,1818),(776,1818),(782,1895),(712,1895)], ((765,1668),(52,22)), ((755,1705),(118,98)))

# 7) BANCS (bois), POUBELLES (vert), PERGOLA FLEURIE
for pts in ([(110,1440),(240,1415),(296,1515),(190,1600),(112,1555)], [(400,1265),(470,1215),(500,1245),(430,1300)], [(540,1150),(610,1080),(630,1105),(560,1170)],
            [(615,985),(690,940),(722,975),(640,1030)], [(990,1090),(1060,1075),(1100,1190),(1060,1225),(1000,1130)], [(1100,1290),(1190,1260),(1225,1385),(1120,1395)]):
    wash(poly(pts), (0.70, 0.52, 0.38), k=0.72, edge=0.5, var=0.45, rough=5)
for pts in ([(305,1310),(360,1305),(362,1385),(330,1398),(308,1385)], [(495,1148),(525,1146),(525,1205),(497,1212)], 
            [(958,1062),(985,1062),(985,1105),(960,1105)], [(1055,1200),(1090,1200),(1088,1252),(1058,1254)]):
    wash(poly(pts), (0.42, 0.62, 0.52), k=0.85, edge=0.5, var=0.3, rough=2)
pergola = poly([(95,1288),(245,1285),(248,1405),(95,1405)])
wash(pergola, (0.58, 0.76, 0.46), k=0.7, edge=0.4, var=0.5, rough=9)
fl = np.zeros((H, W), np.float32)
for _ in range(170):
    x = rng.uniform(100, 242); y = rng.uniform(1292, 1400)
    fl = np.maximum(fl, ellipse((x, y), (rng.uniform(4, 8), rng.uniform(3, 6))))
wash(fl * pergola, (0.93, 0.55, 0.72), k=0.75, edge=0.3, var=0.4, rough=2.5, soft=0.9)

# 8) LAMPADAIRES (traits peints en vert-noir) + lueur chaude des vasques
lampes = [(95,1180,255,1330), (95,1300,140,1672), (355,1112,480,1200), (365,1190,402,1372), (535,1033,612,1100), (725,888,768,932), (878,890,920,945),
          (1005,1052,1100,1122), (1062,1252,1222,1372), (1150,1360,1198,1538)]
for bx in lampes:
    wash(lignes(*bx, d=5), (0.36, 0.46, 0.42), k=0.65, edge=0.0, var=0.15, rough=0, soft=1.0, gran=0.15)
for c, ax in (((228,1270),(24,9)), ((446,1172),(22,8)), ((588,1048),(15,6)), ((1085,1337),(22,9)), ((1040,1110),(14,6))):
    wash(ellipse(c, ax), (0.98, 0.84, 0.42), k=0.95, edge=0.2, var=0.1, rough=1)

# 9) OMBRES PORTEES (glacis lilas, tres doux) : le soleil vient de la droite
for c, ax, ang in (((955,1330),(250,24),-9), ((1010,1525),(330,30),-8), ((760,1180),(110,12),-6), ((395,1330),(105,14),-30)):
    om = ellipse(c, ax, ang) * ground * np.clip(0.6 + 0.8 * noise(18), 0, 1)
    wash(om, (0.66, 0.65, 0.80), k=0.34, edge=0.1, var=0.5, rough=16, soft=5)

# 10) PERSONNAGES : taches de couleur, sans contour (des gens qui "font place")
def prim(fn):
    m = np.zeros((H, W), np.uint8); fn(m); return m.astype(np.float32) / 255
def pt(x, y): return tuple(int(v) for v in P([(x, y)])[0])
def personne(cx, base, h, chemise, pantalon=(0.38, 0.42, 0.58), assis=False, cheveux=(0.35, 0.25, 0.20)):
    s = h / 100.0; K = 1.5
    def torse(m):
        cv2.ellipse(m, pt(cx, base - 62*s), (int(15*s*K), int(24*s*K)), 0, 0, 360, 255, -1)
        cv2.line(m, pt(cx - 14*s, base - 78*s), pt(cx - 19*s, base - 52*s), 255, max(2, int(6*s*K)))
        cv2.line(m, pt(cx + 14*s, base - 78*s), pt(cx + 19*s, base - 52*s), 255, max(2, int(6*s*K)))
    def jambes(m):
        t = max(3, int(9*s*K))
        if assis:
            cv2.line(m, pt(cx - 7*s, base - 36*s), pt(cx - 9*s, base - 16*s), 255, t); cv2.line(m, pt(cx + 7*s, base - 36*s), pt(cx + 9*s, base - 16*s), 255, t)
            cv2.line(m, pt(cx - 9*s, base - 20*s), pt(cx - 10*s, base + 8*s), 255, t); cv2.line(m, pt(cx + 9*s, base - 20*s), pt(cx + 10*s, base + 8*s), 255, t)
        else:
            cv2.line(m, pt(cx - 6*s, base - 42*s), pt(cx - 9*s, base), 255, t); cv2.line(m, pt(cx + 6*s, base - 42*s), pt(cx + 9*s, base), 255, t)
    def tete(m): cv2.circle(m, pt(cx, base - 90*s), max(3, int(8*s*K)), 255, -1)
    def cheveux_m(m): cv2.ellipse(m, pt(cx, base - 94*s), (max(3, int(8.5*s*K)), max(2, int(6*s*K))), 0, 180, 360, 255, -1)
    wash(prim(jambes), pantalon, k=0.85, edge=0.35, var=0.25, rough=1.5, soft=0.9)
    wash(prim(torse), chemise, k=0.88, edge=0.45, var=0.30, rough=1.5, soft=0.9)
    wash(prim(tete), (0.90, 0.72, 0.58), k=0.9, edge=0.3, var=0.1, rough=0.8, soft=0.8)
    wash(prim(cheveux_m), cheveux, k=0.9, edge=0.2, var=0.1, rough=0.8, soft=0.8)
    wash(ellipse((cx, base + 3), (h * 0.24, h * 0.05)), (0.60, 0.60, 0.74), k=0.40, edge=0.0, var=0.1, rough=2, soft=2)
personne(640, 1352, 105, (0.86, 0.56, 0.46)); personne(692, 1356, 100, (0.34, 0.48, 0.70), cheveux=(0.12, 0.10, 0.10))
personne(985, 1392, 108, (0.46, 0.64, 0.56)); personne(1030, 1396, 64, (0.93, 0.74, 0.32))
for cx, by, h, col in ((832,1004,36,(0.85,0.50,0.40)), (770,1008,33,(0.35,0.5,0.7)), (878,990,30,(0.9,0.75,0.35)), (906,1002,34,(0.45,0.62,0.55)), (752,988,28,(0.8,0.6,0.5))):
    personne(cx, by, h, col)


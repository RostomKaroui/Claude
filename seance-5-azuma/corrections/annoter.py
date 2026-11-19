"""Annote les photos du carnet (remarques de la prof) : python3.13 annoter.py"""
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
import math
I = '/tmp/claude-0/-home-user-Claude/0095011d-962b-595a-b8c6-2625d1aef2e9/images/'
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
ROUGE, VERT = (214, 40, 40), (22, 140, 70)

def base(n):
    im = Image.open(I + n + '.jpg').convert('L').rotate(180)
    im = ImageOps.autocontrast(im, cutoff=1)
    im = ImageEnhance.Brightness(im).enhance(1.08)
    return im.convert('RGB')

def marque(d, num, cible, pos, ok=False):
    c = VERT if ok else ROUGE
    if cible:
        x0, y0 = pos; x1, y1 = cible
        a = math.atan2(y1 - y0, x1 - x0)
        d.line([(x0 + 24 * math.cos(a), y0 + 24 * math.sin(a)), (x1, y1)], fill=c, width=5)
        d.ellipse([x1 - 7, y1 - 7, x1 + 7, y1 + 7], fill=c)
    d.ellipse([pos[0] - 24, pos[1] - 24, pos[0] + 24, pos[1] + 24], fill=c, outline='white', width=3)
    t = '✓' if ok and num is None else str(num)
    d.text(pos, t, fill='white', font=F, anchor='mm')

def coupes():
    im = base('55'); d = ImageDraw.Draw(im)
    M = [
        (1, (238, 330), (78, 300)), (1, (322, 1180), (230, 1115)), (1, (322, 1690), (232, 1640)),
        (2, (600, 490), (600, 725)),
        (3, (885, 428), (965, 268)),
        (6, (450, 152), (540, 30)), (6, (480, 852), (590, 765)),
        (7, (1336, 440), (1462, 520)),
        (8, (1336, 192), (1462, 140)), (8, (262, 114), (180, 40)),
        (9, (1358, 545), (1470, 700)),
        (10, (1372, 626), (1300, 725)), (10, (1160, 1284), (1290, 1345)),
        (11, (1162, 1180), (1250, 1110)),
        (12, (1137, 1742), (1240, 1630)),
        (4, (480, 1580), (560, 1500)),
    ]
    OK = [(4, (605, 370), (555, 250)), (5, (1020, 437), (1085, 525)), (5, (467, 1730), (560, 1800)), (14, (338, 806), (262, 760))]
    for n, c, p in M: marque(d, n, c, p)
    for n, c, p in OK: marque(d, n, c, p, ok=True)
    im.resize((1200, 1600), Image.LANCZOS).save('carnet-coupes.jpg', quality=82)

def plans():
    im = base('54'); d = ImageDraw.Draw(im)
    # trait de coupe A (exemple) : sur l'axe du plan du rez-de-chaussée, flèches vers l'escalier
    p0, p1 = (110, 253), (1450, 366)
    L = math.dist(p0, p1); ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
    s = 0
    while s < L:                                  # trait mixte
        for a, b in ((s, min(s + 46, L)), (s + 58, min(s + 66, L))):
            if a < L: d.line([(p0[0] + ux * a, p0[1] + uy * a), (p0[0] + ux * b, p0[1] + uy * b)], fill=ROUGE, width=6)
        s += 78
    for p in (p0, p1):                            # flèches : on regarde vers l'escalier (en haut)
        tip = (p[0] + uy * 70, p[1] - ux * 70)
        d.line([p, tip], fill=ROUGE, width=7)
        d.polygon([(tip[0] + uy * 18, tip[1] - ux * 18), (tip[0] - 14, tip[1] + 6), (tip[0] + 14, tip[1] - 6)], fill=ROUGE)
        d.text((p[0] - 30, p[1] + 34), 'A', fill=ROUGE, font=F, anchor='mm')
    M = [(11, (1396, 356), (1462, 452)), (12, (172, 262), (60, 330)), (12, (535, 137), (535, 40)),
         (1, (1352, 307), (1290, 235)), (13, (700, 302), (700, 560))]
    for n, c, p in M: marque(d, n, c, p)
    OK = [(None, (1365, 905), (1270, 830)), (None, (195, 1535), (300, 1470)), (None, (1367, 1480), (1270, 1420))]
    for n, c, p in OK: marque(d, n, c, p, ok=True)
    im.resize((1200, 1600), Image.LANCZOS).save('carnet-plans.jpg', quality=82)

coupes(); plans(); print('ok')

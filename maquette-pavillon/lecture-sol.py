"""Image annotée : comment lire le sol dans la coupe AA (la marche) et dans la façade 1.
Entrée : la photo de la feuille « lignes de projection » (tournée) et celle des élévations. Sortie : lecture-sol.png"""
import sys
from PIL import Image, ImageDraw, ImageFont

coupe_src, elev_src, sortie = sys.argv[1:4]
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
t, tb, tt = ImageFont.truetype(F, 22), ImageFont.truetype(FB, 24), ImageFont.truetype(FB, 30)
BLEU, ROUGE, VERT, NOIR = (35, 70, 168), (190, 50, 40), (30, 130, 70), (25, 25, 25)

# coupe : bas du dessin, agrandi 2x
c = Image.open(coupe_src).crop((1150, 1180, 1870, 1400))
k = 2; c = c.resize((c.width * k, c.height * k), Image.LANCZOS)
X = lambda x: (x - 1150) * k; Y = lambda y: (y - 1180) * k
W = c.width; H = 300 + c.height + 460
im = Image.new("RGB", (W, H), (250, 250, 247)); im.paste(c, (0, 300)); d = ImageDraw.Draw(im)
oy = 300
d.text((20, 20), "Coupe AA : le sol fait une marche", font=tt, fill=NOIR)
d.text((20, 70), "Sous tout le pavillon (grande pièce ET porche), le sol est 2 fois plus épais que dehors (la rue).", font=t, fill=NOIR)
d.text((20, 102), "1 épaisseur = l'épaisseur d'un mur. Dans la maquette : socle + dalle de sol, chacun en 2 cartons.", font=t, fill=NOIR)
# zones
def accolade(x0, x1, y, txt, col, dy=-1):
    d.line([(x0, y), (x1, y)], fill=col, width=4); d.line([(x0, y - 12 * dy), (x0, y)], fill=col, width=4); d.line([(x1, y - 12 * dy), (x1, y)], fill=col, width=4)
    w = d.textlength(txt, font=tb); d.text(((x0 + x1 - w) / 2, y + (8 if dy < 0 else -40)), txt, font=tb, fill=col)
yb = oy + Y(1384) + 20
accolade(X(1175), X(1262), yb, "la rue", ROUGE)
accolade(X(1265), X(1752), yb, "sous le pavillon : grande pièce + porche", BLEU)
accolade(X(1755), X(1845), yb, "la rue", ROUGE)
# épaisseurs
def cote(x, y0, y1, txt, col, gauche=False, dessus=False):
    d.line([(x, y0), (x, y1)], fill=col, width=4)
    for y in (y0, y1): d.line([(x - 10, y), (x + 10, y)], fill=col, width=4)
    w = d.textlength(txt, font=tb)
    if dessus: d.text((x - w / 2, y0 - 44), txt, font=tb, fill=col)
    else: d.text((x - w - 16 if gauche else x + 16, (y0 + y1) / 2 - 14), txt, font=tb, fill=col)
cote(X(1215), oy + Y(1355), oy + Y(1377), "1 épaisseur", ROUGE, dessus=True)
cote(X(1440), oy + Y(1338), oy + Y(1378), "2 épaisseurs", BLEU, dessus=True)
cote(X(1810), oy + Y(1361), oy + Y(1381), "1 épaisseur", ROUGE, dessus=True)
# marches et murs
for x, txt in ((1264, "marche = nu extérieur\ndu mur ouest"), (1753, "marche = nu extérieur\ndu mur est du porche")):
    d.ellipse([X(x) - 14, oy + Y(1346) - 14, X(x) + 14, oy + Y(1346) + 14], outline=VERT, width=4)
    d.line([(X(x), oy + Y(1346) - 16), (X(x), 255)], fill=VERT, width=3)
    lignes = txt.split("\n")
    for i, l in enumerate(lignes):
        w = d.textlength(l, font=t); xx = min(max(10, X(x) - w / 2), W - w - 10)
        d.text((xx, 175 + 28 * i), l, font=t, fill=VERT)
d.text((X(1600), oy + Y(1300)), "cloison", font=t, fill=NOIR)
d.line([(X(1625), oy + Y(1308)), (X(1625), oy + Y(1335))], fill=NOIR, width=2)
d.text((X(1440) - 140, oy + Y(1290) - 8), "pas de marche sous la cloison :", font=t, fill=BLEU)
d.text((X(1440) - 140, oy + Y(1290) + 20), "le porche est au même niveau", font=t, fill=BLEU)

# façade 1 : la marche vue à travers l'arc
e = Image.open(elev_src).crop((470, 600, 870, 725)); e = e.resize((e.width * 2, e.height * 2), Image.LANCZOS)
y2 = oy + c.height + 110
d.text((20, y2 - 70), "Façade 1 : à travers l'arc du porche, on voit la tranche de la dalle (la marche)", font=tb, fill=NOIR)
im.paste(e, (20, y2)); d2 = ImageDraw.Draw(im)
d2.rectangle([20 + (565 - 470) * 2, y2 + (688 - 600) * 2, 20 + (757 - 470) * 2, y2 + (703 - 600) * 2], outline=VERT, width=4)
d2.text((20 + e.width + 20, y2 + 150), "la marche", font=tb, fill=VERT)
d2.line([(20 + (757 - 470) * 2 + 4, y2 + 192), (20 + e.width + 15, y2 + 165)], fill=VERT, width=3)
im = im.crop((0, 0, W, y2 + e.height + 30))
im.save(sortie); print(sortie, im.size)

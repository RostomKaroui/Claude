"""Masque des personnes sur la photo d'origine (34.jpg, 1500 x 2000) : un polygone par personne, élargi un peu.
Le sac poubelle, l'arbre et tout le reste ne sont pas touchés.
Lancer : python3 masque.py <photo> -> masque-personnes.png"""
import sys
import cv2
import numpy as np

PERSONNES = {
    "dans l'embrasure de la grande porte": [(200, 1180), (268, 1180), (274, 1400), (264, 1600), (270, 1692), (212, 1692), (198, 1600), (192, 1400)],
    "l'homme au sac à dos": [(855, 1138), (920, 1138), (926, 1222), (948, 1238), (948, 1420), (928, 1480), (922, 1640), (972, 1676), (968, 1704),
                             (818, 1704), (820, 1640), (828, 1490), (792, 1545), (778, 1450), (798, 1380), (798, 1238), (850, 1222)],
    "la femme penchée": [(928, 1366), (1002, 1364), (1040, 1438), (1046, 1646), (930, 1646), (922, 1420)],
    "l'homme assis": [(1038, 1418), (1112, 1418), (1172, 1466), (1174, 1624), (1036, 1624)],
    "la femme à la planche": [(1188, 1192), (1264, 1192), (1272, 1288), (1322, 1306), (1344, 1398), (1338, 1444), (1302, 1452), (1312, 1560),
                              (1304, 1752), (1114, 1752), (1122, 1680), (1148, 1580),
                              (1158, 1444), (1146, 1418), (1152, 1300), (1182, 1284)],
    "la personne accroupie": [(1298, 1392), (1438, 1392), (1442, 1768), (1338, 1764), (1302, 1792), (1226, 1792), (1232, 1700), (1248, 1560), (1268, 1498)],
}

if __name__ == "__main__":
    im = cv2.imread(sys.argv[1])
    m = np.zeros(im.shape[:2], np.uint8)
    for poly in PERSONNES.values():
        cv2.fillPoly(m, [np.array(poly, np.int32)], 255)
    m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17)))
    cv2.imwrite("masque-personnes.png", m)
    v = im.copy(); v[m > 0] = (0.4 * v[m > 0] + [0, 0, 150]).astype(np.uint8)
    cv2.imwrite(sys.argv[2] if len(sys.argv) > 2 else "verif-masque.jpg", v)

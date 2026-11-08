# Place Ramadhan Bey : filtre crayon + LH, LT, PF1, PF2 (A3 paysage / 2 × A4)

| fichier | à quoi il sert |
|---|---|
| `croquis-A3.pdf` | le croquis, 1 page **A3 paysage** (316 × 248 mm de dessin) |
| `croquis-2xA4.pdf` | le même en 2 pages **A4 portrait** à l'échelle 1 : feuille 1 = moitié gauche, feuille 2 = moitié droite (jonction au milieu) |
| `photo.jpg` | la photo d'origine ; `photo_redressee.jpg` = redressée (verticales verticales) |

Imprimer en **taille réelle (100 %)**. La photo est en paysage : j'ai donc mis l'A3 en paysage et coupé en 2 A4 portrait (gauche / droite).

## Mesures (photo sans EXIF : focale supposée 24 mm éq. 35 mm = 1386 px)
- **Verticales** : point de fuite des verticales (1329 ; −7699) sur 94 droites → l'appareil regardait ≈ 9° vers le haut et penchait de ≈ 2°. Redressées : verticales à 0,02° de la verticale.
- **LH** : y = 1022 sur 1466 (70 % de la hauteur), à hauteur des yeux. Contrôle : elle passe par les yeux de l'homme debout, et la droite qui joint les deux points de fuite mesurés donne la même hauteur (± 10 px).
- **PF1** (la ruelle sous la voûte) : x ≈ 464 sur la LH, mesuré sur la base du mur droit de la ruelle et le haut de son soubassement gris. Précision ± 150 px (≈ ± 3 cm sur le papier).
- **PF2** (les façades de la place, presque de face) : très loin à droite, vers x ≈ 22 000 px (entre 17 000 et 29 000), soit environ 4 m à droite de la feuille. Indiqué par une flèche.
- **LT** : bas de la photo.
- La ruelle n'est pas exactement perpendiculaire à la façade (≈ 14° d'écart), comme souvent dans une médina : PF1 et PF2 ne sont donc pas « orthogonaux ».
- Le redressement coupe un peu les bords de la photo (la charrette de gauche, un morceau du panneau « Fast Food »).

## Régénérer
```
python3 -I redresse.py photo.jpg photo_redressee.jpg     # (vv.json = point de fuite des verticales)
python3 -I a3.py
node rendu_a3.js "$PWD"
```

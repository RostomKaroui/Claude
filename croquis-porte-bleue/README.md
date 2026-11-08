# Porte bleue : filtre crayon + LH, LT, point de fuite (A3 / 2 × A4)

| fichier | à quoi il sert |
|---|---|
| `croquis-A3.pdf` | le croquis, 1 page **A3 portrait** (251 × 336 mm de dessin) |
| `croquis-2xA4.pdf` | le même en 2 pages **A4 paysage** à l'échelle 1 : feuille 1 = moitié haute, feuille 2 = moitié basse |
| `photo.jpg` | la photo d'origine ; `photo_redressee.jpg` = redressée (verticales verticales, horizon horizontal) |

Imprimer en **taille réelle (100 %)**.

## Mesures
- **Pas d'EXIF** sur cette photo : focale **supposée** = celle du même téléphone (24 mm éq. 35 mm → 1386 px sur 1500 × 2000). Hypothèse.
- **Verticales** : leur point de fuite est très loin (1548 ; −166 799) → l'appareil ne regardait que ≈ 0,5° vers le haut et la photo ne penchait que de ≈ 0,3° : presque d'aplomb. Après redressement, les verticales longues sont à 0,04° de la verticale (moyenne pondérée).
- **LH** : y = 1015 sur 1995 (51 % de la hauteur) : vers le milieu, donc plus haut que sur la porte jaune.
- **PF** : sur la LH, à 6 px du centre. Façade de face → PF2 à l'infini.
- **LT** : bas de la photo.
- **Compromis assumé** : cette vieille façade n'est pas parfaitement d'équerre. En mettant les verticales d'aplomb (ta consigne), les horizontales de la pierre (linteau, seuil) restent inclinées d'environ 0,6° (≈ 1,5 mm sur le papier). La LH, elle, est parfaitement horizontale.

## Régénérer
```
python3 -I redresse.py photo.jpg photo_redressee.jpg     # (vv.json = point de fuite des verticales)
python3 -I a3.py
node rendu_a3.js "$PWD"
```

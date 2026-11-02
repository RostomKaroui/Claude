# Porte jaune : filtre crayon + LH, LT, point de fuite

| fichier | à quoi il sert |
|---|---|
| `construction.png` / `construction.pdf` | **le rendu** : la photo au crayon avec LH, LT, PF et fuyantes en bleu |
| `croquis.png` | la photo passée au filtre crayon seule (1500 × 2000) |
| `photo.jpg` | la photo d'origine (4624 × 3468 avec orientation EXIF) ; `photo_1500.jpg` = redressée de l'orientation et réduite |

## Comment c'est mesuré (photo Samsung SM-A525F, EXIF : 24 mm équivalent 35 mm → focale ≈ 1390–1410 px)
- **Verticales** : 107 droites quasi verticales convergent vers un point de fuite vertical (650 ; −7279) → l'appareil regardait ≈ 9,5° vers le haut, d'où les verticales qui se rapprochent en haut.
- **LH (ligne d'horizon)** : y ≈ 1237 au milieu de la photo (1000 + f² / 8279). Elle est parallèle aux horizontales de la façade (la photo est penchée d'environ 1°).
- **Façade de face** : ses 54 longues horizontales sont parallèles → leur point de fuite (PF2) est à l'infini.
- **PF** : sur la LH, x ≈ 790 (au milieu de la porte). Les vraies arêtes de profondeur du retrait de la fenêtre du haut (segments épais bleus) pointent vers lui, ainsi que les joints du sol.
- **LT (ligne de terre)** : bas de la photo, parallèle à la LH.

Incertitude : LH ± 40 px (selon la précision du point de fuite vertical), PF ± 60 px en x.

## Régénérer
```
python3 -I croquis_filtre.py photo_1500.jpg croquis.png
python3 construire.py
node rendu.js "$PWD"
```

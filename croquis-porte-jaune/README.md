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

## Version A3 / 2 × A4, photo redressée (8 novembre)
| fichier | à quoi il sert |
|---|---|
| `croquis-A3.pdf` | le croquis, 1 page **A3 portrait** (221 × 336 mm de dessin) |
| `croquis-2xA4.pdf` | le même en 2 pages **A4 paysage** à l'échelle 1 : feuille 1 = moitié haute, feuille 2 = moitié basse (jonction à mi-hauteur) |
| `photo_redressee.jpg` | la photo redressée (3142 × 4774) : verticales verticales, horizon horizontal |

- `redresse.py` : rotation de l'appareil virtuel (sans déformation inventée) pour effacer l'inclinaison vers le haut (~9,5°) et le roulis (~1°). Écart restant : 0,08° sur les horizontales, 0,10° sur les verticales.
- `a3.py` + `rendu_a3.js` : filtre crayon, LH (y = 1393 sur 2064, soit 67 % de la hauteur), PF (x = 697, sur la LH), LT (bas de la photo), mise en page A3. Imprimer à 100 %.

```
python3 -I redresse.py photo.jpg photo_redressee.jpg
python3 -I a3.py
node rendu_a3.js "$PWD"
```

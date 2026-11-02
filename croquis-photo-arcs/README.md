# Photo des arcs : filtre crayon + LH, LT, points de fuite

| fichier | à quoi il sert |
|---|---|
| `construction.png` / `construction.pdf` | **le rendu** : la photo au crayon avec LH, LT, PF1 et les fuyantes en bleu |
| `croquis.png` | la photo passée au filtre crayon seule (1500 × 2000, mêmes pixels que la photo) |
| `photo.jpg` | la photo d'origine |

## Ce qui est fait
- **Filtre crayon** : niveaux de gris, égalisation locale (la photo est brumeuse), inversion, flou, division (« color dodge »). Rien n'est déformé ni redessiné.
- **LH (ligne d'horizon)** : y = 1430 sur la photo. C'est la hauteur des yeux : elle passe par la tête du passant au fond de la ruelle.
- **LT (ligne de terre)** : bas de la photo (y = 2000), au pied du pilier de gauche.
- **PF1** : x ≈ 1650, y = 1430, à droite, **hors de la photo**. Les fuyantes (pointillés bleus) passent par de vraies arêtes (cercles bleus) : pied du mur de la ruelle, pied des piliers, traverse de la porte jaune, haut et bas de la porte bleue.
- **PF2** : l'autre direction (perpendiculaire) fuit à gauche, très loin, hors de la feuille. Une flèche l'indique.

## Limites (honnêtes)
- La photo n'a pas de données EXIF : PF1 est mesuré à ± 300 px, et PF2 ne peut pas être placé précisément.
- Les verticales de la photo sont presque parallèles, alors que la LH est bien sous le milieu de la photo : l'appareil (ou la retouche) a redressé les verticales. La LH est donc relevée sur les objets (passant, portes, piliers), pas sur le centre de l'image.

## Régénérer
```
python3 -I croquis_filtre.py photo.jpg croquis.png
python3 construire.py
node rendu.js "$PWD"
```

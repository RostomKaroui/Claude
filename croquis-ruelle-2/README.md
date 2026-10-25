# Dessin · la ruelle aux portes bleues (2e photo), vue assise

| fichier | à quoi il sert |
|---|---|
| `croquis-A3.pdf` | le croquis, 1 page **A3 portrait** |
| `croquis-2xA4.pdf` | le même en 2 pages **A4 paysage** à l'échelle 1 (moitié haute / moitié basse) |
| `photos/ruelle2-photo.jpg` | la photo |
| `photos/ruelle2-photo-redressee.jpg` | la photo redressée : verticales verticales, 1 seul point de fuite |
| `releve-fers-forges.json` | les contours des fers forgés relevés sur la photo |

Imprimer en **taille réelle (100 %)**.

## Méthode
- Points de fuite calculés sur la photo (détection des droites) : celui de la ruelle et celui des verticales. La vue est tournée pour que les verticales soient verticales : c'est la vue de l'œil, en perspective frontale.
- La LH passe à hauteur des poignées de porte. Avec les yeux à 1,20 m (assis), la plaque d'égout fait 0,61 m — la taille d'une vraie plaque : l'échelle est juste.
- Au trait, sans hachures ni remplissage, **sans plantes**. Les fers forgés (grille de la fenêtre, balcons, balcon ventru de droite) sont relevés sur la photo.
- Les dalles du sol sont représentatives (leur taille et leur fuite sont justes, pas chaque pierre).

## Régénérer
```
python3 ruelle2.py .
node rendu.js "$PWD"
```

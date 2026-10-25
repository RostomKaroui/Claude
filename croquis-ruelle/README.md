# Dessin · la ruelle à la porte bleue, vue assise (perspective frontale)

| fichier | à quoi il sert |
|---|---|
| `croquis-A3.pdf` | le croquis corrigé, 1 page **A3 paysage** |
| `croquis-2xA4.pdf` | le même croquis en 2 pages **A4 portrait**, à l'échelle 1 (feuille 1 = moitié gauche, feuille 2 = moitié droite) |
| `apercu-*.png` | aperçus des pages |
| `photos/ruelle-photo-telephone.jpg` | la photo de la ruelle (prise au téléphone, debout) |
| `photos/croquis-eleve.webp` | le croquis de départ ; `croquis-eleve-contraste.png` : le même, contraste renforcé pour voir les traits |

Imprimer en **taille réelle (100 %)**.

## Le point de vue (ce n'est pas un calque de la photo)
- assis, **yeux à 1,20 m** du sol → la LH est à 1,20 m (la photo, prise debout, la met plus haut) ;
- regard droit devant → la **LH au milieu du cadre**, le PF au centre ;
- des **passants debout** (1,75 m) : leur tête dépasse la LH, qui leur passe à la poitrine — c'est ce qui montre qu'on est assis ;
- face à la porte bleue du fond, **un tout petit peu à droite**, à **20 m** d'elle ;
- champ de vision naturel de l'œil (~55° en largeur), pas le zoom du téléphone ;
- les verticales restent verticales ; ce qui est au-dessus du regard (le haut des murs, le fil, le support en fer forgé, la treille) est coupé ou sort du cadre.

## Régénérer
```
python3 ruelle.py .                                  # écrit croquis-A3.html et croquis-2xA4.html
node ../perspective-frontale-rue/rendu.js "$PWD"     # PDF + aperçus (Playwright)
```

# Dessin · la ruelle à la porte bleue, vue assise (perspective frontale)

| fichier | à quoi il sert |
|---|---|
| `croquis-A3.pdf` | le croquis corrigé, 1 page **A3 portrait** |
| `croquis-2xA4.pdf` | le même croquis en 2 pages **A4 paysage**, à l'échelle 1 : feuille 1 = moitié HAUTE de l'A3, feuille 2 = moitié BASSE |
| `apercu-*.png` | aperçus des pages |
| `photos/ruelle-photo-telephone.jpg` | la photo de la ruelle (prise au téléphone, debout) |
| `photos/croquis-eleve.webp` | le croquis de départ ; `croquis-eleve-contraste.png` : le même, contraste renforcé |

Imprimer en **taille réelle (100 %)**. La LH est à 1,6 cm sous la jonction des deux A4 (sur la feuille 2).

## Le point de vue (ce n'est pas un calque de la photo)
- assis, **yeux à 1,20 m** du sol → la LH est à 1,20 m (la photo, prise debout, la met plus haut) ;
- regard droit devant → la **LH au milieu du cadre**, le PF au centre ;
- face à la porte bleue du fond, **un tout petit peu à droite**, à **20 m** d'elle ;
- des **passants debout** (1,75 m) : leur tête dépasse la LH, qui leur passe à la poitrine — c'est ce qui montre qu'on est assis ;
- le support en fer forgé de la photo est au-dessus du regard : hors cadre.

## Le dessin
Au trait seulement : **ni hachures ni remplissage**. Les détails sont dessinés : claveaux, clé et piédroits en pierre taillée de l'arc, briques de son épaisseur, volets à panneaux, descente d'eau et ses colliers, pilier et panneau « Rue du Tribunal », tablette de marbre, porte à deux battants, panneaux et clous, heurtoirs, grille de la fenêtre, compteur, moellons du mur du fond, antenne, pavés, serrure, tag, sacs. Pas de plantes.

Les fers forgés sont relevés sur la photo :
- **l'imposte du portail** : bande pleine en haut, 12 modules à barreau central, barres en V et 3 rangées de volutes en paires ;
- **la grille ventrue** du mur gauche de la ruelle, vue de profil : partie plate à petits cercles en haut, ventre arrondi qui avance dans la ruelle, grandes volutes, barres courbes en panier en bas ;
- **la lanterne posée sur sa potence** : barre, platine, console à volutes (une grande près du mur puis de plus en plus petites), pied, bague, corps évasé à montants, chapeau large, couronne ;
- **le col de cygne** du mur droit : tube, crosse, boîtier, câble tendu jusqu'à sa fixation.

## Régénérer
```
python3 ruelle.py .     # écrit croquis-A3.html et croquis-2xA4.html
node rendu.js "$PWD"    # PDF + aperçus (Playwright)
```

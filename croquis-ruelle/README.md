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

## Le dessin
Au trait seulement : **ni hachures ni remplissage**. Seul ce qui est sur la photo est dessiné (pas de plantes, pas de passants).
Chaque élément est relevé sur la photo, dans le plan de son mur (la porte du fond, 2,40 m, sert d'échelle) :
- **l'arc** : une ouverture en plein cintre dans le mur blanc enduit (appui à 1,90 m, sommet à 3,80 m), épaisseur brute, fond **muré en briques** — pas de pierres taillées ;
- au-dessus, la **fenêtre haute** à deux battants vitrés ;
- la **descente d'eau** (colliers, sabot en bas) et la **gaine fine** à côté ; la petite **tige noire** à attaches ; la **planche** couchée au pied du mur ;
- la **potence en fer forgé** en haut à gauche (barre, platine, bras, 4 volutes, crochet) et le **fil** qui part de son crochet jusqu'au haut du mur au portail ;
- la **tour** : anneau d'angle, gargouille ; le **pilier** : panneau en creux, tablette de marbre, plaque « Rue Du Tribunal » ;
- la **porte bleue** : planches verticales, deux traverses en haut, poignée, seuil ; la **fenêtre** (simple cadre), la **plaque du numéro**, le **compteur** ;
- le **vieux mur** derrière : enduit, moellons visibles seulement là où l'enduit est tombé ; l'**antenne** ;
- le **mur droit de la ruelle** : 6 ouvertures, joint vertical, porte vue de profil au bout, col de cygne et câble ;
- la **grille ventrue** et la **lanterne** posée sur sa potence à volutes ;
- le **mur au portail** : haut en pente, pilier en saillie à l'angle, 2 pitons ; le **portail** : marche blanche, linteau, imposte en fer forgé (11 modules), 2 battants en tôle lisse, loquet, tag « M+D » et cœur ;
- au pied du mur : 3 sacs, une petite boîte, une boîte plate ; le sol : **pavés** dans la placette, **dalles** dans la ruelle.

## Régénérer
```
python3 ruelle.py .     # écrit croquis-A3.html et croquis-2xA4.html
node rendu.js "$PWD"    # PDF + aperçus (Playwright)
```

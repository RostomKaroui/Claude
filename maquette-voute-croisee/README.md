# Maquette de la voûte croisée (voûte d'arêtes)

Hauteur totale **12,7 cm**, emprise **12 × 12 cm**. Une voûte croisée = deux voûtes en berceau (demi-cylindres de rayon 4,5 cm) qui se croisent à angle droit : **4 voûtains**, 2 arêtes qui se rejoignent à la **clef**, 4 arcs au bord, **4 piliers**.

| fichier | à quoi il sert |
|---|---|
| `montage.html` | **la page 3D étape par étape** (à ouvrir dans un navigateur, tourne avec la souris/le doigt, flèches ← → pour les étapes) avec les mesures de chaque pièce, les conseils de matériaux et la liste de découpe |
| `patrons-A4.pdf` | **les 4 patrons à l'échelle 1** (imprimer à 100 %, une règle de 10 cm est sur chaque page pour vérifier) |
| `photos/croquis-du-prof.jpg` | le croquis du tableau |
| `geometrie.py` | la géométrie exacte + les vérifications |
| `patrons.py`, `rendu_patrons.js` | fabrication des patrons |
| `build.py`, `gabarit.html`, `rendu_montage.js` | fabrication et test de la page 3D |

## Dimensions (cm)
| pièce | qté | matière | dimensions |
|---|---|---|---|
| Socle | 1 | carton gris 2 mm | 14,0 × 14,0 (ép. 0,2) ; carrés des piliers 1,5 × 1,5 à 1,0 des bords |
| Pilier | 4 | bristol 200 g | tube carré 1,5 × 1,5 × 8,0 ; patron 6,6 × 11,0 |
| Voûtain | 4 | bristol 200 g | patron 16,14 × 6,35 : arc 14,14 (= π × 4,5), hauteur 6,0 dont bande de l'arc 1,5 ; languettes 0,5 (arête) et 1,0 × 1,5 (piliers) |
| Gabarit de contrôle | 1 | carton gris 2 mm | demi-disque rayon 4,5 (facultatif) |

L'arête du voûtain est la courbe **w = 4,5 × sin(s ÷ 4,5)** (s = distance depuis la clef) : 0 ; 0,99 ; 1,93 ; 2,78 ; 3,49 ; 4,03 ; 4,37 ; 4,50 pour s = 0 … 7 cm. Sa longueur est 8,60 cm.

## Ce qui est vérifié par le calcul (`python3 geometrie.py`)
- les 4 voûtains se touchent exactement le long des 4 arêtes (écart 1e-15 cm) ;
- les 4 clefs se rejoignent au même point, à 12,7 cm ;
- le patron conserve toutes les longueurs : un voûtain est un morceau de cylindre, il se déplie à plat sans déformation ;
- la longueur d'une arête est la même dans le patron et dans la maquette (8,6 cm) ;
- les pointes des arcs tombent exactement sur les angles intérieurs des piliers ;
- la géométrie de la page 3D (JavaScript) donne les mêmes points que le calcul Python (à 6 décimales) ;
- le PDF est à l'échelle 1 (règle de 10 cm mesurée : 99,9 mm).

## Changer la taille
Dans `geometrie.py` : `H` (hauteur des piliers, 8,0 cm → 8,3 pour 13 cm de haut), `A` (rayon), `B` (épaisseur des arcs/piliers). Puis `python3 geometrie.py && python3 patrons.py && node rendu_patrons.js "$PWD" && python3 build.py`.

## Simulation 3D en ligne
`montage-artefact.html` est la même page 3D, sans les balises `<html>/<head>/<body>`, pour être publiée comme page web (`python3 build.py && python3 artifact.py`). `montage.html` fonctionne seule dans un navigateur.

# Discussion · dessin, perspective frontale de la rue

Compte rendu de la séance de travail avec Claude (17–18 octobre 2026), 1re année d'architecture, cours de dessin.

## 1 · La demande

> salut claude comme tu sais je suis en 1ere annee architechture et aujourdhui c'est pour le dession je voudrais stp que tu me fassses comme pour latelier la derniere fois tu peux aller voir la branche stv c'est une perspective donc la je viens de te donner les photos que la prof nous a donné alors c'est pas comme en atleiier ou il faut faire une ligne dattaque A B et tout commme on a vu la derniere fois la cest des points de fuites donc ce que je voudrais que tu fasses c'est de prendre une des photos de la perspective frontale de la route avec les batiments a coté et de me les faires en croquis format A3 genre comme ta fait pour latelier fait a la main et aussi stp fait les moi sur 2 feuilles A4 pour que je puisse les imprimés et les refaires sur une feuille A3

Les 4 photos données par la prof sont dans [`photos-cours/`](photos-cours/) :

| photo | contenu |
|---|---|
| `1-planche-fig9-20.jpg` | planche « Horizon et points de fuite », fig. 9 à 20 (cubes, maisons, couloir, voie ferrée, 2 points de fuite) |
| `2-elements-de-perspective-fig14.jpg` | « Quelques éléments de perspective » : plan du tableau (PT), ligne d'horizon (LH), point de fuite (PF), point de vue (PV), ligne de terre (LT), plan de terre (PDT) |
| `3-perspective-2-points.jpg` | « 2-point perspective » : le cube qui tourne, de 1 point à 2 points de fuite |
| `4-horizon-points-de-fuite-fig43-46.jpg` | fig. 43 à 46 : rues en perspective frontale ; c'est la **fig. 44** qui a été choisie |

## 2 · Ce que Claude a fait

- Pas de branche « stv » sur le dépôt : le croquis d'atelier de la dernière fois a été retrouvé sur la branche
  `claude/tangram-formes-mouvements-rdqcvm` (dossier `croquis-perspective/`, méthode du cadrage à l'acétate avec A, B, A', B', C, D).
  Son rendu « au crayon » (traits qui tremblent et dépassent, construction en bleu, croquis en gris, police manuscrite) a été repris.
- Choix du modèle : la **fig. 44**, la rue en perspective frontale avec la ligne d'horizon à 1,75 m (hauteur des yeux).
- La rue est construite en vraie 3D puis projetée avec **un seul point de fuite** :
  l'œil est à 1,75 m du sol, au milieu de la rue, à 18 m du plan du tableau.
  - chaussée de 7 m, trottoirs, façades alignées, un immeuble en retrait à droite ;
  - immeubles de hauteurs différentes, fenêtres, bandeaux vitrés, vitrines au rez-de-chaussée ;
  - ligne médiane, passage piéton, bordures, joints du trottoir, lampadaires, passants.
- Construction en bleu : LH, LT, PF, fuyantes en pointillés, cote de 1,75 m entre la LT et la LH,
  grille de report en carreaux de 3 cm partant du PF, et les 6 étapes écrites en haut à droite.
- Retouches après les premiers aperçus : œil reculé (12 m → 18 m) pour une perspective moins « grand angle »,
  annotations déplacées pour ne pas chevaucher les lampadaires ni la jonction des deux A4, étiquettes « PF → » / « ← PF » sur chaque feuille.

## 3 · Les fichiers rendus

| fichier | à quoi il sert |
|---|---|
| `croquis-A3.pdf` | le croquis complet, 1 page A3 paysage |
| `croquis-2xA4.pdf` | le même croquis en 2 pages A4 portrait, à l'échelle 1 : feuille 1 = moitié gauche de l'A3, feuille 2 = moitié droite |
| `apercu-A3.png`, `apercu-A4-1.png`, `apercu-A4-2.png` | aperçus |
| `croquis.py`, `rendu.js` | les scripts qui fabriquent le dessin (voir le [README](README.md)) |

Imprimer en **taille réelle (100 %)**. Le PF tombe pile sur la jonction des deux feuilles A4.

### Les étapes pour refaire le dessin sur l'A3
1. Le cadre (39 × 24 cm, à 1,5 cm des bords), la LH à 15,6 cm sous le haut du cadre, le PF au milieu.
2. La LT à 3,0 cm sous la LH (= 1,75 m, la hauteur des yeux).
3. Bords de la chaussée et pieds des façades : fuyantes vers le PF.
4. Arêtes des immeubles : verticales ; toits : fuyantes vers le PF.
5. Fenêtres : hauts et bas sur des fuyantes, côtés verticaux (de plus en plus serrés en s'éloignant).
6. Lampadaires et passants : la tête de chaque passant est sur la LH, quelle que soit sa distance.

### À retenir pour la prof
- En perspective frontale, il n'y a qu'**un seul point de fuite**, au milieu de la ligne d'horizon, en face de l'œil.
- Les **verticales restent verticales** et les **horizontales de face restent horizontales** ; seules les lignes qui partent en profondeur fuient vers le PF.
- Un passant mesure environ 1,75 m comme la hauteur des yeux : **sa tête est toujours sur la LH**, qu'il soit près ou loin.

## 4 · Suite

- Proposition restée ouverte : faire de la même façon la **fig. 46** (le boulevard avec les lampadaires au milieu).
- 18 octobre : à la demande, création de la branche `claude/dessin-perspective-frontale` pour ce dessin, avec ce compte rendu et les photos du cours.

## 5 · Le rendu de dessin : la ruelle à la porte bleue (25 octobre)

> du coup on a un rendu pour le dessin la prochaine fois j'ai deja fait un croquis je vais te le donner et dis moi si il est juste ou pas stp sinon corrige le et rend le moi en croquis fait a la main et aussi quand je vais te demander de faire lautre croquis stp il faut que tu mettes a ma place comme si tu etais assis et tu faisait le croquis et non pas a partir de la photo du telephone

Puis, avec la photo : *« la LH et LT et PF elles y sont mais c'est en trait très très très fin […] j'étais assis en face de la porte bleue un tout petit peu à droite et à environ 20 mètres »*.

Tout est dans [`../croquis-ruelle/`](../croquis-ruelle/) : la photo, le croquis de départ (et une version au contraste renforcé), le croquis corrigé en A3 et en 2 × A4.

### Le retour sur le croquis de départ
**Bien :** les verticales sont verticales ; les faces vues de face ont leurs horizontales horizontales ; un cadre est posé ; la LH, la LT et le PF sont tracés (mais invisibles sur la photo).

**À reprendre :**
1. LH, LT et PF tracés trop fin : il faut qu'ils se voient (trait fin mais net, ou en couleur), c'est la construction que la prof note.
2. Les murs de la ruelle ne fuient pas vers le PF : la profondeur de la ruelle n'est pas construite.
3. Les grands volumes (le mur à l'arc à gauche, le mur au portail à droite, la ruelle, le mur du fond) manquent ou sont à peine indiqués, alors que des détails (le support en fer forgé, la planche) sont dessinés grands.
4. Des éléments flottent, sans ligne de sol.
5. Le trait est partout du même poids et très léger ; la feuille est peu remplie et froissée.

### Le croquis corrigé
Reconstruit en 3D d'après la photo puis dessiné **depuis la place assise** : LH à 1,20 m, PF un peu à droite de la porte, porte à 20 m (petite, juste sous la LH), champ de vision de l'œil (~55°), verticales verticales. Le support en fer forgé et la treille, au-dessus du regard, sortent du cadre.

### Retouche : « là t'es pas assis, c'est une vue debout »
La première version calculait bien des yeux à 1,20 m, mais elle ne se lisait pas comme une vue assise : la LH était placée bas dans le cadre (comme si on regardait vers le haut) et il n'y avait personne dans la scène pour comparer. Corrigé :
- regard droit devant : la **LH au milieu du cadre**, le PF au centre, plus de sol au premier plan, le haut des murs coupé ;
- trois **passants debout** (1,75 m) : leur tête dépasse la LH, qui leur passe à la poitrine. Debout, c'est la tête des passants qui serait sur la LH.

### Retouche : « pas de hachures, il manque des détails, et c'est en portrait »
- **Plus aucune hachure ni aucun remplissage** : tout est au trait (« ce n'est pas de l'art plastique »).
- **Les détails** : la pierre taillée de l'arc (claveaux, clé, piédroits alternés, imposte), les briques de son épaisseur, les volets à panneaux, la descente d'eau et ses colliers, le pilier avec sa corniche et le panneau « Rue du Tribunal », la porte bleue (2 battants, panneaux, clous, heurtoirs, seuil), la grille de la fenêtre, les moellons du mur du fond, le moucharabieh, la lanterne et sa potence à volutes, le portail à volutes avec sa serrure, la treille, les pavés.
- **A3 portrait** (et 2 × A4 paysage : moitié haute et moitié basse).

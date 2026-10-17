# Dessin · perspective frontale (1 point de fuite) — la rue

D'après la **fig. 44** du polycopié « Horizon et points de fuite » (photo : `modele-fig44-46.jpg`).

| fichier | à quoi il sert |
|---|---|
| `croquis-A3.pdf` | le croquis complet, 1 page **A3 paysage** |
| `croquis-2xA4.pdf` | le même croquis coupé en 2 pages **A4 portrait**, à l'échelle 1 : la feuille 1 = moitié gauche de l'A3, la feuille 2 = moitié droite. Mises côte à côte, elles font exactement l'A3. |
| `apercu-*.png` | aperçus des pages |

Imprimer en **taille réelle (100 %)**, pas « ajuster à la page ».

## Construction (en bleu sur le croquis)
1. Cadre 39 × 24 cm, à 1,5 cm des bords de l'A3. LH à 15,6 cm sous le haut du cadre, PF au milieu de la LH (= pile sur la jonction des deux A4).
2. LT à 3,0 cm sous la LH : c'est 1,75 m, la hauteur des yeux, à l'échelle du tableau.
3. Bords de la chaussée, bordures et pieds des façades : fuyantes vers le PF.
4. Arêtes des immeubles : verticales. Toits et corniches : fuyantes vers le PF.
5. Fenêtres : hauts et bas sur des fuyantes, côtés verticaux, de plus en plus serrés en s'éloignant.
6. Lampadaires et passants : la tête de chaque passant (1,75 m) est sur la LH, quelle que soit sa distance.

Carreaux bleus de 3 cm partant du PF : pour reporter le dessin carreau par carreau.

## Régénérer
```
python3 croquis.py .   # écrit croquis-A3.html et croquis-2xA4.html
node rendu.js .        # PDF + aperçus (Playwright)
```

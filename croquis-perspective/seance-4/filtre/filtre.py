"""Filtre croquis (crayon) appliqué à la photo d'origine, sans rien changer d'autre.
Méthode classique du « dessin au crayon » : niveaux de gris, négatif flouté, fusion en « densité couleur - »
(color dodge), un léger renfort des contours (différence de gaussiennes) pour le trait,\net une estompe des valeurs sombres de la photo.
Lancer : python3 filtre.py <photo> [sortie.png] -> croquis-filtre.png par défaut"""
import sys
import cv2
import numpy as np

src = sys.argv[1]
im = cv2.imread(src)
g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
g = cv2.fastNlMeansDenoising(g, None, 5, 7, 21).astype(np.float32)      # enlève le grain de la photo (sinon il ressort en « bruit »)

# 1. crayon : color dodge du gris par son négatif flouté
neg_flou = cv2.GaussianBlur(255 - g, (0, 0), 9)
crayon = np.clip(g * 255 / np.maximum(255 - neg_flou, 1), 0, 255)

# 2. trait : contours fins (différence de gaussiennes), assombrissent légèrement le crayon
dog = cv2.GaussianBlur(g, (0, 0), 0.8) - cv2.GaussianBlur(g, (0, 0), 2.2)
trait = np.clip(1 + dog / 22, 0.55, 1)                       # < 1 là où il y a un bord sombre

# 3. ombres : une partie des valeurs de la photo, en estompe, pour garder les zones sombres (grilles, silhouettes, ombre)
ombre = 0.8 + 0.2 * (cv2.GaussianBlur(g, (0, 0), 1.5) / 255) ** 0.8

out = crayon * trait * ombre
out = 255 * (out / 255) ** 1.3                              # un peu plus de mine, sans noircir
sortie = sys.argv[2] if len(sys.argv) > 2 else "croquis-filtre.png"
cv2.imwrite(sortie, np.clip(out, 0, 255).astype(np.uint8))
print(sortie, "écrit", out.shape)

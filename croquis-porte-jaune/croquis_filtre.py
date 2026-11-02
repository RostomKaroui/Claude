"""Filtre « crayon » appliqué à la photo, sans rien déformer : mêmes pixels, même cadrage.
Technique classique : niveaux de gris -> égalisation locale (la photo est brumeuse) -> inversion -> flou
-> division (color dodge). Sortie : croquis.png (1500 x 2000, comme la photo)."""
import cv2, numpy as np, sys
src, out = sys.argv[1], sys.argv[2]
im = cv2.imread(src)
g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
g = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8)).apply(g)           # la brume écrase les contrastes
inv = 255 - g
flou = cv2.GaussianBlur(inv, (0, 0), 9)
dodge = cv2.divide(g, 255 - flou, scale=256)                                 # color dodge : traits de crayon
dodge = np.clip(dodge.astype(np.float32), 0, 255)
# papier légèrement chaud, contraste du trait un peu renforcé
t = (dodge / 255.0) ** 1.35
t = np.clip((t - 0.06) / 0.94, 0, 1)
papier = np.array([248, 252, 253], np.float32)                               # BGR : blanc cassé
crayon = np.array([48, 48, 52], np.float32)
res = papier[None, None, :] * t[..., None] + crayon[None, None, :] * (1 - t[..., None])
cv2.imwrite(out, np.clip(res, 0, 255).astype(np.uint8))
print("écrit", out, res.shape)

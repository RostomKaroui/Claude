"""Efface les personnes de la photo d'origine : LaMa (big-lama, TorchScript) reconstitue le fond sous le masque.
Seule la zone masquée change ; tout le reste de la photo est remis à l'identique.
Lancer : python3 efface.py <photo> <masque-personnes.png> <big-lama.pt> -> photo-sans-personnes.png"""
import sys
import cv2
import numpy as np
import torch

photo, masque, modele = sys.argv[1:4]
im = cv2.imread(photo)
m = cv2.imread(masque, cv2.IMREAD_GRAYSCALE)

# on ne travaille que sur la bande du bas (les personnes), avec du contexte autour
y0, y1 = 900, im.shape[0]
crop, mc = im[y0:y1], m[y0:y1]
h, w = mc.shape
H, W = (h + 7) // 8 * 8, (w + 7) // 8 * 8
img = np.pad(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB), ((0, H - h), (0, W - w), (0, 0)), mode="reflect")
msk = np.pad(mc, ((0, H - h), (0, W - w)), mode="reflect")

lama = torch.jit.load(modele, map_location="cpu").eval()
with torch.inference_mode():
    t_img = torch.from_numpy(img).permute(2, 0, 1)[None].float() / 255
    t_msk = (torch.from_numpy(msk)[None, None].float() > 127).float()
    res = lama(t_img, t_msk)[0].permute(1, 2, 0).clamp(0, 1).numpy()
res = cv2.cvtColor((res[:h, :w] * 255).round().astype(np.uint8), cv2.COLOR_RGB2BGR)

# fondu doux au bord du masque, et la photo d'origine partout ailleurs
a = cv2.GaussianBlur((mc > 127).astype(np.float32), (0, 0), 2)[..., None]
a = np.maximum(a, (mc > 127)[..., None])
out = im.copy()
out[y0:y1] = (res * a + crop * (1 - a)).round().astype(np.uint8)
cv2.imwrite("photo-sans-personnes.png", out)
print("photo-sans-personnes.png écrit")

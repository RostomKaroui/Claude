# ===== crayon par-dessus l'aquarelle, marges, export =====
graphite = np.array([0.24, 0.25, 0.30], np.float32)
a = np.clip(dark * 0.9, 0, 1)
canvas = canvas * (1 - a[..., None] * (1 - graphite))
canvas = np.clip(canvas, 0, 1)
out = (canvas * 255).astype(np.uint8)
PW = 2040; PH = int(round(PW * 1.4142))
page = np.zeros((PH, PW, 3), np.uint8); page[:] = (np.array([0.945, 0.975, 0.99]) * 255).astype(np.uint8)  # BGR
ox, oy = (PW - W) // 2, (PH - H) // 2
page[oy:oy + H, ox:ox + W] = out[..., ::-1]
cv2.imwrite(os.path.join(HERE, "..", "Avenue_HB_aquarelle.png"), page)   # rect est deja en BGR-compatible (canvas suit l'ordre RGB -> voir ci-dessous)

# version "traits seuls" (ton crayon + les ajouts) pour imprimer et peindre soi-meme
a2 = np.clip(dark * 1.15, 0, 1)
lines = np.ones((H, W, 3), np.float32) * np.array([0.99, 0.985, 0.97], np.float32)
lines *= 1 - a2[..., None] * (1 - np.array([0.30, 0.31, 0.36], np.float32))
pg = np.ones((PH, PW, 3), np.uint8) * 253
pg[oy:oy + H, ox:ox + W] = (np.clip(lines, 0, 1) * 255).astype(np.uint8)
cv2.imwrite(os.path.join(HERE, "..", "Avenue_HB_traits_a_peindre.png"), pg[..., ::-1])

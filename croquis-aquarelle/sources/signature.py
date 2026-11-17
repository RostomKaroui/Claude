# Signature au crayon en bas a droite de la feuille (ajoutee apres la peinture)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
NOM = "Rostom Karoui"
def signer(path):
    im = Image.open(path).convert("RGB"); Wp, Hp = im.size
    font = ImageFont.truetype(os.path.join(HERE, "fonts", "caveat-700.ttf"), 82)
    layer = Image.new("L", (900, 220), 0); d = ImageDraw.Draw(layer)
    d.text((20, 40), NOM, font=font, fill=255)
    bb = layer.getbbox(); layer = layer.crop((bb[0] - 10, bb[1] - 10, bb[2] + 10, bb[3] + 10))
    layer = layer.rotate(3, resample=Image.BICUBIC, expand=True).filter(ImageFilter.GaussianBlur(0.6))
    a = np.asarray(layer, np.float32) / 255 * 0.85
    a *= np.clip(0.80 + 0.25 * np.random.default_rng(5).standard_normal(a.shape), 0.4, 1.0)   # grain du crayon
    x0 = Wp - layer.width - 90; y0 = Hp - layer.height - 45
    arr = np.asarray(im, np.float32) / 255
    reg = arr[y0:y0 + layer.height, x0:x0 + layer.width]
    reg[:] = reg * (1 - a[..., None] * (1 - np.array([0.24, 0.25, 0.30], np.float32)))
    Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8)).save(path)
for n in ("Avenue_HB_aquarelle.png", "Avenue_HB_traits_a_peindre.png"): signer(os.path.join(HERE, "..", n))

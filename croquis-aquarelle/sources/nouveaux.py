# ===== Ajouts : skatepark (inspire de l'image 2) + banc en bois ondule (image 4) =====
exec(open(os.path.join(HERE, "crayon.py")).read())
def maskpoly(pts_xyz): return polyR(SL(pts_xyz))
def ombre_lilas(mask, k=0.5): wash(mask, (0.64, 0.63, 0.78), k=k, edge=0.1, var=0.4, rough=6, soft=4)
def round_poly(pts, r, n=6):
    pts = [np.array(p, float) for p in pts]; out = []
    for i in range(len(pts)):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % len(pts)]
        da, dc = (a - b) / np.linalg.norm(a - b), (c - b) / np.linalg.norm(c - b)
        p0, p2 = b + da * r, b + dc * r
        for t in np.linspace(0, 1, n): out.append(tuple((1 - t) ** 2 * p0 + 2 * t * (1 - t) * b + t ** 2 * p2))
    return out
def ellipse_r(c, ax, ay):
    m = np.zeros((H, W), np.uint8); cv2.ellipse(m, (int(c[0]), int(c[1])), (int(max(1, ax)), int(max(1, ay))), 0, 0, 360, 255, -1); return m.astype(np.float32) / 255
def contour_strokes(mask, p=0.55, w=1.7, chunk=60):
    m8 = (mask > 0.5).astype(np.uint8) * 255
    cs, _ = cv2.findContours(m8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cs:
        pts = cv2.approxPolyDP(c, 1.4, True).reshape(-1, 2).astype(np.float32)
        if len(pts) < 4: continue
        n = len(pts); i = int(rng.integers(0, n))
        pts = np.roll(pts, -i, axis=0); k = 0
        while k < n:
            L = int(rng.integers(chunk // 2, chunk)); seg = pts[k:k + L + 3]
            if len(seg) >= 2: stroke([tuple(q) for q in seg], p=p * rng.uniform(0.75, 1.0), w=w, wob=0.5, over=1.5)
            k += L
# ------------------------------------------------------------------ personnages
def limb(m, a, b, ra, rb):
    a, b = np.array(a, np.float32), np.array(b, np.float32); L = np.hypot(*(b - a)); n = max(2, int(L / max(1, min(ra, rb) * 0.6)))
    for t in np.linspace(0, 1, n): c = a + (b - a) * t; cv2.circle(m, (int(c[0]), int(c[1])), max(1, int(ra + (rb - ra) * t)), 255, -1)
def personne3d(X, Y, Z, chemise, pantalon, pose="debout", planche=None, cheveux=(0.20, 0.15, 0.12), peau=(0.88, 0.68, 0.54), bras="bas", livre=False, sexe="h"):
    s = px_m(Z); J = {}
    if pose == "assis":
        J.update(hL=(X - .11, Y + .06, Z), hR=(X + .11, Y + .06, Z), kL=(X - .13, Y + .08, Z - .42), kR=(X + .12, Y + .05, Z - .40), fL=(X - .15, Y - .40, Z - .48), fR=(X + .13, Y - .40, Z - .44),
                 sL=(X - .19, Y + .58, Z), sR=(X + .19, Y + .60, Z), nk=(X, Y + .66, Z), hd=(X, Y + .82, Z))
    elif pose == "skate":
        J.update(hL=(X - .12, Y + .76, Z), hR=(X + .10, Y + .78, Z), kL=(X - .30, Y + .42, Z - .06), kR=(X + .26, Y + .44, Z - .02), fL=(X - .22, Y + .04, Z), fR=(X + .22, Y + .04, Z),
                 sL=(X - .12, Y + 1.26, Z - .06), sR=(X + .30, Y + 1.30, Z - .04), nk=(X + .09, Y + 1.36, Z - .06), hd=(X + .12, Y + 1.52, Z - .08))
    else:
        J.update(hL=(X - .10, Y + .90, Z), hR=(X + .10, Y + .93, Z), kL=(X - .13, Y + .47, Z - .05), kR=(X + .10, Y + .49, Z), fL=(X - .16, Y + .02, Z - .08), fR=(X + .10, Y + .02, Z),
                 sL=(X - .20, Y + 1.44, Z), sR=(X + .20, Y + 1.41, Z), nk=(X, Y + 1.50, Z), hd=(X + .01, Y + 1.66, Z))
    sh = J['sL'], J['sR']
    if bras == "bas": J.update(eL=(sh[0][0] - .06, sh[0][1] - .30, Z), eR=(sh[1][0] + .05, sh[1][1] - .30, Z), wL=(sh[0][0] - .04, sh[0][1] - .58, Z - .05), wR=(sh[1][0] + .06, sh[1][1] - .58, Z))
    elif bras == "ecarte": J.update(eL=(sh[0][0] - .30, sh[0][1] - .02, Z), eR=(sh[1][0] + .32, sh[1][1] - .14, Z), wL=(sh[0][0] - .60, sh[0][1] + .10, Z), wR=(sh[1][0] + .62, sh[1][1] - .26, Z))
    elif bras == "livre": J.update(eL=(sh[0][0] - .07, sh[0][1] - .30, Z - .10), eR=(sh[1][0] + .07, sh[1][1] - .30, Z - .10), wL=(X - .08, sh[0][1] - .36, Z - .40), wR=(X + .10, sh[1][1] - .36, Z - .40))
    elif bras == "hanche": J.update(eL=(sh[0][0] - .20, sh[0][1] - .28, Z), eR=(sh[1][0] + .05, sh[1][1] - .30, Z), wL=(J['hL'][0] - .02, J['hL'][1] + .04, Z), wR=(sh[1][0] + .07, sh[1][1] - .58, Z))
    Q = {k: np.array(S(*v), np.float32) for k, v in J.items()}
    z8 = lambda: np.zeros((H, W), np.uint8)
    # planche
    if planche:
        if planche == "dessous": d0, d1 = S(X - .42, Y, Z), S(X + .42, Y, Z)
        else: d0, d1 = S(X + .50, Y, Z - .05), S(X + 1.18, Y, Z + .05)
        mb = z8(); limb(mb, d0, d1, 0.045 * s, 0.045 * s); mb = mb.astype(np.float32) / 255
        wash(mb, (0.30, 0.62, 0.66), k=0.95, edge=0.35, var=0.1, rough=0.8, soft=0.8)
        contour_strokes(mb, p=0.7, w=1.7)
        for t in (0.17, 0.83):
            c = np.array(d0) + (np.array(d1) - np.array(d0)) * t + [0, 0.05 * s]
            mw = ellipse_r(c, 0.038 * s, 0.038 * s); wash(mw, (0.22, 0.22, 0.25), k=0.95, edge=0.1, var=0.1, rough=0.4, soft=0.5)
    # groupes de couleur (union => pas de surcharges aux articulations)
    legs, shirt, skin, hair, shoes = z8(), z8(), z8(), z8(), z8()
    for a, b, c in (("hL", "kL", "fL"), ("hR", "kR", "fR")): limb(legs, Q[a], Q[b], 0.088 * s, 0.062 * s); limb(legs, Q[b], Q[c], 0.060 * s, 0.040 * s)
    waist = 0.5 * (Q['hL'] + Q['hR']); wd = 0.5 * np.abs(Q['hR'][0] - Q['hL'][0]) + 0.05 * s
    cv2.fillPoly(shirt, [np.round(np.array([Q['sL'] + [-0.02 * s, -0.02 * s], Q['sR'] + [0.02 * s, -0.02 * s], [Q['hR'][0] + wd * 0.3, Q['hR'][1] - 0.12 * s], [Q['hL'][0] - wd * 0.3, Q['hL'][1] - 0.12 * s]])).astype(np.int32)], 255)
    for a, b in (("sL", "eL"), ("sR", "eR")): limb(shirt, Q[a], Q[b], 0.058 * s, 0.046 * s)
    for a, b in (("eL", "wL"), ("eR", "wR")): limb(skin, Q[a], Q[b], 0.040 * s, 0.030 * s)
    for k in ("wL", "wR"): cv2.circle(skin, (int(Q[k][0]), int(Q[k][1])), int(0.035 * s), 255, -1)
    cv2.line(skin, tuple(int(v) for v in Q['nk']), tuple(int(v) for v in (Q['hd'] + [0, 0.07 * s])), 255, max(2, int(0.09 * s)))
    cv2.ellipse(skin, tuple(int(v) for v in Q['hd']), (int(0.098 * s), int(0.122 * s)), 0, 0, 360, 255, -1)
    cv2.ellipse(hair, tuple(int(v) for v in (Q['hd'] + [0, -0.028 * s])), (int(0.104 * s), int(0.100 * s)), 0, 180, 360, 255, -1)
    if sexe == "f": limb(hair, Q['hd'] + [-0.09 * s, 0], Q['hd'] + [-0.10 * s, 0.22 * s], 0.035 * s, 0.03 * s); limb(hair, Q['hd'] + [0.09 * s, 0], Q['hd'] + [0.10 * s, 0.22 * s], 0.035 * s, 0.03 * s)
    for k in ("fL", "fR"): cv2.ellipse(shoes, tuple(int(v) for v in Q[k] + [0, 0.012 * s]), (int(0.085 * s), int(0.040 * s)), 0, 0, 360, 255, -1)
    f = lambda m: m.astype(np.float32) / 255
    legs, shirt, skin, hair, shoes = f(legs), f(shirt), f(skin), f(hair), f(shoes)
    skin = skin * (1 - shirt) * (1 - hair)
    wash(legs, pantalon, k=0.92, edge=0.45, var=0.25, rough=0.9, soft=0.8)
    wash(shirt, chemise, k=0.92, edge=0.45, var=0.30, rough=1.0, soft=0.8)
    gx = np.clip(1.2 - (xx - Q['sL'][0]) / (0.5 * s + 1), 0, 1)           # cote gauche a l'ombre (soleil a droite)
    wash(shirt * gx, tuple(np.array(chemise) * 0.75), k=0.35, edge=0.0, var=0.2, rough=0.8, soft=1.5)
    wash(legs * np.clip(1.2 - (xx - Q['hL'][0]) / (0.4 * s + 1), 0, 1), tuple(np.array(pantalon) * 0.75), k=0.35, edge=0.0, var=0.2, rough=0.8, soft=1.5)
    wash(skin, peau, k=0.92, edge=0.35, var=0.15, rough=0.8, soft=0.8)
    wash(hair, cheveux, k=0.95, edge=0.2, var=0.1, rough=0.8, soft=0.7)
    wash(shoes, (0.93, 0.93, 0.92), k=0.85, edge=0.4, var=0.1, rough=0.6, soft=0.6)
    for mk, pp in ((legs, 0.55), (shirt, 0.55), (skin, 0.45), (hair, 0.5), (shoes, 0.55)): contour_strokes(mk, p=pp, w=1.6, chunk=55)
    wash(ellipse_r(S(X, Y, Z), 0.40 * s, 0.09 * s), (0.62, 0.62, 0.76), k=0.35, edge=0.0, var=0.1, rough=2, soft=3)
    if livre:
        a, b = Q['wL'], Q['wR']; pg = polyR([a + [-9, -6], b + [9, -6], b + [9, 24], a + [-9, 24]])
        wash(pg, (0.95, 0.93, 0.86), k=0.9, edge=0.3, var=0.1, rough=0.8, soft=0.7); contour_strokes(pg, p=0.6, w=1.5)

# ------------------------------------------------------------------ SKATEPARC : plateau beton, croissant-rampe, banc rond, murets courbes, marches lumineuses, haies
cx, cz = 3.35, 15.3
slabp = round_poly([(1.15, 12.5), (4.95, 12.5), (5.75, 18.7), (1.15, 18.7)], 0.7)
slabS = SL([(X, 0, Z) for X, Z in slabp]); slab_m = polyR(slabS)
wash(slab_m, (0.76, 0.78, 0.86), k=0.70, edge=0.45, var=0.40, rough=4)
wash(slab_m * np.clip(noise(26), 0, 1), (0.68, 0.70, 0.82), k=0.35, edge=0.0, var=0.3, rough=4)
poly_stroke(slabS, p=0.85, w=2.4, wob=0.8)
stroke(SL([(X, 0.05, Z) for X, Z in slabp] + [(slabp[0][0], 0.05, slabp[0][1])]), p=0.4, w=1.4, wob=0.7)
for X in np.arange(1.6, 5.6, 0.95): stroke(SL([(X, 0, 12.7), (X + 0.15 * (X - 3.3) / 2, 0, 18.5)]), p=0.20, w=1.3, wob=0.7, over=0, mask=slab_m)
for Z in np.arange(13.4, 18.6, 0.95): stroke(SL([(1.2, 0, Z), (5.7, 0, Z)]), p=0.20, w=1.3, wob=0.7, over=0, mask=slab_m)
# rampe en croissant (concave vers le spectateur)
th = np.deg2rad(np.linspace(42, 138, 44)); r_in, r_out, hl = 2.1, 3.0, 1.05
prof_y = lambda s_: hl * s_ ** 2.0
bot = SL([(cx + r_in * np.cos(t), 0, cz + r_in * np.sin(t)) for t in th]); top = SL([(cx + r_out * np.cos(t), hl, cz + r_out * np.sin(t)) for t in th])
ramp_m = polyR(bot + top[::-1])
bx0, bx1 = min(p[0] for p in bot + top), max(p[0] for p in bot + top)
g = np.clip((xx - bx0) / (bx1 - bx0 + 1e-6), 0, 1)                   # 0 = gauche (ombre) -> 1 = droite (soleil)
wash(ramp_m, (0.88, 0.86, 0.86), k=0.55, edge=0.35, var=0.3, rough=2)
wash(ramp_m * (1 - g) ** 0.9, (0.54, 0.56, 0.72), k=0.90, edge=0.2, var=0.35, rough=2)
wash(ramp_m * np.clip((yy - np.minimum.reduce([p[1] for p in top])) / 140, 0, 1) * 0.5, (0.70, 0.70, 0.80), k=0.4, edge=0.0, var=0.2, rough=2)
lip_m = np.zeros((H, W), np.uint8); cv2.polylines(lip_m, [np.round(np.array(top)).astype(np.int32)], False, 255, 10, cv2.LINE_AA)
wash(lip_m.astype(np.float32) / 255, (0.99, 0.85, 0.45), k=0.85, edge=0.0, var=0.2, rough=1.5, soft=2.0)
stroke(bot, p=0.9, w=2.6, wob=0.7); stroke(top, p=1.0, w=2.8, wob=0.7)
stroke(SL([(cx + (r_out + .14) * np.cos(t), hl + .07, cz + (r_out + .14) * np.sin(t)) for t in th]), p=0.6, w=1.8, wob=0.6)
stroke([bot[0], top[0]], p=0.85, w=2.2, wob=0.4); stroke([bot[-1], top[-1]], p=0.85, w=2.2, wob=0.4)
for t in np.deg2rad(np.linspace(46, 134, 15)):
    pts = [(cx + (r_in + (r_out - r_in) * s_) * np.cos(t), prof_y(s_), cz + (r_in + (r_out - r_in) * s_) * np.sin(t)) for s_ in np.linspace(0, 1, 9)]
    stroke(SL(pts), p=0.34, w=1.4, wob=0.5, over=0)
hatch(ramp_m * (1 - g) ** 1.3, ang=72, gap=5, p=0.42, w=1.2)
hatch(ramp_m * (1 - g) ** 2.2, ang=-20, gap=7, p=0.30, w=1.1)
# banc rond au centre du plateau
ro, ri, hb = 0.82, 0.55, 0.44; bx, bz = 3.35, 13.95
ob, ot, it = circ_pts(bx, bz, ro, 0), circ_pts(bx, bz, ro, hb), circ_pts(bx, bz, ri, hb)
hull = cv2.convexHull(np.round(np.array(ot + ob)).astype(np.int32)); wall = np.zeros((H, W), np.uint8); cv2.fillConvexPoly(wall, hull, 255); wall = wall.astype(np.float32) / 255
wash(wall, (0.72, 0.72, 0.82), k=0.75, edge=0.45, var=0.3, rough=2)
wash(wall * (1 - g) ** 0.8, (0.52, 0.54, 0.70), k=0.5, edge=0.0, var=0.3, rough=2)
wash(polyR(ot) * (1 - polyR(it)), (0.92, 0.90, 0.88), k=0.50, edge=0.3, var=0.3, rough=1.5)
wash(polyR(it), (0.70, 0.72, 0.80), k=0.60, edge=0.2, var=0.3, rough=1.5)
for pts, pp in ((ot, 0.9), (it, 0.75)): poly_stroke(pts, p=pp, w=2.2, wob=0.5)
stroke(ob[: len(ob) // 2 + 1], p=0.85, w=2.2, wob=0.5)
stroke([ot[0], ob[0]], p=0.85, w=2.0, wob=0.3, over=0); stroke([ot[len(ot) // 2], ob[len(ob) // 2]], p=0.85, w=2.0, wob=0.3, over=0)
# muret courbe (a gauche), avec bandeau lumineux
cur = spline([(1.75, 13.1), (1.55, 14.4), (1.65, 15.9), (2.15, 17.3)], 10); hm_ = 0.5
tx = [(X - .10, hm_, Z) for X, Z in cur]; ty = [(X + .10, hm_, Z) for X, Z in cur]; bx_ = [(X - .10, 0, Z) for X, Z in cur]
wash(polyR(SL(tx) + SL(ty)[::-1]), (0.92, 0.90, 0.88), k=0.5, edge=0.3, var=0.2, rough=1.5)
wash(polyR(SL(tx) + SL(bx_)[::-1]), (0.58, 0.60, 0.74), k=0.85, edge=0.4, var=0.3, rough=1.5)
led2 = np.zeros((H, W), np.uint8); cv2.polylines(led2, [np.round(np.array(SL(tx))).astype(np.int32)], False, 255, 6, cv2.LINE_AA)
wash(led2.astype(np.float32) / 255, (0.99, 0.84, 0.44), k=0.9, edge=0.0, var=0.1, rough=0.8, soft=1.6)
stroke(SL(tx), p=0.9, w=2.2, wob=0.5); stroke(SL(ty), p=0.7, w=1.8, wob=0.5); stroke(SL(bx_), p=0.85, w=2.0, wob=0.5)
stroke([SL(tx)[0], SL(bx_)[0]], p=0.8, w=1.8, wob=0.3, over=0); stroke([SL(tx)[-1], SL(bx_)[-1]], p=0.8, w=1.8, wob=0.3, over=0)
# marches eclairees (a droite)
for k in range(3):
    X0, X1 = 4.1, 4.95; Z0 = 12.95 + 0.6 * k; Z1 = Z0 + 0.6; h = 0.17 * (k + 1)
    top_s = [(X0, h, Z0), (X1, h, Z0), (X1, h, Z1), (X0, h, Z1)]; fr_s = [(X0, 0, Z0), (X1, 0, Z0), (X1, h, Z0), (X0, h, Z0)]; lf_s = [(X0, 0, Z0), (X0, 0, Z1), (X0, h, Z1), (X0, h, Z0)]
    wash(maskpoly(top_s), (0.92, 0.90, 0.88), k=0.50, edge=0.3, var=0.2, rough=1.2); wash(maskpoly(fr_s), (0.74, 0.74, 0.84), k=0.75, edge=0.3, var=0.2, rough=1.2); wash(maskpoly(lf_s), (0.56, 0.58, 0.74), k=0.8, edge=0.3, var=0.2, rough=1.2)
    led = np.zeros((H, W), np.uint8); cv2.polylines(led, [np.round(np.array(SL([(X0, h, Z0), (X1, h, Z0)]))).astype(np.int32)], False, 255, 7, cv2.LINE_AA)
    wash(led.astype(np.float32) / 255, (0.99, 0.83, 0.40), k=0.95, edge=0.0, var=0.1, rough=0.8, soft=1.5)
    for sset in (top_s, fr_s, lf_s): poly_stroke(SL(sset), p=0.85, w=2.0, wob=0.5)
# haies : boules de buis alignees (organique, pas des blocs)
def haie(X, Zs, r=0.33):
    msk = np.zeros((H, W), np.uint8); hi = np.zeros((H, W), np.uint8)
    for Z in Zs:
        c = S(X + rng.uniform(-.04, .04), r * 1.2, Z + rng.uniform(-.05, .05)); rr = r * px_m(Z) * rng.uniform(0.9, 1.1)
        cv2.circle(msk, (int(c[0]), int(c[1])), int(rr), 255, -1); cv2.circle(hi, (int(c[0] + rr * .25), int(c[1] - rr * .3)), int(rr * .55), 255, -1)
        stroke([(c[0] + rr * np.cos(a), c[1] + rr * np.sin(a)) for a in np.linspace(-0.2, 2 * np.pi - 0.6, 18)], p=0.7, w=1.8, wob=1.0, over=0)
    msk = msk.astype(np.float32) / 255; hi = hi.astype(np.float32) / 255
    wash(msk, (0.30, 0.52, 0.32), k=0.95, edge=0.5, var=0.5, rough=3); wash(hi * msk, (0.62, 0.78, 0.40), k=0.7, edge=0.1, var=0.5, rough=3)
    hatch(msk * (1 - hi), ang=-50, gap=6, p=0.35, w=1.2)
haie(5.45, np.arange(13.4, 18.0, 0.55)); haie(0.95, np.arange(15.4, 18.2, 0.55), r=0.28)
# ombres portees (soleil a droite)
ombre_lilas(polyR(SL([(cx - 3.0, 0, 15.6), (cx - 1.6, 0, 15.6), (cx - 1.6, 0, 18.0), (cx - 3.0, 0, 18.0)])) * slab_m, 0.30)
ombre_lilas(polyR(SL([(2.1, 0, 13.7), (2.8, 0, 13.7), (2.8, 0, 14.3), (2.1, 0, 14.3)])), 0.40)
# usagers : un skateur dans le plateau, un debout avec sa planche, un assis sur le banc rond
personne3d(2.45, 0, 13.55, (0.88, 0.40, 0.32), (0.28, 0.34, 0.52), pose="skate", planche="dessous", bras="ecarte")
personne3d(2.75, 0, 16.2, (0.30, 0.50, 0.72), (0.22, 0.24, 0.30), pose="debout", planche="cote", bras="hanche", cheveux=(0.10, 0.09, 0.09))
personne3d(3.35, hb, 13.25, (0.93, 0.76, 0.30), (0.40, 0.46, 0.64), pose="assis", bras="bas", sexe="f", cheveux=(0.25, 0.14, 0.10))

# ------------------------------------------------------------------ BANC EN BOIS ONDULE (image 4) : avant-plan gauche
Zf, Zb, X0b = 11.2, 12.6, -5.4
prof = [(0.00, 0.55), (0.30, 0.88), (0.65, 0.64), (1.05, 0.38), (1.55, 0.36), (2.05, 0.64), (2.45, 1.18), (2.85, 1.50), (3.22, 1.34), (3.38, 1.00), (3.18, 0.78)]
sp = spline(prof, 12); thk = 0.20
def edge(Z, dy=0.0): return [S(X0b + u, v + dy, Z) for u, v in sp]
upF, loF, upB = edge(Zf), edge(Zf, -thk), edge(Zb)
ombre_lilas(polyR(SL([(X0b - 1.1, 0, Zf + .3), (X0b + 3.2, 0, Zf + .3), (X0b + 3.2, 0, Zb + 1.0), (X0b - 1.1, 0, Zb + 1.0)])) * ground, 0.40)
Zi = Zf + 0.26; ui = [(u, v) for u, v in sp if 0.6 <= u <= 2.2]
base_front = SL([(X0b + u, max(0.0, v - thk), Zi) for u, v in ui]) + SL([(X0b + u, 0, Zi) for u, v in ui[::-1]])
wash(polyR(base_front), (0.50, 0.30, 0.20), k=0.9, edge=0.5, var=0.4, rough=2)
for u in np.linspace(0.7, 2.1, 11): stroke(SL([(X0b + u, 0.0, Zi), (X0b + u, float(np.interp(u, [p[0] for p in sp], [p[1] for p in sp])) - thk, Zi)]), p=0.38, w=1.3, wob=0.5, over=0)
poly_stroke(base_front, p=0.85, w=2.2, wob=0.7)
wash(polyR(upF + loF[::-1]), (0.60, 0.33, 0.20), k=0.95, edge=0.55, var=0.4, rough=1.5)
topm = polyR(upF + upB[::-1])
tx0, tx1 = min(p[0] for p in upF + upB), max(p[0] for p in upF + upB); gb = np.clip((xx - tx0) / (tx1 - tx0), 0, 1)
wash(topm, (0.88, 0.64, 0.42), k=0.80, edge=0.45, var=0.5, rough=2)
wash(topm * (1 - gb) ** 1.4, (0.62, 0.36, 0.22), k=0.65, edge=0.0, var=0.3, rough=3)                 # creux a l'ombre
wash(topm * gb ** 2.0, (0.99, 0.80, 0.52), k=0.45, edge=0.0, var=0.3, rough=3)                         # crete au soleil
for i in range(1, 5): stroke(edge(Zf, -thk * i / 5), p=0.55, w=1.5, wob=0.5, over=0)               # lames empilees
for fz in np.linspace(0.12, 0.88, 7): stroke(edge(Zf + (Zb - Zf) * fz), p=0.34, w=1.4, wob=0.6, over=0)  # lames du dessus
stroke(upF, p=1.0, w=2.8, wob=0.6); stroke(loF, p=0.95, w=2.4, wob=0.6); stroke(upB, p=0.75, w=2.0, wob=0.6)
for pa, pb in ((upF[0], upB[0]), (upF[-1], upB[-1]), (upF[0], loF[0]), (upF[-1], loF[-1])): stroke([pa, pb], p=0.85, w=2.1, wob=0.4, over=0)
personne3d(X0b + 1.35, 0.37, 11.85, (0.93, 0.50, 0.22), (0.30, 0.40, 0.62), pose="assis", bras="livre", livre=True, sexe="f", cheveux=(0.16, 0.10, 0.08))

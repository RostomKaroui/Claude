# ===== Ajouts : nouveaux bancs en bois ondule (le long des allees), lampadaires/poubelles redessines a droite,
#       skatepark detaille (rampe en croissant, plateforme, rampe d'acces, rail, banc rond, eclairages), usagers =====
def ombre_lilas(mask, k=0.5): wash(mask, (0.72, 0.66, 0.88), k=k, edge=0.2, var=0.4, rough=5, soft=3)
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
def band_mask(pts, th):
    m = np.zeros((H, W), np.uint8); cv2.polylines(m, [np.round(np.array(pts)).astype(np.int32)], False, 255, max(1, int(th)), cv2.LINE_AA); return m.astype(np.float32) / 255
def contour_strokes(mask, p=0.5, w=1.6, chunk=60):
    m8 = (mask > 0.5).astype(np.uint8) * 255
    cs, _ = cv2.findContours(m8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cs:
        pts = cv2.approxPolyDP(c, 1.4, True).reshape(-1, 2).astype(np.float32)
        if len(pts) < 4: continue
        n = len(pts); pts = np.roll(pts, -int(rng.integers(0, n)), axis=0); k = 0
        while k < n:
            L = int(rng.integers(chunk // 2, chunk)); seg = pts[k:k + L + 3]
            if len(seg) >= 2 and rng.uniform() > 0.12: stroke([tuple(q) for q in seg], p=p * rng.uniform(0.7, 1.0), w=w, wob=0.6, over=1.5)
            k += L

# ------------------------------------------------------------------ personnages (squelette 3D)
def limb(m, a, b, ra, rb):
    a, b = np.array(a, np.float32), np.array(b, np.float32); L = np.hypot(*(b - a)); n = max(2, int(L / max(1, min(ra, rb) * 0.6)))
    for t in np.linspace(0, 1, n): c = a + (b - a) * t; cv2.circle(m, (int(c[0]), int(c[1])), max(1, int(ra + (rb - ra) * t)), 255, -1)
def personne3d(X, Y, Z, chemise, pantalon, pose="debout", planche=None, cheveux=(0.20, 0.15, 0.12), peau=(0.90, 0.70, 0.56), bras="bas", sexe="h", taille=1.0, cote_planche=1):
    s = px_m(Z); T_ = taille
    def jp(dx, dy, dz=0.0): return (X + dx * T_, Y + dy * T_, Z + dz * T_)
    J = {}
    if pose == "assis":
        J.update(hL=jp(-.11, .06), hR=jp(.11, .06), kL=jp(-.13, .08, -.42), kR=jp(.12, .05, -.40), fL=(X - .15 * T_, Y - .42, Z - .48 * T_), fR=(X + .13 * T_, Y - .42, Z - .44 * T_),
                 sL=jp(-.19, .58), sR=jp(.19, .60), nk=jp(0, .66), hd=jp(0, .82))
    elif pose == "skate":
        J.update(hL=jp(-.12, .76), hR=jp(.10, .78), kL=jp(-.30, .42, -.06), kR=jp(.26, .44, -.02), fL=jp(-.22, .06), fR=jp(.22, .06),
                 sL=jp(-.12, 1.26, -.06), sR=jp(.30, 1.30, -.04), nk=jp(.09, 1.36, -.06), hd=jp(.12, 1.52, -.08))
    else:
        J.update(hL=jp(-.10, .90), hR=jp(.10, .93), kL=jp(-.13, .47, -.05), kR=jp(.10, .49), fL=jp(-.16, .02, -.08), fR=jp(.10, .02),
                 sL=jp(-.20, 1.44), sR=jp(.20, 1.41), nk=jp(0, 1.50), hd=jp(.01, 1.66))
    sL_, sR_ = J['sL'], J['sR']
    def rel(p, dx, dy, dz=0.0): return (p[0] + dx * T_, p[1] + dy * T_, p[2] + dz * T_)
    if bras == "bas": J.update(eL=rel(sL_, -.06, -.30), eR=rel(sR_, .05, -.30), wL=rel(sL_, -.04, -.58, -.05), wR=rel(sR_, .06, -.58))
    elif bras == "ecarte": J.update(eL=rel(sL_, -.30, -.02), eR=rel(sR_, .32, -.14), wL=rel(sL_, -.60, .10), wR=rel(sR_, .62, -.26))
    elif bras == "hanche": J.update(eL=rel(sL_, -.20, -.28), eR=rel(sR_, .05, -.30), wL=rel(J['hL'], -.02, .04), wR=rel(sR_, .07, -.58))
    elif bras == "marche": J.update(eL=rel(sL_, -.05, -.30, .10), eR=rel(sR_, .05, -.29, -.10), wL=rel(sL_, -.03, -.56, .18), wR=rel(sR_, .04, -.55, -.18))
    Q = {k: np.array(S(*v), np.float32) for k, v in J.items()}
    z8 = lambda: np.zeros((H, W), np.uint8)
    ombre_lilas(ellipse_r(S(X, min(Y, 0.0) if pose == "assis" else Y, Z), 0.42 * s * T_, 0.10 * s * T_), 0.45)
    if planche:
        if planche == "dessous": d0, d1 = S(X - .42 * T_, Y, Z), S(X + .42 * T_, Y, Z)
        else: d0, d1 = S(X + cote_planche * .50, Y, Z - .05), S(X + cote_planche * 1.18, Y, Z + .05)
        mb = z8(); limb(mb, d0, d1, 0.045 * s, 0.045 * s); mb = mb.astype(np.float32) / 255
        wash(mb, (0.95, 0.42, 0.30), k=0.95, edge=0.35, var=0.1, rough=0.8, soft=0.8)
        contour_strokes(mb, p=0.6, w=1.6)
        for t in (0.17, 0.83):
            c = np.array(d0) + (np.array(d1) - np.array(d0)) * t + [0, 0.05 * s]
            wash(ellipse_r(c, 0.038 * s, 0.038 * s), (0.25, 0.25, 0.30), k=0.95, edge=0.1, var=0.1, rough=0.4, soft=0.5)
    legs, shirt, skin, hair, shoes = z8(), z8(), z8(), z8(), z8()
    for a, b, c in (("hL", "kL", "fL"), ("hR", "kR", "fR")): limb(legs, Q[a], Q[b], 0.088 * s * T_, 0.062 * s * T_); limb(legs, Q[b], Q[c], 0.060 * s * T_, 0.040 * s * T_)
    wd = 0.5 * np.abs(Q['hR'][0] - Q['hL'][0]) + 0.05 * s * T_
    cv2.fillPoly(shirt, [np.round(np.array([Q['sL'] + [-0.02 * s, -0.02 * s], Q['sR'] + [0.02 * s, -0.02 * s], [Q['hR'][0] + wd * 0.3, Q['hR'][1] - 0.12 * s * T_], [Q['hL'][0] - wd * 0.3, Q['hL'][1] - 0.12 * s * T_]])).astype(np.int32)], 255)
    for a, b in (("sL", "eL"), ("sR", "eR")): limb(shirt, Q[a], Q[b], 0.058 * s * T_, 0.046 * s * T_)
    for a, b in (("eL", "wL"), ("eR", "wR")): limb(skin, Q[a], Q[b], 0.040 * s * T_, 0.030 * s * T_)
    for k in ("wL", "wR"): cv2.circle(skin, (int(Q[k][0]), int(Q[k][1])), int(0.035 * s * T_), 255, -1)
    cv2.line(skin, tuple(int(v) for v in Q['nk']), tuple(int(v) for v in (Q['hd'] + [0, 0.07 * s * T_])), 255, max(2, int(0.09 * s * T_)))
    cv2.ellipse(skin, tuple(int(v) for v in Q['hd']), (int(0.098 * s * T_), int(0.122 * s * T_)), 0, 0, 360, 255, -1)
    cv2.ellipse(hair, tuple(int(v) for v in (Q['hd'] + [0, -0.028 * s * T_])), (int(0.104 * s * T_), int(0.100 * s * T_)), 0, 180, 360, 255, -1)
    if sexe == "f":
        limb(hair, Q['hd'] + [-0.09 * s * T_, 0], Q['hd'] + [-0.10 * s * T_, 0.22 * s * T_], 0.035 * s * T_, 0.03 * s * T_); limb(hair, Q['hd'] + [0.09 * s * T_, 0], Q['hd'] + [0.10 * s * T_, 0.22 * s * T_], 0.035 * s * T_, 0.03 * s * T_)
    for k in ("fL", "fR"): cv2.ellipse(shoes, tuple(int(v) for v in Q[k] + [0, 0.012 * s]), (int(0.085 * s * T_), int(0.040 * s * T_)), 0, 0, 360, 255, -1)
    f = lambda m: m.astype(np.float32) / 255
    legs, shirt, skin, hair, shoes = f(legs), f(shirt), f(skin), f(hair), f(shoes)
    skin = skin * (1 - shirt) * (1 - hair)
    cxp = 0.5 * (Q['sL'][0] + Q['sR'][0])
    wash(legs, pantalon, k=0.92, edge=0.5, var=0.25, rough=0.9, soft=0.8)
    wash(shirt, chemise, k=0.92, edge=0.5, var=0.30, rough=1.0, soft=0.8)
    wash((shirt + legs) * (xx < cxp), (0.74, 0.68, 0.88), k=0.40, edge=0.0, var=0.2, rough=0.8, soft=1.5)
    wash(skin, peau, k=0.92, edge=0.35, var=0.15, rough=0.8, soft=0.8)
    wash(hair, cheveux, k=0.95, edge=0.2, var=0.1, rough=0.8, soft=0.7)
    wash(shoes, (0.95, 0.95, 0.93), k=0.8, edge=0.4, var=0.1, rough=0.6, soft=0.6)
    if s * T_ > 60:
        for mk in (legs, shirt, skin, hair): contour_strokes(mk, p=0.40, w=1.5, chunk=50)

# ------------------------------------------------------------------ BANC EN BOIS ONDULE, oriente le long de l'allee
PROF = [(0.00, 0.55), (0.30, 0.88), (0.65, 0.64), (1.05, 0.38), (1.55, 0.36), (2.05, 0.64), (2.45, 1.18), (2.85, 1.50), (3.22, 1.34), (3.38, 1.00), (3.18, 0.78)]
SPB = spline(PROF, 12); UMAX = 3.38
BENCH_OCC = np.zeros((H, W), np.float32)
def banc_ondule(Xc, Z0, L=3.0, side=-1, larg=1.0, thk=0.20):
    """side=-1 : banc a gauche de l'allee (on voit sa face cote allee, X+). side=+1 : banc a droite."""
    global BENCH_OCC
    Xin, Xout = Xc - side * larg / 2, Xc + side * larg / 2
    Zu = lambda u: Z0 + u * L / UMAX
    inT = [S(Xin, v, Zu(u)) for u, v in SPB]; inB = [S(Xin, v - thk, Zu(u)) for u, v in SPB]; outT = [S(Xout, v, Zu(u)) for u, v in SPB]
    k_ = px_m(Z0 + L / 2)
    # ombre portee (soleil a droite -> vers la gauche)
    ombre_lilas(polyR(SL([(Xc - 1.3, 0, Z0 - .1), (Xc + .3, 0, Z0 - .1), (Xc + .3, 0, Z0 + L + .3), (Xc - 1.3, 0, Z0 + L + .3)])), 0.45)
    # socle sous la partie basse
    Xi = Xin + side * 0.18; ui = [(u, v) for u, v in SPB if 0.6 <= u <= 2.2]
    base = SL([(Xi, max(0.0, v - thk), Zu(u)) for u, v in ui]) + SL([(Xi, 0, Zu(u)) for u, v in ui[::-1]])
    bm = polyR(base); wash(bm, (0.52, 0.32, 0.22), k=0.9, edge=0.5, var=0.4, rough=1.5, brush=80, dry=0.3)
    # face cote allee (bois stratifie) + dessus (assise)
    fm = polyR(inT + inB[::-1]); tm = polyR(inT + outT[::-1])
    wash(fm, (0.62, 0.34, 0.20), k=0.95, edge=0.55, var=0.4, rough=1.2, brush=0, dry=0.3)
    wash(tm, (0.90, 0.66, 0.42), k=0.85, edge=0.45, var=0.5, rough=1.5, brush=0, dry=0.45)
    ty0, ty1 = min(p[1] for p in inT + outT), max(p[1] for p in inT + outT)
    wash(tm * np.clip((yy - ty0) / (ty1 - ty0 + 1), 0, 1) ** 1.5, (0.66, 0.40, 0.26), k=0.45, edge=0.0, var=0.3, rough=2)
    lift(tm * (fleck > 2.2), 0.6)
    # extremite proche (bout du ruban)
    cap = [inT[0], outT[0], S(Xout, SPB[0][1] - thk, Zu(0)), inB[0]]
    wash(polyR(cap), (0.50, 0.28, 0.18), k=0.9, edge=0.4, var=0.2, rough=1)
    # crayon
    if k_ > 25:
        for i in range(1, 4): stroke([S(Xin, v - thk * i / 4, Zu(u)) for u, v in SPB], p=0.45, w=1.4, wob=0.4, over=0)
        for fx_ in np.linspace(0.2, 0.8, 4): stroke([S(Xin + (Xout - Xin) * fx_, v, Zu(u)) for u, v in SPB], p=0.30, w=1.3, wob=0.5, over=0)
        for u in np.linspace(0.75, 2.05, 7): stroke(SL([(Xi, 0.0, Zu(u)), (Xi, float(np.interp(u, SPB[:, 0], SPB[:, 1])) - thk, Zu(u))]), p=0.32, w=1.2, wob=0.4, over=0)
    stroke(inT, p=0.95, w=2.4, wob=0.5); stroke(inB, p=0.9, w=2.1, wob=0.5); stroke(outT, p=0.65, w=1.8, wob=0.5)
    poly_stroke(cap, p=0.8, w=1.8, wob=0.3); poly_stroke(base, p=0.75, w=1.8, wob=0.5)
    stroke([inT[-1], outT[-1]], p=0.8, w=1.8, wob=0.3, over=0)
    BENCH_OCC = np.maximum(BENCH_OCC, np.clip(fm + tm + bm + polyR(cap), 0, 1))

# ------------------------------------------------------------------ LAMPADAIRE (meme dessin que les tiens) et POUBELLE, en perspective
def lampadaire(X, Z, dirx=-1, Ht=4.0):
    k_ = px_m(Z); r = 0.07
    post = polyR(SL([(X - r, 0, Z), (X + r, 0, Z), (X + r, Ht, Z), (X - r, Ht, Z)]))
    socle = polyR(SL([(X - .16, 0, Z), (X + .16, 0, Z), (X + .12, .45, Z), (X - .12, .45, Z)]))
    arm = [S(X + dirx * dx, Ht + dy, Z) for dx, dy in ((0, -0.05), (0.05, 0.25), (0.25, 0.42), (0.55, 0.40), (0.80, 0.25), (0.88, 0.10))]
    curl = [S(X - dirx * (0.10 + 0.12 * np.cos(t)), Ht - 0.05 + 0.12 * np.sin(t), Z) for t in np.linspace(0, 2 * np.pi * 0.85, 14)]
    bc = np.array(S(X + dirx * 0.88, Ht - 0.12, Z))
    bowl = ellipse_r(bc, 0.24 * k_, 0.11 * k_) * (yy > bc[1] - 0.02 * k_)
    for m_ in (post, socle): wash(m_, (0.30, 0.42, 0.76), k=0.9, edge=0.4, var=0.2, rough=0.8, soft=0.8)
    wash(band_mask(arm, 0.07 * k_), (0.30, 0.42, 0.76), k=0.9, edge=0.3, var=0.2, rough=0.6, soft=0.7)
    wash(bowl, (0.99, 0.86, 0.42), k=0.95, edge=0.4, var=0.1, rough=0.6, soft=0.7)
    stroke(SL([(X - r, 0, Z), (X - r, Ht, Z)]), p=0.85, w=1.8, wob=0.3); stroke(SL([(X + r, 0, Z), (X + r, Ht, Z)]), p=0.75, w=1.6, wob=0.3)
    stroke(arm, p=0.85, w=1.8, wob=0.3); stroke(curl, p=0.7, w=1.5, wob=0.2, over=0); poly_stroke(SL([(X - .16, 0, Z), (X + .16, 0, Z), (X + .12, .45, Z), (X - .12, .45, Z)]), p=0.75, w=1.6, wob=0.3)
    contour_strokes(bowl, p=0.7, w=1.5, chunk=40)
    stroke([tuple(bc + [-0.24 * k_, 0]), tuple(bc + [0.24 * k_, 0])], p=0.7, w=1.5, wob=0.2, over=0)
def poubelle(X, Z, r=0.24, h=0.9):
    k_ = px_m(Z); c0, c1 = np.array(S(X, 0, Z)), np.array(S(X, h, Z))
    body = polyR([c1 + [-r * k_, 0], c1 + [r * k_, 0], c0 + [r * k_, 0], c0 + [-r * k_, 0]])
    wash(np.clip(body + ellipse_r(c0, r * k_, r * k_ * 0.3), 0, 1), (0.40, 0.56, 0.84), k=0.9, edge=0.45, var=0.3, rough=0.8, soft=0.8)
    wash(body * (xx < c0[0]), (0.70, 0.66, 0.90), k=0.45, edge=0.0, var=0.2, rough=0.6)
    wash(ellipse_r(c1, r * k_, r * k_ * 0.3), (0.30, 0.42, 0.70), k=0.8, edge=0.3, var=0.2, rough=0.6)
    stroke([tuple(c1 + [-r * k_, 0]), tuple(c0 + [-r * k_, 0])], p=0.8, w=1.6, wob=0.3); stroke([tuple(c1 + [r * k_, 0]), tuple(c0 + [r * k_, 0])], p=0.8, w=1.6, wob=0.3)
    stroke([tuple(c1 + [r * k_ * np.cos(t), r * k_ * 0.3 * np.sin(t)]) for t in np.linspace(0, 2 * np.pi, 20)], p=0.75, w=1.5, wob=0.2, over=0)
    stroke([tuple(c0 + [r * k_ * np.cos(t), r * k_ * 0.3 * np.sin(t)]) for t in np.linspace(0, np.pi, 12)], p=0.7, w=1.5, wob=0.2, over=0)
    ombre_lilas(ellipse_r(c0 + [-0.35 * k_, 0], 0.5 * k_, 0.12 * k_), 0.4)


# ================================================================== FONTAINES MODERNES
def jet(X, Yb, Z, Hj):
    """Jet d'eau : colonne fine et translucide qui retombe en gerbe (parabole) dans le bassin."""
    k_ = px_m(Z); b0, t0 = np.array(S(X, Yb, Z)), np.array(S(X, Yb + Hj, Z)); w = max(1.4, 0.035 * k_)
    col = band_mask([b0, t0], w * 3.0)
    wash(col, (0.70, 0.86, 0.96), k=0.45, edge=0.4, var=0.3, rough=0.8, soft=1.2)
    lift(band_mask([b0 + [w * 0.4, 0], t0 + [w * 0.4, 0]], w * 0.9), 0.75, soft=0.7)
    for sg in (-1, 1):
        for sp_ in (0.22, 0.34):
            arc = [S(X + sg * sp_ * t, Yb + Hj * (1 - t * t) + 0.12 * t * (1 - t), Z) for t in np.linspace(0, 1, 14)]
            wash(band_mask(arc, max(1.5, w * 1.6)), (0.70, 0.86, 0.96), k=0.38, edge=0.3, var=0.3, rough=0.6, soft=1.0)
            if k_ > 18: stroke(arc, p=0.30, w=1.1, wob=0.3, over=0)
    wash(ellipse_r(b0, 0.36 * k_, 0.08 * k_), (0.75, 0.90, 0.97), k=0.45, edge=0.3, var=0.3, rough=1, soft=1.2)
    if k_ > 18:
        stroke([tuple(b0 + [-w * 0.6, 0]), tuple(t0 + [-w * 0.4, 0])], p=0.32, w=1.1, wob=0.3, over=0)
        stroke([tuple(b0 + [0.36 * k_ * np.cos(a), 0.08 * k_ * np.sin(a)]) for a in np.linspace(0.15, np.pi - 0.15, 12)], p=0.32, w=1.1, wob=0.3, over=0)

def fontaine_carree(F, FM, n=3, h_jet=(1.0, 1.9)):
    """Bassin carre moderne : margelle en pierre claire (assise), eau turquoise, grille de jets, bandeau lumineux."""
    cx_, cz_, a_, c, h = F['cx'], F['cz'], F['a'], F['c'], F['h']
    X0, X1, Z0, Z1 = cx_ - a_, cx_ + a_, cz_ - a_, cz_ + a_
    k_ = px_m(cz_)
    ombre_lilas(polyR(SL([(X0 - 0.7, 0, Z0 + .1), (X0, 0, Z0 + .1), (X0, 0, Z1 + .2), (X0 - 0.7, 0, Z1 + .2)])), 0.5)
    front = SL([(X0, 0, Z0), (X1, 0, Z0), (X1, h, Z0), (X0, h, Z0)])
    side = SL([(X0, 0, Z0), (X0, 0, Z1), (X0, h, Z1), (X0, h, Z0)]) if S(X0, 0, Z0)[0] > S(cx_, 0, cz_)[0] - 1e9 and X0 > 0 else SL([(X1, 0, Z0), (X1, 0, Z1), (X1, h, Z1), (X1, h, Z0)])
    otop = SL([(X0, h, Z0), (X1, h, Z0), (X1, h, Z1), (X0, h, Z1)]); itop = SL([(X0 + c, h, Z0 + c), (X1 - c, h, Z0 + c), (X1 - c, h, Z1 - c), (X0 + c, h, Z1 - c)])
    wat = SL([(X0 + c, h - .08, Z0 + c), (X1 - c, h - .08, Z0 + c), (X1 - c, h - .08, Z1 - c), (X0 + c, h - .08, Z1 - c)])
    # face laterale visible (celle tournee vers l'axe de la vue)
    sm = polyR(side) * (1 - polyR(front))
    wash(sm, (0.68, 0.66, 0.86), k=0.75, edge=0.5, var=0.3, rough=1.2)
    wash(polyR(front), (0.80, 0.80, 0.92), k=0.80, edge=0.5, var=0.3, rough=1.2, brush=0, dry=0.15)
    wash(polyR(otop) * (1 - polyR(itop)), (0.96, 0.95, 0.93), k=0.50, edge=0.4, var=0.3, rough=1.2)
    wm = polyR(wat); wash(wm, (0.42, 0.80, 0.84), k=0.88, edge=0.5, var=0.35, rough=1.5, brush=0, bstr=0.3, dry=0.15)
    yb, yt = max(q[1] for q in wat), min(q[1] for q in wat)
    wash(wm * np.clip((yb - yy) / (yb - yt + 1), 0, 1) ** 1.3, (0.28, 0.58, 0.72), k=0.55, edge=0.0, var=0.3, rough=1.5)
    lift(wm * (STK[0] > 1.7) * (lo2 > -0.2), 0.7, soft=1.0)
    led = SL([(X0 + .05, h * 0.55, Z0 - .002), (X1 - .05, h * 0.55, Z0 - .002)])
    wash(band_mask(led, max(2, 0.05 * k_)), (0.99, 0.86, 0.45), k=0.9, edge=0.0, var=0.1, rough=0.5, soft=1.2)
    poly_stroke(front, p=0.9, w=2.1, wob=0.5); poly_stroke(otop, p=0.85, w=2.0, wob=0.5); poly_stroke(itop, p=0.75, w=1.7, wob=0.5)
    stroke(side[:2], p=0.8, w=1.8, wob=0.3, over=0); stroke(side[1:3], p=0.8, w=1.8, wob=0.3, over=0)
    if k_ > 25:   # joints de la margelle
        for t in np.linspace(0, 1, 6)[1:-1]:
            xs_ = X0 + (X1 - X0) * t; stroke(SL([(xs_, h, Z0), (xs_, h, Z0 + c)]), p=0.35, w=1.2, wob=0.2, over=0)
    xs = np.linspace(X0 + c + 0.45, X1 - c - 0.45, n); zs = np.linspace(Z0 + c + 0.45, Z1 - c - 0.45, n)
    jets = [(X, Z, h_jet[1] if (i == n // 2 and j == n // 2) else h_jet[0]) for i, X in enumerate(xs) for j, Z in enumerate(zs)]
    for X, Z, Hj in sorted(jets, key=lambda t: -t[1]): jet(X, h - 0.08, Z, Hj)

# ================================================================== VEGETATION : massifs fleuris en bordure + buissons sous les arbres
VEG_OCC = np.zeros((H, W), np.float32)
FLEURS = [(0.95, 0.42, 0.68), (0.74, 0.62, 0.95), (0.99, 0.86, 0.30), (0.99, 0.58, 0.42), (0.98, 0.98, 0.96)]
def massif(plantes, base_col=(0.60, 0.80, 0.46), dark_col=(0.22, 0.52, 0.44), fleur_p=0.55):
    """plantes = liste (X, Z, r). Peint en couches (comme a l'aquarelle) puis contours au crayon."""
    global VEG_OCC
    mA, mB, hi, sh, fl = [np.zeros((H, W), np.uint8) for _ in range(5)]
    flc = {i: np.zeros((H, W), np.uint8) for i in range(len(FLEURS))}
    arcs = []
    for i, (X, Z, r) in enumerate(sorted(plantes, key=lambda t: -t[1])):
        k_ = px_m(Z); c = np.array(S(X, r * 0.85, Z)); rr = r * k_
        if rr < 1.5: continue
        cv2.circle(mA if i % 2 else mB, (int(c[0]), int(c[1])), int(rr), 255, -1)
        cv2.circle(hi, (int(c[0] + rr * .30), int(c[1] - rr * .30)), int(rr * .55), 255, -1)
        cv2.ellipse(sh, (int(c[0] - rr * .25), int(c[1] + rr * .30)), (int(rr * .75), int(rr * .55)), 0, 0, 360, 255, -1)
        if rng.uniform() < fleur_p:
            fc = int(rng.integers(0, len(FLEURS)))
            for _ in range(int(6 + rr / 3)):
                a, d = rng.uniform(0, 2 * np.pi), rng.uniform(0, 0.85) * rr
                cv2.circle(flc[fc], (int(c[0] + d * np.cos(a)), int(c[1] - abs(d * np.sin(a)) * 0.8)), max(2, int(rr * rng.uniform(0.10, 0.17))), 255, -1)
        if rr > 7: arcs.append((c, rr))
    f = lambda m: m.astype(np.float32) / 255
    allm = np.clip(f(mA) + f(mB), 0, 1)
    wash(f(mA), base_col, k=0.85, edge=0.5, var=0.45, rough=2.5, brush=35, dry=0.2)
    wash(f(mB), tuple(np.clip(np.array(base_col) * 0.85 + 0.08, 0, 1)), k=0.85, edge=0.5, var=0.45, rough=2.5, brush=-35, dry=0.2)
    wash(f(hi) * allm, (0.86, 0.92, 0.48), k=0.55, edge=0.2, var=0.4, rough=2)
    wash(f(sh) * allm, dark_col, k=0.55, edge=0.4, var=0.4, rough=2, dry=0.2)
    for i, m_ in flc.items():
        if i == 4: lift(f(m_) * allm, 0.9, soft=0.6)
        else: lift(f(m_) * allm, 0.7, soft=0.6); wash(f(m_) * allm, FLEURS[i], k=0.95, edge=0.35, var=0.3, rough=0.8, soft=0.7)
    for c, rr in arcs:
        a0 = rng.uniform(0, 1.0)
        stroke([(c[0] + rr * np.cos(a), c[1] + rr * np.sin(a)) for a in np.linspace(np.pi * (0.9 + a0 * 0.2), np.pi * (2.15 + a0 * 0.2), 14)], p=0.55, w=1.6, wob=0.9, over=0)
    hatch(allm * f(sh), ang=-55, gap=6, p=0.28, w=1.1)
    VEG_OCC = np.maximum(VEG_OCC, allm)
def libre(Z, zones, marge):
    return all(not (a - marge <= Z <= b + marge) for a, b in zones)
# bordures plantees le long de l'allee (avec des trouees pour les bancs, lampadaires et poubelles)
bancsG = [(15.6, 18.6), (28.0, 31.0), (42.0, 45.0), (70.0, 73.0)]
objD = [(22.5, 25.5), (32.5, 35.5), (21.0, 21.0), (30.8, 30.8), (26.6, 26.6), (36.6, 36.6)]
bord = []
Z = 12.2
while Z < 125:
    st = max(0.42, Z * 0.028)
    if libre(Z, bancsG, 0.7):
        for dx in (-0.17, 0.17): bord.append((-5.45 + dx + rng.uniform(-.05, .05), Z + (st / 2 if dx > 0 else 0), rng.uniform(0.30, 0.42)))
    if Z > 20.0 and libre(Z, objD, 0.65):
        for dx in (-0.17, 0.17): bord.append((5.05 + dx + rng.uniform(-.05, .05), Z + (st / 2 if dx > 0 else 0), rng.uniform(0.30, 0.42)))
    Z += st
# buissons fleuris sous les arbres (bougainvilliers, lauriers-roses...), plus etendus
evit = [(14.2, 15.6), (22.4, 26.0), (37.6, 39.2), (60.0, 66.0)]                 # lampadaires, poubelles et pergola existants
sousG, sousD = [], []
Z = 13.5
while Z < 115:
    st = max(0.8, Z * 0.05)
    if libre(Z, evit, 0.3): sousG.append((rng.uniform(-10.5, -7.6), Z, rng.uniform(0.45, 0.75)))
    sousG.append((rng.uniform(-13.0, -10.8), Z + st / 2, rng.uniform(0.5, 0.8)))
    if Z > 19.6:
        sousD.append((rng.uniform(7.0, 9.4), Z, rng.uniform(0.45, 0.75))); sousD.append((rng.uniform(9.6, 12.5), Z + st / 2, rng.uniform(0.5, 0.8)))
    Z += st

# --- on peint : fontaine du fond, vegetation, puis le mobilier par-dessus
fontaine_carree(FF, FONT_FAR, n=3, h_jet=(1.1, 2.3))
massif(sousG + sousD, base_col=(0.56, 0.78, 0.46), dark_col=(0.20, 0.50, 0.44), fleur_p=0.8)
massif(bord, fleur_p=0.85)

# ================================================================== MOBILIER LE LONG DES ALLEES
# (du plus loin au plus proche pour que les objets proches recouvrent les lointains)
banc_ondule(-6.6, 70.0, side=-1); banc_ondule(-6.4, 42.0, side=-1)
poubelle(5.6, 36.6); banc_ondule(5.9, 32.5, side=+1); lampadaire(5.8, 30.8, dirx=-1)
banc_ondule(-6.6, 28.0, side=-1)
poubelle(5.7, 26.6); banc_ondule(6.1, 22.5, side=+1); lampadaire(5.95, 21.0, dirx=-1)
banc_ondule(-6.4, 15.6, side=-1)
# promeneurs
for (X, Z, ch, pa, sx_, t_) in ((-2.9, 58, (0.85, 0.50, 0.40), (0.35, 0.40, 0.60), "h", 1.0), (2.9, 64, (0.35, 0.50, 0.75), (0.30, 0.30, 0.38), "f", 1.0),
                                (-2.6, 76, (0.95, 0.78, 0.35), (0.35, 0.40, 0.60), "h", 1.0), (3.0, 86, (0.45, 0.65, 0.55), (0.30, 0.32, 0.45), "f", 1.0),
                                (-2.75, 25.8, (0.88, 0.56, 0.46), (0.32, 0.38, 0.58), "h", 1.0), (-1.84, 25.6, (0.34, 0.50, 0.74), (0.26, 0.28, 0.36), "f", 0.96),
                                (2.91, 23.6, (0.46, 0.66, 0.56), (0.30, 0.36, 0.55), "h", 1.0), (3.6, 23.4, (0.96, 0.76, 0.32), (0.36, 0.44, 0.66), "h", 0.62)):
    personne3d(X, 0, Z, ch, pa, pose="debout", bras="marche", sexe=sx_, taille=t_)

fontaine_carree(FN, FONT_NEAR, n=3, h_jet=(1.0, 1.9))

# ================================================================== SKATEPARK (inspire de l'image 2), au premier plan a droite
cx, cz = SK_C; th = TH_SK; r_in, r_out, hl, dk = SK_RIN, SK_ROUT, SK_H, SK_DECK
xx_ = xx
# plateau beton
slabS = SL([(X, 0, Z) for X, Z in SLAB_W])
wash(slab_m, (0.78, 0.81, 0.92), k=0.85, edge=0.5, var=0.4, rough=3, brush=0, bstr=0.3, dry=0.3)
wash(slab_m * np.clip(noise(26) - 0.1, 0, 1), (0.72, 0.74, 0.88), k=0.35, edge=0.1, var=0.3, rough=3)
poly_stroke(slabS, p=0.9, w=2.4, wob=0.7)
for X in np.arange(1.6, 7.8, 1.0): stroke(SL([(X, 0, 11.3), (X, 0, 18.5)]), p=0.22, w=1.3, wob=0.6, over=0, mask=slab_m)
for Z in np.arange(12.2, 18.5, 1.0): stroke(SL([(0.2, 0, Z), (7.8, 0, Z)]), p=0.22, w=1.3, wob=0.6, over=0, mask=slab_m)
# rampe en croissant
prof_y = lambda s_: hl * s_ ** 2.0
bot, top, deckO = SK_BOT, SK_TOP, SK_DO
bx0, bx1 = min(p[0] for p in bot + top), max(p[0] for p in bot + top)
g = np.clip((xx_ - bx0) / (bx1 - bx0 + 1e-6), 0, 1)
wash(ramp_m, (0.97, 0.93, 0.88), k=0.50, edge=0.45, var=0.35, rough=2, brush=80, bstr=0.25, dry=0.3)
wash(ramp_m * (1 - g) ** 0.9, (0.58, 0.58, 0.80), k=0.90, edge=0.2, var=0.35, rough=2, brush=80, dry=0.3)
wash(deck_m, (0.86, 0.88, 0.95), k=0.60, edge=0.45, var=0.3, rough=1.5, dry=0.3)
# murs d'extremite de la rampe
for wall, t_end in zip(SK_WALLS, (th[0], th[-1])):
    wash(polyR(wall), (0.70, 0.70, 0.86) if t_end > np.pi / 2 else (0.86, 0.86, 0.94), k=0.75, edge=0.5, var=0.3, rough=1.2)
    poly_stroke(wall, p=0.85, w=2.0, wob=0.4)
# arete (coping) metallique et eclairage chaud sous l'arete
wash(band_mask(top, 0.09 * px_m(cz + r_out)), (0.80, 0.80, 0.84), k=0.8, edge=0.3, var=0.1, rough=0.8, soft=0.9)
wash(band_mask(SL([(cx + (r_out - 0.06) * np.cos(t), hl - 0.12, cz + (r_out - 0.06) * np.sin(t)) for t in th]), 0.10 * px_m(cz + r_out)), (0.99, 0.86, 0.45), k=0.85, edge=0.0, var=0.2, rough=1, soft=2)
stroke(bot, p=0.95, w=2.6, wob=0.6); stroke(top, p=1.0, w=2.8, wob=0.6); stroke(deckO, p=0.85, w=2.2, wob=0.6)
stroke(SL([(cx + r_out * np.cos(t), hl - 0.07, cz + r_out * np.sin(t)) for t in th]), p=0.6, w=1.6, wob=0.5)
for t in np.deg2rad(np.linspace(30, 150, 19)):
    stroke(SL([(cx + (r_in + (r_out - r_in) * s_) * np.cos(t), prof_y(s_), cz + (r_in + (r_out - r_in) * s_) * np.sin(t)) for s_ in np.linspace(0, 1, 9)]), p=0.32, w=1.3, wob=0.4, over=0)
hatch(ramp_m * (1 - g) ** 1.3, ang=74, gap=5, p=0.40, w=1.2)
hatch(ramp_m * (1 - g) ** 2.4, ang=-18, gap=7, p=0.28, w=1.1)
# rail de glisse (bleu), parallele a l'image, avec son ombre
rX0, rX1, rZ, rH = 1.45, 3.0, 12.7, 0.38
ombre_lilas(polyR(SL([(rX0 - .5, 0, rZ - .05), (rX1 - .5, 0, rZ - .05), (rX1 - .5, 0, rZ + .12), (rX0 - .5, 0, rZ + .12)])), 0.55)
barre = SL([(rX0, rH, rZ), (rX1, rH, rZ)])
wash(band_mask(barre, 0.06 * px_m(rZ)), (0.30, 0.42, 0.76), k=0.9, edge=0.2, var=0.1, rough=0.5, soft=0.7)
stroke(barre, p=0.95, w=2.2, wob=0.2); stroke(SL([(rX0, rH - .05, rZ), (rX1, rH - .05, rZ)]), p=0.5, w=1.4, wob=0.2, over=0)
for x_ in (rX0 + 0.15, rX1 - 0.15):
    pm = band_mask(SL([(x_, 0, rZ), (x_, rH, rZ)]), 0.05 * px_m(rZ)); wash(pm, (0.30, 0.42, 0.76), k=0.9, edge=0.2, var=0.1, rough=0.4, soft=0.6)
    stroke(SL([(x_, 0, rZ), (x_, rH, rZ)]), p=0.9, w=2.0, wob=0.2, over=0)
# banc rond (assise, convivialite)
ro, ri, hb = 0.82, 0.55, 0.44; bxc, bzc = 4.05, 12.2
ob, ot, it = circ_pts(bxc, bzc, ro, 0), circ_pts(bxc, bzc, ro, hb), circ_pts(bxc, bzc, ri, hb)
hullb = cv2.convexHull(np.round(np.array(ot + ob)).astype(np.int32)); wallb = np.zeros((H, W), np.uint8); cv2.fillConvexPoly(wallb, hullb, 255); wallb = wallb.astype(np.float32) / 255
ombre_lilas(ellipse_r(np.array(S(bxc - 0.5, 0, bzc)), 1.0 * px_m(bzc), 0.35 * px_m(bzc)), 0.45)
wash(wallb, (0.76, 0.76, 0.90), k=0.95, edge=0.5, var=0.3, rough=1.5)
wash(wallb * (xx_ < S(bxc, 0, bzc)[0]), (0.62, 0.60, 0.82), k=0.5, edge=0.0, var=0.3, rough=1.5)
wash(polyR(ot) * (1 - polyR(it)), (0.97, 0.94, 0.90), k=0.45, edge=0.3, var=0.3, rough=1.2)
wash(polyR(it), (0.62, 0.80, 0.50), k=0.70, edge=0.3, var=0.4, rough=1.5)          # coeur plante
for pts_, pp in ((ot, 0.9), (it, 0.75)): poly_stroke(pts_, p=pp, w=2.0, wob=0.4)
stroke(ob[: len(ob) // 2 + 1], p=0.85, w=2.0, wob=0.4)
stroke([ot[0], ob[0]], p=0.85, w=1.8, wob=0.3, over=0); stroke([ot[len(ot) // 2], ob[len(ob) // 2]], p=0.85, w=1.8, wob=0.3, over=0)
# usagers du skatepark
personne3d(3.32, hl, 17.44, (0.30, 0.50, 0.74), (0.22, 0.24, 0.30), pose="debout", planche="cote", cote_planche=-1, bras="hanche", cheveux=(0.10, 0.09, 0.09))
personne3d(2.45, 0.30, 16.36, (0.95, 0.46, 0.34), (0.28, 0.34, 0.52), pose="skate", planche="dessous", bras="ecarte")
personne3d(2.2, rH + 0.04, rZ, (0.98, 0.80, 0.30), (0.30, 0.36, 0.56), pose="skate", planche="dessous", bras="ecarte", cheveux=(0.30, 0.18, 0.10))

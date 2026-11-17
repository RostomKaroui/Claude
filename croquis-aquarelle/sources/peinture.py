# ===== Peinture : base (mise en cache) + ajouts =====
CACHE = os.path.join(os.environ.get("AQ_CACHE", HERE), "_base.npz")
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
if os.environ.get("QUICK") and os.path.exists(CACHE):
    z = np.load(CACHE); canvas = z["canvas"]; dark = z["dark"]; ombre_f = z["ombre_f"]
else:
    exec(open(os.path.join(HERE, "base.py")).read())
    np.savez(CACHE, canvas=canvas, dark=dark, ombre_f=ombre_f)
exec(open(os.path.join(HERE, "nouveaux.py")).read())
exec(open(os.path.join(HERE, "details.py")).read())
exec(open(os.path.join(HERE, "finition.py")).read())

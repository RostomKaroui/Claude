import cv2, numpy as np, json
src="/tmp/claude-0/-home-user-Claude/0095011d-962b-595a-b8c6-2625d1aef2e9/images/"
CAS = {
 "angle1": dict(ac=26, net=29, fen=[(445,520),(1115,545),(1090,1530),(437,1545)],
                ext=[(355,465),(1205,480),(1160,1600),(355,1635)],
                main=[(0,170),(830,120),(860,560),(330,560),(0,840)]),
 "angle2": dict(ac=27, net=28, fen=[(367,347),(1202,320),(1206,1514),(452,1540)],
                ext=[(255,245),(1302,222),(1300,1598),(358,1638)],
                main=[(90,0),(840,0),(840,345),(260,310),(90,300)]),
}
# grille de la photo 27 : 4 x 6 carreaux de 4 cm
grille27 = np.float32([(401,392),(1180,368),(1185,1474),(467,1499)])
cm = np.float32([(0,0),(16,0),(16,24),(0,24)])
Hg = cv2.getPerspectiveTransform(grille27, cm)
fen_cm = cv2.perspectiveTransform(np.float32([CAS["angle2"]["fen"]]), Hg)[0]
print("fenêtre en cm (repère grille):", fen_cm.round(2).tolist())
sift = cv2.SIFT_create(8000)
res = {}
for nom, c in CAS.items():
    A = cv2.imread(src+f"{c['ac']}.jpg"); B = cv2.imread(src+f"{c['net']}.jpg")
    m = np.full(A.shape[:2], 255, np.uint8)
    cv2.fillPoly(m, [np.int32(c["ext"])], 0); cv2.fillPoly(m, [np.int32(c["fen"])], 255); cv2.fillPoly(m, [np.int32(c["main"])], 0)
    ka, da = sift.detectAndCompute(cv2.cvtColor(A, cv2.COLOR_BGR2GRAY), m)
    kb, db = sift.detectAndCompute(cv2.cvtColor(B, cv2.COLOR_BGR2GRAY), None)
    mt = cv2.BFMatcher().knnMatch(da, db, k=2)
    bons = [a for a, b in mt if a.distance < 0.72 * b.distance]
    pa = np.float32([ka[x.queryIdx].pt for x in bons]); pb = np.float32([kb[x.trainIdx].pt for x in bons])
    H, inl = cv2.findHomography(pa, pb, cv2.RANSAC, 4.0)
    print(nom, "appariements", len(bons), "retenus", int(inl.sum()))
    fen_net = cv2.perspectiveTransform(np.float32([c["fen"]]), H)[0]
    res[nom] = dict(H=H.tolist(), fen_net=fen_net.tolist(), net=c["net"])
    v = B.copy(); cv2.polylines(v, [np.int32(fen_net)], True, (0,0,255), 5)
    cv2.imwrite(f"cadre_{nom}.jpg", cv2.resize(v, (750,1000)))
res["fen_cm"] = fen_cm.tolist()
json.dump(res, open("cale.json","w"))

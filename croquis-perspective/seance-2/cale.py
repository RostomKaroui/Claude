import cv2, numpy as np, json
src="/tmp/claude-0/-home-user-Claude/0095011d-962b-595a-b8c6-2625d1aef2e9/images/"
fen = [(255,210),(1280,145),(1328,1740),(312,1745)]
ext = [(90,45),(1450,0),(1500,1920),(160,1920)]
main = [(0,600),(290,700),(300,1260),(0,1300)]
A = cv2.imread(src+"30.jpg"); B = cv2.imread(src+"31.jpg")
m = np.full(A.shape[:2], 255, np.uint8)
cv2.fillPoly(m, [np.int32(ext)], 0); cv2.fillPoly(m, [np.int32(fen)], 255); cv2.fillPoly(m, [np.int32(main)], 0)
sift = cv2.SIFT_create(10000)
ka, da = sift.detectAndCompute(cv2.cvtColor(A, cv2.COLOR_BGR2GRAY), m)
kb, db = sift.detectAndCompute(cv2.cvtColor(B, cv2.COLOR_BGR2GRAY), None)
bons = [a for a, b in cv2.BFMatcher().knnMatch(da, db, k=2) if a.distance < 0.72*b.distance]
pa = np.float32([ka[x.queryIdx].pt for x in bons]); pb = np.float32([kb[x.trainIdx].pt for x in bons])
H, inl = cv2.findHomography(pa, pb, cv2.RANSAC, 4.0)
print("appariements", len(bons), "retenus", int(inl.sum()))
fn = cv2.perspectiveTransform(np.float32([fen]), H)[0]
S=40; X0,Y0,W,Hc=-0.5,-1.0,17.0,26.0
fen_cm = np.float32([(-0.5,-1.0),(16.5,-1.0),(16.5,25.0),(-0.5,25.0)])
dst = (fen_cm-[X0,Y0])*S
M = cv2.getPerspectiveTransform(np.float32(fn), np.float32(dst))
out = cv2.warpPerspective(B, M, (int(W*S), int(Hc*S)), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
cv2.imwrite("redresse.png", out)
v=B.copy(); cv2.polylines(v,[np.int32(fn)],True,(0,0,255),6); cv2.imwrite("cadre.jpg", cv2.resize(v,(750,1000)))

import cv2, numpy as np, json
src="/tmp/claude-0/-home-user-Claude/0095011d-962b-595a-b8c6-2625d1aef2e9/images/"
R = json.load(open("cale.json"))
S = 40                       # px par cm
X0, Y0, W, Hc = -0.5, -1.0, 17.0, 26.0   # fenêtre de l'acétate en cm (repère de la grille 4 cm)
dst_cm = np.float32(R["fen_cm"])
dst = (dst_cm - [X0, Y0]) * S
for nom in ("angle1", "angle2"):
    B = cv2.imread(src + f"{R[nom]['net']}.jpg")
    M = cv2.getPerspectiveTransform(np.float32(R[nom]["fen_net"]), np.float32(dst))
    out = cv2.warpPerspective(B, M, (int(W*S), int(Hc*S)), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    v = out.copy()
    for i in range(5):
        x = int((0 + 4*i - X0) * S); cv2.line(v, (x,0), (x,v.shape[0]), (0,0,0), 1)
    for j in range(7):
        y = int((0 + 4*j - Y0) * S); cv2.line(v, (0,y), (v.shape[1],y), (0,0,0), 1)
    cv2.imwrite(f"redresse_{nom}.png", out); cv2.imwrite(f"redresse_{nom}_grille.jpg", v)
    json.dump(M.tolist(), open(f"M_{nom}.json","w"))
a=cv2.imread("redresse_angle1_grille.jpg"); b=cv2.imread("redresse_angle2_grille.jpg")
cv2.imwrite("redresses.jpg", np.hstack([a, np.full((a.shape[0],20,3),255,np.uint8), b]))

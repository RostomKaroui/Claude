"""zoom quadrillé sur la photo redressée 2x ; coordonnées en px du cadre (720 x 960)"""
import cv2, sys
nom = sys.argv[1]; x0, y0, x1, y1 = map(int, sys.argv[2:6]); f = float(sys.argv[6]); out = sys.argv[7]
st = int(sys.argv[8]) if len(sys.argv) > 8 else 10
im = cv2.imread(f"redresse2_{nom}.jpg")[2*y0:2*y1, 2*x0:2*x1]
im = cv2.resize(im, None, fx=f/2, fy=f/2, interpolation=cv2.INTER_AREA if f < 2 else cv2.INTER_CUBIC)
for x in range(x0 - x0 % st + st, x1, st):
    X = int((x-x0)*f); c = (0,0,255) if x % 50 == 0 else (0,200,0)
    cv2.line(im, (X,0), (X,im.shape[0]), c, 1)
    if x % 50 == 0: cv2.putText(im, str(x), (X+2, 12), 0, .4, (255,0,255), 1)
for y in range(y0 - y0 % st + st, y1, st):
    Y = int((y-y0)*f); c = (0,0,255) if y % 50 == 0 else (0,200,0)
    cv2.line(im, (0,Y), (im.shape[1],Y), c, 1)
    if y % 50 == 0: cv2.putText(im, str(y), (2, Y-2), 0, .4, (255,0,255), 1)
cv2.imwrite(out, im)

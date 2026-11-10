import cv2, sys
nom = sys.argv[1]; x0, y0, x1, y1 = map(int, sys.argv[2:6]); f = float(sys.argv[6]); out = sys.argv[7]
im = cv2.imread(f"redresse_{nom}.png")[y0:y1, x0:x1]
im = cv2.resize(im, None, fx=f, fy=f, interpolation=cv2.INTER_AREA if f < 1 else cv2.INTER_CUBIC)
st = 20 if f >= 1 else 40
for x in range(x0 - x0 % st + st, x1, st):
    X = int((x-x0)*f); cv2.line(im, (X,0), (X,im.shape[0]), (0,0,255) if x%100==0 else (0,200,0), 1)
    if x % (2*st) == 0: cv2.putText(im, str(x), (X+2, 12), 0, .4, (255,0,255), 1)
for y in range(y0 - y0 % st + st, y1, st):
    Y = int((y-y0)*f); cv2.line(im, (0,Y), (im.shape[1],Y), (0,0,255) if y%100==0 else (0,200,0), 1)
    if y % (2*st) == 0: cv2.putText(im, str(y), (2, Y-2), 0, .4, (255,0,255), 1)
cv2.imwrite(out, im)

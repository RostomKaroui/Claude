"""Pose la construction (A, B, A', B', C, D, horizontales, fuyantes) par-dessus croquis-filtre-2.png, sans toucher à l'image.

Relevé sur la photo (35.jpg, 1500 x 2000 px) :
  - AB  : l'arête droite de la porte jaune (la plus loin), A en haut, B en bas ;
  - A'B': l'arête gauche de la porte jaune, plus proche et plus longue ;
  - les horizontales depuis A et B donnent A' et B' ; C et D sont le vrai haut et le vrai bas sur A'B' ;
  - les fuyantes CA et DB vont vers le point de fuite (1231, 1345), qui n'est pas dessiné : elles s'arrêtent avant.
Sortie : croquis-filtre-2-construction.html (puis rendu2.js -> PNG et PDF A4).
"""
import numpy as np

PF = np.array([1231.0, 1345.0])                     # intersection des arêtes haute et basse de la porte (non dessiné)
C, D = np.array([387.0, 764.0]), np.array([354.0, 1606.0])     # haut et bas de l'arête gauche (A'B')
A, B = np.array([592.0, 900.0]), np.array([571.0, 1543.0])     # haut et bas de l'arête droite (AB)
fx = lambda p, q, y: p[0] + (q[0] - p[0]) * (y - p[1]) / (q[1] - p[1])   # x sur la droite pq à la hauteur y
A2 = np.array([fx(C, D, A[1]), A[1]])                           # A' : horizontale depuis A sur A'B'
B2 = np.array([fx(C, D, B[1]), B[1]])                           # B'
X_FIN = 960                                                     # les fuyantes s'arrêtent au bout du mur, avant PF

COUL = "#3f6596"


def sur_fuyante(p, x):
    return p + (PF - p) * (x - p[0]) / (PF[0] - p[0])


def ligne(p, q, ep=2.6, op=0.85, tirets=None):
    da = f' stroke-dasharray="{tirets}"' if tirets else ""
    return (f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{COUL}" stroke-width="{ep}" '
            f'stroke-opacity="{op}" stroke-linecap="round"{da}/>')


def point(p):
    return f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="5.5" fill="{COUL}"/>'


def lettre(p, t, dx, dy):
    return (f'<text x="{p[0] + dx:.1f}" y="{p[1] + dy:.1f}" font-family="\'Architects Daughter\', cursive" font-size="46" '
            f'fill="{COUL}" stroke="#fff" stroke-width="7" paint-order="stroke" stroke-linejoin="round">{t}</text>')


def svg():
    s = []
    s.append(ligne(sur_fuyante(C, C[0] - 40), sur_fuyante(C, X_FIN)))           # fuyante C -> A -> (PF)
    s.append(ligne(sur_fuyante(D, D[0] - 40), sur_fuyante(D, X_FIN)))           # fuyante D -> B -> (PF)
    s.append(ligne(C + (C - D) * 0.04, D + (D - C) * 0.03, 3.2, 0.95))           # A'B' (arête gauche)
    s.append(ligne(A + (A - B) * 0.05, B + (B - A) * 0.05, 3.2, 0.95))           # AB (arête droite)
    s.append(ligne(A, A2, 2.4, 0.9, "14 10"))                                    # horizontales
    s.append(ligne(B, B2, 2.4, 0.9, "14 10"))
    for p in (A, B, A2, B2, C, D): s.append(point(p))
    s += [lettre(A, "A", 14, -14), lettre(B, "B", 14, 46), lettre(A2, "A'", -66, 44), lettre(B2, "B'", -66, -14),
          lettre(C, "C", -46, -14), lettre(D, "D", -46, 46)]
    return f'<svg viewBox="0 0 1500 2000" xmlns="http://www.w3.org/2000/svg">{"".join(s)}</svg>'


if __name__ == "__main__":
    html = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Croquis filtre et construction</title>
<link rel="stylesheet" href="../../polices-local.css">
<style>html, body {{ margin: 0; background: #fff; }}
.cadre {{ position: relative; width: 1500px; height: 2000px; }}
.cadre img, .cadre svg {{ position: absolute; inset: 0; width: 100%; height: 100%; display: block; }}</style></head>
<body><div class="cadre"><img src="croquis-filtre-2.png" alt="">{svg()}</div></body></html>"""
    open("croquis-filtre-2-construction.html", "w", encoding="utf-8").write(html)
    print("A'", A2.round(1), "B'", B2.round(1), "CA'", round(A2[1] - C[1]), "px  B'D", round(D[1] - B2[1]), "px")

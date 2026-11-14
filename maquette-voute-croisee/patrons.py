"""Patrons à l'échelle 1 (A4) de la maquette de voûte croisée, et dessins cotés pour la fiche de montage.

Tout est dessiné en millimètres (1 cm du patron = 10 unités). On imprime à 100 % : un carré de contrôle et une règle
de 10 cm sont dessinés sur chaque page.

Conventions (face imprimée = face INTÉRIEURE, cachée sous la voûte / dans le pilier) :
  trait noir plein   : on COUPE
  tirets bleus       : pli vers soi (« vallée »)   -> la languette passe vers la face imprimée
  tirets rouges      : pli en s'éloignant (« montagne »)
  pointillés gris    : simple repère, on ne coupe ni ne plie
  zone grisée        : languette à encoller
Lancer :  python3 patrons.py   (écrit patrons-A4.html, svg-fiche.json)
"""
import json, math, os
import numpy as np
import geometrie as g

ICI = os.path.dirname(os.path.abspath(__file__))
A, B, H = g.A, g.B, g.H
L = g.L
NOIR, BLEU, ROUGE, GRIS = "#111", "#1f4fd0", "#d02b2b", "#8a8f94"
FONT = "font-family=\"'Architects Daughter', 'DejaVu Sans', Arial, sans-serif\""


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


class Dessin:
    """un dessin dans un repère en cm (Y vers le haut), posé sur la page en mm"""
    def __init__(self, ox, oy, u=10.0):
        self.ox, self.oy, self.u, self.o = ox, oy, u, []

    def P(self, x, y):
        return self.ox + self.u * x, self.oy - self.u * y

    def pts(self, ps):
        return " ".join(f"{f(a)},{f(b)}" for a, b in (self.P(x, y) for x, y in ps))

    def ligne(self, x1, y1, x2, y2, col=NOIR, w=0.35, dash=None, op=1):
        a, b = self.P(x1, y1); c, d = self.P(x2, y2)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.o.append(f'<line x1="{f(a)}" y1="{f(b)}" x2="{f(c)}" y2="{f(d)}" stroke="{col}" stroke-width="{w}"{da} stroke-opacity="{op}" stroke-linecap="round"/>')

    def poly(self, ps, col=NOIR, w=0.35, fond="none", ferme=True, dash=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        tag = "polygon" if ferme else "polyline"
        self.o.append(f'<{tag} points="{self.pts(ps)}" fill="{fond}" stroke="{col}" stroke-width="{w}"{da} stroke-linejoin="round" stroke-linecap="round"/>')

    def texte(self, x, y, s, size=3.2, anchor="start", col="#222", rot=0, weight="normal"):
        a, b = self.P(x, y)
        tr = f' transform="rotate({rot} {f(a)} {f(b)})"' if rot else ""
        self.o.append(f'<text x="{f(a)}" y="{f(b)}" {FONT} font-size="{size}" fill="{col}" text-anchor="{anchor}" font-weight="{weight}"{tr}>{s}</text>')

    def cote_h(self, x1, x2, y, txt, dy=0.0, size=3.0):
        """cote horizontale entre x1 et x2, à l'ordonnée y (cm) ; le texte est au-dessus"""
        self.ligne(x1, y, x2, y, "#444", 0.2)
        for x in (x1, x2):
            self.ligne(x, y - 0.18, x, y + 0.18, "#444", 0.2)
        self.texte((x1 + x2) / 2, y + 0.3 + dy, txt, size, "middle", "#333")

    def cote_v(self, x, y1, y2, txt, size=3.0, cote=-1):
        """cote verticale entre y1 et y2, à l'abscisse x (cm) ; le texte est tourné"""
        self.ligne(x, y1, x, y2, "#444", 0.2)
        for y in (y1, y2):
            self.ligne(x - 0.18, y, x + 0.18, y, "#444", 0.2)
        self.texte(x + cote * 0.3, (y1 + y2) / 2, txt, size, "middle", "#333", rot=-90)

    def rendu(self):
        return "".join(self.o)


def cm(v, d=2):
    return f"{v:.{d}f}".replace(".", ",")


# ------------------------------------------------------------------ le voûtain
def voutain(ox, oy, numero=None, cotes=True, u=10.0):
    d = Dessin(ox, oy, u)
    courbe, decalee, entailles, lg = g.languette_arete()
    left = [(-x, y) for x, y in courbe]                        # courbe gauche, de la clef à l'extrémité (X < 0)
    lp = g.LANGUETTE_PILIER
    # languettes (zones à encoller, en gris)
    d.poly(courbe + decalee[::-1], "none", 0, "#e4e6e8")
    d.poly([(L, A), (L + lp, A), (L + lp, A + B), (L, A + B)], "none", 0, "#e4e6e8")
    d.poly([(-L, A), (-L - lp, A), (-L - lp, A + B), (-L, A + B)], "none", 0, "#e4e6e8")
    # contour de coupe continu : clef -> arête gauche -> languette gauche -> haut -> languette droite -> languette d'arête -> clef
    cont = list(left) + [(-L - lp, A), (-L - lp, A + B), (-L, A + B), (L, A + B), (L + lp, A + B), (L + lp, A), (L, A)] + decalee[::-1]
    d.poly(cont, NOIR, 0.4)
    # entailles de la languette d'arête
    for (p, q) in entailles:
        d.ligne(p[0], p[1], q[0], q[1], NOIR, 0.35)
    # plis
    d.poly(courbe, BLEU, 0.45, "none", False, "2.6 1.2")                       # arête droite : vallée
    d.ligne(-L, A, -L, A + B, ROUGE, 0.45, "2.6 1.2")                          # languette de pilier gauche : montagne
    d.ligne(L, A, L, A + B, ROUGE, 0.45, "2.6 1.2")                            # languette de pilier droite : montagne
    # repères
    d.ligne(-L, A, L, A, GRIS, 0.25, "0.6 1.4")                                # plan de l'arc : début de la bande
    d.ligne(0, -0.6, 0, A + B + 0.6, GRIS, 0.25, "4 1 0.6 1")                  # axe de la clef
    d.o.append(f'<circle cx="{f(d.P(0, 0)[0])}" cy="{f(d.P(0, 0)[1])}" r="0.9" fill="none" stroke="{NOIR}" stroke-width="0.3"/>')
    d.texte(0.35, -0.65, "clef", 3.0, "start", GRIS)
    d.texte(0, A + B / 2 + 0.25, "BANDE DE L'ARC (1,5 cm)", 2.8, "middle", GRIS)
    d.texte(0, A - 0.45, "ligne pointillée = plan de l'arc (repère)", 2.4, "middle", GRIS)
    d.texte(L + 0.2, A - 1.2, "colle", 2.4, "start", "#666")
    if numero:
        d.texte(0, 2.9, f"VOÛTAIN {numero}", 5.0, "middle", "#222", weight="bold")
        d.texte(0, 2.2, "(face imprimée = dessous)", 2.6, "middle", "#666")
    if cotes:
        d.cote_h(-L, L, A + B + 0.9, f"{cm(math.pi * A)} cm (= π × 4,5 : longueur de l'arc)")
        d.cote_v(-L - lp - 0.9, 0, A + B, f"{cm(A + B, 1)} cm", cote=1)
        d.cote_v(L + lp + 0.9, A, A + B, f"{cm(B, 1)} cm", cote=-1)
        d.cote_h(L, L + lp, A + B + 0.35, f"{cm(lp, 1)}", size=2.4)
        d.texte(L + 0.2, A - 1.9, f"largeur {cm(g.LANGUETTE_ARETE, 1)}", 2.4, "start", "#333")
        d.texte(-L + 0.1, 1.3, "arête : w = 4,5 × sin(s ÷ 4,5)", 2.6, "start", "#333")
        d.texte(-L + 0.1, 0.7, "(s = distance depuis la clef, en cm)", 2.3, "start", "#666")
    return d.rendu()


# ------------------------------------------------------------------ le pilier
def pilier(ox, oy, numero=None, cotes=True, u=10.0):
    p = g.patron_pilier()
    C = g.COLLE_PILIER
    d = Dessin(ox, oy, u)
    d.poly(p["colle"], "none", 0, "#e4e6e8")
    d.poly([(0, H), (B, H), (B, H + B), (0, H + B)], "none", 0, "#e4e6e8")
    d.poly([(0, 0), (B, 0), (B, -B), (0, -B)], "none", 0, "#e4e6e8")
    cont = [(0, -B), (B, -B), (B, 0), (4 * B, 0), (4 * B + C, 0.3), (4 * B + C, H - 0.3), (4 * B, H), (B, H), (B, H + B), (0, H + B)]
    d.poly(cont, NOIR, 0.4)
    for i in (1, 2, 3, 4):
        d.ligne(i * B, 0, i * B, H, BLEU, 0.45, "2.6 1.2")
    d.ligne(0, H, B, H, BLEU, 0.45, "2.6 1.2")
    d.ligne(0, 0, B, 0, BLEU, 0.45, "2.6 1.2")
    for i in range(4):
        d.texte(i * B + B / 2, H / 2, f"face {i + 1}", 2.6, "middle", "#777", rot=-90)
    d.texte(B / 2, H + B / 2 - 0.1, "dessus", 2.4, "middle", "#666")
    d.texte(B / 2, -B / 2 - 0.1, "fond", 2.4, "middle", "#666")
    d.texte(4 * B + C / 2 + 0.1, H / 2, "colle", 2.4, "middle", "#666", rot=-90)
    if numero:
        d.texte(2 * B, H + 0.55, f"PILIER {numero}", 3.6, "middle", "#222", weight="bold")
    if cotes:
        d.cote_h(0, 4 * B, H + B + 1.0, f"4 × {cm(B, 1)} = {cm(4 * B, 1)} cm")
        d.cote_v(-0.8, 0, H, f"{cm(H, 1)} cm", cote=1)
        d.cote_v(-0.8, H, H + B, f"{cm(B, 1)}", size=2.4, cote=1)
        d.cote_h(4 * B, 4 * B + C, -0.55, f"{cm(C, 1)}", size=2.4)
    return d.rendu()


# ------------------------------------------------------------------ le socle (avec les repères des piliers) et le gabarit de contrôle
def socle(ox, oy, cotes=True, u=10.0):
    S = g.SOCLE
    d = Dessin(ox, oy, u)
    d.poly([(0, 0), (S, 0), (S, S), (0, S)], NOIR, 0.4)
    m = (S - 2 * (A + B)) / 2
    for (x0, y0) in ((m, m), (S - m - B, m), (m, S - m - B), (S - m - B, S - m - B)):
        d.poly([(x0, y0), (x0 + B, y0), (x0 + B, y0 + B), (x0, y0 + B)], ROUGE, 0.3, "none", True)
    d.ligne(S / 2 - 0.5, S / 2, S / 2 + 0.5, S / 2, GRIS, 0.25); d.ligne(S / 2, S / 2 - 0.5, S / 2, S / 2 + 0.5, GRIS, 0.25)
    d.texte(S / 2, S / 2 + 0.7, "centre de la voûte", 2.4, "middle", GRIS)
    d.texte(S / 2, S - 0.5 - m, "SOCLE — carton gris 2 mm", 3.4, "middle", "#222", weight="bold")
    d.texte(S / 2, S - 1.3 - m, "carrés rouges = emplacement des piliers", 2.6, "middle", ROUGE)
    if cotes:
        d.cote_h(0, S, S + 0.7, f"{cm(S, 1)} cm")
        d.cote_v(-0.7, 0, S, f"{cm(S, 1)} cm", cote=1)
        d.cote_h(m, m + B, -0.8, f"{cm(B, 1)}", size=2.4)
        d.cote_h(m + B, S - m - B, -0.8, f"{cm(2 * A, 1)} cm (portée libre)")
        d.cote_h(0, m, -0.8, f"{cm(m, 1)}", size=2.4)
    return d.rendu()


def cintre(ox, oy, cotes=True, u=10.0):
    d = Dessin(ox, oy, u)
    th = np.linspace(0, math.pi, 91)
    d.poly([(A * math.cos(t), A * math.sin(t)) for t in th], NOIR, 0.4)
    d.texte(0, A * 0.62, "GABARIT DE CONTRÔLE (facultatif)", 3.0, "middle", "#222", weight="bold")
    d.texte(0, A * 0.62 - 0.7, "carton gris 2 mm", 2.6, "middle", "#555")
    d.texte(0, A * 0.62 - 1.4, "à glisser sous un arc pour", 2.4, "middle", "#555")
    d.texte(0, A * 0.62 - 2.0, "vérifier qu'il est bien rond", 2.4, "middle", "#555")
    if cotes:
        d.cote_h(-A, A, -0.9, f"{cm(2 * A, 1)} cm (diamètre)")
        d.cote_v(A + 0.8, 0, A, f"{cm(A, 1)} cm (rayon)", cote=-1)
    return d.rendu()


# ------------------------------------------------------------------ pages A4
def page(titre, sous, corps, num):
    regle = "".join(f'<line x1="{15 + i * 10}" y1="286" x2="{15 + i * 10}" y2="{288.2 if i % 5 else 289.2}" stroke="#222" stroke-width="0.25"/>' for i in range(11))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 210 297" width="210mm" height="297mm">
<rect width="210" height="297" fill="#fff"/>
<text x="12" y="14" {FONT} font-size="7" fill="#111">{titre}</text>
<text x="12" y="20.5" {FONT} font-size="3.4" fill="#555">{sous}</text>
<g {FONT} font-size="2.7" fill="#333">
 <line x1="12" y1="26" x2="26" y2="26" stroke="{NOIR}" stroke-width="0.4"/><text x="28" y="27">on COUPE</text>
 <line x1="52" y1="26" x2="66" y2="26" stroke="{BLEU}" stroke-width="0.45" stroke-dasharray="2.6 1.2"/><text x="68" y="27">pli vers soi (vallée)</text>
 <line x1="102" y1="26" x2="116" y2="26" stroke="{ROUGE}" stroke-width="0.45" stroke-dasharray="2.6 1.2"/><text x="118" y="27">pli en s'éloignant (montagne)</text>
 <rect x="168" y="24" width="8" height="3.6" fill="#e4e6e8"/><text x="178" y="27">languette</text>
</g>
{corps}
<line x1="15" y1="286" x2="115" y2="286" stroke="#222" stroke-width="0.3"/>{regle}
<text x="15" y="283.6" {FONT} font-size="2.6" fill="#333">règle de contrôle : doit mesurer exactement 10 cm — imprimer à 100 % (« taille réelle »), sans « ajuster à la page »</text>
<text x="198" y="291" {FONT} font-size="2.8" fill="#666" text-anchor="end">page {num} / 4 · voûte croisée</text>
</svg>"""


def pages():
    ps = []
    ps.append(page("Voûtains 1 et 2", "bristol 200 g · à imprimer sur la face qui sera DESSOUS · on garde les languettes",
                   voutain(105, 112, 1) + voutain(105, 212, 2), 1))
    ps.append(page("Voûtains 3 et 4", "bristol 200 g · identiques aux voûtains 1 et 2",
                   voutain(105, 112, 3) + voutain(105, 212, 4), 2))
    # piliers : 2 colonnes x 2 rangées ; origine de chaque patron = coin bas-gauche des faces (le fond est dessous)
    piliers = (pilier(24, 141, 1) + pilier(114, 141, 2) + pilier(24, 255, 3, cotes=False) + pilier(114, 255, 4, cotes=False))
    ps.append(page("Piliers 1 à 4", "bristol 200 g · 4 piliers identiques : tube carré 1,5 × 1,5 × 8 cm, avec dessus et fond", piliers, 3))
    ps.append(page("Socle et gabarit", "carton gris 2 mm · le socle et le gabarit de contrôle (facultatif)",
                   socle(28, 192) + cintre(105, 262) , 4))
    return ps


def html(ps):
    divs = "".join(f"<div class='p'>{p}</div>" for p in ps)
    return (f"<!doctype html><html lang='fr'><head><meta charset='utf-8'><title>Patrons de la voûte croisée</title>"
            f"<link rel='stylesheet' href='polices-local.css'><style>@page {{ size: 210mm 297mm; margin: 0; }} html, body {{ margin: 0; background: #fff; }}"
            f".p {{ width: 210mm; height: 297mm; page-break-after: always; break-after: page; overflow: hidden; }}"
            f".p:last-child {{ page-break-after: auto; break-after: auto; }} svg {{ width: 210mm; height: 297mm; display: block; }}</style></head><body>{divs}</body></html>")


def svg_fiche():
    """dessins cotés pour la page 3D (viewBox ajusté, sans titre) : voûtain, pilier, socle, gabarit"""
    out = {}
    d = voutain(0, 0, None, True, 10.0)
    out["voutain"] = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-100 -92 200 124" class="patron">{d}</svg>'
    d = pilier(0, 0, None, True, 10.0)
    out["pilier"] = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-16 -118 100 142" class="patron">{d}</svg>'
    d = socle(0, 0, True, 10.0)
    out["socle"] = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-12 -148 164 164" class="patron">{d}</svg>'
    d = cintre(0, 0, True, 10.0)
    out["cintre"] = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-60 -58 120 76" class="patron">{d}</svg>'
    return out


if __name__ == "__main__":
    ps = pages()
    open(os.path.join(ICI, "patrons-A4.html"), "w", encoding="utf-8").write(html(ps))
    json.dump(svg_fiche(), open(os.path.join(ICI, "svg-fiche.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("patrons-A4.html (", len(ps), "pages ) et svg-fiche.json écrits")

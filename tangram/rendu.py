"""Construit tangram/index.html a partir de formes.json (lancer generer.py avant)."""
import json
import math
import os

ICI = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(ICI, "formes.json")))
STD, F = D["std"], D["formes"]
S = 40  # px par carreau


def P(x, y):
    return x * S, -y * S


def pts(poly):
    return " ".join(f"{P(x, y)[0]:.1f},{P(x, y)[1]:.1f}" for x, y in poly)


def centroid(p):
    return sum(x for x, _ in p) / len(p), sum(y for _, y in p) / len(p)


def arc(cx, cy, r, a0, a1):
    """arc (degres, sens trigo) en coordonnees maths"""
    x0, y0 = P(cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    x1, y1 = P(cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    large = 1 if abs(a1 - a0) > 180 else 0
    return f'<path class="fl" d="M{x0:.1f},{y0:.1f} A{r*S:.1f},{r*S:.1f} 0 {large} 0 {x1:.1f},{y1:.1f}" marker-end="url(#m-{{id}})"/>'


def line(a, b, cls):
    (x0, y0), (x1, y1) = P(*a), P(*b)
    extra = {"fl": ' marker-end="url(#m-{id})"',
             "fl2": ' marker-start="url(#m-{id})" marker-end="url(#m-{id})"'}.get(cls, "")
    return f'<line class="{cls}" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}"{extra}/>'


def label(x, y, txt, cls="note", anchor="middle"):
    X, Y = P(x, y)
    return f'<text class="{cls}" x="{X:.1f}" y="{Y:.1f}" text-anchor="{anchor}">{txt}</text>'


def point(x, y, name):
    X, Y = P(x, y)
    return (f'<circle class="pt" cx="{X:.1f}" cy="{Y:.1f}" r="4"/>'
            + label(x - 0.25, y - 0.45, name, "note", "end"))


def figure(fid, fig, moved=(), ghosts=(), annot="", extra_pts=(), title=""):
    allp = [q for p in fig.values() for q in p] + [q for g in ghosts for q in g] + list(extra_pts)
    x0 = math.floor(min(x for x, _ in allp)) - 1
    x1 = math.ceil(max(x for x, _ in allp)) + 1
    y0 = math.floor(min(y for _, y in allp)) - 1
    y1 = math.ceil(max(y for _, y in allp)) + 1
    vb = f"{x0*S} {-y1*S} {(x1-x0)*S} {(y1-y0)*S}"
    out = [f'<svg viewBox="{vb}" role="img" aria-label="{title}" xmlns="http://www.w3.org/2000/svg">',
           f'<defs><marker id="m-{fid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
           f'<path d="M0,0 L10,5 L0,10 z" class="tete"/></marker></defs>']
    # quadrillage
    for gx in range(x0, x1 + 1):
        for gy in range(y0, y1 + 1):
            X, Y = P(gx, gy)
            out.append(f'<circle class="grille" cx="{X}" cy="{Y}" r="1.4"/>')
    for g in ghosts:
        out.append(f'<polygon class="fantome" points="{pts(g)}"/>')
    for k, p in fig.items():
        cls = "pc moved" if k in moved else "pc"
        out.append(f'<polygon class="{cls}" points="{pts(p)}"/>')
    for k, p in fig.items():
        cx, cy = centroid(p)
        out.append(label(cx, cy - 0.12, k, "lbl"))
    out.append(annot.replace("{id}", fid))
    out.append("</svg>")
    return "\n".join(out)


B = ["M", "P1", "C", "P2", "Pa"]
SVG = {}

SVG["depart"] = figure("depart", STD, title="Carré de départ, 7 pièces")

SVG["faille"] = figure(
    "faille", F["faille"], moved=B, ghosts=[[(4, 0), (4, 4), (0, 4)]],
    annot=line((-0.6, 4.6), (6.6, -2.6), "axe")
    + line((2.9, 3.1), (4.75, 1.25), "fl")
    + label(4.55, 2.75, "v", "note") ,
    title="La Faille : translation")

SVG["porche"] = figure(
    "porche", F["porche"], moved=["G1"], ghosts=[STD["G1"]],
    annot=arc(0, 0, 1.6, 12, 104) + label(1.95, 0.95, "90°", "note")
    + point(0, 0, "O"),
    title="Le Porche : rotation de 90°")

SVG["chevron"] = figure(
    "chevron", F["chevron"], moved=["G2"], extra_pts=[(0, 5.6), (0, -3.2)],
    annot=line((0, -3.2), (0, 5.2), "axe") + label(0.2, 5.3, "axe", "note", "start")
    + line((-1.45, 3.65), (1.45, 3.65), "fl2"),
    title="Le Chevron : symétrie axiale")

SVG["torsion"] = figure(
    "torsion", F["torsion"], moved=["G2"], extra_pts=[(-3.6, 0), (3.6, 0)],
    annot=arc(0, 0, 3.4, 125, 292) + label(-3.9, -1.6, "180°", "note")
    + point(0, 0, "O"),
    title="La Torsion : symétrie centrale")

SVG["pas"] = figure(
    "pas", F["pas"], moved=B, ghosts=[[(0, 0), (4, 0), (0, -4)]], extra_pts=[(1, -5.2)],
    annot=line((-1.2, 0), (7.2, 0), "axe") + label(7.2, 0.25, "axe", "note", "end")
    + line((0, -4.45), (2, -4.45), "fl") + label(1, -5.05, "glissement", "note"),
    title="Le Pas : symétrie glissée")

html = open(os.path.join(ICI, "gabarit.html"), encoding="utf-8").read()
for k, v in SVG.items():
    html = html.replace("{{" + k + "}}", v)
assert "{{" not in html
open(os.path.join(ICI, "index.html"), "w", encoding="utf-8").write(html)
print("index.html ecrit", len(html), "octets")

"""Planches A4 à calquer : l'Azuma House à l'échelle 1/100 (a = 4 cm), en 3 feuilles x 3 couches.

Couche « base »   : le bâtiment au trait noir (à calquer en premier).
Calque 1          : bleu (a, le carré) + rouge (1/3 a, le tiers) : les grandes formes.
Calque 2          : vert (1/4 a, le quart) + violet (e = 1/21 a, le mur) : les petites formes.
Feuille 4         : la trame (modules de 1/3 a) sur les 3 plans, en une seule page.
Sur les calques, le bâtiment reste en gris pâle pour se repérer (à ne pas recopier).
Les 4 croix de calage sont au même endroit sur les 9 pages : on les pose l'une sur l'autre.
Lancer : python3 calques.py  ->  calques.html, puis rendu-calques.js  ->  calques-a4.pdf
"""
import html, os
import build
from build import COL

build.IMPRESSION = True
MM = 40 / build.S             # 1/100 : a = 4 m = 40 mm sur la feuille
ICI = os.path.dirname(os.path.abspath(__file__))

FEUILLES = [
    ("Feuille 1 · les plans", [(build.plan_rdc, "Rez-de-chaussée"), (build.plan_etage, "Étage"), (build.plan_toit, "Toiture")], "colonne"),
    ("Feuille 2 · coupe longitudinale, coupe C, façade B", [(build.coupe_longue, "Coupe longitudinale"), (build.coupe_c, "Coupe C"), (build.facade_b, "Façade B (rue)")], "1+2"),
    ("Feuille 3 · coupe E, façade C", [(build.coupe_e, "Coupe E (patio)"), (build.facade_c, "Façade C (jardin)")], "2"),
]
COUCHES = [
    ("base", "Base · le bâtiment au trait", "base", []),
    ("c1", "Calque 1 · le carré et le tiers", {"a", "t"}, [("a", "a · le carré"), ("t", "1/3 a · le tiers, 1/15 a")]),
    ("c2", "Calque 2 · le quart et le mur", {"q", "e"}, [("q", "1/4 a · le quart, 1/8 a"), ("e", "e = 1/21 a · le mur")]),
]
CROIX = [(12, 12), (198, 12), (12, 285), (198, 285)]


def croix(x, y):
    return (f'<g stroke="#000" stroke-width="0.25" fill="none"><line x1="{x-4}" y1="{y}" x2="{x+4}" y2="{y}"/>'
            f'<line x1="{x}" y1="{y-4}" x2="{x}" y2="{y+4}"/><circle cx="{x}" cy="{y}" r="2"/></g>')


def page(nom_f, vues, mise, couche):
    cle, titre_c, garde, leg = couche
    dessins = []
    for f, t in vues:
        d, nom, _ = f()
        dessins.append((d, t, nom))
    out, y = [], 36.0
    def place(d, t, nom, x, y):
        w, h = d.W * MM, d.H * MM
        out.append(f'<text x="{x + d.mg * 40:.1f}" y="{y - 1.2:.1f}" font-family="Archivo, Arial, sans-serif" font-size="3.6" font-weight="700" fill="#111">{html.escape(t)}</text>')
        out.append(f'<svg x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" viewBox="0 0 {d.W:.0f} {d.H:.0f}">'
                   + d.svg(nom, couche=garde).split(">", 1)[1].replace('<rect width="100%" height="100%" fill="#fbfbf8"/>', ""))   # contenu du dessin, sans fond
        return w, h
    if mise == "colonne":
        for d, t, nom in dessins:
            w, h = d.W * MM, d.H * MM
            place(d, t, nom, (210 - w) / 2, y); y += h + 6
    elif mise == "1+2":
        d, t, nom = dessins[0]; w, h = place(d, t, nom, (210 - d.W * MM) / 2, y); y += h + 8
        w1, w2 = dessins[1][0].W * MM, dessins[2][0].W * MM; g = (210 - w1 - w2) / 3
        place(*dessins[1], g, y); place(*dessins[2], 2 * g + w1, y)
    else:
        w1, w2 = dessins[0][0].W * MM, dessins[1][0].W * MM; g = (210 - w1 - w2) / 3
        y = 40
        place(*dessins[0], g, y); place(*dessins[1], 2 * g + w1, y)
    entete = (f'<text x="20" y="13.5" font-family="Archivo, Arial, sans-serif" font-size="5" font-weight="800" fill="#111">Azuma House · {html.escape(titre_c)}</text>'
              f'<text x="20" y="19.5" font-family="IBM Plex Mono, monospace" font-size="2.7" fill="#444">{html.escape(nom_f)} · échelle 1/100 (a = 4 cm) · imprimer à 100 %</text>')
    lx = 20
    for k, t in leg:
        entete += f'<rect x="{lx}" y="22.2" width="3.2" height="3.2" fill="{COL[k]}"/><text x="{lx+4.6}" y="25" font-family="IBM Plex Mono, monospace" font-size="2.8" font-weight="700" fill="{COL[k]}">{html.escape(t)}</text>'
        lx += 52
    if cle not in ("base", "trame"):
        entete += f'<text x="190" y="25" text-anchor="end" font-family="IBM Plex Mono, monospace" font-size="2.4" fill="#777">en gris pâle : repère, à ne pas recopier</text>'
    regle = ('<g stroke="#111" stroke-width="0.3"><line x1="150" y1="290" x2="190" y2="290"/>'
             + "".join(f'<line x1="{150 + 10*i}" y1="288.5" x2="{150 + 10*i}" y2="291.5"/>' for i in range(5))
             + '</g><text x="170" y="295" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="2.4" fill="#111">4 cm = a = 4 m</text>')
    return (f'<div class="page"><svg width="210mm" height="297mm" viewBox="0 0 210 297" xmlns="http://www.w3.org/2000/svg">'
            f'{entete}{"".join(out)}{"".join(croix(*c) for c in CROIX)}{regle}</svg></div>')


TRAME = [(build.trame, "Rez-de-chaussée sur la trame"), (lambda: build.trame(build.plan_etage), "Étage sur la trame"),
         (lambda: build.trame(build.plan_toit), "Toiture sur la trame")]


def document():
    pages = [page(nf, v, m, c) for nf, v, m in FEUILLES for c in COUCHES]
    pages.append(page("Feuille 4 · la trame", TRAME, "colonne", ("trame", "La trame · modules de 1/3 a", None, [("a", "a = 3 modules"), ("t", "1/3 a = 1 module")])))
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Azuma House · calques A4</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&family=IBM+Plex+Mono:wght@400;700&display=swap">
<style>@page {{ size: 210mm 297mm; margin: 0; }} html, body {{ margin: 0; padding: 0; background: #fff; }}
.page {{ width: 210mm; height: 297mm; overflow: hidden; page-break-after: always; break-after: page; }} .page svg {{ display: block; }}</style></head>
<body>{"".join(pages)}</body></html>"""


if __name__ == "__main__":
    open(os.path.join(ICI, "calques.html"), "w", encoding="utf-8").write(document())
    print("calques.html écrit")

"""Le rendu : constructions des coupes et façades, rendu au trait (fort / moyen / fin) de toutes les vues, détails des portes et fenêtres.
A4 paysage, à l'échelle du carnet (a = 5,55 cm), à imprimer à 100 %.
Lancer : python3 rendu_pdf.py  ->  rendu.html, puis rendu-pdf.js  ->  azuma-rendu-x1-5.pdf
"""
import html, os, re, math
import build, trait
from build import COL, A_CARNET, A_FEUILLE, A_REEL, K_CARNET

build.IMPRESSION = True
ICI = os.path.dirname(os.path.abspath(__file__))
MM = A_CARNET * 10 / build.S
vir = build._vir


def entete(titre, sous=None):
    sous = sous or f"carnet : a = {vir(A_CARNET, 2)} cm (feuille {vir(A_FEUILLE)} cm × {vir(K_CARNET)}) · ≈ 1/{A_REEL / A_CARNET:.0f} · imprimer à 100 %"
    return f'<header><div class="t">Azuma House · {html.escape(titre)}</div><div class="s">{sous}</div></header>'


def page(contenu, titre, sous=None, cls=""):
    return f'<section class="page {cls}">{entete(titre, sous)}<div class="corps">{contenu}</div></section>'


def etapes_html(etapes, cols=2):
    li = "".join(f'<li><span class="num">{j+1}</span><span>{t}</span></li>' for j, t in enumerate(etapes))
    return f'<ol class="etapes c{cols}">{li}</ol>'


def pages_constructions():
    out = []
    ids = [c[0] for c in trait.CONSTR]
    def fig(i): return trait.construire_vue(i).svg(trait.CONSTR[i][1], mm=MM)
    i = ids.index("coupe_longue")
    out.append(page(f'<div class="centre">{fig(i)}</div>{etapes_html(trait.CONSTR[i][6], 2)}', "Construction · la coupe longitudinale", cls="serre"))
    for pair in (("coupe_c", "coupe_e"), ("facade_b", "facade_c")):
        cases = ""
        for id_ in pair:
            j = ids.index(id_)
            cases += f'<div class="cas"><h3>{html.escape(trait.CONSTR[j][1])}</h3>{fig(j)}{etapes_html(trait.CONSTR[j][6], 1)}</div>'
        out.append(page(f'<div class="duo">{cases}</div>', "Construction · " + " et ".join(trait.CONSTR[ids.index(p)][1].split(" : ")[0] for p in pair), cls="serre"))
    # les agrandissements des façades
    cases = ""
    for j, (zid, zt, zr, z) in enumerate(trait.ZOOMS):
        f = trait.construire_zoom(j)
        w, h = f.W * MM, f.H * MM
        sc = min(1.0, 133 / w, 118 / h)
        cases += f'<div class="cas"><h3>{html.escape(zt)} <span class="zt">zoom × {z:g}</span></h3>{f.svg(zt, mm=MM * sc)}</div>'
    out.append(page(f'<div class="duo">{cases}</div>', "Construction · agrandissements des façades", cls="serre"))
    return out


def pages_rendu():
    """le rendu au trait de toutes les vues"""
    build.TRAIT_MODE = True
    try:
        out = []
        vues = {t: f for t, _, f in build.VUES}
        def svg(nom):
            d, titre, notes = vues[nom]()
            return d.svg(titre, mm=MM), notes
        for nom in ("Coupe longitudinale",):
            s, notes = svg(nom)
            out.append(page(f'<div class="centre">{s}</div>', "Rendu au trait · " + nom, cls="serre"))
        for pair in (("Coupe C", "Coupe E (patio)"), ("Façade B (rue)", "Façade C (jardin)")):
            cases = "".join(f'<div class="cas"><h3>{html.escape(n)}</h3>{svg(n)[0]}</div>' for n in pair)
            out.append(page(f'<div class="duo">{cases}</div>', "Rendu au trait · " + " et ".join(pair)))
        for nom in ("Plan du rez-de-chaussée", "Plan de l'étage", "Plan de toiture"):
            s, notes = svg(nom)
            out.append(page(f'<div class="centre">{s}</div>', "Rendu au trait · " + nom, cls="serre"))
        return out
    finally:
        build.TRAIT_MODE = False


def page_legende():
    k = MM
    lignes = "".join(
        f'<tr><td><svg width="50mm" height="4mm" viewBox="0 0 50 4"><line x1="1" y1="2" x2="49" y2="2" stroke="{c}" stroke-width="{w * k:.3f}"/></svg></td>'
        f'<td><b>{nom}</b><br><span class="n">{w * k:.2f} mm · {crayon}</span></td><td>{quoi}</td></tr>'
        for nom, w, c, quoi, crayon in trait.TRAITS)
    contenu = f"""<div class="garde"><div><table class="lt"><thead><tr><th>Échantillon</th><th>Trait</th><th>Où</th></tr></thead><tbody>{lignes}</tbody></table></div>
    <div><h4>Ce qu'a demandé la prof</h4><ul>
      <li><b>Trait fort là où il y a la coupe</b>, fin pour le reste, et bien doser.</li>
      <li><b>Constructions géométriques</b> pour les coupes et les façades aussi (diagonales, tiers, Thalès).</li>
      <li><b>Plus de détails</b> : portes, fenêtres, épaisseur du vitrage de la porte.</li></ul>
      <h4>L'ordre de travail</h4><ol>
      <li>Les constructions (très légères) : l'échelle des e, les diagonales, les tiers.</li>
      <li>Le contour de la vue au trait moyen.</li>
      <li>Les ouvertures : cadres en moyen, vitrage en fin.</li>
      <li>En dernier, le trait fort sur tout ce qui est coupé : murs, dalles, garde-corps et escalier coupés.</li></ol>
      <h4>Les portes et fenêtres</h4>
      <p>À 1/72, 1 cm de verre fait 0,14 mm : le vitrage se dessine en <b>un trait fin</b>. L'épaisseur du verre (1 cm, à valider) et les cadres (e/2, e/3, e/6) se montrent sur les <b>détails à 1/10</b>, aux deux dernières pages.</p></div></div>"""
    return page(contenu, "Le trait et le rendu", "fort · moyen · fin · construction")


def pages_details():
    out = []
    byid = {d[0]: d for d in trait.DETAILS}
    def cas(id_):
        _, titre, ech, f, steps = byid[id_]
        D = f()
        return (f'<div class="cas"><h3>{html.escape(titre)} <span class="zt">échelle {ech}</span></h3>{D.svg(titre)}{etapes_html(steps, 1)}</div>')
    out.append(page(f'<div class="centre">{cas("porte_plan")}</div>', "Détail · la porte d'entrée en plan (1/10)", "1/10 : 1 cm réel = 1 mm sur la feuille", cls="serre"))
    def lat(id_):
        _, titre, ech, f, steps = byid[id_]
        D = f()
        return (f'<div class="lat"><div>{D.svg(titre)}</div><div class="cote-l"><h3>{html.escape(titre)} <span class="zt">échelle {ech}</span></h3>{etapes_html(steps, 1)}</div></div>')
    out.append(page(lat("porte_elev"), "Détail · la porte d'entrée en élévation (1/20)", "1/20 : 1 cm réel = 0,5 mm sur la feuille", cls="serre"))
    out.append(page(lat("fente"), "Détail · la fente vitrée en plan (1/10)", "1/10 : 1 cm réel = 1 mm sur la feuille", cls="serre"))
    out.append(page(f'<div class="centre">{cas("fenetre_jardin")}</div>', "Détail · la fenêtre du jardin (1/10)", "1/10 : 1 cm réel = 1 mm sur la feuille", cls="serre"))
    return out


def document():
    pages = [page_legende()] + pages_constructions() + pages_rendu() + pages_details()
    css = """@page { size: 297mm 210mm; margin: 0; }
html, body { margin: 0; padding: 0; background: #fff; font-family: "Source Serif 4", Georgia, serif; color: #1c2120; }
.page { width: 297mm; height: 210mm; padding: 8mm 10mm; box-sizing: border-box; overflow: hidden; page-break-after: always; break-after: page; }
.page.serre { padding: 6mm 5mm; }
.page header { display: flex; justify-content: space-between; align-items: baseline; border-bottom: 0.4mm solid #1c2120; padding-bottom: 1.5mm; margin-bottom: 3mm; }
.page header .t { font-family: "Archivo", Arial, sans-serif; font-weight: 800; font-size: 5mm; }
.page header .s { font-family: "IBM Plex Mono", monospace; font-size: 2.5mm; color: #555; }
.corps svg { display: block; flex: none; max-width: none; }
.centre { display: flex; justify-content: center; } .centre .cas { display: block; }
.duo { display: flex; gap: 8mm; justify-content: center; align-items: flex-start; } .duo2 { display: flex; gap: 8mm; align-items: flex-start; }
.cas h3 { font-family: "Archivo", Arial, sans-serif; font-size: 3.8mm; margin: 0 0 1mm; } .zt { font-family: "IBM Plex Mono", monospace; font-size: 2.3mm; font-weight: 500; color: #555; }
.etapes { list-style: none; margin: 2mm 0 0; padding: 0; display: grid; gap: 0.9mm; font-size: 2.95mm; line-height: 1.22; }
.serre .etapes { font-size: 2.65mm; line-height: 1.15; gap: 0.6mm; margin-top: 1.2mm; }
.lat { display: flex; gap: 8mm; align-items: flex-start; } .cote-l { flex: 1; } .cote-l .etapes { font-size: 3.2mm; }
.etapes.c2 { grid-template-columns: 1fr 1fr; column-gap: 8mm; }
.etapes li { display: flex; gap: 1.6mm; align-items: flex-start; }
.num { flex: none; width: 4mm; height: 4mm; border-radius: 50%; background: #555; color: #fff; font-family: "IBM Plex Mono", monospace; font-size: 2.4mm; font-weight: 700; display: inline-grid; place-items: center; margin-top: 0.2mm; }
.garde { display: grid; grid-template-columns: 150mm 1fr; gap: 10mm; font-size: 3.4mm; line-height: 1.35; } .garde h4 { font-family: "Archivo", Arial, sans-serif; font-size: 3.9mm; margin: 3mm 0 1mm; } .garde ul, .garde ol { margin: 0; padding-left: 5mm; display: grid; gap: 1mm; }
.lt { border-collapse: collapse; width: 100%; font-size: 3.1mm; } .lt th { text-align: left; font-family: "IBM Plex Mono", monospace; font-size: 2.2mm; text-transform: uppercase; border-bottom: 0.4mm solid #1c2120; padding: 1mm 2mm 1mm 0; }
.lt td { border-bottom: 0.2mm solid #ccc; padding: 2mm 2mm 2mm 0; vertical-align: top; } .lt .n { font-size: 2.6mm; color: #666; }"""
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Azuma House · rendu</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&family=IBM+Plex+Mono:wght@400;500;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<style>{css}</style></head><body>{"".join(pages)}</body></html>"""


if __name__ == "__main__":
    open(os.path.join(ICI, "rendu.html"), "w", encoding="utf-8").write(document())
    print("rendu.html écrit")

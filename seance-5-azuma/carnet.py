"""Le carnet : l'Azuma House avec a = 5,55 cm (la feuille a = 3,7 cm, agrandie par 1,5), en pages A4 paysage à imprimer à 100 %.

Page de garde et tableau des mesures, les 8 vues dessinées à l'échelle du carnet, puis chaque construction (pli et règle-compas)
à l'échelle du carnet (les zooms sont indiqués).
Lancer : python3 carnet.py  ->  carnet.html, puis rendu-carnet.js  ->  azuma-carnet-x1-5.pdf
"""
import html, math, os, re
import build
from build import COL, A_CARNET, A_FEUILLE, A_REEL, K_CARNET

build.IMPRESSION = True
ICI = os.path.dirname(os.path.abspath(__file__))
MM = A_CARNET * 10 / build.S              # mm par unité du dessin : a = 55,5 mm
UTILE_L, UTILE_H = 277.0, 182.0           # zone utile d'une page (mm), sous l'en-tête


def vir(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")


def en_tete(titre, sous=""):
    return (f'<header><div class="t">Azuma House · {html.escape(titre)}</div>'
            f'<div class="s">{sous or f"carnet : a = {vir(A_CARNET, 2)} cm (feuille {vir(A_FEUILLE)} cm × {vir(K_CARNET)}) · ≈ 1/{A_REEL / A_CARNET:.0f} · imprimer à 100 %"}</div></header>')


def page(contenu, titre, sous=""):
    return f'<section class="page">{en_tete(titre, sous)}<div class="corps">{contenu}</div></section>'


def pages_vues():
    out = []
    vues = [(f, t) for t, _, f in build.VUES]
    for i in (2, 1, 0):                                   # toiture, étage, rez-de-chaussée : un plan par page
        d, nom, notes = vues[i][0]()
        li = "".join(f'<li><i style="background:{COL[k]}"></i><span>{t}</span></li>' for k, t in notes)
        out.append(page(f'<div class="vue">{d.svg(nom, mm=MM)}</div><ul class="notes">{li}</ul>', vues[i][1]))
    d, nom, notes = vues[3][0]()
    li = "".join(f'<li><i style="background:{COL[k]}"></i><span>{t}</span></li>' for k, t in notes)
    out.append(page(f'<div class="vue">{d.svg(nom, mm=MM)}</div><ul class="notes">{li}</ul>', vues[3][1]))
    for paire in ((4, 5), (6, 7)):                        # les 4 petites vues, 2 par page
        cases = ""
        for i in paire:
            d, nom, notes = vues[i][0]()
            cases += f'<div class="petite"><div class="titre">{html.escape(vues[i][1])}</div>{d.svg(nom, mm=MM)}</div>'
        out.append(page(f'<div class="paire">{cases}</div>', " · ".join(vues[i][1] for i in paire)))
    return out


def pages_constructions():
    """les 14 constructions : les zooms sont réduits pour tenir à deux par page (le carnet n'est pas à cette échelle : c'est un zoom)"""
    cartes = []
    for i, (id_, titre, k, vue, region, z, dessin, au_pli, etapes) in enumerate(build.CONSTRUCTIONS):
        fig = build.construire(i)
        large = id_ in ("milieu", "escalier_plan")
        maxw, maxh = (270.0, 84.0) if large else (133.0, 100.0)
        w0, h0 = fig.W * MM, fig.H * MM
        sc = min(1.0, maxw / w0, maxh / h0)
        w, h = w0 * sc, h0 * sc
        cw = 277.0 if large else 135.0
        li = "".join(f'<li><span class="num">{j+1}</span><span>{t}</span></li>' for j, t in enumerate(etapes))
        zoom = f' <span class="zoomtag">zoom × {z:g}</span>' if z != 1 else ""
        lignes = sum(math.ceil(len(re.sub(r"<[^>]+>", "", t)) / ((cw - 7) / 1.7)) for t in etapes)
        hh = 9 + h + 3 + lignes * 4.4 + len(etapes) * 1.0 + 9
        cartes.append((large, cw, hh, f'<article class="cons" style="width:{cw:.0f}mm;border-color:{COL[k]}"><h3><span class="n" style="color:{COL[k]}">{i+1}</span> {html.escape(titre)}{zoom}</h3>'
                                       f'{fig.svg(titre, mm=MM * sc)}<ol class="etapes">{li}</ol><p class="aupli">{au_pli}</p></article>'))
    rows, row = [], []
    for large, cw, hh, h in cartes:
        if large:
            if row: rows.append(row); row = []
            rows.append([(cw, hh, h)])
        else:
            row.append((cw, hh, h))
            if len(row) == 2: rows.append(row); row = []
    if row: rows.append(row)
    pages, page_rows, y = [], [], 0.0
    for r in rows:
        rh = max(c[1] for c in r)
        if page_rows and y + rh > UTILE_H:
            pages.append(page_rows); page_rows, y = [], 0.0
        page_rows.append(r); y += rh + 5
    if page_rows: pages.append(page_rows)
    return [page("".join(f'<div class="rangee">{"".join(c[2] for c in r)}</div>' for r in pr), "Les constructions", "règle, équerre, compas · les zooms sont des agrandissements du carnet") for pr in pages]


def tableau_groupes(indices):
    """un tableau par groupe de mesures (réel, feuille, carnet)"""
    out = ['<div class="tab"><table><thead><tr><th>Mesure</th><th>en a</th><th>réel (cm)</th><th>feuille (mm)</th><th>carnet (mm)</th></tr></thead><tbody>']
    for gi in indices:
        groupe, lignes = build.MESURES[gi]
        out.append(f'<tr class="grp"><td colspan="5">{html.escape(groupe)}</td></tr>')
        for nom, txt, v, note in lignes:
            cm = float(v) * A_REEL
            n = f'<span class="note"> · {html.escape(note)}</span>' if note else ""
            out.append(f'<tr><td>{html.escape(nom)}{n}</td><td class="m">{html.escape(txt)}</td><td>{vir(cm, 1 if cm < 100 else 0)}</td>'
                       f'<td>{vir(float(v) * A_FEUILLE * 10)}</td><td class="carnet">{vir(float(v) * A_CARNET * 10)}</td></tr>')
    out.append('</tbody></table></div>')
    return "".join(out)


def page_tableau():
    return page(f'<div class="deuxcol"><div>{tableau_groupes((0, 1))}</div><div>{tableau_groupes((2, 3, 4))}</div></div>', "Le tableau des mesures",
                f"réel : a = {A_REEL} cm · feuille : {vir(A_FEUILLE)} cm · carnet : {vir(A_CARNET, 2)} cm · en mm")


def page_garde():
    echelle = (f'<div class="echelle"><div><b>{A_REEL} cm</b><span>a, en vrai</span></div><i>→</i>'
               f'<div><b>{vir(A_FEUILLE)} cm</b><span>a sur la feuille<br>≈ 1/{A_REEL / A_FEUILLE:.0f}</span></div><i>× {vir(K_CARNET)} →</i>'
               f'<div class="cn"><b>{vir(A_CARNET, 2)} cm</b><span>a dans le carnet<br>≈ 1/{A_REEL / A_CARNET:.0f}</span></div></div>')
    leg = "".join(f'<li><i style="background:{COL[k]}"></i>{html.escape(v)}</li>' for k, v in build.NOMS.items())
    echelle_notes = f"""<h4>Ce qu'il faut retenir</h4>
        <ul class="retenir">
          <li><b>a</b> se prend à l'<b>extérieur</b> des murs ; les plis tombent sur les <b>axes</b>.</li>
          <li>La structure suit les <b>tiers</b> (trame de 1/3 a : 12 × 3 modules). Les ouvertures suivent les <b>quarts</b> et les <b>huitièmes</b>.</li>
          <li><b>e = 1/21 a</b> = 1/7 du tiers (≈ 19 cm), pas 1/20. Le garde-corps du pont : <b>5 e = 95 cm</b>, son sommet à <b>2/3 a</b>.</li>
          <li>Escalier : <b>11 marches de 1/15 a</b> ; largeur <b>1/4 a mur compris</b>, donc 1/4 a − e pour l'escalier seul.</li>
          <li>Fenêtres des longs murs : <b>2 fentes + 1 trumeau de 1/15 a</b> (1/5 a), à <b>1/9 a</b> de l'axe du mur du patio. Fenêtres du jardin : <b>1/8 a + 1/7 a + 1/8 a</b>.</li>
          <li>On ne plie pas en 7 ni en 5 : on construit par <b>Thalès</b>.</li>
        </ul>"""
    texte = f"""<div class="garde">
      <div class="col">
        {echelle}
        <p>Sur la feuille, a mesure <b>{vir(A_FEUILLE)} cm</b>. Dans le carnet, tout est multiplié par <b>{vir(K_CARNET)}</b> : <b>a = {vir(A_CARNET, 2)} cm</b>.
        Le plan fait donc <b>{vir(4 * A_CARNET, 1)} cm</b> de long sur <b>{vir(A_CARNET, 2)} cm</b> de large ; la coupe fait <b>{vir(13 / 8 * A_CARNET, 1)} cm</b> de haut.
        Il faut une page <b>A4 en paysage</b> (le plan dépasse 21 cm).</p>
        <h4>L'ordre de travail</h4>
        <ol class="ordre">
          <li>Trace le rectangle de {vir(4 * A_CARNET, 1)} × {vir(A_CARNET, 2)} cm. Construis les <b>milieux</b> (diagonales) puis le <b>tiers</b> (diagonale + milieu).</li>
          <li>Construis <b>e = 1/21 a</b> et <b>1/15 a</b> en <b>grand</b> avec Thalès (sur un segment de ton choix), puis <b>reporte-les</b> au compas : e ne mesure que {vir(A_CARNET * 10 / 21)} mm.</li>
          <li>Place les murs, les ouvertures, l'escalier, le pont (voir les constructions, pages suivantes).</li>
          <li>Pour chaque mesure, note les <b>deux méthodes</b> : le pli et la construction géométrique.</li>
        </ol>
        <ul class="legende">{leg}</ul>
      </div>
      <div class="col">{echelle_notes}</div></div>"""
    return page(texte, "Le carnet", "à imprimer à 100 % · A4 paysage")


def document():
    pages = [page_garde(), page_tableau()] + pages_vues() + pages_constructions()
    css = """@page { size: 297mm 210mm; margin: 0; }
html, body { margin: 0; padding: 0; background: #fff; font-family: "Source Serif 4", Georgia, serif; color: #1c2120; }
.page { width: 297mm; height: 210mm; padding: 8mm 10mm; box-sizing: border-box; overflow: hidden; page-break-after: always; break-after: page; position: relative; }
.page header { display: flex; justify-content: space-between; align-items: baseline; border-bottom: 0.4mm solid #1c2120; padding-bottom: 1.5mm; margin-bottom: 4mm; }
.page header .t { font-family: "Archivo", Arial, sans-serif; font-weight: 800; font-size: 5.2mm; }
.page header .s { font-family: "IBM Plex Mono", monospace; font-size: 2.6mm; color: #555; }
.corps svg { display: block; flex: none; max-width: none; }
.vue { display: flex; justify-content: center; }
.notes { list-style: none; margin: 3mm 0 0; padding: 0; columns: 2; column-gap: 8mm; font-size: 3.05mm; line-height: 1.25; }
.notes li { break-inside: avoid; margin-bottom: 1.3mm; }
.notes li { display: flex; gap: 2mm; align-items: flex-start; }
.notes i, .legende i { width: 3mm; height: 3mm; flex: none; margin-top: 0.7mm; border-radius: 0.5mm; display: inline-block; margin-right: 1.6mm; }
.paire { display: flex; gap: 10mm; justify-content: center; }
.petite .titre { font-family: "Archivo", Arial, sans-serif; font-weight: 700; font-size: 4mm; margin-bottom: 1mm; }
.rangee { display: flex; gap: 7mm; align-items: flex-start; margin-bottom: 5mm; }
.cons { border-top: 1mm solid; padding-top: 1.5mm; box-sizing: border-box; }
.cons h3 { font-family: "Archivo", Arial, sans-serif; font-size: 4.2mm; margin: 0 0 1.5mm; display: flex; gap: 2mm; align-items: baseline; flex-wrap: wrap; }
.cons h3 .n { font-size: 6mm; font-weight: 800; }
.zoomtag { font-family: "IBM Plex Mono", monospace; font-size: 2.4mm; font-weight: 500; color: #555; }
.etapes { list-style: none; margin: 1.5mm 0 0; padding: 0; display: grid; gap: 0.9mm; font-size: 3.2mm; line-height: 1.25; }
.etapes li { display: flex; gap: 1.8mm; align-items: flex-start; }
.num { flex: none; width: 4.2mm; height: 4.2mm; border-radius: 50%; background: #555; color: #fff; font-family: "IBM Plex Mono", monospace; font-size: 2.6mm; font-weight: 700; display: inline-grid; place-items: center; margin-top: 0.2mm; }
.aupli { margin: 1.2mm 0 0; font-family: "IBM Plex Mono", monospace; font-size: 2.5mm; color: #555; }
.garde { display: grid; grid-template-columns: 112mm 1fr; gap: 10mm; font-size: 3.5mm; line-height: 1.35; }
.retenir { margin: 0; padding-left: 5mm; display: grid; gap: 1.6mm; } .deuxcol { display: grid; grid-template-columns: 1fr 1fr; gap: 10mm; } .garde p { margin: 2mm 0; } .garde h4 { font-family: "Archivo", Arial, sans-serif; font-size: 4mm; margin: 3mm 0 1mm; }
.ordre { margin: 0; padding-left: 5mm; display: grid; gap: 1.2mm; }
.legende { list-style: none; margin: 3mm 0 0; padding: 0; display: grid; gap: 1mm; font-family: "IBM Plex Mono", monospace; font-size: 3mm; font-weight: 700; }
.echelle { display: flex; align-items: center; gap: 3mm; }
.echelle > div { text-align: center; display: grid; } .echelle b { font-family: "IBM Plex Mono", monospace; font-size: 5.4mm; }
.echelle span { font-size: 2.6mm; color: #555; } .echelle i { font-style: normal; font-family: "IBM Plex Mono", monospace; color: #555; }
.echelle .cn { border: 0.5mm solid #1f5fd1; border-radius: 1.2mm; padding: 1mm 3mm; } .echelle .cn b { color: #1f5fd1; }
.tab table { border-collapse: collapse; width: 100%; font-size: 2.7mm; line-height: 1.15; }
.tab th { text-align: left; font-family: "IBM Plex Mono", monospace; font-size: 2.2mm; text-transform: uppercase; border-bottom: 0.4mm solid #1c2120; padding: 0.6mm 1.4mm 0.6mm 0; white-space: nowrap; }
.tab td { border-bottom: 0.2mm solid #ccc; padding: 0.35mm 1.4mm 0.35mm 0; vertical-align: top; }
.tab td:nth-child(n+3), .tab th:nth-child(n+3) { text-align: right; white-space: nowrap; }
.tab td.m { font-family: "IBM Plex Mono", monospace; font-size: 2.4mm; white-space: nowrap; }
.tab tr.grp td { font-family: "Archivo", Arial, sans-serif; font-weight: 700; padding-top: 1.6mm; border-bottom: 0.4mm solid #1c2120; }
.tab .note { color: #666; font-size: 2.3mm; } .tab .carnet { font-weight: 700; background: #e8eefb; padding: 0.35mm 1.2mm; }"""
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Azuma House · carnet</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&family=IBM+Plex+Mono:wght@400;500;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<style>{css}</style></head><body>{"".join(pages)}</body></html>"""


if __name__ == "__main__":
    open(os.path.join(ICI, "carnet.html"), "w", encoding="utf-8").write(document())
    print("carnet.html écrit")

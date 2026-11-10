#!/usr/bin/env python3
"""Construit les deux pages HTML du dossier DS :
   - ds_entrainement.html : 3 sujets blancs (vrai/faux + dissertation) puis leurs corrigés ;
   - mini_fiche_ds.html   : la mini fiche de révision (1 page).
Tout le contenu vient des trois cours d'environnement (voir les fiches de révision).
Usage : python3 construire_ds.py   puis   node generer_pdf.js
"""
import html, os

ICI = os.path.dirname(os.path.abspath(__file__))
e = html.escape

# ----------------------------------------------------------------------------------------------
# Les trois sujets : (vrai ?, énoncé, justification donnée au corrigé)
# ----------------------------------------------------------------------------------------------
SUJETS = [
  {
    "titre": "Sujet 1", "theme": "L'homme et l'environnement : les défis et les solutions",
    "vf": [
      (True,  "Au Paléolithique, la population mondiale était de 5 à 10 millions d'individus, des chasseurs-cueilleurs à l'impact limité sur l'environnement.",
              "Cours : Paléolithique = 5 à 10 millions, chasseurs-cueilleurs, impact limité."),
      (False, "Au Néolithique, le passage à l'agriculture et à l'élevage n'a eu aucun effet sur le sol.",
              "Faux : il a conduit à la <b>surexploitation du sol</b> (30 millions d'individus)."),
      (True,  "L'Antiquité (200 millions d'individus) est marquée par une intensification de l'urbanisation aux répercussions environnementales importantes.",
              "Cours : Antiquité = 200 millions, urbanisation intense, répercussions importantes."),
      (False, "L'urbanisation désigne la diminution de la population des villes.",
              "Faux : c'est la <b>concentration de la population dans les villes</b> ; la population urbaine augmente et les villes s'étendent."),
      (True,  "L'exode rural et l'étalement des villes réduisent les espaces naturels et agricoles.",
              "Cours : diminution des espaces naturels et agricoles, des terres arables, effondrement de la biodiversité."),
      (False, "Le nucléaire fait partie des énergies renouvelables.",
              "Faux : il est <b>non renouvelable</b>, car il repose sur l'uranium."),
      (True,  "Le pétrole, le charbon et le gaz représentent environ 80 % de l'énergie utilisée dans le monde.",
              "Cours : notre civilisation thermo-industrielle repose sur eux (80 %)."),
      (False, "L'agriculture intensive a remplacé l'agriculture traditionnelle au XIX<sup>e</sup> siècle.",
              "Faux : au <b>XX<sup>e</sup> siècle</b>, pour un meilleur rendement et la sécurité alimentaire."),
      (True,  "Selon le WWF, l'agriculture est responsable de 80 % de la déforestation mondiale et de 70 % de l'utilisation d'eau douce.",
              "Cours : 80 % de la déforestation, 70 % de l'eau douce, 70 % de la perte de biodiversité terrestre."),
      (False, "Dans le monde, 70 % de l'eau sont utilisés pour l'usage domestique.",
              "Faux : <b>70 % pour l'irrigation</b>, 22 % pour l'industrie, 8 % pour l'usage domestique."),
      (True,  "L'Afrique perd jusqu'à 4 millions d'hectares de forêt chaque année.",
              "Cours : étude FAO et AUDA-NEPAD du 29 septembre 2021."),
      (False, "Le premier Sommet de la Terre, à Rio, a eu lieu en 1997.",
              "Faux : <b>1992</b> (Convention-cadre sur les changements climatiques, Agenda 21). 1997 = protocole de Kyoto."),
      (True,  "Le rapport Brundtland (1987) marque l'apparition du concept de développement durable.",
              "Cours : 1987, rapport Brundtland et concept de développement durable."),
      (True,  "L'Accord de Paris a été adopté par 195 pays pour lutter contre le changement climatique.",
              "Cours : engagement collectif pour limiter le réchauffement mondial."),
      (False, "Plus de la moitié des déchets sont recyclés dans le monde.",
              "Faux : seuls <b>13,5 %</b> des déchets sont recyclés."),
      (False, "La reforestation suffit : il n'est pas nécessaire de protéger les forêts existantes.",
              "Faux : la <b>protection des forêts existantes</b> est tout aussi vitale (gestion durable, engagement collectif)."),
    ],
    "diss": "« L'homme est le premier responsable des changements de l'environnement. » À partir des défis actuels que vous connaissez, expliquez cette affirmation, puis présentez les solutions mises en œuvre.",
    "plan": [
      ("Introduction", "Population passée de 5 à 10 millions (Paléolithique) à 8,3 milliards ; l'homme est le premier responsable des changements, surtout depuis la révolution industrielle et l'expansion démographique. Problématique : quels défis, quelles solutions ?"),
      ("I. Une responsabilité qui s'est accrue avec le temps", "Du Paléolithique (impact limité) au Néolithique (surexploitation du sol), à l'Antiquité (urbanisation), au Moyen âge (500 millions), puis à la révolution industrielle."),
      ("II. Les défis actuels", "Urbanisation (exode rural, perte d'espaces naturels) ; énergie (80 % fossiles, surexploitation) ; agriculture intensive (nitrates, pesticides, 80 % de la déforestation) ; eau (70 % irrigation) ; déforestation (4 M d'ha par an en Afrique) ; pollution."),
      ("III. Les solutions", "Gouvernance mondiale (Stockholm 1972, Brundtland 1987, Rio 1992, Kyoto 1997, Paris 2015) ; parcs nationaux ; énergies renouvelables ; agriculture durable ; recyclage (13,5 % seulement) ; reforestation."),
      ("Conclusion", "Responsabilité humaine mais aussi capacité d'agir : gouvernance de plus en plus proactive, engagement collectif pour les générations futures."),
    ],
  },
  {
    "titre": "Sujet 2", "theme": "La pollution : définitions, causes, effets et formes",
    "vf": [
      (False, "La pollution a toujours une origine humaine.",
              "Faux : elle peut être <b>naturelle</b> (éruption volcanique, tempêtes de sable, feux de forêt), même si elle est principalement liée aux activités humaines."),
      (True,  "Un polluant est une substance, liquide, solide ou gazeuse, présente dans un milieu où elle ne devrait pas se trouver ou en concentration anormalement élevée.",
              "Cours : définition du polluant."),
      (True,  "Une pollution ponctuelle a une source localisée dans l'espace, et les polluants sont rejetés directement dans les milieux.",
              "Cours : pollution ponctuelle = source localisée."),
      (False, "La pollution diffuse provient d'un rejet unique et localisé.",
              "Faux : elle est due à de <b>multiples rejets</b> dans le temps et dans l'espace."),
      (True,  "L'effet de serre est d'abord un phénomène naturel qui maintient une température vitale d'environ 15 °C.",
              "Cours : phénomène naturel grâce aux gaz à effet de serre."),
      (False, "L'effet de serre n'existe que depuis le développement de l'activité humaine.",
              "Faux : il est <b>naturel</b> ; l'activité humaine l'<b>intensifie</b> (domestique, agricole, industrielle)."),
      (True,  "L'urbanisation, la production d'énergie, l'industrie, l'agriculture et le plastique font partie des causes humaines de la pollution.",
              "Cours : « principales causes de la pollution »."),
      (False, "Selon le rapport State of Global Air, la pollution de l'air est à l'origine de 700 000 décès en 2021.",
              "Faux : <b>8,1 millions</b> de décès ; 700 000 concerne les <b>enfants de moins de 5 ans</b>."),
      (True,  "La pollution de l'air est le deuxième facteur de risque de décès des enfants de moins de 5 ans, après la malnutrition.",
              "Cours : source UNICEF."),
      (True,  "Les particules fines (PM10, PM2,5), le SO₂, les NOx, le CO et l'ozone sont des polluants de l'air.",
              "Cours : polluants de la pollution atmosphérique."),
      (True,  "L'eutrophisation, l'acidification des océans et des maladies comme le choléra sont des conséquences de la pollution de l'eau.",
              "Cours : conséquences de la pollution de l'eau."),
      (False, "La pollution de l'eau ne concerne que les cours d'eau.",
              "Faux : aussi les <b>nappes</b>, les eaux saumâtres, l'<b>eau de pluie</b>, la neige et la glace polaire."),
      (True,  "Les polluants du sol (métaux lourds, hydrocarbures, solvants) peuvent entrer dans la chaîne alimentaire par absorption par les plantes.",
              "Cours : pollution des sols."),
      (True,  "Le bruit commence à gêner à partir de 60 décibels et devient un agent de stress.",
              "Cours : gêne psychologique et fonctionnelle."),
      (False, "99 % de la population mondiale vit sous un ciel pollué par la lumière artificielle.",
              "Faux : <b>plus de 80 %</b> pour le monde ; <b>99 %</b> pour la population européenne et nord-américaine (Falchi et al., 2016)."),
      (False, "Environ 60 % des vertébrés sont des animaux nocturnes.",
              "Faux : environ <b>30 % des vertébrés</b> et <b>60 % des invertébrés</b>."),
    ],
    "diss": "Air, eau, sol, bruit, lumière : présentez ces cinq formes de pollution, leurs causes et leurs effets, puis proposez des moyens de lutter contre elles.",
    "plan": [
      ("Introduction", "Définition : dégradation de l'environnement par des substances, des déchets ou des nuisances (Larousse), principalement liée aux activités humaines. Annonce des cinq formes."),
      ("I. Causes et effets généraux", "Causes naturelles (volcans, tempêtes de sable, feux de forêt) et humaines (urbanisation, énergie, industrie, agriculture, plastique). Effets : santé, nature, agriculture, bâti, climat ; gaz à effet de serre (15 °C naturels, intensifiés par l'homme)."),
      ("II. Les cinq formes", "Air (8,1 M de décès en 2021 ; PM2,5, SO₂, NOx, CO, O₃) ; eau (nitrates, pesticides, microplastiques ; choléra, eutrophisation) ; sol (métaux lourds, chaîne alimentaire) ; bruit (gêne dès 60 dB, stress) ; lumière (plus de 80 % sous un ciel pollué, faune nocturne)."),
      ("III. Lutter contre la pollution", "Logements, centrales et industries plus efficaces ; énergie domestique propre ; épuration et réutilisation de l'eau ; insonorisation et isolation phonique des bâtiments ; zones de quiétude pour la faune (parcs)."),
      ("Conclusion", "La pollution touche tous les milieux et s'additionne ; agir sur les causes humaines est possible."),
    ],
  },
  {
    "titre": "Sujet 3", "theme": "Les déchets et le réchauffement climatique",
    "vf": [
      (True,  "Les déchets désignent tous les matériaux, objets ou substances que les individus, les entreprises ou les collectivités jettent ou considèrent comme inutiles.",
              "Cours : définition des déchets."),
      (False, "Le plastique représente la majorité des déchets municipaux.",
              "Faux : seulement <b>12 %</b>, mais sa décomposition est excessivement longue."),
      (True,  "Une bouteille en plastique peut rester entre 100 et 1 000 ans dans l'environnement.",
              "Cours : les déchets organiques, eux, se dégradent en quelques jours ou semaines."),
      (False, "Les ménages sont, de loin, la première source de déchets.",
              "Faux : l'<b>industrie</b> en génère <b>18 fois plus</b>."),
      (True,  "Les déchets organiques se dégradent en quelques jours ou semaines, alors que le plastique met un temps excessivement long.",
              "Cours : c'est ce qui rend le plastique dangereux pour la faune et les océans (microplastiques)."),
      (True,  "Les déchets industriels dangereux (amiante, déchets médicaux) sont particulièrement difficiles à traiter et très toxiques.",
              "Cours : c'est le vrai problème ; les déchets non dangereux peuvent être valorisés."),
      (False, "Les déchets nucléaires ne restent dangereux que quelques dizaines d'années.",
              "Faux : les isotopes radioactifs peuvent rester dangereux pendant des <b>milliers d'années</b>."),
      (True,  "Le stockage géologique profond est une solution à long terme pour les déchets nucléaires.",
              "Cours : après le conditionnement et le stockage temporaire."),
      (True,  "Le fumier, le lisier et les résidus de récolte sont des déchets agricoles qui peuvent être réutilisés, par exemple comme engrais.",
              "Cours : collecte séparée, engrais ou nourriture du bétail."),
      (True,  "Dans le cycle de vie des déchets, les déchets recyclables passent par un centre de traitement avant le centre de valorisation.",
              "Cours : schéma du cycle de vie des déchets."),
      (False, "Dans le cycle de vie des déchets, le centre de tri envoie tous les déchets à la décharge.",
              "Faux : valorisation, <b>décharge ou incinération</b>, ou <b>compostage</b>."),
      (False, "Le réchauffement climatique est une diminution générale des températures moyennes.",
              "Faux : c'est une <b>augmentation</b> générale des températures moyennes."),
      (True,  "Les températures ont augmenté d'environ 1,2 °C entre 1880 et 2020.",
              "Cours : chiffre de la diapo (youmatter)."),
      (False, "Le dioxyde de carbone et le méthane sont présents dans l'atmosphère uniquement à cause de l'activité humaine.",
              "Faux : ils sont <b>naturellement présents</b> et régulent le climat (15 °C en moyenne)."),
      (True,  "Le réchauffement actuel est principalement dû aux activités de l'homme, surtout la production d'énergie à partir des énergies fossiles.",
              "Cours : énergies fossiles et carburants des transports = principale cause."),
      (False, "La déforestation, l'agriculture et l'élevage n'ont aucun lien avec le réchauffement climatique.",
              "Faux : ils <b>contribuent</b> à ce phénomène, comme la gestion des territoires."),
    ],
    "diss": "Les déchets et le réchauffement climatique sont deux conséquences de nos modes de vie. Présentez-les et indiquez comment on peut en limiter les effets.",
    "plan": [
      ("Introduction", "Les déchets sont un problème qui a toujours menacé les sociétés ; le réchauffement climatique est un phénomène global de hausse des températures. Annonce du plan."),
      ("I. Les déchets", "Ménagers (dont le plastique : 12 %, 100 à 1 000 ans), agricoles (fumier, lisier), industriels (18 fois plus ; dangereux vs non dangereux), nucléaires (milliers d'années, stockage géologique profond)."),
      ("II. Le réchauffement climatique", "+ 1,2 °C entre 1880 et 2020 ; gaz à effet de serre (CO₂, méthane, 15 °C naturels) ; causes humaines : énergies fossiles, transports, déforestation, agriculture, élevage ; conséquences : écosystèmes bouleversés, événements climatiques extrêmes."),
      ("III. Agir", "Cycle de vie : collecte, tri, valorisation, compostage, recyclage (seulement 13,5 % dans le monde) ; énergies renouvelables ; reforestation et protection des forêts ; accords internationaux (Kyoto, Paris)."),
      ("Conclusion", "Réduire les déchets et les émissions passe par un engagement collectif, pour les générations futures."),
    ],
  },
]

AUTRES_SUJETS = [
  ("L'urbanisation", "définition (Larousse) → exode rural → étalement des villes → perte d'espaces naturels et de biodiversité → besoin de mobilité ; solution : éco-quartiers (Vauban à Fribourg)."),
  ("L'énergie", "non renouvelables (pétrole, charbon, gaz, nucléaire ; 80 %) et surexploitation → les 5 renouvelables (solaire, éolien, hydraulique, géothermie, biomasse)."),
  ("L'agriculture", "intensive (XXe siècle, pesticides, monoculture, 80 % de la déforestation) → agriculture durable (moins d'engrais, eau de pluie, semences, biodiversité, lutte contre l'érosion)."),
  ("Les forêts", "déforestation (causes, conséquences, 4 M d'ha par an en Afrique) → reforestation et protection des forêts existantes."),
  ("La gouvernance mondiale", "1972 Stockholm, 1987 Brundtland, 1992 Rio, 1997 Kyoto, 2007 Grenelle, 2015 Paris : une prise de conscience de plus en plus proactive."),
  ("L'eau", "70 % irrigation, 22 % industrie, 8 % domestique ; demande croissante ; pollution (nitrates, microplastiques) ; solutions : gestion durable, irrigation économe, purification, sensibilisation."),
]

CSS = """
  @font-face { font-family: "Inter"; font-weight: 400; src: url("../../sources/fonts/inter-latin-400-normal.woff2"); }
  @font-face { font-family: "Inter"; font-weight: 600; src: url("../../sources/fonts/inter-latin-600-normal.woff2"); }
  @font-face { font-family: "Inter"; font-weight: 800; src: url("../../sources/fonts/inter-latin-800-normal.woff2"); }
  @font-face { font-family: "Playfair"; font-weight: 700; src: url("../../sources/fonts/playfair-display-latin-700-normal.woff2"); }
  @font-face { font-family: "Playfair"; font-weight: 400; font-style: italic; src: url("../../sources/fonts/playfair-display-latin-400-italic.woff2"); }
  :root { --encre:#1f2328; --gris:#5f6670; --filet:#dfe3e8; --fond:#f6f7f9; --c1:#2F4858; --c2:#B4501E; --c3:#3C7A3E; --c4:#8C1C13; }
  @page { size: A4; margin: 11mm 12mm 13mm; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  body { font-family: "Inter", sans-serif; font-size: 9pt; line-height: 1.3; color: var(--encre); }
  b { font-weight: 800; } i { font-style: italic; }
  .entete { border-bottom: 2.5px solid var(--encre); padding-bottom: 6px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: flex-end; }
  .kicker { font-weight: 800; font-size: 7.2pt; letter-spacing: .1em; color: var(--gris); }
  h1 { font-family: "Playfair", serif; font-weight: 700; font-size: 21pt; line-height: 1.05; margin-top: 2px; }
  .sous { font-family: "Playfair", serif; font-style: italic; font-size: 10pt; color: var(--gris); text-align: right; max-width: 85mm; line-height: 1.25; }
"""

CSS_DS = CSS + """
  .page { break-after: page; }
  .page:last-child { break-after: auto; }
  .infos { display: flex; gap: 16px; font-size: 8.4pt; margin-bottom: 6px; }
  .infos span { flex: 1; border-bottom: 1px dotted #8a9099; padding-bottom: 1px; color: var(--gris); }
  .consigne { background: var(--fond); border-left: 4px solid var(--c1); padding: 4px 8px; font-size: 8.4pt; margin-bottom: 7px; }
  h2 { font-family: "Playfair", serif; font-weight: 700; font-size: 12.5pt; margin: 5px 0 4px; color: var(--c1); }
  table.vf { width: 100%; border-collapse: collapse; }
  table.vf td { border-bottom: 1px solid var(--filet); padding: 4px 5px; vertical-align: top; font-size: 8.9pt; }
  table.vf td.n { width: 6mm; font-weight: 800; color: var(--c1); }
  table.vf td.c { width: 22mm; text-align: center; white-space: nowrap; font-size: 8.6pt; }
  table.vf td.c span { display: inline-block; width: 3.3mm; height: 3.3mm; border: 1.2px solid var(--encre); border-radius: 1px; vertical-align: -.5mm; margin-right: 1px; }
  table.vf tr:nth-child(even) td { background: #fafbfc; }
  .diss { border: 1.5px solid var(--encre); border-radius: 6px; padding: 6px 9px; margin-top: 8px; }
  .diss .q { font-weight: 800; margin-bottom: 4px; font-size: 9.4pt; }
  .diss .l { height: 15px; border-bottom: 1px dotted #aab0b8; }
  .bareme { font-size: 7.8pt; color: var(--gris); margin-top: 4px; text-align: right; }
  /* corrigés */
  .rep { font-weight: 800; text-align: center; width: 12mm; }
  .rep.v { color: #2e7d32; } .rep.f { color: #c0392b; }
  table.vf td.j { font-size: 8.4pt; }
  .plan { margin-top: 3px; }
  .plan div { border-left: 3px solid var(--c1); padding: 2px 7px; margin-bottom: 3px; font-size: 8.5pt; background: var(--fond); }
  .plan b { color: var(--c1); }
  .autres { display: grid; grid-template-columns: 1fr 1fr; gap: 4px 10px; font-size: 8.3pt; margin-top: 3px; }
  .autres div { border-bottom: 1px solid var(--filet); padding-bottom: 2px; }
  .conseils { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; margin: 6px 0; }
  .conseils div { border: 1px solid var(--filet); border-top: 3px solid var(--c3); border-radius: 5px; padding: 4px 7px; font-size: 8.4pt; }
  .conseils b { display: block; color: var(--c3); margin-bottom: 1px; }
"""

def page_sujet(i, s):
    lignes = []
    for n, (vrai, txt, _) in enumerate(s["vf"], 1):
        lignes.append(f'<tr><td class="n">{n}</td><td>{txt}</td><td class="c"><span></span> Vrai &nbsp;<span></span> Faux</td></tr>')
    ls = "".join('<div class="l"></div>' for _ in range(8))
    return f'''
<div class="page">
  <div class="entete">
    <div><div class="kicker">ENVIRONNEMENT · DS BLANC · ESAD TUNIS</div><h1>{e(s["titre"])}</h1></div>
    <div class="sous">{e(s["theme"])}</div>
  </div>
  <div class="infos"><span>Nom :</span><span>Date :</span><span>Note : &nbsp;&nbsp;&nbsp;/ 20</span></div>
  <div class="consigne"><b>Consigne :</b> pour chaque affirmation, cochez <b>Vrai</b> ou <b>Faux</b>. Si c'est faux, corrigez-la dans la marge. Puis traitez la dissertation (introduction, développement en 3 parties, conclusion).</div>
  <h2>Partie 1 · Vrai ou faux <span style="font:600 8.5pt Inter,sans-serif;color:var(--gris)">(16 affirmations · 12 points)</span></h2>
  <table class="vf">{"".join(lignes)}</table>
  <div class="diss">
    <div class="q">Partie 2 · Dissertation <span style="font-weight:600;font-size:8.3pt;color:var(--gris)">(8 points)</span><br>{e(s["diss"])}</div>
    {ls}
  </div>
  <div class="bareme">Barème indicatif : 0,75 point par affirmation exacte (avec correction si fausse) · 8 points la dissertation.</div>
</div>'''

def page_corrige(i, s):
    lignes = []
    for n, (vrai, _, just) in enumerate(s["vf"], 1):
        lignes.append(f'<tr><td class="n">{n}</td><td class="rep {"v" if vrai else "f"}">{"VRAI" if vrai else "FAUX"}</td><td class="j">{just}</td></tr>')
    plan = "".join(f'<div><b>{e(t)}</b> : {e(c)}</div>' for t, c in s["plan"])
    return f'''
<div class="page">
  <div class="entete">
    <div><div class="kicker">ENVIRONNEMENT · DS BLANC · CORRIGÉ</div><h1>Corrigé · {e(s["titre"])}</h1></div>
    <div class="sous">{e(s["theme"])}</div>
  </div>
  <h2>Partie 1 · Vrai ou faux</h2>
  <table class="vf">{"".join(lignes)}</table>
  <h2>Partie 2 · Plan de dissertation proposé</h2>
  <div class="plan">{plan}</div>
</div>'''

def page_conseils_autres():
    autres = "".join(f'<div><b>{e(t)}</b> : {e(c)}</div>' for t, c in AUTRES_SUJETS)
    return f'''
<div class="page">
  <div class="entete">
    <div><div class="kicker">ENVIRONNEMENT · DS BLANC</div><h1>Méthode et autres sujets</h1></div>
    <div class="sous">Pour bien réussir le vrai ou faux et la dissertation</div>
  </div>
  <h2>Réussir le vrai ou faux</h2>
  <div class="conseils">
    <div><b>1 · Cherchez le chiffre piège</b>Souvent une seule valeur est changée : 1992 / 1997, XX<sup>e</sup> / XIX<sup>e</sup>, 30 % / 60 %, 8,1 M / 700 000, 80 % / 99 %.</div>
    <div><b>2 · Méfiez-vous de « toujours », « aucun », « uniquement »</b>Ces mots rendent souvent l'affirmation fausse (la pollution peut être naturelle ; l'effet de serre est naturel).</div>
    <div><b>3 · Corrigez si c'est faux</b>Écrivez la bonne information : c'est souvent ce qui rapporte les points.</div>
  </div>
  <h2>Réussir la dissertation</h2>
  <div class="conseils">
    <div><b>Introduction</b>Une phrase d'accroche, la définition du sujet, la problématique, l'annonce du plan.</div>
    <div><b>Développement</b>3 parties avec des titres clairs, une idée par paragraphe, chaque idée appuyée par un fait ou un chiffre du cours.</div>
    <div><b>Conclusion</b>Répondre à la problématique en 2 ou 3 phrases, puis ouvrir (générations futures, engagement collectif).</div>
  </div>
  <h2>Autres sujets de dissertation possibles</h2>
  <div class="autres">{autres}</div>
  <h2>Les sujets blancs de ce dossier</h2>
  <div class="autres">
    <div><b>Sujet 1</b> : l'homme, les défis, les solutions (cours 1)</div>
    <div><b>Sujet 2</b> : la pollution et ses cinq formes (cours 2)</div>
    <div><b>Sujet 3</b> : les déchets et le réchauffement climatique (cours 3)</div>
    <div><b>Conseil</b> : faites chaque sujet en 45 minutes sans les fiches, puis corrigez avec le corrigé.</div>
  </div>
</div>'''

def construire_ds():
    sujets = "".join(page_sujet(i, s) for i, s in enumerate(SUJETS, 1))
    corriges = "".join(page_corrige(i, s) for i, s in enumerate(SUJETS, 1))
    doc = f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Environnement · DS blanc</title><style>{CSS_DS}</style></head><body>{sujets}{corriges}{page_conseils_autres()}</body></html>'
    open(os.path.join(ICI, "ds_entrainement.html"), "w", encoding="utf-8").write(doc)

# ----------------------------------------------------------------------------------------------
# Mini fiche (1 page)
# ----------------------------------------------------------------------------------------------
CSS_MINI = CSS + """
  body { font-size: 8.3pt; line-height: 1.27; }
  h1 { font-size: 19pt; }
  .entete { margin-bottom: 6px; padding-bottom: 5px; }
  h2 { font-family: "Playfair", serif; font-weight: 700; font-size: 11pt; margin: 0 0 3px; }
  .g { display: grid; gap: 6px; margin-bottom: 6px; }
  .g2 { grid-template-columns: 1fr 1fr; } .g3 { grid-template-columns: 1fr 1fr 1fr; }
  .bloc { border: 1px solid var(--filet); border-top: 3px solid var(--acc, var(--c1)); border-radius: 6px; padding: 3px 7px 4px; }
  .bloc h2 { color: var(--acc, var(--c1)); }
  .a { --acc: var(--c1); } .b { --acc: var(--c2); } .c { --acc: var(--c3); } .d { --acc: var(--c4); }
  ul { list-style: none; } li { padding-left: 9px; position: relative; margin-bottom: .6px; }
  li::before { content: ""; position: absolute; left: 1px; top: .55em; width: 3.5px; height: 3.5px; border-radius: 50%; background: currentColor; opacity: .5; }
  table { width: 100%; border-collapse: collapse; }
  td { padding: 1px 4px; border-bottom: 1px solid var(--filet); vertical-align: top; font-size: 8.1pt; }
  td:first-child { font-weight: 800; white-space: nowrap; color: var(--acc, var(--c1)); width: 1%; }
  tr:nth-child(even) td { background: #fafbfc; }
  .piege { background: #fdf0ee; border: 1px solid #efc3bd; border-radius: 6px; padding: 3px 8px; }
  .piege h2 { color: #c0392b; }
  .piege .cols { columns: 2; column-gap: 14px; }
  .piege li { break-inside: avoid; }
"""

def construire_mini():
    doc = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Environnement · mini fiche DS</title><style>{CSS_MINI}</style></head><body>
<div class="entete">
  <div><div class="kicker">ENVIRONNEMENT · 1RE ANNÉE ARCHITECTURE · ESAD TUNIS</div><h1>Mini fiche pour le DS</h1></div>
  <div class="sous">Tout l'essentiel des 3 cours en 1 page : dates, chiffres, listes et pièges du vrai ou faux</div>
</div>

<div class="g g2">
  <div class="bloc a"><h2>Dates à connaître</h2>
    <table>
      <tr><td>1972</td><td>Stockholm : Conférence de l'ONU sur l'Environnement Humain (CNUEH), coopération internationale</td></tr>
      <tr><td>1987</td><td>Rapport Brundtland : concept de développement durable</td></tr>
      <tr><td>1992</td><td>Rio, 1<sup>er</sup> Sommet de la Terre : Convention-cadre sur les changements climatiques, Agenda 21</td></tr>
      <tr><td>1997</td><td>Protocole de Kyoto : limiter les gaz à effet de serre</td></tr>
      <tr><td>2007</td><td>Grenelle de l'environnement (France)</td></tr>
      <tr><td>2015</td><td>Accord de Paris : 195 pays</td></tr>
    </table>
  </div>
  <div class="bloc b"><h2>Population et histoire</h2>
    <table>
      <tr><td>Paléolithique</td><td>5 à 10 M · chasseurs-cueilleurs · impact limité</td></tr>
      <tr><td>Néolithique</td><td>30 M · agriculture, élevage · surexploitation du sol</td></tr>
      <tr><td>Antiquité</td><td>200 M · urbanisation intense</td></tr>
      <tr><td>Moyen âge</td><td>500 M · rotation des cultures</td></tr>
      <tr><td>Aujourd'hui</td><td>8,3 milliards (9 à 9,7 milliards en 2050)</td></tr>
    </table>
    <div style="margin-top:2px">L'<b>homme</b> est le <b>premier responsable</b> des changements, surtout depuis la <b>révolution industrielle</b>.</div>
  </div>
</div>

<div class="bloc d" style="margin-bottom:6px"><h2>Chiffres clés</h2>
  <table style="columns:1">
    <tr><td>80 %</td><td>de l'énergie mondiale = pétrole, charbon, gaz</td><td style="white-space:nowrap">70 / 22 / 8 %</td><td>eau : irrigation / industrie / domestique</td></tr>
    <tr><td>80 · 70 · 70 %</td><td>agriculture (WWF) : déforestation / eau douce / perte de biodiversité</td><td>4 M d'ha</td><td>forêt perdue par an en Afrique</td></tr>
    <tr><td>13,5 %</td><td>des déchets recyclés dans le monde</td><td>12 %</td><td>plastique dans les déchets municipaux (100 à 1 000 ans)</td></tr>
    <tr><td>× 18 · 12,7 kg</td><td>industrie : 18 fois plus de déchets que les ménages, 12,7 kg/jour/habitant</td><td>+ 1,2 °C</td><td>réchauffement entre 1880 et 2020 (≈ 15 °C naturels)</td></tr>
    <tr><td>8,1 M</td><td>décès liés à l'air en 2021 (700 000 enfants de moins de 5 ans)</td><td>60 dB</td><td>début de la gêne due au bruit</td></tr>
    <tr><td>&gt; 80 % · 99 %</td><td>ciel pollué par la lumière : monde / Europe et Amérique du Nord</td><td>30 · 60 %</td><td>vertébrés · invertébrés nocturnes</td></tr>
  </table>
</div>

<div class="g g3">
  <div class="bloc a"><h2>6 défis</h2>
    <ul><li>Urbanisation (exode rural, étalement)</li><li>Énergie (80 % fossiles)</li><li>Agriculture intensive (pesticides, monoculture)</li><li>Eau (demande croissante)</li><li>Déforestation</li><li>Pollution</li></ul>
  </div>
  <div class="bloc c"><h2>6 solutions</h2>
    <ul><li>Prise de conscience internationale</li><li>Parcs nationaux et réserves</li><li>Énergies renouvelables : solaire, éolien, hydraulique, géothermie, biomasse</li><li>Agriculture durable</li><li>Recyclage</li><li>Reforestation et protection des forêts</li></ul>
  </div>
  <div class="bloc b"><h2>5 formes de pollution</h2>
    <ul><li><b>Air</b> : PM10, PM2,5, SO₂, NOx, CO, O₃ ; maladies respiratoires, smog</li><li><b>Eau</b> : nitrates, pesticides, microplastiques ; choléra, eutrophisation</li><li><b>Sol</b> : métaux lourds, hydrocarbures ; chaîne alimentaire</li><li><b>Bruit</b> : gêne, stress, moins de biodiversité urbaine</li><li><b>Lumière</b> : ciel étoilé, faune nocturne, énergie gaspillée</li></ul>
  </div>
</div>

<div class="g g3">
  <div class="bloc d"><h2>Définitions</h2>
    <ul><li><b>Pollution</b> : dégradation du milieu par des substances, déchets ou nuisances ; surtout humaine, parfois naturelle</li><li><b>Polluant</b> : substance là où elle ne devrait pas être, ou en excès</li><li><b>Ponctuelle</b> : source localisée · <b>Diffuse</b> : multiples rejets</li><li><b>Déchets</b> : ce qu'on jette ou juge inutile</li></ul>
  </div>
  <div class="bloc a"><h2>4 types de déchets</h2>
    <ul><li><b>Ménagers</b> (plastique)</li><li><b>Agricoles</b> : fumier, lisier, résidus</li><li><b>Industriels</b> : dangereux (amiante, médicaux) ou non</li><li><b>Nucléaires</b> : milliers d'années ; stockage géologique profond</li></ul>
    <div>Cycle : création → collecte → tri → valorisation / décharge-incinération / compostage.</div>
  </div>
  <div class="bloc c"><h2>Réchauffement</h2>
    <ul><li>Hausse générale des températures moyennes</li><li>Gaz à effet de serre : CO₂, méthane (barrière qui garde ≈ 15 °C)</li><li>Causes : énergies fossiles, transports, déforestation, agriculture, élevage</li><li>Effets : écosystèmes bouleversés, événements extrêmes</li></ul>
  </div>
</div>

<div class="piege"><h2>Pièges du vrai ou faux</h2>
  <ul class="cols">
    <li>Rio = <b>1992</b>, Kyoto = <b>1997</b>, Paris = <b>2015</b>.</li>
    <li>Agriculture intensive : <b>XX<sup>e</sup></b> siècle.</li>
    <li>Le nucléaire est <b>non renouvelable</b> (uranium).</li>
    <li>Eau : <b>70 %</b> = irrigation, pas domestique (8 %).</li>
    <li>Recyclage : <b>13,5 %</b> seulement.</li>
    <li>Pollution : <b>pas toujours humaine</b> (volcan).</li>
    <li>Effet de serre : <b>naturel</b>, l'homme l'intensifie.</li>
    <li>Air 2021 : <b>8,1 M</b> de décès ; 700 000 = enfants.</li>
    <li>Enfants : <b>2<sup>e</sup></b> facteur de risque, après la malnutrition.</li>
    <li>Lumière : <b>80 %</b> monde, <b>99 %</b> Europe et Amérique du Nord.</li>
    <li>Nocturnes : <b>30 %</b> vertébrés, <b>60 %</b> invertébrés.</li>
    <li>Industrie : <b>18 fois plus</b> que les ménages.</li>
  </ul>
</div>
</body></html>'''
    open(os.path.join(ICI, "mini_fiche_ds.html"), "w", encoding="utf-8").write(doc)

if __name__ == "__main__":
    construire_ds()
    construire_mini()
    print("OK : ds_entrainement.html et mini_fiche_ds.html")

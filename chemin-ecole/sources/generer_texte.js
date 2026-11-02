// Genere le Word « texte a dire » a partir de notes.js.
// Usage : node generer_texte.js  ->  ../Chemin_de_l_ecole_texte_a_dire.docx
const fs = require("fs");
const path = require("path");
const { Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat, BorderStyle, LineRuleType, Footer, PageNumber, TabStopType } = require("docx");
const NOTES = require("./notes.js");

const SANS = "Arial", SERIF = "Times New Roman", VERT = "1B3A3F", OR = "C2562F", GRIS = "666666";
const cm = (v) => Math.round(v * 567);
const NBSP = " ";
const fr = (s) => s.replace(/ ([:;!?»%])/g, NBSP + "$1").replace(/« /g, "«" + NBSP);
const run = (t, o = {}) => new TextRun({ text: fr(t), ...o });
const LARGEUR = 11906 - 2 * cm(2.2);
const titres = ["Diapo 1 · Titre", "Diapo 2 · Notre problématique", "Diapo 3 · Circulation ou socialisation ?", "Diapo 4 · Un espace de socialisation", "Diapo 5 · Aventure, apprentissage, épanouissement", "Diapo 6 · Françoise Dolto", "Diapo 7 · L'enfant-paquet", "Diapo 8 · Pourquoi, et avec quelles conséquences ?", "Diapo 9 · Enfant-paquet ou enfant acteur ?", "Diapo 10 · Et l'architecte dans tout ça ?", "Diapo 11 · Conclusion"];
const QR = [
  ["C'est quoi un « enfant-paquet » ?", "C'est l'expression utilisée dans notre sujet : un enfant que l'on transporte, souvent en voiture, et que l'on dépose devant l'école, sans qu'il vive quoi que ce soit en chemin. Il est passif, comme un colis."],
  ["Pourquoi Dolto ?", "Parce que Françoise Dolto (1908-1988), pédiatre et psychanalyste, insiste sur l'autonomie de l'enfant, qui se détache peu à peu de l'adulte, avec confiance et respect. Elle a aussi fondé la Maison Verte (Paris, 1979), un lieu de socialisation des tout-petits avant l'école. Le lien avec le chemin de l'école est notre lecture, pas une phrase de Dolto sur le trajet. (Si ta prof t'a donné un texte précis de Dolto, ajoute-le ici : ______________________)"],
  ["Les parents ont-ils tort d'accompagner leurs enfants ?", "Non. Leur peur de la circulation est compréhensible, et leurs horaires de travail comptent aussi. Le problème n'est pas d'accompagner, c'est de ne jamais laisser l'enfant vivre le chemin. D'où l'idée d'un gradient : voiture, marche avec un parent, pédibus, puis autonomie."],
  ["À quel âge un enfant peut-il aller seul à l'école ?", "Il n'y a pas d'âge unique : cela dépend de l'enfant, de la distance et de la sécurité de la rue. L'important est d'y aller progressivement, avec un chemin sûr (trottoirs, traversées)."],
  ["Qu'est-ce que le pédibus ?", "Un groupe d'enfants qui vont à l'école à pied, accompagnés d'adultes, comme un bus sans moteur. Les enfants se retrouvent, discutent et apprennent le chemin ensemble."],
  ["Que peut faire l'architecte ?", "Il ne contrôle pas les horaires des parents, mais il peut rendre le chemin plus sûr et plus agréable : trottoirs continus, traversées sûres, abords d'école piétons, arbres pour l'ombre, bancs et petites places, commerces et fenêtres qui donnent sur la rue (les « yeux sur la rue » de Jane Jacobs)."],
  ["Et chez nous, en Tunisie ?", "À préparer toi-même : pense à ton propre chemin de l'école (ou à celui de tes frères et sœurs) : qui t'accompagnait, ce que tu y voyais, les boutiques, la chaleur, la circulation. Écris ton exemple ici : ____________________________________"],
  ["Pourquoi l'étude de Hillman est-elle anglaise ?", "C'est une étude célèbre sur l'autonomie des enfants : elle a comparé 1971 et 1990 dans des écoles anglaises (80 % puis 9 % des enfants de 7-8 ans allaient à l'école sans adulte). Je ne dis pas que c'est pareil chez nous, c'est un exemple pour montrer une tendance."],
];
const enfants = [
  new Paragraph({ spacing: { after: 40 }, children: [run("SOCIOLOGIE · 1RE ANNÉE ARCHITECTURE · ESAD TUNIS", { font: SANS, size: 16, bold: true, color: GRIS, characterSpacing: 30 })] }),
  new Paragraph({ spacing: { after: 60 }, children: [run("Texte à dire : le chemin de l'école", { font: SANS, size: 32, bold: true, color: VERT })] }),
  new Paragraph({ spacing: { after: 160 }, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: OR, space: 4 } }, children: [run("Durée totale : environ 13 minutes. Lis le texte à voix haute deux ou trois fois, puis parle avec tes propres mots. Les passages entre crochets sont à personnaliser.", { font: SERIF, size: 22, italics: true, color: GRIS })] }),
];
NOTES.forEach((n, i) => {
  enfants.push(new Paragraph({ keepNext: true, spacing: { before: 200, after: 60 }, tabStops: [{ type: TabStopType.RIGHT, position: LARGEUR }], children: [run(titres[i], { font: SANS, size: 24, bold: true, color: VERT }), run("\t" + n.minutes, { font: SANS, size: 20, bold: true, color: OR })] }));
  enfants.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 70, line: 300, lineRule: LineRuleType.AUTO }, children: [run(n.texte, { font: SERIF, size: 24 })] }));
  enfants.push(new Paragraph({ spacing: { after: 40 }, indent: { left: cm(0.4) }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: OR, space: 8 } }, children: [run("Conseil : ", { font: SANS, size: 20, bold: true, color: OR }), run(n.conseil, { font: SANS, size: 20, color: GRIS })] }));
});
enfants.push(new Paragraph({ keepNext: true, pageBreakBefore: true, spacing: { after: 100 }, children: [run("Questions possibles de la prof (et réponses)", { font: SANS, size: 28, bold: true, color: VERT })] }));
QR.forEach(([q, r]) => {
  enfants.push(new Paragraph({ keepNext: true, spacing: { before: 140, after: 30 }, children: [run(q, { font: SANS, size: 22, bold: true, color: VERT })] }));
  enfants.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 40, line: 280, lineRule: LineRuleType.AUTO }, children: [run(r, { font: SERIF, size: 23 })] }));
});
enfants.push(new Paragraph({ keepNext: true, spacing: { before: 260, after: 60 }, children: [run("Sources", { font: SANS, size: 24, bold: true, color: VERT })] }));
[
  "HILLMAN Mayer, ADAMS John et WHITELEGG John, One False Move: a study of children's independent mobility, Policy Studies Institute, Londres, 1990.",
  "BRAMI Élisabeth, L'Éducation selon Dolto : ce qu'elle a vraiment dit pour aider les parents, Albin Michel.",
  "Bibliothèque nationale de France, notice Françoise Dolto (fondation de la Maison Verte, Paris, 1979).",
  "TONUCCI Francesco, La città dei bambini (projet « La ville des enfants », Fano, Italie, 1991).",
  "JACOBS Jane, The Death and Life of Great American Cities, 1961 (« les yeux sur la rue »).",
  "Cours de sociologie : les cadres sociaux (famille, école, espaces publics) et Goffman (inattention civile).",
].forEach((t) => enfants.push(new Paragraph({ spacing: { after: 30 }, numbering: { reference: "refs", level: 0 }, children: [run(t, { font: SERIF, size: 21 })] })));

const doc = new Document({
  title: "Texte à dire : le chemin de l'école",
  styles: { default: { document: { run: { font: SERIF, size: 24 } } } },
  numbering: { config: [{ reference: "refs", levels: [{ level: 0, format: LevelFormat.BULLET, text: "▪", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: cm(0.6), hanging: cm(0.4) } }, run: { color: OR } } }] }] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: cm(1.8), bottom: cm(1.7), left: cm(2.2), right: cm(2.2), footer: cm(0.8) } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: SANS, size: 16, color: GRIS }), new TextRun({ text: " / ", font: SANS, size: 16, color: GRIS }), new TextRun({ children: [PageNumber.TOTAL_PAGES], font: SANS, size: 16, color: GRIS })] })] }) },
    children: enfants,
  }],
});
Packer.toBuffer(doc).then((b) => { const out = path.join(__dirname, "..", "Chemin_de_l_ecole_texte_a_dire.docx"); fs.writeFileSync(out, b); console.log("OK ->", out); });

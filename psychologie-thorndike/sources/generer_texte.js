// Genere le Word « texte a dire » (script de l'oral) a partir de notes.js.
// Usage : node generer_texte.js  ->  ../Thorndike_texte_a_dire.docx
const fs = require("fs");
const path = require("path");
const { Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat, BorderStyle, LineRuleType, Footer, PageNumber, TabStopType } = require("docx");
const NOTES = require("./notes.js");

const SANS = "Arial", SERIF = "Times New Roman", BLEU = "1F3A68", OR = "B7791F", GRIS = "666666";
const cm = (v) => Math.round(v * 567);
const NBSP = " ";
const fr = (s) => s.replace(/ ([:;!?»])/g, NBSP + "$1").replace(/« /g, "«" + NBSP);
const run = (t, o = {}) => new TextRun({ text: fr(t), ...o });
const LARGEUR = 11906 - 2 * cm(2.2);

const titres = ["Diapo 1 · Titre", "Diapo 2 · Au programme", "Diapo 3 · Qui est Thorndike ?", "Diapo 4 · La loi de l'effet", "Diapo 5 · 1920 : la découverte", "Diapo 6 · Définition", "Diapo 7 · L'exemple : Nisbett et Wilson, 1977", "Diapo 8 · Résultats", "Diapo 9 · Dans la vie et en architecture", "Diapo 10 · Ce qu'il faut retenir"];

const QR = [
  ["Pourquoi dit-on « effet de halo » ?", "Le halo, c'est l'auréole des saints dans les tableaux : une lumière autour de la tête qui fait paraître la personne parfaite. De la même façon, un trait positif « éclaire » tous les autres traits."],
  ["Comment Thorndike a-t-il découvert cet effet ?", "En 1920, il a regardé des évaluations faites dans l'armée américaine. Il a remarqué que les notes données à une même personne pour des qualités différentes (physique, intelligence, leadership…) étaient trop proches les unes des autres. Pour lui, ce n'était pas réaliste : les juges se laissaient guider par une impression générale."],
  ["C'est la même chose qu'un stéréotype ?", "Ce n'est pas exactement pareil, mais c'est proche. Un stéréotype est une croyance sur un groupe de personnes. L'effet de halo est un biais de jugement : un seul trait d'une personne influence le jugement sur ses autres traits."],
  ["L'effet de halo est-il toujours négatif ?", "Il peut être positif (une personne agréable paraît plus compétente) ou négatif (un défaut visible fait juger le reste plus sévèrement). Dans les deux cas, c'est un biais, parce que le jugement n'est plus juste."],
  ["Les étudiants savaient-ils qu'ils étaient influencés ?", "Non. C'est un des résultats les plus importants de l'expérience de 1977 : ils pensaient que c'était l'accent du professeur qui les irritait, alors que c'était l'impression de froideur. L'effet de halo est inconscient."],
  ["Quel lien avec le cours de sociologie ?", "On a vu que le comportement dépend de la perception et de l'apprentissage. Thorndike montre que notre jugement sur les autres est influencé par des impressions. On peut aussi faire le lien avec Goffman : l'apparence et la manière (la « façade ») créent l'impression qui donne le halo."],
  ["Un exemple tiré de ta vie ?", "À préparer toi-même : pense à un professeur, un camarade ou un acteur que tu as trouvé « compétent » parce qu'il était sympathique ou bien habillé, avant de le connaître vraiment. Écris ton exemple ici : ________________________________"],
];

const enfants = [
  new Paragraph({ spacing: { after: 40 }, children: [run("PSYCHOLOGIE · 1RE ANNÉE ARCHITECTURE · ESAD TUNIS", { font: SANS, size: 16, bold: true, color: GRIS, characterSpacing: 30 })] }),
  new Paragraph({ spacing: { after: 60 }, children: [run("Texte à dire pour la présentation : l'effet de halo", { font: SANS, size: 32, bold: true, color: BLEU })] }),
  new Paragraph({ spacing: { after: 160 }, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: OR, space: 4 } },
    children: [run("Durée totale : environ 11 minutes. Lis le texte à voix haute deux ou trois fois, puis parle avec tes propres mots : la prof préfère que tu ne lises pas.", { font: SERIF, size: 22, italics: true, color: GRIS })] }),
];
NOTES.forEach((n, i) => {
  enfants.push(new Paragraph({ keepNext: true, spacing: { before: 200, after: 60 }, tabStops: [{ type: TabStopType.RIGHT, position: LARGEUR }],
    children: [run(titres[i], { font: SANS, size: 24, bold: true, color: BLEU }), run("\t" + n.minutes, { font: SANS, size: 20, bold: true, color: OR })] }));
  enfants.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 70, line: 300, lineRule: LineRuleType.AUTO }, children: [run(n.texte, { font: SERIF, size: 24 })] }));
  enfants.push(new Paragraph({ spacing: { after: 40 }, indent: { left: cm(0.4) }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: OR, space: 8 } },
    children: [run("Conseil : ", { font: SANS, size: 20, bold: true, color: OR }), run(n.conseil, { font: SANS, size: 20, color: GRIS })] }));
});
enfants.push(new Paragraph({ keepNext: true, pageBreakBefore: true, spacing: { after: 100 }, children: [run("Questions possibles de la prof (et réponses)", { font: SANS, size: 28, bold: true, color: BLEU })] }));
QR.forEach(([q, r]) => {
  enfants.push(new Paragraph({ keepNext: true, spacing: { before: 140, after: 30 }, children: [run(q, { font: SANS, size: 22, bold: true, color: BLEU })] }));
  enfants.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 40, line: 280, lineRule: LineRuleType.AUTO }, children: [run(r, { font: SERIF, size: 23 })] }));
});
enfants.push(new Paragraph({ keepNext: true, spacing: { before: 260, after: 60 }, children: [run("Sources", { font: SANS, size: 24, bold: true, color: BLEU })] }));
[
  "THORNDIKE Edward L., « A Constant Error in Psychological Ratings », Journal of Applied Psychology, 4(1), 1920, p. 25-29.",
  "NISBETT Richard E. et WILSON Timothy D., « The Halo Effect: Evidence for Unconscious Alteration of Judgments », Journal of Personality and Social Psychology, 35(4), 1977, p. 250-256.",
  "DION Karen, BERSCHEID Ellen et WALSTER Elaine, « What is beautiful is good », Journal of Personality and Social Psychology, 24, 1972, p. 285-290.",
  "THORNDIKE Edward L., Animal Intelligence, thèse, Columbia University, 1898.",
].forEach((t) => enfants.push(new Paragraph({ spacing: { after: 30 }, numbering: { reference: "refs", level: 0 }, children: [run(t, { font: SERIF, size: 21 })] })));

const doc = new Document({
  title: "Texte à dire : l'effet de halo (Thorndike)",
  styles: { default: { document: { run: { font: SERIF, size: 24 } } } },
  numbering: { config: [{ reference: "refs", levels: [{ level: 0, format: LevelFormat.BULLET, text: "▪", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: cm(0.6), hanging: cm(0.4) } }, run: { color: OR } } }] }] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: cm(1.8), bottom: cm(1.7), left: cm(2.2), right: cm(2.2), footer: cm(0.8) } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: SANS, size: 16, color: GRIS }), new TextRun({ text: " / ", font: SANS, size: 16, color: GRIS }), new TextRun({ children: [PageNumber.TOTAL_PAGES], font: SANS, size: 16, color: GRIS })] })] }) },
    children: enfants,
  }],
});
Packer.toBuffer(doc).then((b) => { const out = path.join(__dirname, "..", "Thorndike_texte_a_dire.docx"); fs.writeFileSync(out, b); console.log("OK ->", out); });

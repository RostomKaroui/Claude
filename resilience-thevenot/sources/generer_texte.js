// Genere le Word « texte a dire » a partir de notes.js.
// Usage : node generer_texte.js  ->  ../Resilience_Thevenot_texte_a_dire.docx
const fs = require("fs");
const path = require("path");
const { Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat, BorderStyle, LineRuleType, Footer, PageNumber, TabStopType } = require("docx");
const NOTES = require("./notes.js");

const SANS = "Arial", SERIF = "Times New Roman", VERT = "24303F", OR = "C47F1A", GRIS = "666666";
const cm = (v) => Math.round(v * 567);
const NBSP = " ";
const fr = (s) => s.replace(/ ([:;!?»%])/g, NBSP + "$1").replace(/« /g, "«" + NBSP);
const run = (t, o = {}) => new TextRun({ text: fr(t), ...o });
const LARGEUR = 11906 - 2 * cm(2.2);
const QR = [
  ["Qu'est-ce que la résilience, en une phrase ?", "C'est la capacité de se reconstruire et de continuer à se développer après une épreuve. Le mot vient de la physique (un matériau qui reprend sa forme après un choc) et a été popularisé en France par Boris Cyrulnik."],
  ["Être résilient, est-ce ne plus souffrir ou oublier ?", "Non. La personne résiliente souffre, elle garde une cicatrice, et elle n'est pas « comme avant » : elle est transformée. Ce qui change, c'est qu'elle continue à vivre et à se construire."],
  ["Tout le monde peut-il être résilient ?", "Les recherches (par exemple l'étude de Kauai) montrent que la résilience n'est pas un don réservé à quelques-uns : elle dépend beaucoup de l'entourage et de ce qui est disponible autour de la personne. Mais cela ne veut pas dire que c'est facile : certaines épreuves demandent une aide professionnelle."],
  ["Quel est le lien exact entre Thévenot et la résilience ?", "Je dois être honnête : à ma connaissance, Thévenot ne parle pas de résilience au sens de Cyrulnik. Le rapprochement est ma lecture : si la vie comporte aussi de l'aise (familiarité), des projets (plan) et de la reconnaissance (justification), ces trois façons d'être engagé sont des ressources pour se relever. (Si ta prof t'a donné un texte précis de Thévenot, ajoute ici la phrase exacte : ______________________)"],
  ["C'est quoi un « régime d'engagement » ?", "C'est une manière d'être engagé dans une situation. Chez Thévenot, il y en a plusieurs : la familiarité (l'aise des habitudes et des proches), le plan (agir pour réaliser un projet) et la justification (rendre des comptes, être reconnu publiquement). On passe de l'un à l'autre au cours d'une même journée."],
  ["Qu'est-ce qu'un tuteur de résilience ?", "Une notion de Boris Cyrulnik : une personne, un lieu ou une activité (l'art, l'écriture, le sport) autour desquels on se reconstruit, comme un jeune arbre s'appuie sur un tuteur pour pousser droit."],
  ["Pourquoi l'étude de Kauai ?", "Parce que c'est l'une des recherches les plus citées sur la résilience : 698 enfants nés en 1955 à Kauai (Hawaï), suivis pendant des décennies. Environ un tiers des enfants à haut risque sont devenus des adultes équilibrés, grâce notamment à un adulte attentionné et au soutien de leur entourage."],
  ["Quand faut-il demander de l'aide à un professionnel ?", "Quand la détresse dure, empêche de dormir, de manger, d'étudier ou de voir les autres, ou quand on a des idées noires. Demander de l'aide n'est pas un signe de faiblesse : c'est une façon de se relever."],
  ["Avez-vous un exemple personnel ou concret ?", "À préparer toi-même : pense à une épreuve que tu as traversée (un échec, un déménagement, un deuil dans la famille) et à ce qui t'a aidé : une personne, un lieu, une habitude. Écris ton exemple ici : ____________________________________ (inutile de dire des choses trop intimes : tu peux choisir un exemple léger ou parler d'une personne que tu as observée)."],
  ["Quel rapport avec l'architecture ?", "Si un lieu peut être un tuteur de résilience, alors l'espace compte : repères familiers pour retrouver l'aise, lieux pour se retrouver, lumière et nature, coins calmes pour se retirer. C'est une idée personnelle, pas une citation d'un auteur."],
];
const enfants = [
  new Paragraph({ spacing: { after: 40 }, children: [run("SOCIOLOGIE · 1RE ANNÉE ARCHITECTURE · ESAD TUNIS", { font: SANS, size: 16, bold: true, color: GRIS, characterSpacing: 30 })] }),
  new Paragraph({ spacing: { after: 60 }, children: [run("Texte à dire : Thévenot et la résilience", { font: SANS, size: 32, bold: true, color: VERT })] }),
  new Paragraph({ spacing: { after: 160 }, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: OR, space: 4 } }, children: [run("Durée totale : environ 15 minutes. Lis le texte à voix haute deux ou trois fois, puis parle avec tes propres mots. Les passages entre crochets sont à personnaliser.", { font: SERIF, size: 22, italics: true, color: GRIS })] }),
];
NOTES.forEach((n) => {
  enfants.push(new Paragraph({ keepNext: true, spacing: { before: 200, after: 60 }, tabStops: [{ type: TabStopType.RIGHT, position: LARGEUR }], children: [run(n.titre, { font: SANS, size: 24, bold: true, color: VERT }), run("\t" + n.minutes, { font: SANS, size: 20, bold: true, color: OR })] }));
  enfants.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 70, line: 300, lineRule: LineRuleType.AUTO }, children: [run(n.texte, { font: SERIF, size: 24 })] }));
  enfants.push(new Paragraph({ spacing: { after: 40 }, indent: { left: cm(0.4) }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: OR, space: 8 } }, children: [run("Conseil : ", { font: SANS, size: 20, bold: true, color: OR }), run(n.conseil, { font: SANS, size: 20, color: GRIS })] }));
});
enfants.push(new Paragraph({ keepNext: true, spacing: { before: 280, after: 100 }, children: [run("Questions possibles de la prof (et réponses)", { font: SANS, size: 28, bold: true, color: VERT })] }));
QR.forEach(([q, r]) => {
  enfants.push(new Paragraph({ keepNext: true, spacing: { before: 110, after: 20 }, children: [run(q, { font: SANS, size: 22, bold: true, color: VERT })] }));
  enfants.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 40, line: 264, lineRule: LineRuleType.AUTO }, children: [run(r, { font: SERIF, size: 22 })] }));
});
enfants.push(new Paragraph({ keepNext: true, spacing: { before: 180, after: 40 }, children: [run("Sources", { font: SANS, size: 24, bold: true, color: VERT })] }));
[
  "BOLTANSKI Luc et THÉVENOT Laurent, De la justification : les économies de la grandeur, Gallimard, 1991.",
  "THÉVENOT Laurent, L'Action au pluriel : sociologie des régimes d'engagement, La Découverte, 2006.",
  "CYRULNIK Boris, Un merveilleux malheur, Odile Jacob, 1999.",
  "WERNER Emmy E. et SMITH Ruth S., Vulnerable but Invincible, McGraw-Hill, 1982 ; Overcoming the Odds, Cornell University Press, 1992.",
  "American Psychological Association, The Road to Resilience (brochure de conseils).",
  "À vérifier avant de présenter : compare ces points avec le texte ou le résumé de Thévenot donné en classe, et corrige si ta prof emploie d'autres mots.",
].forEach((t) => enfants.push(new Paragraph({ spacing: { after: 30 }, numbering: { reference: "refs", level: 0 }, children: [run(t, { font: SERIF, size: 21 })] })));

const doc = new Document({
  title: "Texte à dire : Thévenot et la résilience",
  styles: { default: { document: { run: { font: SERIF, size: 24 } } } },
  numbering: { config: [{ reference: "refs", levels: [{ level: 0, format: LevelFormat.BULLET, text: "▪", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: cm(0.6), hanging: cm(0.4) } }, run: { color: OR } } }] }] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: cm(1.8), bottom: cm(1.7), left: cm(2.2), right: cm(2.2), footer: cm(0.8) } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: SANS, size: 16, color: GRIS }), new TextRun({ text: " / ", font: SANS, size: 16, color: GRIS }), new TextRun({ children: [PageNumber.TOTAL_PAGES], font: SANS, size: 16, color: GRIS })] })] }) },
    children: enfants,
  }],
});
Packer.toBuffer(doc).then((b) => { const out = path.join(__dirname, "..", "Resilience_Thevenot_texte_a_dire.docx"); fs.writeFileSync(out, b); console.log("OK ->", out); });

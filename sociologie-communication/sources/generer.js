// Feuille d'exercice (1 page) : pourquoi est-il difficile de se comprendre meme en parlant la meme langue ?
// Usage : node generer.js  ->  ../Se_comprendre_meme_langue.docx
const fs = require("fs"), path = require("path");
const { Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat, BorderStyle, LineRuleType } = require("docx");
const NB = " ", fr = (s) => s.replace(/ ([:;!?»%])/g, NB + "$1").replace(/« /g, "«" + NB);
const SANS = "Arial", BLEU = "1F3B6E", ROUGE = "B5361F", GRIS = "555555";
const cm = (v) => Math.round(v * 567);
const r = (t, o = {}) => new TextRun({ text: fr(t), font: SANS, size: 20, ...o });
const sp = { line: 252, lineRule: LineRuleType.AUTO };
const titre = (t) => new Paragraph({ spacing: { before: 130, after: 40 }, children: [r(t, { bold: true, size: 22, color: BLEU })] });
const p = (runs, o = {}) => new Paragraph({ spacing: { after: 30, ...sp }, children: runs, ...o });
const puce = (runs) => new Paragraph({ numbering: { reference: "p", level: 0 }, spacing: { after: 20, ...sp }, children: runs });
const B = (t) => r(t, { bold: true });

const etape = (n, t, d, ex) => new Paragraph({ numbering: { reference: "p", level: 0 }, spacing: { after: 20, ...sp }, children: [B(n + " " + t + " : "), r(d + " "), r(ex, { italics: true, color: GRIS })] });
const enfants = [
  new Paragraph({ spacing: { after: 20 }, children: [r("Sociologie · 1re année Architecture · ESAD Tunis · Rostom Karoui", { size: 16, color: GRIS })] }),
  new Paragraph({ spacing: { after: 60 }, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: ROUGE, space: 3 } },
    children: [r("Pourquoi est-il difficile de se comprendre même lorsqu'on parle la même langue ?", { bold: true, size: 26, color: ROUGE })] }),
  p([B("Idée de départ : "), r("parler la même langue ne suffit pas. Ce sont nos "), B("modes de communication"), r(" qui créent soit le "), B("conflit"), r(", soit la "), B("compréhension, la coopération et l'entraide"), r(". Le but : créer un lien qui n'est pas basé sur la violence.")]),

  titre("1. Qui est Marshall Rosenberg ?"),
  puce([B("Psychologue américain"), r(" (né en 1934 à Canton, Ohio – mort en 2015), élève de Carl Rogers, le psychologue de l'écoute bienveillante.")]),
  puce([r("Il grandit à Detroit, dans un quartier marqué par la violence et les émeutes raciales de 1943 : il se demande "), B("pourquoi certains deviennent violents et d'autres restent bienveillants"), r(".")]),
  puce([r("Il crée la "), B("communication non violente (CNV)"), r(" dans les années 1960-70 et fonde en 1984 le "), B("Center for Nonviolent Communication"), r(". Il l'enseigne dans des écoles, des familles et des zones de conflit.")]),
  puce([B("Livre principal : "), r("« Les mots sont des fenêtres (ou bien ce sont des murs) », 1999.")]),

  titre("2. Pourquoi on se comprend mal, selon Rosenberg"),
  p([r("Même en parlant la même langue, on utilise souvent un "), B("langage « chacal »"), r(" qui coupe le lien :")]),
  puce([B("Juger et étiqueter : "), r("« Tu es égoïste », « Il est nul ».")]),
  puce([B("Comparer : "), r("« Ton frère, lui, il réussit ».")]),
  puce([B("Exiger et menacer : "), r("« Fais-le, sinon… ».")]),
  puce([B("Nier sa responsabilité : "), r("« Je n'ai pas le choix », « C'est à cause de toi ».")]),
  p([r("→ L'autre entend une "), B("attaque"), r(", il se défend ou contre-attaque : c'est le début du conflit. Les mots deviennent des "), B("murs"), r(".")]),

  titre("3. La solution : la CNV en 4 étapes (le langage « girafe »)"),
  p([r("La girafe est l'animal terrestre qui a le plus grand cœur et elle voit loin : elle symbolise l'écoute et la bienveillance.", { italics: true, color: GRIS })]),
  etape("1.", "Observer", "décrire les faits, sans juger.", "« Tu es arrivé 30 minutes après l'heure. »"),
  etape("2.", "Sentiment", "dire ce que je ressens.", "« Je me sens déçu… »"),
  etape("3.", "Besoin", "dire le besoin qui se cache derrière.", "« …car j'ai besoin qu'on respecte mon temps. »"),
  etape("4.", "Demande", "faire une demande claire et réalisable (pas un ordre).", "« La prochaine fois, peux-tu me prévenir ? »"),
  p([r("Et surtout : "), B("écouter l'autre avec empathie"), r(", en cherchant à son tour son sentiment et son besoin.")]),

  titre("Conclusion"),
  p([r("Pour Rosenberg, on ne se comprend pas parce que nos mots "), B("jugent"), r(" au lieu de "), B("décrire"), r(", et "), B("accusent"), r(" au lieu d'"), B("exprimer des besoins"), r(". En changeant notre façon de parler et d'écouter, les mots deviennent des "), B("fenêtres"), r(" : le conflit laisse place à la coopération et à l'entraide.")]),
  new Paragraph({ spacing: { before: 80 }, children: [r("Sources : Rosenberg, Les mots sont des fenêtres (ou bien ce sont des murs), La Découverte, 1999 · Center for Nonviolent Communication (cnvc.org), biographie du fondateur.", { size: 15, italics: true, color: GRIS })] }),
];
const doc = new Document({
  numbering: { config: [{ reference: "p", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: cm(0.6), hanging: cm(0.35) } }, run: { color: BLEU } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: cm(1.5), bottom: cm(1.3), left: cm(1.8), right: cm(1.8) } } }, children: enfants }],
});
Packer.toBuffer(doc).then((b) => { const o = path.join(__dirname, "..", "Se_comprendre_meme_langue.docx"); fs.writeFileSync(o, b); console.log("OK"); });

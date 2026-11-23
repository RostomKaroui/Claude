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

const enfants = [
  new Paragraph({ spacing: { after: 20 }, children: [r("Sociologie · 1re année Architecture · ESAD Tunis · Rostom Karoui", { size: 16, color: GRIS })] }),
  new Paragraph({ spacing: { after: 60 }, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: ROUGE, space: 3 } },
    children: [r("Pourquoi est-il difficile de se comprendre même lorsqu'on parle la même langue ?", { bold: true, size: 26, color: ROUGE })] }),
  p([B("Idée de départ : "), r("parler la même langue ne suffit pas. Ce sont nos "), B("modes de communication"), r(" qui créent soit le "), B("conflit"), r(", soit la "), B("compréhension, la coopération et l'entraide"), r(". Le but : créer un lien qui n'est pas basé sur la violence.")]),

  titre("1. Pourquoi on se comprend mal"),
  puce([B("Les mots n'ont pas le même sens pour tous : "), r("chacun les « décode » avec son vécu, son âge, sa culture, son milieu (ex. : « tout à l'heure » = 5 min ou 2 h ?).")]),
  puce([B("Le message passe aussi sans les mots : "), r("ton, regard, gestes, silence. Si le corps dit autre chose que les mots, on croit le corps.")]),
  puce([B("Le contenu et la relation : "), r("on n'entend pas seulement ce qui est dit, mais aussi comment on nous parle. « Tu ne ranges jamais rien ! » est entendu comme un reproche, pas comme une information.")]),
  puce([B("Les émotions et les jugements : "), r("quand on est en colère ou qu'on se sent attaqué, on interprète, on se défend, et on n'écoute plus.")]),
  puce([B("Le « bruit » : "), r("fatigue, bruit, distance, écran, message trop court (SMS) : une partie du message se perd.")]),

  titre("2. Ce que disent les auteurs"),
  puce([B("Shannon et Weaver (1949) : "), r("un émetteur code un message, un récepteur le décode ; entre les deux, le bruit peut le déformer.")]),
  puce([B("Paul Watzlawick (École de Palo Alto, 1967) : "), r("« on ne peut pas ne pas communiquer » ; tout message a un contenu et une dimension relationnelle.")]),
  puce([B("Marshall Rosenberg, la communication non violente (CNV) : "), r("nos mots peuvent être des « murs » ou des « fenêtres ». Il propose 4 étapes : "),
    B("observer"), r(" sans juger, dire son "), B("sentiment"), r(", exprimer son "), B("besoin"), r(", faire une "), B("demande"), r(" claire.")]),

  titre("3. Deux manières de communiquer"),
  p([r("✗ Communication qui mène au conflit : ", { bold: true, color: ROUGE }), r("« Tu es toujours en retard, tu t'en fiches de moi ! » (jugement, généralisation, reproche) → l'autre se défend, le ton monte.")]),
  p([r("✓ Communication qui mène à la coopération : ", { bold: true, color: "2F7D4A" }), r("« Tu es arrivé 30 minutes après l'heure (observation). Je suis déçu (sentiment) parce que j'ai besoin qu'on respecte mon temps (besoin). La prochaine fois, peux-tu me prévenir ? (demande) » → l'autre comprend et peut aider.")]),

  titre("Conclusion"),
  p([r("On ne se comprend pas toujours car la communication ne se limite pas aux mots : elle passe par le sens qu'on leur donne, le non-verbal, la relation et les émotions. En "), B("écoutant"), r(", en "), B("décrivant au lieu de juger"), r(" et en "), B("exprimant ses besoins"), r(", on transforme un risque de conflit en coopération et en entraide.")]),
  new Paragraph({ spacing: { before: 80 }, children: [r("Sources : Shannon et Weaver, The Mathematical Theory of Communication (1949) · Watzlawick, Beavin et Jackson, Une logique de la communication (1967, trad. 1972) · Rosenberg, Les mots sont des fenêtres (ou bien ce sont des murs).", { size: 15, italics: true, color: GRIS })] }),
];
const doc = new Document({
  numbering: { config: [{ reference: "p", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: cm(0.6), hanging: cm(0.35) } }, run: { color: BLEU } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: cm(1.5), bottom: cm(1.3), left: cm(1.8), right: cm(1.8) } } }, children: enfants }],
});
Packer.toBuffer(doc).then((b) => { const o = path.join(__dirname, "..", "Se_comprendre_meme_langue.docx"); fs.writeFileSync(o, b); console.log("OK"); });

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

const para = (runs) => new Paragraph({ alignment: AlignmentType.JUSTIFIED, indent: { firstLine: cm(0.6) }, spacing: { after: 70, ...sp }, children: runs });
const sous = (t) => new Paragraph({ spacing: { before: 60, after: 30 }, children: [r(t, { bold: true, italics: true, size: 20, color: BLEU })] });
const enfants = [
  new Paragraph({ spacing: { after: 20 }, children: [r("Sociologie · 1re année Architecture · ESAD Tunis · Rostom Karoui", { size: 16, color: GRIS })] }),
  new Paragraph({ spacing: { after: 80 }, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: ROUGE, space: 3 } },
    children: [r("Pourquoi est-il difficile de se comprendre même lorsqu'on parle la même langue ?", { bold: true, size: 26, color: ROUGE })] }),

  titre("Introduction"),
  para([r("Parler la même langue ne garantit pas que l'on se comprenne. Dans une famille, entre amis ou à l'école, des malentendus naissent chaque jour entre des personnes qui utilisent pourtant les mêmes mots. Le problème ne vient donc pas de la langue elle-même, mais des "), B("modes de communication"), r(" que nous adoptons : ils peuvent être à l'origine du "), B("conflit"), r(" ou, au contraire, de la "), B("compréhension, de la coopération et de l'entraide"), r(". Pour comprendre ce phénomène et chercher comment tisser un lien qui ne repose pas sur la violence, nous nous appuierons sur les travaux de Marshall Rosenberg.")]),

  titre("I. Marshall Rosenberg et la communication non violente"),
  para([r("Marshall Rosenberg est un "), B("psychologue américain"), r(", né en 1934 à Canton, dans l'Ohio, et mort en 2015. Élève de Carl Rogers, connu pour son approche fondée sur l'écoute bienveillante, il grandit à Detroit dans un quartier marqué par la violence. Cette expérience l'amène à se poser une question centrale : "), B("pourquoi certaines personnes deviennent-elles violentes alors que d'autres restent bienveillantes, même dans des situations difficiles ?")]),
  para([r("Pour y répondre, il développe dans les années 1960 et 1970 la "), B("communication non violente (CNV)"), r(", puis fonde en 1984 le "), B("Center for Nonviolent Communication"), r(". Il diffuse sa méthode dans des écoles, des familles, des entreprises et même des zones de conflit. Son livre principal, "), r("Les mots sont des fenêtres (ou bien ce sont des murs)", { italics: true }), r(" (1999), résume son idée : selon la manière dont nous les utilisons, les mots peuvent rapprocher les personnes ou les séparer.")]),

  titre("II. Pourquoi on se comprend mal : le langage « chacal »"),
  para([r("Pour Rosenberg, nous avons appris très tôt une façon de parler qui coupe le lien avec l'autre. Il la symbolise par le "), B("chacal"), r(". Ce langage consiste d'abord à "), B("juger et étiqueter"), r(" les personnes (« tu es égoïste »), à les "), B("comparer"), r(" (« ton frère, lui, réussit »), à "), B("exiger"), r(" ou menacer (« fais-le, sinon… »), et enfin à "), B("nier sa propre responsabilité"), r(" (« c'est à cause de toi », « je n'ai pas le choix »).")]),
  para([r("Le message, même exprimé dans une langue commune, est alors reçu comme une "), B("attaque"), r(". Celui qui l'entend ne retient plus le contenu, mais le reproche : il se défend ou contre-attaque, et le conflit commence. Les mots deviennent des "), B("murs"), r(". C'est pourquoi deux personnes peuvent parler longtemps sans jamais se comprendre.")]),

  titre("III. La solution : parler et écouter en « girafe »"),
  para([r("À l'opposé du chacal, Rosenberg choisit la "), B("girafe"), r(", symbole de l'écoute et de la bienveillance. La communication non violente repose sur "), B("quatre étapes"), r(". Il s'agit d'abord d'"), B("observer"), r(" les faits sans les juger (« tu es arrivé trente minutes après l'heure »), puis d'exprimer son "), B("sentiment"), r(" (« je me sens déçu »), d'identifier le "), B("besoin"), r(" qui se cache derrière ce sentiment (« car j'ai besoin qu'on respecte mon temps ») et enfin de formuler une "), B("demande"), r(" claire et réalisable, qui n'est pas un ordre (« la prochaine fois, peux-tu me prévenir ? »).")]),
  para([r("Cette démarche ne concerne pas seulement la manière de parler : elle demande aussi d'"), B("écouter l'autre avec empathie"), r(", en cherchant à son tour ce qu'il ressent et ce dont il a besoin. Le même reproche, exprimé ainsi, ne provoque plus de défense : l'autre comprend la situation et peut proposer son aide. La communication devient alors une source de "), B("coopération et d'entraide"), r(".")]),

  titre("Conclusion"),
  para([r("Il est difficile de se comprendre même en parlant la même langue, car nos mots expriment souvent des "), B("jugements"), r(" plutôt que des faits, et des "), B("accusations"), r(" plutôt que des besoins. Marshall Rosenberg montre qu'en changeant notre manière de parler et d'écouter, les mots cessent d'être des murs pour devenir des "), B("fenêtres"), r(". La communication non violente permet ainsi de créer un lien fondé non plus sur la violence, mais sur la compréhension mutuelle.")]),
  new Paragraph({ spacing: { before: 80 }, children: [r("Sources : Rosenberg, Les mots sont des fenêtres (ou bien ce sont des murs), La Découverte, 1999 · Center for Nonviolent Communication (cnvc.org), biographie du fondateur.", { size: 15, italics: true, color: GRIS })] }),
];
const doc = new Document({
  numbering: { config: [{ reference: "p", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: cm(0.6), hanging: cm(0.35) } }, run: { color: BLEU } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: cm(1.5), bottom: cm(1.3), left: cm(1.8), right: cm(1.8) } } }, children: enfants }],
});
Packer.toBuffer(doc).then((b) => { const o = path.join(__dirname, "..", "Se_comprendre_meme_langue.docx"); fs.writeFileSync(o, b); console.log("OK"); });

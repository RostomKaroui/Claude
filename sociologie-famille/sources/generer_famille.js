// Genere le devoir de sociologie « Le comportement de l'individu dans la famille : mon pere » (Word, ~2 pages A4).
// Usage : node generer_famille.js  ->  ../Sociologie_famille_mon_pere.docx
// Mini-balisage : **gras**, *italique*, ==passage a completer== (surligne en jaune).
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, AlignmentType, LevelFormat,
  BorderStyle, WidthType, ShadingType, Footer, PageNumber, TabStopType, VerticalAlign, LineRuleType,
} = require("docx");

const SERIF = "Times New Roman", SANS = "Arial";
const ROUGE = "8C1C13", ENCRE = "222222", GRIS = "666666";
const CORPS = 22;                 // 11 pt
const INTERLIGNE = 250;
const cm = (v) => Math.round(v * 567);
const MARGE = 2.0;
const LARGEUR = 11906 - 2 * cm(MARGE);
const NBSP = " ";
const fr = (s) => s.replace(/ ([:;!?»])/g, NBSP + "$1").replace(/« /g, "«" + NBSP);

function runs(texte, base = {}) {
  const out = [], t = fr(texte), re = /(==[^=]+==|\*\*[^*]+\*\*|\*[^*]+\*)/g;
  let last = 0, m;
  while ((m = re.exec(t))) {
    if (m.index > last) out.push(new TextRun({ ...base, text: t.slice(last, m.index) }));
    const tok = m[0];
    if (tok.startsWith("==")) out.push(new TextRun({ ...base, text: tok.slice(2, -2), highlight: "yellow" }));
    else if (tok.startsWith("**")) out.push(new TextRun({ ...base, text: tok.slice(2, -2), bold: true }));
    else out.push(new TextRun({ ...base, text: tok.slice(1, -1), italics: !base.italics }));
    last = m.index + tok.length;
  }
  if (last < t.length) out.push(new TextRun({ ...base, text: t.slice(last) }));
  return out;
}
const p = (texte, o = {}) => new Paragraph({ alignment: AlignmentType.JUSTIFIED, children: runs(texte), ...o });
const titre = (texte) => new Paragraph({ keepNext: true, spacing: { before: 150, after: 60 }, children: runs(texte, { font: SANS, size: 23, bold: true, color: ROUGE }) });
const puce = (texte) => new Paragraph({ alignment: AlignmentType.JUSTIFIED, numbering: { reference: "puces", level: 0 }, spacing: { after: 30 }, children: runs(texte) });

// ---------- tableau d'observation ----------
const COLS = [cm(3.0), LARGEUR - cm(3.0) - cm(3.4), cm(3.4)];
const bord = { style: BorderStyle.SINGLE, size: 4, color: "C9B8B0" };
const bords = { top: bord, bottom: bord, left: bord, right: bord };
function cellule(texte, i, entete = false) {
  return new TableCell({
    width: { size: COLS[i], type: WidthType.DXA }, borders: bords, verticalAlign: VerticalAlign.CENTER,
    shading: entete ? { fill: ROUGE, type: ShadingType.CLEAR, color: "auto" } : i === 0 ? { fill: "F6EEEA", type: ShadingType.CLEAR, color: "auto" } : undefined,
    margins: { top: 40, bottom: 40, left: 80, right: 80 },
    children: [new Paragraph({ spacing: { after: 0, line: 236, lineRule: LineRuleType.AUTO },
      children: entete ? runs(texte, { font: SANS, size: 17, bold: true, color: "FFFFFF" }) : i === 0 ? runs(texte, { font: SANS, size: 17, bold: true, color: ROUGE }) : i === 2 ? runs(texte, { size: 19, color: GRIS }) : runs(texte, { size: 20 }) })],
  });
}
const lignes = [
  ["Autorité et décisions", "Les décisions importantes (argent, études, sorties) sont prises par ==[mon père seul / mes parents ensemble / toute la famille]==. Les autres le respectent parce que ==[c'est la tradition / sa personnalité / les règles de la maison]==.", "Autorité (Weber)"],
  ["Éducation des enfants", "Avec nous, il est plutôt ==[autoritaire / démocratique / permissif]==. Exemple concret : ==[une situation vécue : un conseil, une punition, une discussion…]==.", "Styles éducatifs (Baumrind)"],
  ["Place dans le foyer", "Il s'occupe surtout de ==[l'argent, les décisions, les réparations, le suivi scolaire…]== ; ma mère s'occupe surtout de ==[…]==.", "Rôle instrumental et expressif (Parsons)"],
  ["Émotions", "Il montre son affection par ==[des paroles / des gestes / des cadeaux / sa présence…]== et il parle ==[beaucoup / peu]== de ce qu'il ressent.", "Socialisation, rôle de père"],
  ["Dehors / à la maison", "Devant des invités ou au travail, il est ==[…]==, alors qu'à la maison il est ==[…]==.", "Scène et coulisses (Goffman)"],
  ["Valeurs transmises", "Il nous transmet surtout ==[le respect / le travail / la religion / l'honnêteté…]==, par ==[son exemple / ses conseils / ses histoires]==.", "Socialisation primaire"],
];
const tableau = new Table({
  width: { size: LARGEUR, type: WidthType.DXA }, columnWidths: COLS,
  rows: [
    new TableRow({ tableHeader: true, children: ["Domaine", "Ce que j'observe chez mon père", "Concept"].map((t, i) => cellule(t, i, true)) }),
    ...lignes.map((l) => new TableRow({ cantSplit: true, children: l.map((t, i) => cellule(t, i)) })),
  ],
});

const enTete = [
  new Paragraph({ spacing: { after: 20, line: 240, lineRule: LineRuleType.AUTO }, children: [new TextRun({ text: "SOCIOLOGIE · LA FAMILLE", font: SANS, size: 17, bold: true, color: GRIS, characterSpacing: 40 })] }),
  new Paragraph({ spacing: { after: 40, line: 240, lineRule: LineRuleType.AUTO }, children: runs("Le comportement de l'individu dans la famille : l'exemple de mon père", { font: SANS, size: 27, bold: true, color: ROUGE }) }),
  new Paragraph({
    spacing: { after: 140 }, tabStops: [{ type: TabStopType.RIGHT, position: LARGEUR }],
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: ROUGE, space: 4 } },
    children: [...runs("1re année Architecture · ESAD Tunis", { font: SANS, size: 17, color: GRIS }), ...runs("\tNom et prénom : ==[à compléter]==", { font: SANS, size: 17, color: GRIS })],
  }),
];

const corps = [
  titre("Introduction"),
  p("La famille est le **premier cadre social** de l'individu : c'est là qu'il apprend les règles de la vie en société (la **socialisation primaire**). Chaque membre y occupe une place, son **statut**, et y joue un **rôle**, c'est-à-dire l'ensemble des comportements que les autres attendent de lui. J'ai choisi d'étudier **mon père**, car son comportement montre bien comment un rôle social se construit entre ce que la société attend d'un père et sa propre personnalité. Ma question est la suivante : **comment le comportement de mon père dans la famille s'explique-t-il, et comment influence-t-il la vie de la famille ?**"),

  titre("1. Présentation de mon père"),
  p("Mon père s'appelle ==[prénom]== et il a ==[âge]== ans. Il est ==[profession]== et il travaille ==[horaires, lieu : tous les jours, le soir, à l'extérieur…]==. Il est originaire de ==[ville ou région]== et il a grandi dans une famille de ==[nombre]== enfants. Notre famille est ==[nucléaire (parents et enfants) / élargie (avec grands-parents ou autres proches)]== : nous vivons ==[nombre]== personnes dans ==[une maison / un appartement]==."),

  titre("2. Les outils de la sociologie"),
  puce("**Statut et rôle** : le statut est la place dans le groupe (père, chef de ménage) ; le rôle est le comportement attendu (protéger, faire vivre la famille, éduquer, décider)."),
  puce("**Rôle instrumental et rôle expressif** (Parsons et Bales, 1955) : traditionnellement, le père a le rôle *instrumental* (ressources, décisions, lien avec l'extérieur) et la mère le rôle *expressif* (affection, ambiance du foyer). Cette théorie est aujourd'hui critiquée, car les rôles ont changé."),
  puce("**Les types d'autorité** (Max Weber) : *traditionnelle* (« c'est la coutume »), *charismatique* (on suit la personnalité de celui qui commande) et *légale-rationnelle* (on suit des règles). Dans la famille, on trouve surtout les deux premières."),
  puce("**Les styles éducatifs** (Diana Baumrind, 1967) : *autoritaire* (règles strictes, peu de dialogue), *démocratique* (règles claires et dialogue), *permissif* (peu de règles). Maccoby et Martin (1983) y ajoutent le style *négligent*."),
  puce("**Scène et coulisses** (Erving Goffman) : on ne se comporte pas de la même façon devant le public et dans les coulisses."),

  titre("3. Le comportement de mon père dans la famille"),
  tableau,

  titre("4. Comment l'expliquer ?"),
  p("Le comportement de mon père ne dépend pas seulement de son caractère. Il s'explique par plusieurs facteurs : **l'éducation qu'il a reçue** de son propre père (on reproduit souvent le modèle familial dans lequel on a grandi), sa **génération** et son **milieu social**, sa **profession** (qui décide de sa disponibilité) et la **culture** de notre société. Dans son cas : ==[explique en 2 ou 3 phrases : par exemple « il a grandi dans une famille où le père décidait de tout, donc… »]==."),
  p("Le rôle du père a aussi beaucoup évolué. Autrefois, il était surtout le **chef de famille**, celui qui fait vivre le foyer et dont l'autorité s'exerce à distance. Avec le travail des femmes, la scolarisation et la famille nucléaire, de plus en plus de pères participent à l'éducation et aux tâches de la maison. En Tunisie, le **Code du statut personnel** (1956), réformé en 1993 (article 23), demande aux époux de **coopérer** dans la conduite des affaires de la famille et l'éducation des enfants, même si le mari reste désigné comme chef de famille pour les charges financières."),
  p("**Et l'architecture ?** Le logement met en scène ces rôles : le salon est une scène où l'on reçoit, la cuisine et les chambres sont des coulisses. Chez nous, ==[où se place mon père à table ? a-t-il un fauteuil ou un espace à lui ? où se tient-il quand il y a des invités ?]==."),

  titre("Conclusion"),
  p("Cette étude montre que le comportement d'un individu dans la famille n'est pas seulement une question de caractère : il résulte aussi de son **statut**, de son **rôle**, de son **éducation** et de la **société** dans laquelle il vit. Mon père est ==[résume-le en une phrase : père autoritaire, proche, discret, travailleur…]==, et son comportement influence la famille car ==[une conséquence concrète sur toi, ta mère, tes frères et sœurs…]==. Comprendre ces mécanismes aide aussi l'architecte à concevoir des logements adaptés aux manières de vivre ensemble."),

  new Paragraph({ spacing: { before: 100, after: 30 }, border: { top: { style: BorderStyle.SINGLE, size: 4, color: "C9B8B0", space: 4 } }, children: runs("Références", { font: SANS, size: 16, bold: true, color: ROUGE }) }),
  new Paragraph({ spacing: { after: 0, line: 228, lineRule: LineRuleType.AUTO }, children: runs("WEBER Max, *Économie et société*, 1921 · PARSONS Talcott et BALES Robert, *Family, Socialization and Interaction Process*, 1955 · BAUMRIND Diana, « Child care practices anteceding three patterns of preschool behavior », *Genetic Psychology Monographs*, 1967 · MACCOBY Eleanor et MARTIN John, « Socialization in the context of the family », 1983 · GOFFMAN Erving, *La Mise en scène de la vie quotidienne*, 1973 · *Code du statut personnel tunisien*, art. 23 (loi n° 93-74 de 1993).", { size: 16 }) }),
];

const doc = new Document({
  creator: "Étudiant·e 1re année Architecture, ESAD Tunis",
  title: "Le comportement de l'individu dans la famille : l'exemple de mon père",
  styles: {
    default: { document: { run: { font: SERIF, size: CORPS, color: ENCRE } } },
    paragraphStyles: [{ id: "Normal", name: "Normal", run: { font: SERIF, size: CORPS, color: ENCRE }, paragraph: { spacing: { after: 80, line: INTERLIGNE, lineRule: LineRuleType.AUTO } } }],
  },
  numbering: { config: [{ reference: "puces", levels: [{ level: 0, format: LevelFormat.BULLET, text: "▪", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: cm(0.6), hanging: cm(0.4) } }, run: { color: ROUGE } } }] }] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: cm(1.7), bottom: cm(1.6), left: cm(MARGE), right: cm(MARGE), header: cm(0.8), footer: cm(0.7) } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: SANS, size: 16, color: GRIS }), new TextRun({ text: " / ", font: SANS, size: 16, color: GRIS }), new TextRun({ children: [PageNumber.TOTAL_PAGES], font: SANS, size: 16, color: GRIS })] })] }) },
    children: [...enTete, ...corps.map((c) => c)],
  }],
});
// interligne par defaut (regle « auto » explicite, comme Word)
Packer.toBuffer(doc).then((b) => { const out = path.join(__dirname, "..", "Sociologie_famille_mon_pere.docx"); fs.writeFileSync(out, b); console.log("OK ->", out); });

// Genere le rendu Word (3 pages A4) sur Goffman, La Mise en scene de la vie quotidienne.
// Usage : node generer_rendu.js  ->  ../Goffman_mise_en_scene_vie_quotidienne.docx
//
// Mini-balisage dans les textes : *italique*, **gras**.
// Les espaces avant : ; ! ? et a l'interieur des guillemets « » sont rendues insecables.

const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, LevelFormat, BorderStyle, WidthType, ShadingType,
  Header, Footer, PageNumber, TabStopType, VerticalAlign, LineRuleType,
} = require("docx");

// ---------- reglages ----------
const SERIF = "Times New Roman";
const SANS = "Arial";
const ROUGE = "8C1C13"; // rouge « rideau de theatre »
const ENCRE = "222222";
const GRIS = "666666";
const CORPS = 24; // demi-points -> 12 pt
const INTERLIGNE = 252; // 1,05 (regle "auto", comme Word)
const cm = (v) => Math.round(v * 567);
const MARGE = 2.2; // cm, gauche et droite
const LARGEUR_TEXTE = 11906 - 2 * cm(MARGE); // A4 moins les marges

// ---------- typographie francaise ----------
const NBSP = " ";
function fr(s) {
  return s
    .replace(/ ([:;!?»])/g, NBSP + "$1")
    .replace(/« /g, "«" + NBSP)
    .replace(/ – /g, NBSP + "– ");
}

// Transforme "texte *italique* **gras**" en TextRun[]
function runs(texte, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*)/g;
  let last = 0;
  let m;
  const t = fr(texte);
  while ((m = re.exec(t))) {
    if (m.index > last) out.push(new TextRun({ text: t.slice(last, m.index), ...base }));
    const tok = m[0];
    if (tok.startsWith("**")) out.push(new TextRun({ ...base, text: tok.slice(2, -2), bold: true }));
    else out.push(new TextRun({ ...base, text: tok.slice(1, -1), italics: !base.italics }));
    last = m.index + tok.length;
  }
  if (last < t.length) out.push(new TextRun({ text: t.slice(last), ...base }));
  return out;
}

const p = (texte, opts = {}) =>
  new Paragraph({ alignment: AlignmentType.JUSTIFIED, children: runs(texte), ...opts });

const titre = (texte) =>
  new Paragraph({ style: "Titre1", keepNext: true, children: runs(texte) });

const puce = (texte) =>
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    numbering: { reference: "puces", level: 0 },
    spacing: { after: 70, line: INTERLIGNE, lineRule: LineRuleType.AUTO },
    children: runs(texte),
  });

const citation = (texte, source) =>
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    indent: { left: cm(0.6), right: cm(0.3) },
    spacing: { before: 40, after: 100 },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: ROUGE, space: 8 } },
    children: [
      ...runs(texte, { italics: true }),
      ...(source ? runs(" " + source, { size: CORPS - 3, color: GRIS }) : []),
    ],
  });

// ---------- tableau « lexique » ----------
const COLS = [cm(3.6), LARGEUR_TEXTE - cm(3.6) - cm(5.4), cm(5.4)];
const bord = { style: BorderStyle.SINGLE, size: 4, color: "C9B8B0" };
const bords = { top: bord, bottom: bord, left: bord, right: bord };

function cellule(texte, i, entete = false) {
  return new TableCell({
    width: { size: COLS[i], type: WidthType.DXA },
    borders: bords,
    verticalAlign: VerticalAlign.CENTER,
    shading: entete
      ? { fill: ROUGE, type: ShadingType.CLEAR, color: "auto" }
      : i === 0
        ? { fill: "F6EEEA", type: ShadingType.CLEAR, color: "auto" }
        : undefined,
    margins: { top: 50, bottom: 50, left: 90, right: 90 },
    children: [
      new Paragraph({
        spacing: { after: 0, line: 240, lineRule: LineRuleType.AUTO },
        children: entete
          ? runs(texte, { font: SANS, size: 18, bold: true, color: "FFFFFF" })
          : i === 0
            ? runs(texte, { font: SANS, size: 18, bold: true, color: ROUGE })
            : runs(texte, { size: 20 }),
      }),
    ],
  });
}

const lignesLexique = [
  ["Décor (*setting*)", "Le cadre matériel de la représentation : lieu, mobilier, objets. Il est en général fixe : l'acteur doit s'y rendre pour jouer.", "Le cabinet du médecin, le bureau du directeur, l'amphithéâtre."],
  ["Façade personnelle", "L'**apparence** (vêtements, insignes, âge) annonce le statut ; la **manière** (ton, gestes) annonce le rôle que l'on va jouer. Les deux doivent être cohérentes.", "La blouse blanche, l'uniforme… Un chirurgien en tongs ou un juge qui ricane crée un malaise."],
  ["Idéalisation", "On montre une version idéale de soi, conforme aux valeurs attendues, et on cache ce qui ne colle pas.", "Le restaurant « fait maison » ; l'étudiant qui cache qu'il a tout fait la veille."],
  ["Équipe", "On joue rarement seul : un groupe coopère pour maintenir une même impression et partage des secrets.", "Le personnel d'un hôpital face aux patients ; un couple qui reçoit des invités."],
  ["Sincère ou cynique", "L'acteur peut croire à son propre rôle, ou le jouer en sachant qu'il trompe son public.", "Le vendeur convaincu de son produit… ou pas du tout."],
];

const lexique = new Table({
  width: { size: LARGEUR_TEXTE, type: WidthType.DXA },
  columnWidths: COLS,
  rows: [
    new TableRow({
      tableHeader: true,
      children: ["Notion", "Ce que cela veut dire", "Exemple"].map((t, i) => cellule(t, i, true)),
    }),
    ...lignesLexique.map((l) => new TableRow({ cantSplit: true, children: l.map((t, i) => cellule(t, i)) })),
  ],
});

// ---------- contenu ----------
const enTete = [
  new Paragraph({
    spacing: { after: 20, line: 240, lineRule: LineRuleType.AUTO },
    children: [new TextRun({ text: "ERVING GOFFMAN (1922-1982)", font: SANS, size: 18, bold: true, color: GRIS, characterSpacing: 40 })],
  }),
  new Paragraph({
    spacing: { after: 40, line: 240, lineRule: LineRuleType.AUTO },
    children: runs("La vie quotidienne comme une scène de théâtre", { font: SANS, size: 36, bold: true, color: ROUGE }),
  }),
  new Paragraph({
    spacing: { after: 60 },
    children: runs("Travail de recherche sur *La Mise en scène de la vie quotidienne* (1959 ; traduction française 1973)", { size: 22, italics: false, color: ENCRE }),
  }),
  new Paragraph({
    spacing: { after: 200 },
    tabStops: [{ type: TabStopType.RIGHT, position: LARGEUR_TEXTE }],
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: ROUGE, space: 4 } },
    children: [
      ...runs("Sociologie · 1re année Architecture · ESAD Tunis · 2026-2027", { font: SANS, size: 17, color: GRIS }),
      new TextRun({ text: "\tNom et prénom : …………………………………", font: SANS, size: 17, color: GRIS }),
    ],
  }),
];

const corps = [
  titre("Introduction"),
  p("Erving Goffman (1922-1982) est un sociologue canadien-américain formé à l'université de Chicago. Au lieu d'étudier les grandes structures de la société (l'État, l'économie, les classes sociales), il s'intéresse à ce que tout le monde fait sans y penser : saluer, entrer dans une pièce, servir un client, éviter un regard, rougir après une gaffe. Son premier livre, *The Presentation of Self in Everyday Life* (1956, réédité en 1959), traduit en français sous le titre *La Mise en scène de la vie quotidienne* (Éditions de Minuit, 1973), pose une question simple : lorsque nous sommes en présence des autres, comment contrôlons-nous l'image que nous donnons de nous-mêmes ? Il publiera ensuite d'autres ouvrages devenus classiques, comme *Asiles* (1961), sur la vie dans les hôpitaux psychiatriques, ou *Stigmate* (1963), sur la façon dont on vit avec une différence visible."),
  p("Ce livre est né d'un terrain très concret. De décembre 1949 à mai 1951, Goffman vit à Unst, une petite île des Shetland, au nord de l'Écosse, et travaille comme plongeur dans l'hôtel du village. Depuis la cuisine, il voit le personnel franchir sans cesse la porte de la salle à manger… et remarque que ce ne sont pas tout à fait les mêmes personnes de chaque côté de cette porte."),

  titre("1. La vie sociale comme une pièce de théâtre"),
  p("Goffman propose de lire la vie sociale avec le vocabulaire du théâtre : c'est l'approche « dramaturgique ». Chaque individu est un **acteur** qui joue un **rôle** devant un **public**, et chaque rencontre est une **représentation**. L'enjeu est la « définition de la situation » : tous les participants doivent s'accorder sur ce qui est en train de se passer (un cours, un entretien d'embauche, un dîner de famille) et sur qui est qui. Pour y parvenir, chacun pratique la **gestion des impressions** (*impression management*) : il contrôle, plus ou moins consciemment, l'image qu'il renvoie."),
  p("Goffman distingue deux formes d'expression : ce que l'on **donne** volontairement (les paroles, les informations que l'on choisit de communiquer) et ce que l'on **laisse échapper** (un regard, un ton, une posture, une hésitation). Le public se fie surtout à ce second canal, qui lui paraît plus difficile à truquer… et les acteurs habiles apprennent justement à le travailler. Goffman l'illustre par un passage de roman de William Sansom : Preedy, un Anglais en vacances, arrive sur une plage espagnole. Il évite de croiser les regards pour paraître indifférent, s'arrange pour qu'on aperçoive le titre de son livre (une traduction d'Homère : cultivé, mais sans prétention), range ses affaires en une pile soignée, puis entre dans l'eau avec assurance. Tout est calculé pour avoir l'air naturel."),
  p("Goffman rappelle enfin, en citant le sociologue Robert E. Park, que ce n'est sans doute pas un hasard si le mot « personne » vient du latin *persona*, le masque de l'acteur : c'est dans nos rôles que nous nous connaissons les uns les autres, et que nous nous connaissons nous-mêmes."),

  titre("2. Le lexique de la représentation"),
  p("Pour jouer son rôle, l'acteur s'appuie sur une **façade** (*front*) : tout l'équipement expressif, matériel ou corporel, qu'il met en scène.", { spacing: { after: 100 } }),
  lexique,

  titre("3. Scène et coulisses : la représentation a besoin d'espaces"),
  p("C'est la partie du livre qui parle le plus directement aux architectes. Goffman définit une **région** comme « tout lieu borné, dans une certaine mesure, par des barrières à la perception » : murs, portes, cloisons, rideaux, mais aussi distance ou bruit. Il en distingue deux :"),
  puce("la **région antérieure**, ou **scène** (*front stage*) : le lieu où se joue la représentation devant le public, où l'on respecte les règles de politesse et les exigences du rôle ;"),
  puce("la **région postérieure**, ou **coulisses** (*backstage*) : le lieu interdit au public, où l'on peut « tomber le masque » : se détendre, plaisanter, critiquer les clients, répéter, réparer le décor, préparer ce qui sera montré."),
  p("Goffman ajoute une troisième région, l'« extérieur » : tous les lieux qui ne sont ni la scène ni les coulisses de la représentation en cours (pour un restaurant, la rue et ses passants)."),
  p("Pour que la représentation tienne, les coulisses doivent rester cachées et leur accès contrôlé ; on passe de l'une à l'autre par des **seuils** : une porte, un couloir, un comptoir. À l'hôtel des Shetland, le personnel adopte en salle les manières attendues par les clients, puis retrouve en cuisine son langage et ses habitudes d'insulaires. Goffman cite aussi George Orwell, qui avait été plongeur dans un grand hôtel parisien (voir visuel 1) :"),
  citation("« C'est un spectacle instructif que de voir un garçon entrer dans la salle à manger d'un hôtel. Au moment où il passe la porte, un brusque changement s'opère en lui. Le port de ses épaules change ; toute la saleté, la hâte et l'irritation disparaissent en un instant. Il glisse sur le tapis avec un air solennel de prêtre. »", "– G. Orwell, *Dans la dèche à Paris et à Londres*, 1933 (trad. libre)."),
  p("Quand un intrus franchit le seuil au mauvais moment (le client qui entre dans la cuisine, l'invité qui ouvre la mauvaise porte), la représentation s'effondre et tout le monde est gêné. Le public fait d'ailleurs souvent preuve de **tact** : il fait semblant de ne rien avoir vu, pour aider l'acteur à « sauver la face ». Le même mécanisme existe à la maison : quand des invités arrivent, on range le salon, on ferme la porte de la chambre en désordre, et la cuisine devient l'endroit où l'on se parle à voix basse avant de revenir sourire à table."),

  titre("4. Lecture d'architecte : l'espace comme dispositif de mise en scène"),
  p("Si la vie sociale est un théâtre, l'architecte en dessine les décors, les coulisses et les portes. Quelques exemples :"),
  puce("**La maison.** Le salon est une scène (beaux meubles, objets exposés, photos de famille) ; la cuisine, la salle de bains et les chambres sont des coulisses. Beaucoup de foyers ont même un salon « des invités », soigné et peu utilisé au quotidien : une scène qui n'existe que pour la représentation."),
  puce("**La dar de la médina de Tunis.** Depuis la rue, on franchit la porte puis, dans les grandes demeures, la *driba*, vestibule muni de banquettes où le maître de maison reçoit les visiteurs étrangers à la famille. Vient ensuite la *skifa*, vestibule coudé qui empêche de voir depuis l'entrée ce qui se passe dans le patio (*west ed-dar*), cœur de la vie familiale. La skifa est exactement une « barrière à la perception » au sens de Goffman : la maison trie ses publics (voir visuel 2)."),
  puce("**Le « gradient d'intimité ».** Christopher Alexander en fait une règle de conception (*A Pattern Language*, 1977, pattern n° 127) : si les espaces ne sont pas disposés du plus public au plus privé, les visites des étrangers, des amis, des invités ou des clients « seront toujours un peu gênantes »."),
  puce("**La Glass House de Philip Johnson (1949).** Une maison aux murs entièrement vitrés, sans cloisons intérieures… sauf un cylindre de brique qui abrite la salle de bains. Même dans la transparence totale, il faut une coulisse."),
  puce("**Le bureau en open space.** En supprimant les cloisons, on supprime aussi les coulisses : chacun est en permanence « en scène » devant ses collègues. Les salariés s'en recréent ailleurs : la machine à café, l'escalier, les toilettes, les cabines téléphoniques."),
  puce("**La cuisine ouverte** des restaurants contemporains renverse le schéma : les coulisses deviennent un spectacle, le chef devient acteur… et les vraies coulisses se déplacent ailleurs (plonge, réserve, vestiaire)."),

  titre("5. Limites et actualité de Goffman"),
  p("On reproche parfois à Goffman une vision trop calculatrice de l'être humain, comme si nous passions notre vie à manipuler les autres. Pourtant, il ne prétend pas qu'un « vrai moi » se cache derrière le masque : pour lui, le soi « n'est pas une chose organique » située quelque part, « c'est un effet dramatique » qui naît de la scène jouée. Il précise d'ailleurs, à la fin du livre, que le théâtre n'est qu'une image : « les échafaudages, après tout, servent à construire autre chose, et doivent être dressés en pensant qu'on les démontera ». Une belle formule pour de futurs architectes ! On peut ajouter une autre limite : Goffman parle peu des inégalités. Or avoir des coulisses est aussi un privilège : dans un logement surpeuplé, impossible de s'isoler pour « tomber le masque », ce que tout architecte qui dessine du logement devrait garder en tête."),
  p("Soixante ans plus tard, ses outils restent très actuels. Un profil Instagram est une façade soignée, la photo retouchée relève de l'idéalisation et le « second compte » réservé aux amis proches joue le rôle de coulisses. Dès 1985, Joshua Meyrowitz (*No Sense of Place*) montrait que les médias électroniques brouillent la frontière entre scène et coulisses : un même message touche à la fois la famille, les amis et les professeurs, et l'on ne sait plus vraiment devant quel public on joue."),

  titre("Conclusion"),
  p("Goffman nous apprend que la vie quotidienne est faite de représentations, et que ces représentations ont besoin d'espaces : des scènes où l'on se montre, des coulisses où l'on se repose, et des seuils pour passer de l'un à l'autre. Pour un étudiant en architecture, la leçon est claire : dessiner une maison, un restaurant ou une école, c'est aussi écrire en partie la mise en scène de ceux qui vont y vivre."),
];

const refs = [
  "GOFFMAN Erving, *La Mise en scène de la vie quotidienne*, t. 1 : *La Présentation de soi*, trad. Alain Accardo, Paris, Éditions de Minuit, coll. « Le sens commun », 1973 [*The Presentation of Self in Everyday Life*, 1959].",
  "ORWELL George, *Dans la dèche à Paris et à Londres* [*Down and Out in Paris and London*], 1933.",
  "ALEXANDER Christopher *et al.*, *A Pattern Language*, New York, Oxford University Press, 1977.",
  "MEYROWITZ Joshua, *No Sense of Place*, New York, Oxford University Press, 1985.",
];

const references = [
  new Paragraph({
    spacing: { before: 160, after: 60 },
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: "C9B8B0", space: 6 } },
    children: runs("Références", { font: SANS, size: 19, bold: true, color: ROUGE }),
  }),
  ...refs.map((r) => new Paragraph({
    spacing: { after: 20, line: 240, lineRule: LineRuleType.AUTO },
    indent: { left: cm(0.5), hanging: cm(0.5) },
    children: runs(r, { size: 19 }),
  })),
];

// ---------- document ----------
const doc = new Document({
  creator: "Étudiant·e 1re année Architecture, ESAD Tunis",
  title: "Erving Goffman : la vie quotidienne comme une scène de théâtre",
  styles: {
    default: { document: { run: { font: SERIF, size: CORPS, color: ENCRE } } },
    paragraphStyles: [
      {
        id: "Normal", name: "Normal",
        run: { font: SERIF, size: CORPS, color: ENCRE },
        paragraph: { spacing: { after: 120, line: INTERLIGNE, lineRule: LineRuleType.AUTO } },
      },
      {
        id: "Titre1", name: "Titre 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: SANS, size: 24, bold: true, color: ROUGE },
        paragraph: { spacing: { before: 220, after: 90 }, outlineLevel: 0, keepNext: true },
      },
    ],
  },
  numbering: {
    config: [{
      reference: "puces",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "▪", alignment: AlignmentType.LEFT,
        style: {
          paragraph: { indent: { left: cm(0.6), hanging: cm(0.4) } },
          run: { color: ROUGE },
        },
      }],
    }],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: cm(1.8), bottom: cm(1.7), left: cm(MARGE), right: cm(MARGE), header: cm(0.9), footer: cm(0.8) },
      },
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: runs("Goffman · *La Mise en scène de la vie quotidienne*", { font: SANS, size: 15, color: GRIS }),
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ children: [PageNumber.CURRENT], font: SANS, size: 16, color: GRIS }),
            new TextRun({ text: " / ", font: SANS, size: 16, color: GRIS }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], font: SANS, size: 16, color: GRIS }),
          ],
        })],
      }),
    },
    children: [...enTete, ...corps, ...references],
  }],
});

const sortie = path.join(__dirname, "..", "Goffman_mise_en_scene_vie_quotidienne.docx");
Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(sortie, buf);
  console.log("OK ->", sortie);
});

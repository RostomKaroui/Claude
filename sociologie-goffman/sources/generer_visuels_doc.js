// Genere le Word des 2 visuels (A4 paysage, une page par visuel + legende de 2 lignes).
// Usage : node rendre_visuels.js visuel1_porte visuel2_dar && node generer_visuels_doc.js
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, AlignmentType, PageOrientation, PageBreak, LineRuleType,
} = require("docx");

const ROUGE = "8C1C13";
const NBSP = " ";
const fr = (s) => s.replace(/ ([:;!?»])/g, NBSP + "$1").replace(/« /g, "«" + NBSP);
const cm = (v) => Math.round(v * 567);
const LARGEUR_PX = Math.round((23.5 / 2.54) * 96); // 23,5 cm a 96 dpi
const HAUTEUR_PX = Math.round(LARGEUR_PX * 2475 / 3500);

const VISUELS = [
  {
    fichier: "visuel1_porte.png",
    titre: "Visuel 1 · Une porte, deux personnages",
    legende: "Orwell, cité par Goffman : le serveur qui hurlait en cuisine passe la porte et devient en un instant solennel « comme un prêtre ». Une simple porte sépare les coulisses de la scène.",
  },
  {
    fichier: "visuel2_dar.png",
    titre: "Visuel 2 · La dar de la médina, une maison qui trie ses publics",
    legende: "Dans la dar de la médina, la driba accueille l'étranger (la scène) et la skifa coudée bloque le regard : le patio reste les coulisses de la famille. L'architecture organise la mise en scène.",
  },
];

const enfants = [];
VISUELS.forEach((v, i) => {
  enfants.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 80 },
    children: [
      ...(i > 0 ? [new PageBreak()] : []),
      new ImageRun({
        type: "png",
        data: fs.readFileSync(path.join(__dirname, "..", v.fichier)),
        transformation: { width: LARGEUR_PX, height: HAUTEUR_PX },
        altText: { title: v.titre, description: v.legende, name: v.fichier },
      }),
    ],
  }));
  enfants.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 0, line: 252, lineRule: LineRuleType.AUTO },
    indent: { left: cm(1), right: cm(1) },
    children: [new TextRun({ text: fr(v.legende), font: "Times New Roman", size: 25 })],
  }));
});

const doc = new Document({
  title: "Goffman · visuels pour le tableau",
  styles: { default: { document: { run: { font: "Times New Roman", size: 24 } } } },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE },
        margin: { top: cm(1.1), bottom: cm(1), left: cm(1.5), right: cm(1.5) },
      },
    },
    children: enfants,
  }],
});

const sortie = path.join(__dirname, "..", "Goffman_visuels_tableau.docx");
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(sortie, b); console.log("OK ->", sortie); });

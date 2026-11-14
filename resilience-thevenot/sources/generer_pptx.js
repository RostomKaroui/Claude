// Genere la presentation PowerPoint « Laurent Thevenot et la resilience psychologique ».
// Usage : NODE_PATH=<dossier node_modules> node generer_pptx.js  ->  ../Resilience_Thevenot.pptx
const path = require("path");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require("/root/.claude/skills/synced/e25176ef-0d6b-426f-88d1-18a43a6852b2_f6f6c202-53e5-4ae9-bc09-471b71e888ab/pptx/scripts/apply_theme.js");
const NOTES = require("./notes.js");

const THEME = {
  name: "Aube",
  headFontFace: "Cambria", bodyFontFace: "Calibri",
  colors: { dk1: "24303F", lt1: "FFFFFF", dk2: "4A5A6A", lt2: "FBF3E6", accent1: "E9A23B", accent2: "5B8E7D", accent3: "D9774C", accent4: "8A97A6", accent5: "3E5C76", accent6: "F6D9A8", hlink: "3E5C76", folHlink: "8A97A6" },
};
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "Laurent Thévenot et la résilience psychologique";
pres.author = "Étudiant·e 1re année Architecture, ESAD Tunis";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

const titrePh = (couleur) => ({ placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.35, w: 9, h: 0.8, fontSize: 32, bold: true, color: couleur, align: "left", valign: "middle", margin: 0 }, text: "" } });
pres.defineSlideMaster({ title: "TITRE", background: { color: C.text1 }, objects: [
  { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 1.1, w: 5.6, h: 2.2, fontSize: 38, bold: true, color: C.background1, align: "left", valign: "bottom", margin: 0 }, text: "" } },
  { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 3.45, w: 5.4, h: 0.9, fontSize: 18, color: C.accent6, align: "left", valign: "top", margin: 0 }, text: "" } },
] });
pres.defineSlideMaster({ title: "CLAIR", background: { color: C.background1 }, objects: [titrePh(C.text1)], slideNumber: { x: 9.0, y: 5.2, w: 0.5, h: 0.3, fontSize: 11, color: C.accent4, align: "right" } });
pres.defineSlideMaster({ title: "SOMBRE", background: { color: C.text1 }, objects: [titrePh(C.background1)], slideNumber: { x: 9.0, y: 5.2, w: 0.5, h: 0.3, fontSize: 11, color: C.accent6, align: "right" } });

const T = (s, texte, o) => s.addText(texte, { isTextBox: true, margin: 0, ...o });
const carte = (s, x, y, w, h, fill, nom, extra = {}) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: fill }, line: { color: fill, width: 0 }, objectName: nom, ...extra });
const rect = (s, x, y, w, h, fill, nom) => s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: fill, width: 0 }, objectName: nom });
const ovale = (s, x, y, w, h, fill, nom, extra = {}) => s.addShape(pres.shapes.OVAL, { x, y, w, h, fill: { color: fill }, line: { color: fill, width: 0 }, objectName: nom, ...extra });
const pastille = (s, x, y, d, texte, fill, couleur, taille, nom) => { ovale(s, x, y, d, d, fill, nom); T(s, texte, { x, y, w: d, h: d, fontSize: taille, bold: true, color: couleur, align: "center", valign: "middle", objectName: nom + " texte" }); };
const personnage = (s, cx, cy, tete, corps, nom, e = 1) => {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: cx - 0.62 * e, y: cy + 0.42 * e, w: 1.24 * e, h: 0.9 * e, rectRadius: 0.35 * e, fill: { color: corps }, line: { color: corps, width: 0 }, objectName: nom + " corps" });
  ovale(s, cx - 0.34 * e, cy - 0.34 * e, 0.68 * e, 0.68 * e, tete, nom + " tête");
};
const maison = (s, x, y, w, h, murs, toit, nom) => {
  rect(s, x, y + h * 0.4, w, h * 0.6, murs, nom + " murs");
  s.addShape(pres.shapes.ISOSCELES_TRIANGLE, { x: x - w * 0.08, y, w: w * 1.16, h: h * 0.42, fill: { color: toit }, line: { color: toit, width: 0 }, objectName: nom + " toit" });
};
const soleil = (s, cx, cy, r, couleur, nom) => {
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * Math.PI * 2;
    s.addShape(pres.shapes.LINE, { x: cx + Math.cos(a) * r * 1.35, y: cy + Math.sin(a) * r * 1.35, w: Math.cos(a) * r * 0.55, h: Math.sin(a) * r * 0.55, line: { color: couleur, width: 2 }, objectName: nom + " rayon " + (i + 1) });
  }
  ovale(s, cx - r, cy - r, 2 * r, 2 * r, couleur, nom);
};
const notes = (s, i) => s.addNotes(`[${NOTES[i].minutes}] ${NOTES[i].texte}\n\nConseil : ${NOTES[i].conseil}`);
const puces = (items, o = {}) => items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1, paraSpaceAfter: 6, ...o } }));
const bandeau = (s, y, h, fond, texte, coul, taille, nom = "Bandeau") => {
  carte(s, 0.5, y, 9, h, fond, nom);
  T(s, texte, { x: 0.75, y, w: 8.5, h, fontSize: taille, color: coul, align: "center", valign: "middle", objectName: "Texte " + nom.toLowerCase() });
};

// ============ 1. TITRE ============
pres.addSection({ title: "Introduction" });
let s = pres.addSlide({ masterName: "TITRE", sectionTitle: "Introduction" });
s.addText("Se relever après l'épreuve : la résilience", { placeholder: "title" });
s.addText("Laurent Thévenot : la vie n'est pas que des épreuves", { placeholder: "body" });
T(s, "Sociologie · 1re année Architecture · ESAD Tunis", { x: 0.6, y: 4.55, w: 5.5, h: 0.3, fontSize: 14, color: C.background1, objectName: "Classe" });
T(s, "Présenté par : [ton nom]", { x: 0.6, y: 4.9, w: 5.5, h: 0.3, fontSize: 14, color: C.accent1, objectName: "Auteur" });
// illustration : soleil levant sur une courbe de remontee
rect(s, 6.4, 4.6, 3.4, 0.05, C.accent4, "Horizon");
soleil(s, 8.2, 2.2, 0.55, C.accent1, "Soleil");
for (let i = 0; i < 16; i++) {
  const t = i / 15, x = 6.5 + t * 2.9;
  const y = t < 0.2 ? 3.7 : t < 0.35 ? 3.7 + 0.6 * (1 - Math.cos(((t - 0.2) / 0.15) * Math.PI / 2)) : 4.3 - 0.9 * (1 - Math.exp(-(t - 0.35) * 4.5)) / (1 - Math.exp(-2.9));
  ovale(s, x - 0.05, y - 0.05, 0.1, 0.1, C.accent6, "Point courbe " + (i + 1));
}
notes(s, 0);

// ============ 2. PROBLEMATIQUE ============
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "Introduction" });
s.addText("Notre problématique", { placeholder: "title" });
carte(s, 0.5, 1.35, 9, 1.35, C.text1, "Question centrale");
T(s, [{ text: "Si la vie ne comporte pas que des épreuves, ", options: { color: C.accent6 } }, { text: "comment se relever après un événement malheureux ?", options: { bold: true, color: C.background1 } }], { x: 0.8, y: 1.35, w: 8.4, h: 1.35, fontSize: 22, valign: "middle", objectName: "Texte question" });
[["Qui est Thévenot ?", "Ses idées : épreuves et régimes d'engagement"], ["Qu'est-ce que la résilience ?", "Définition et étude de Kauai"], ["Comment se relever ?", "Ce qui aide, 5 étapes concrètes"], ["Et pour l'architecte ?", "L'espace comme appui"]].forEach(([q, d], i) => {
  const x = 0.5 + i * 2.28;
  carte(s, x, 2.95, 2.15, 2.1, C.background2, "Étape " + (i + 1));
  pastille(s, x + 0.15, 3.1, 0.5, String(i + 1), i === 3 ? C.accent3 : C.accent2, C.background1, 18, "Numéro " + (i + 1));
  T(s, [{ text: q, options: { bold: true, fontSize: 16, breakLine: true } }, { text: d, options: { fontSize: 14 } }], { x: x + 0.15, y: 3.75, w: 1.9, h: 1.2, color: C.text1, valign: "top", objectName: "Texte étape " + (i + 1) });
});
notes(s, 1);

// ============ 3. THEVENOT ============
pres.addSection({ title: "Laurent Thévenot" });
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "Laurent Thévenot" });
s.addText("Qui est Laurent Thévenot ?", { placeholder: "title" });
carte(s, 0.5, 1.4, 3.3, 2.75, C.text1, "Carte portrait");
personnage(s, 2.15, 2.05, C.accent6, C.accent1, "Portrait", 0.8);
T(s, [{ text: "Laurent Thévenot", options: { bold: true, fontSize: 19, color: C.accent1, breakLine: true } }, { text: "Sociologue français · EHESS", options: { fontSize: 14, color: C.background1, breakLine: true } }, { text: "Sociologie pragmatique", options: { fontSize: 14, color: C.accent6 } }], { x: 0.7, y: 3.3, w: 2.9, h: 0.8, align: "center", valign: "top", objectName: "Texte portrait" });
[["De la justification (1991)", "Avec Luc Boltanski. Comment les gens justifient leurs actes et sont mis à l'épreuve.", C.accent2, 1.4], ["L'Action au pluriel (2006)", "On n'agit pas toujours de la même façon : plusieurs régimes d'engagement.", C.accent5, 2.8]].forEach(([t, d, fond, y]) => {
  carte(s, 4.1, y, 5.4, 1.3, fond, "Livre " + t);
  T(s, [{ text: t, options: { bold: true, fontSize: 17, breakLine: true } }, { text: d, options: { fontSize: 14 } }], { x: 4.35, y, w: 4.95, h: 1.3, color: C.background1, valign: "middle", objectName: "Texte livre " + t });
});
bandeau(s, 4.35, 0.7, C.background2, "Son point de départ : observer comment les personnes agissent dans des situations concrètes.", C.text1, 15);
notes(s, 2);

// ============ 4. DEUX SENS D'EPREUVE ============
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "Laurent Thévenot" });
s.addText("Deux sens du mot « épreuve »", { placeholder: "title" });
[["CHEZ THÉVENOT", C.accent5, C.background1, "Un moment où l'on est mis à l'essai : examen, entretien, dispute.", "On doit montrer sa valeur ou se justifier.", 0.5], ["DANS NOTRE SUJET", C.accent1, C.text1, "Un événement douloureux : deuil, échec, accident, rupture.", "On doit le traverser et se relever.", 5.1]].forEach(([t, fond, coul, d1, d2, x]) => {
  carte(s, x, 1.4, 4.4, 2.65, fond, "Carte " + t);
  T(s, t, { x: x + 0.3, y: 1.55, w: 3.8, h: 0.4, fontSize: 15, bold: true, color: coul, objectName: "Étiquette " + t });
  T(s, [{ text: d1, options: { bold: true, fontSize: 20, breakLine: true, paraSpaceAfter: 10 } }, { text: d2, options: { fontSize: 16 } }], { x: x + 0.3, y: 2.05, w: 3.8, h: 1.9, color: coul, valign: "top", objectName: "Texte " + t });
});
pastille(s, 4.7, 2.5, 0.6, "≠", C.text1, C.background1, 22, "Différent");
bandeau(s, 4.25, 0.8, C.background2, "Le rapprochement entre les deux sens est notre interprétation : l'objectif est de comprendre comment traverser une épreuve.", C.text1, 15);
notes(s, 3);

// ============ 5. REGIMES D'ENGAGEMENT ============
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "Laurent Thévenot" });
s.addText("La vie n'est pas que des épreuves", { placeholder: "title" });
T(s, "Trois façons d'être engagé dans une situation (les « régimes d'engagement »)", { x: 0.5, y: 1.2, w: 9, h: 0.35, fontSize: 15, italic: true, color: C.text2, objectName: "Sous-titre" });
[["FAMILIARITÉ", "L'aise", "Habitudes, objets, lieux et proches qu'on connaît : on se sent bien.", C.accent1, C.text1], ["PLAN", "Les projets", "Viser un but, se réaliser : réussir ses études, construire un métier.", C.accent2, C.background1], ["JUSTIFICATION", "Se justifier", "Rendre des comptes, argumenter, être reconnu publiquement.", C.accent5, C.background1]].forEach(([t, sous, d, fond, coul], i) => {
  const x = 0.5 + i * 3.05;
  carte(s, x, 1.7, 2.9, 2.55, fond, "Carte " + t);
  T(s, t, { x: x + 0.25, y: 1.85, w: 2.4, h: 0.3, fontSize: 13, bold: true, color: coul, objectName: "Étiquette " + t });
  T(s, sous, { x: x + 0.25, y: 2.2, w: 2.4, h: 0.5, fontSize: 22, bold: true, color: coul, objectName: "Titre " + t });
  T(s, d, { x: x + 0.25, y: 2.8, w: 2.45, h: 1.35, fontSize: 15, color: coul, valign: "top", objectName: "Texte " + t });
});
bandeau(s, 4.4, 0.7, C.text1, "Notre lecture : la vie alterne entre ces trois manières d'être, elle n'est pas une suite d'épreuves.", C.background1, 15);
notes(s, 4);

// ============ 6. RESILIENCE : DEFINITION ============
pres.addSection({ title: "La résilience" });
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "La résilience" });
s.addText("La résilience : définition", { placeholder: "title" });
carte(s, 0.5, 1.4, 4.4, 3.0, C.background2, "Carte définition");
T(s, "DÉFINITION", { x: 0.75, y: 1.55, w: 3.9, h: 0.3, fontSize: 12, bold: true, color: C.accent3, objectName: "Étiquette définition" });
T(s, [{ text: "Se reconstruire et continuer à se développer malgré une épreuve.", options: { bold: true, fontSize: 20, breakLine: true, paraSpaceAfter: 10 } }, { text: "Mot venu de la physique : un matériau qui reprend sa forme après un choc.", options: { fontSize: 14, breakLine: true, paraSpaceAfter: 6 } }, { text: "Popularisé en France par Boris Cyrulnik, neuropsychiatre.", options: { fontSize: 14 } }], { x: 0.75, y: 1.9, w: 3.9, h: 2.4, color: C.text1, valign: "top", objectName: "Texte définition" });
// schema : courbe de resilience
carte(s, 5.1, 1.4, 4.4, 3.0, C.text1, "Fond schéma");
T(s, "Trajectoire d'une personne", { x: 5.3, y: 1.5, w: 4.0, h: 0.3, fontSize: 12, bold: true, color: C.accent6, objectName: "Titre schéma" });
s.addShape(pres.shapes.LINE, { x: 5.35, y: 2.0, w: 0, h: 2.1, line: { color: C.accent4, width: 1.5 }, objectName: "Axe vertical" });
s.addShape(pres.shapes.LINE, { x: 5.35, y: 4.1, w: 3.9, h: 0, line: { color: C.accent4, width: 1.5 }, objectName: "Axe horizontal" });
s.addShape(pres.shapes.LINE, { x: 5.35, y: 2.75, w: 3.9, h: 0, line: { color: C.accent4, width: 1, dashType: "dash" }, objectName: "Niveau initial" });
const courbe = (t) => {
  if (t < 0.22) return 2.75;
  if (t < 0.38) { const u = (t - 0.22) / 0.16; return 2.75 + 1.1 * (1 - Math.cos(u * Math.PI / 2)); }
  const u = (t - 0.38) / 0.62; return 3.85 - 1.6 * (1 - Math.exp(-u * 3)) / (1 - Math.exp(-3));
};
for (let i = 0; i <= 38; i++) { const t = i / 38; ovale(s, 5.45 + t * 3.6 - 0.04, courbe(t) - 0.04, 0.08, 0.08, t < 0.38 ? C.accent3 : C.accent1, "Point " + (i + 1)); }
T(s, "Avant", { x: 5.45, y: 2.35, w: 0.9, h: 0.3, fontSize: 12, bold: true, color: C.background1, objectName: "Étiquette avant" });
T(s, "Choc", { x: 5.75, y: 3.7, w: 0.95, h: 0.3, fontSize: 13, bold: true, color: C.accent3, align: "right", objectName: "Étiquette choc" });
T(s, "Se relever", { x: 7.25, y: 3.6, w: 1.2, h: 0.3, fontSize: 13, bold: true, color: C.accent1, objectName: "Étiquette remontée" });
T(s, "Après : transformé", { x: 7.6, y: 1.85, w: 1.7, h: 0.3, fontSize: 12, bold: true, color: C.background1, align: "right", objectName: "Étiquette après" });
bandeau(s, 4.55, 0.55, C.accent6, "Résilient ne veut pas dire : sans souffrance, sans cicatrice, ni seul.", C.text1, 15);
notes(s, 5);

// ============ 7. WERNER ============
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "La résilience" });
s.addText("L'étude de Kauai (Werner)", { placeholder: "title" });
carte(s, 0.5, 1.4, 4.3, 3.0, C.text1, "Carte chiffres");
T(s, "ÎLE DE KAUAI (HAWAÏ) · SUIVI DEPUIS 1955", { x: 0.75, y: 1.55, w: 3.8, h: 0.3, fontSize: 12, bold: true, color: C.accent6, objectName: "Étiquette chiffres" });
T(s, "698", { x: 0.7, y: 1.9, w: 1.9, h: 0.9, fontSize: 52, bold: true, color: C.accent1, align: "center", valign: "middle", objectName: "Chiffre 698" });
T(s, "enfants nés en 1955, suivis pendant des décennies", { x: 2.65, y: 1.95, w: 2.0, h: 0.85, fontSize: 14, color: C.background1, valign: "middle", objectName: "Texte 698" });
T(s, "≈ 1/3", { x: 0.7, y: 3.05, w: 1.9, h: 0.9, fontSize: 44, bold: true, color: C.accent1, align: "center", valign: "middle", objectName: "Chiffre un tiers" });
T(s, "des enfants à haut risque sont devenus des adultes équilibrés", { x: 2.65, y: 3.05, w: 2.0, h: 0.9, fontSize: 14, color: C.background1, valign: "middle", objectName: "Texte un tiers" });
T(s, "Qu'est-ce qui les distinguait ?", { x: 5.1, y: 1.4, w: 4.4, h: 0.4, fontSize: 18, bold: true, color: C.text1, objectName: "Question facteurs" });
[["Un adulte attentionné", "au moins une relation stable, pas forcément un parent"], ["Le soutien de l'entourage", "école, voisinage, communauté"]].forEach(([t, d], i) => {
  const y = 1.9 + i * 1.25;
  carte(s, 5.1, y, 4.4, 1.15, C.background2, "Facteur " + (i + 1));
  pastille(s, 5.25, y + 0.3, 0.5, String(i + 1), C.accent2, C.background1, 18, "Numéro facteur " + (i + 1));
  T(s, [{ text: t, options: { bold: true, fontSize: 17, breakLine: true } }, { text: d, options: { fontSize: 14 } }], { x: 5.95, y, w: 3.45, h: 1.15, color: C.text1, valign: "middle", objectName: "Texte facteur " + (i + 1) });
});
bandeau(s, 4.55, 0.55, C.accent6, "La résilience se construit avec les autres. · Werner et Smith, 1982 et 1992", C.text1, 15);
notes(s, 6);

// ============ 8. CE QUI AIDE ============
pres.addSection({ title: "Se relever" });
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "Se relever" });
s.addText("Ce qui aide à se relever", { placeholder: "title" });
[["Des relations", "Famille, amis, groupe : le soutien des autres.", C.accent2, C.background1], ["La confiance", "Croire qu'on peut résoudre ses problèmes.", C.accent5, C.background1], ["Des activités saines", "Sport, art, écriture, rituels qui font du bien.", C.accent6, C.text1], ["Apprendre du passé", "Qu'est-ce qui m'a aidé la dernière fois ?", C.background2, C.text1]].forEach(([t, d, fond, coul], i) => {
  const x = 0.5 + (i % 2) * 3.0, y = 1.4 + Math.floor(i / 2) * 1.6;
  carte(s, x, y, 2.85, 1.5, fond, "Carte " + t);
  T(s, [{ text: t, options: { bold: true, fontSize: 18, breakLine: true } }, { text: d, options: { fontSize: 14 } }], { x: x + 0.2, y, w: 2.5, h: 1.5, color: coul, valign: "middle", objectName: "Texte " + t });
});
carte(s, 6.7, 1.4, 2.8, 3.1, C.text1, "Carte tuteur");
T(s, "SELON CYRULNIK", { x: 6.9, y: 1.55, w: 2.4, h: 0.3, fontSize: 12, bold: true, color: C.accent6, objectName: "Étiquette Cyrulnik" });
T(s, "Le tuteur de résilience", { x: 6.9, y: 1.9, w: 2.4, h: 0.8, fontSize: 20, bold: true, color: C.accent1, objectName: "Titre tuteur" });
T(s, "Une personne, un lieu ou une activité autour desquels on se reconstruit, comme un jeune arbre s'appuie sur son tuteur.", { x: 6.9, y: 2.75, w: 2.4, h: 1.7, fontSize: 14, color: C.background1, valign: "top", objectName: "Texte tuteur" });
T(s, "Sources : American Psychological Association (« The Road to Resilience ») · Cyrulnik, Un merveilleux malheur (1999)", { x: 0.5, y: 4.7, w: 9, h: 0.4, fontSize: 11, italic: true, color: C.accent4, objectName: "Sources diapo" });
notes(s, 7);

// ============ 9. CINQ ETAPES ============
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "Se relever" });
s.addText("Se relever : 5 étapes", { placeholder: "title" });
const etapes = [["Reconnaître le choc", "Accepter que ça fait mal, sans se juger.", C.accent3, C.text1], ["Ne pas rester seul", "Parler à une personne de confiance.", C.accent1, C.text1], ["Retrouver des repères", "Routines : dormir, manger, bouger, voir du monde.", C.accent6, C.text1], ["De petits objectifs", "Pas de grands projets : le prochain pas.", C.accent2, C.background1], ["Donner un sens", "En parler, écrire, se demander ce qu'on a appris.", C.accent5, C.background1]];
etapes.forEach(([t, d, fond, coul], i) => {
  const x = 0.5 + i * 1.82, h = 2.3 + i * 0.2, y = 4.35 - h;
  carte(s, x, y, 1.7, h, fond, "Marche " + (i + 1));
  pastille(s, x + 0.15, y + 0.15, 0.45, String(i + 1), coul === C.background1 ? C.accent6 : C.text1, coul === C.background1 ? C.text1 : C.background1, 16, "Numéro marche " + (i + 1));
  T(s, [{ text: t, options: { bold: true, fontSize: 15, breakLine: true, paraSpaceAfter: 4 } }, { text: d, options: { fontSize: 13 } }], { x: x + 0.15, y: y + 0.7, w: 1.4, h: h - 0.8, color: coul, valign: "top", objectName: "Texte marche " + (i + 1) });
});
bandeau(s, 4.5, 0.6, C.background2, "Si la détresse dure ou devient trop lourde : demander l'aide d'un professionnel (médecin, psychologue).", C.text1, 14);
notes(s, 8);

// ============ 10. THEVENOT <-> RESILIENCE ============
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "Se relever" });
s.addText("Thévenot et résilience : notre lecture", { placeholder: "title", options: { fontSize: 30 } });
T(s, "Les trois régimes d'engagement comme ressources après le choc", { x: 0.5, y: 1.2, w: 9, h: 0.35, fontSize: 15, italic: true, color: C.text2, objectName: "Sous-titre" });
[["FAMILIARITÉ", "Retrouver de l'aise : habitudes, proches, lieux connus", "étape 3", C.accent1, C.text1], ["PLAN", "Se redonner des objectifs, même petits", "étape 4", C.accent2, C.background1], ["JUSTIFICATION", "Mettre des mots, donner un sens, être reconnu", "étape 5", C.accent5, C.background1]].forEach(([r, d, e, fond, coul], i) => {
  const y = 1.7 + i * 0.9;
  carte(s, 0.5, y, 2.6, 0.8, fond, "Régime " + r);
  T(s, r, { x: 0.5, y, w: 2.6, h: 0.8, fontSize: 16, bold: true, color: coul, align: "center", valign: "middle", objectName: "Texte régime " + r });
  T(s, "→", { x: 3.15, y, w: 0.4, h: 0.8, fontSize: 22, bold: true, color: C.accent4, align: "center", valign: "middle", objectName: "Flèche " + (i + 1) });
  carte(s, 3.6, y, 4.6, 0.8, C.background2, "Effet " + r);
  T(s, d, { x: 3.8, y, w: 4.2, h: 0.8, fontSize: 15, color: C.text1, valign: "middle", objectName: "Texte effet " + r });
  carte(s, 8.3, y, 1.2, 0.8, C.accent6, "Étape " + r);
  T(s, e, { x: 8.3, y, w: 1.2, h: 0.8, fontSize: 14, bold: true, color: C.text1, align: "center", valign: "middle", objectName: "Texte étape " + r });
});
bandeau(s, 4.45, 0.65, C.text1, "Un rapprochement de notre part, pas une citation : à notre connaissance, Thévenot n'emploie pas « résilience » au sens de Cyrulnik.", C.background1, 13.5);
notes(s, 9);

// ============ 11. L'ARCHITECTE ============
pres.addSection({ title: "Conclusion" });
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "Conclusion" });
s.addText("Et l'architecte dans tout ça ?", { placeholder: "title" });
const iconeCartes = [
  ["Des lieux familiers", "Repères, matières, odeurs : retrouver l'aise", C.accent6, (cx, cy) => { maison(s, cx - 0.4, cy - 0.35, 0.8, 0.8, C.background1, C.accent3, "Icône maison"); }],
  ["Des lieux pour se retrouver", "Places, cours, bancs : le soutien des autres", C.background2, (cx, cy) => { personnage(s, cx - 0.35, cy - 0.35, C.accent3, C.accent5, "Icône 1", 0.32); personnage(s, cx + 0.35, cy - 0.35, C.accent1, C.accent2, "Icône 2", 0.32); }],
  ["Lumière et nature", "Patio, jardin, arbre : un cadre qui apaise", C.accent6, (cx, cy) => { soleil(s, cx - 0.2, cy - 0.15, 0.2, C.accent1, "Icône soleil"); rect(s, cx + 0.32, cy + 0.0, 0.08, 0.4, C.accent5, "Icône tronc"); ovale(s, cx + 0.12, cy - 0.4, 0.5, 0.5, C.accent2, "Icône feuillage"); }],
  ["Des coins calmes", "Pouvoir se retirer quand on en a besoin", C.background2, (cx, cy) => { rect(s, cx - 0.4, cy + 0.1, 0.8, 0.3, C.accent5, "Icône banc assise"); rect(s, cx - 0.4, cy - 0.25, 0.8, 0.32, C.accent4, "Icône banc dossier"); }],
];
iconeCartes.forEach(([t, d, fond, icone], i) => {
  const x = 0.5 + i * 2.28;
  carte(s, x, 1.4, 2.15, 2.9, fond, "Carte " + t);
  icone(x + 1.075, 2.15);
  T(s, [{ text: t, options: { bold: true, fontSize: 16, breakLine: true, paraSpaceAfter: 4 } }, { text: d, options: { fontSize: 14 } }], { x: x + 0.15, y: 2.85, w: 1.85, h: 1.4, color: C.text1, align: "center", valign: "top", objectName: "Texte " + t });
});
bandeau(s, 4.45, 0.6, C.text1, "Notre idée, pas une citation : l'espace peut être un « tuteur de résilience ».", C.background1, 16);
notes(s, 10);

// ============ 12. CONCLUSION ============
s = pres.addSlide({ masterName: "SOMBRE", sectionTitle: "Conclusion" });
s.addText("Conclusion", { placeholder: "title" });
T(s, "On se relève pas à pas, et rarement seul.", { x: 0.5, y: 1.25, w: 9, h: 0.55, fontSize: 24, bold: true, color: C.accent1, objectName: "Phrase clé" });
["La vie n'est pas que des épreuves : aise, projets et reconnaissance sont des ressources", "La résilience : se reconstruire après un choc, avec les autres", "Repères, petits objectifs, sens, et de l'aide quand il le faut"].forEach((t, i) => {
  const y = 2.0 + i * 0.7;
  pastille(s, 0.5, y + 0.05, 0.5, String(i + 1), C.accent1, C.text1, 18, "Numéro " + (i + 1));
  T(s, t, { x: 1.25, y, w: 8.25, h: 0.6, fontSize: 18, color: C.background1, valign: "middle", objectName: "Idée " + (i + 1) });
});
T(s, "Merci ! Des questions ?", { x: 0.5, y: 4.15, w: 9, h: 0.4, fontSize: 22, bold: true, color: C.accent1, objectName: "Merci" });
T(s, "Sources : Boltanski et Thévenot, De la justification (1991) · Thévenot, L'Action au pluriel (2006) · Cyrulnik, Un merveilleux malheur (1999) · Werner et Smith, Vulnerable but Invincible (1982), Overcoming the Odds (1992) · American Psychological Association, The Road to Resilience", { x: 0.5, y: 4.65, w: 9, h: 0.55, fontSize: 10, color: C.accent6, valign: "top", objectName: "Sources" });
notes(s, 11);

(async () => {
  const sortie = path.join(__dirname, "..", "Resilience_Thevenot.pptx");
  await pres.writeFile({ fileName: sortie });
  await applyTheme(sortie, THEME);
  console.log("OK ->", sortie);
})();

// Genere la presentation PowerPoint « L'effet de halo » (Thorndike).
// Usage : node generer_pptx.js  ->  ../Thorndike_effet_de_halo.pptx
const path = require("path");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require("/root/.claude/skills/synced/e25176ef-0d6b-426f-88d1-18a43a6852b2_f6f6c202-53e5-4ae9-bc09-471b71e888ab/pptx/scripts/apply_theme.js");
const NOTES = require("./notes.js");

const THEME = {
  name: "Halo",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: { dk1: "14213D", lt1: "FFFFFF", dk2: "3B4A6B", lt2: "F1F4FA", accent1: "F2B705", accent2: "B5303A", accent3: "2F6690", accent4: "6B7A99", accent5: "2A9D8F", accent6: "FFE08A", hlink: "2F6690", folHlink: "6B7A99" },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";           // 10 x 5.625 po
pres.title = "L'effet de halo : Edward Thorndike";
pres.author = "Étudiant·e 1re année Architecture, ESAD Tunis";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

// ---------- layouts ----------
const titreContenu = (couleur) => ({ placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.35, w: 9, h: 0.8, fontSize: 32, bold: true, color: couleur, align: "left", valign: "middle", margin: 0 }, text: "" } });
pres.defineSlideMaster({ title: "TITRE", background: { color: C.text1 }, objects: [
  { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 1.55, w: 5.4, h: 1.5, fontSize: 48, bold: true, color: C.background1, align: "left", valign: "bottom", margin: 0 }, text: "" } },
  { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 3.2, w: 5.2, h: 0.9, fontSize: 20, color: C.accent6, align: "left", valign: "top", margin: 0 }, text: "" } },
] });
pres.defineSlideMaster({ title: "CLAIR", background: { color: C.background1 }, objects: [titreContenu(C.text1)], slideNumber: { x: 9.0, y: 5.2, w: 0.5, h: 0.3, fontSize: 11, color: C.accent4, align: "right" } });
pres.defineSlideMaster({ title: "SOMBRE", background: { color: C.text1 }, objects: [titreContenu(C.background1)], slideNumber: { x: 9.0, y: 5.2, w: 0.5, h: 0.3, fontSize: 11, color: C.accent6, align: "right" } });

// ---------- helpers ----------
const T = (s, texte, o) => s.addText(texte, { isTextBox: true, margin: 0, ...o });
const carte = (s, x, y, w, h, fill, nom, extra = {}) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: fill }, line: { color: fill, width: 0 }, objectName: nom, ...extra });
const pastille = (s, x, y, d, texte, fill, couleur, taille, nom) => {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: fill, width: 0 }, objectName: nom });
  T(s, texte, { x, y, w: d, h: d, fontSize: taille, bold: true, color: couleur, align: "center", valign: "middle", objectName: nom + " texte" });
};
const personnage = (s, cx, cy, tete, corps, nom, echelle = 1) => {
  const r = 0.34 * echelle;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: cx - 0.62 * echelle, y: cy + 0.42 * echelle, w: 1.24 * echelle, h: 0.9 * echelle, rectRadius: 0.35 * echelle, fill: { color: corps }, line: { color: corps, width: 0 }, objectName: nom + " corps" });
  s.addShape(pres.shapes.OVAL, { x: cx - r, y: cy - r, w: 2 * r, h: 2 * r, fill: { color: tete }, line: { color: tete, width: 0 }, objectName: nom + " tête" });
};
const notes = (s, i) => s.addNotes(`[${NOTES[i].minutes}] ${NOTES[i].texte}\n\nConseil : ${NOTES[i].conseil}`);
const puces = (items, o = {}) => items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1, paraSpaceAfter: 7, ...o } }));

// ================= 1. TITRE =================
pres.addSection({ title: "Introduction" });
let s = pres.addSlide({ masterName: "TITRE", sectionTitle: "Introduction" });
s.addText("L'effet de halo", { placeholder: "title" });
s.addText("Edward Thorndike et le biais de l'impression générale", { placeholder: "body" });
T(s, "Psychologie · 1re année Architecture · ESAD Tunis", { x: 0.6, y: 4.55, w: 6, h: 0.3, fontSize: 14, color: C.background1, objectName: "Classe" });
T(s, "Présenté par : [ton nom]", { x: 0.6, y: 4.9, w: 6, h: 0.3, fontSize: 14, color: C.accent6, objectName: "Auteur" });
// illustration : une personne avec une auréole
s.addShape(pres.shapes.OVAL, { x: 6.55, y: 1.15, w: 2.6, h: 1.1, fill: { color: C.accent1, transparency: 85 }, line: { color: C.accent1, width: 0 }, objectName: "Lueur large" });
s.addShape(pres.shapes.OVAL, { x: 6.9, y: 1.35, w: 1.9, h: 0.75, fill: { color: C.accent1, transparency: 70 }, line: { color: C.accent1, width: 0 }, objectName: "Lueur" });
personnage(s, 7.85, 2.9, C.background2, C.accent4, "Silhouette", 1.5);
s.addShape(pres.shapes.OVAL, { x: 7.1, y: 1.72, w: 1.5, h: 0.42, fill: { type: "none" }, line: { color: C.accent1, width: 6 }, objectName: "Halo" });
notes(s, 0);

// ================= 2. PLAN =================
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "Introduction" });
s.addText("Au programme", { placeholder: "title" });
["Qui est Thorndike ?", "Sa découverte : l'effet de halo", "Un exemple précis : l'expérience de 1977", "Dans la vie… et en architecture"].forEach((t, i) => {
  const y = 1.45 + i * 0.9;
  carte(s, 0.5, y, 9, 0.72, C.background2, "Ligne " + (i + 1));
  pastille(s, 0.68, y + 0.1, 0.52, String(i + 1), C.accent1, C.text1, 20, "Numéro " + (i + 1));
  T(s, t, { x: 1.5, y, w: 7.8, h: 0.72, fontSize: 22, bold: true, color: C.text1, valign: "middle", objectName: "Titre ligne " + (i + 1) });
});
notes(s, 1);

// ================= 3. QUI EST THORNDIKE =================
pres.addSection({ title: "Thorndike" });
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "Thorndike" });
s.addText("Qui est Thorndike ?", { placeholder: "title" });
s.addShape(pres.shapes.LINE, { x: 0.9, y: 2.35, w: 8.2, h: 0, line: { color: C.accent4, width: 2.5 }, objectName: "Frise" });
[["1874", "Naît à Williamsburg (Massachusetts)"], ["1898", "Thèse « Animal Intelligence » à Columbia"], ["1899", "Entre à Teachers College (Columbia)"], ["1920", "Publie l'article sur l'effet de halo"], ["1949", "Décède aux États-Unis"]].forEach(([an, txt], i) => {
  const cx = 1.5 + i * 1.75;
  T(s, an, { x: cx - 0.85, y: 1.55, w: 1.7, h: 0.5, fontSize: 24, bold: true, color: i === 3 ? C.accent2 : C.accent3, align: "center", valign: "middle", objectName: "Année " + an });
  s.addShape(pres.shapes.OVAL, { x: cx - 0.17, y: 2.18, w: 0.34, h: 0.34, fill: { color: i === 3 ? C.accent2 : C.accent1 }, line: { color: C.background1, width: 2 }, objectName: "Repère " + an });
  T(s, txt, { x: cx - 0.85, y: 2.7, w: 1.7, h: 1.05, fontSize: 14, color: C.text2, align: "center", valign: "top", objectName: "Texte " + an });
});
carte(s, 0.5, 3.95, 4.4, 1.1, C.background2, "Carte père");
T(s, [{ text: "Psychologue américain", options: { bold: true, breakLine: true } }, { text: "surnommé le « père de la psychologie de l'éducation »" }], { x: 0.7, y: 3.95, w: 4.0, h: 1.1, fontSize: 15, color: C.text1, valign: "middle", objectName: "Texte père" });
carte(s, 5.1, 3.95, 4.4, 1.1, C.background2, "Carte idée");
T(s, [{ text: "Idée clé : le connexionnisme", options: { bold: true, breakLine: true } }, { text: "apprendre, c'est relier une situation à une réponse" }], { x: 5.3, y: 3.95, w: 4.0, h: 1.1, fontSize: 15, color: C.text1, valign: "middle", objectName: "Texte idée" });
notes(s, 2);

// ================= 4. LOI DE L'EFFET =================
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "Thorndike" });
s.addText("La loi de l'effet", { placeholder: "title" });
["Un chat est enfermé dans une « boîte-problème »", "Il essaie plein de gestes : des essais et des erreurs", "Un geste ouvre la porte : il sort et mange", "À chaque essai, il s'échappe plus vite"].forEach((t, i) => {
  const x = 0.5 + i * 2.3;
  carte(s, x, 1.4, 2.1, 2.15, C.background2, "Étape " + (i + 1));
  pastille(s, x + 0.15, 1.55, 0.5, String(i + 1), C.accent3, C.background1, 18, "Numéro étape " + (i + 1));
  T(s, t, { x: x + 0.15, y: 2.2, w: 1.8, h: 1.25, fontSize: 15, color: C.text1, valign: "top", objectName: "Texte étape " + (i + 1) });
});
carte(s, 0.5, 3.8, 9, 1.25, C.accent1, "Encadré loi");
T(s, [{ text: "LOI DE L'EFFET", options: { bold: true, fontSize: 12, breakLine: true } }, { text: "Un comportement suivi d'un résultat agréable a plus de chances de se répéter.", options: { bold: true, fontSize: 22 } }], { x: 0.8, y: 3.8, w: 8.4, h: 1.25, color: C.text1, valign: "middle", objectName: "Texte loi" });
notes(s, 3);

// ================= 5. DECOUVERTE 1920 =================
pres.addSection({ title: "L'effet de halo" });
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "L'effet de halo" });
s.addText("1920 : une découverte dans l'armée", { placeholder: "title" });
T(s, puces([
  "Article « A Constant Error in Psychological Ratings » (1920)",
  "Des supérieurs notent des officiers américains : physique, intelligence, leadership, qualités personnelles",
  "Surprise : les notes se ressemblent trop. Elles sont trop élevées et trop régulières pour être réelles",
  "Conclusion : les juges se laissent guider par une impression générale",
]), { x: 0.5, y: 1.4, w: 4.4, h: 3.7, fontSize: 16, color: C.text1, valign: "top", objectName: "Texte découverte" });
[[5.05, 3.0, "Intelligence", 1.4], [8.0, 3.0, "Qualités personnelles", 1.5], [6.55, 1.4, "Physique", 1.4], [6.55, 4.4, "Leadership", 1.4]].forEach(([x, y, t, w], i) => {
  const cx = 7.25;
  const horiz = i < 2;
  if (horiz) s.addShape(pres.shapes.LINE, { x: i === 0 ? x + w : cx + 0.65, y: 3.33, w: i === 0 ? cx - 0.65 - (x + w) : x - (cx + 0.65), h: 0, line: { color: C.accent4, width: 2 }, objectName: "Lien " + t });
  else s.addShape(pres.shapes.LINE, { x: cx, y: i === 2 ? y + 0.66 : 3.85, w: 0, h: i === 2 ? 2.55 - (y + 0.66) : y - 3.85, line: { color: C.accent4, width: 2 }, objectName: "Lien " + t });
  carte(s, horiz ? x : cx - w / 2, y, w, 0.66, C.accent3, "Qualité " + t);
  T(s, t.replace(" ", "\n"), { x: horiz ? x : cx - w / 2, y, w, h: 0.66, fontSize: 14, bold: true, color: C.background1, align: "center", valign: "middle", objectName: "Texte " + t });
});
s.addShape(pres.shapes.OVAL, { x: 6.6, y: 2.55, w: 1.3, h: 1.3, fill: { color: C.accent1 }, line: { color: C.accent1, width: 0 }, objectName: "Impression générale" });
T(s, "Impression\ngénérale", { x: 6.6, y: 2.55, w: 1.3, h: 1.3, fontSize: 14, bold: true, color: C.text1, align: "center", valign: "middle", objectName: "Texte impression" });
notes(s, 4);

// ================= 6. DEFINITION =================
s = pres.addSlide({ masterName: "SOMBRE", sectionTitle: "L'effet de halo" });
s.addText("L'effet de halo : définition", { placeholder: "title" });
T(s, [
  { text: "Un seul trait", options: { bold: true, color: C.accent1 } },
  { text: " d'une personne (beauté, sympathie, belle présentation…) " },
  { text: "colore le jugement", options: { bold: true, color: C.accent1 } },
  { text: " que l'on porte sur " },
  { text: "tous ses autres traits.", options: { bold: true, color: C.accent1 } },
], { x: 0.5, y: 1.45, w: 5.0, h: 2.6, fontSize: 24, color: C.background1, valign: "top", objectName: "Définition" });
T(s, "Halo = l'auréole des saints dans la peinture : une lumière qui fait paraître la personne parfaite.", { x: 0.5, y: 4.2, w: 5.0, h: 0.8, fontSize: 14, italic: true, color: C.accent6, valign: "top", objectName: "Origine du mot" });
carte(s, 5.85, 1.45, 3.65, 1.6, C.accent1, "Carte positive");
T(s, [{ text: "Effet de halo positif", options: { bold: true, fontSize: 17, breakLine: true } }, { text: "« Il est beau, donc il doit être intelligent, honnête et compétent. »", options: { fontSize: 14 } }], { x: 6.05, y: 1.45, w: 3.25, h: 1.6, color: C.text1, valign: "middle", objectName: "Texte positif" });
carte(s, 5.85, 3.3, 3.65, 1.6, C.accent2, "Carte négative");
T(s, [{ text: "L'effet inverse", options: { bold: true, fontSize: 17, breakLine: true } }, { text: "Un défaut qui se voit, et tout le reste est jugé plus sévèrement.", options: { fontSize: 14 } }], { x: 6.05, y: 3.3, w: 3.25, h: 1.6, color: C.background1, valign: "middle", objectName: "Texte négatif" });
notes(s, 5);

// ================= 7. EXEMPLE : SETUP =================
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "L'effet de halo" });
s.addText("L'exemple : Nisbett et Wilson, 1977", { placeholder: "title" });
[["Vidéo A", "chaleureux, sympathique", 0.5, C.accent6, C.accent1, C.text1], ["Vidéo B", "froid, distant", 2.95, C.accent4, C.accent4, C.background1]].forEach(([titre, sous, x, fond, corps, couleur], i) => {
  carte(s, x, 1.45, 2.25, 1.85, fond, "Écran " + titre);
  T(s, titre, { x: x + 0.15, y: 1.55, w: 1.9, h: 0.3, fontSize: 14, bold: true, color: couleur, objectName: "Titre " + titre });
  personnage(s, x + 1.12, 2.2, C.background2, i === 0 ? C.accent3 : C.text2, "Professeur " + titre, 0.65);
  T(s, sous, { x, y: 3.36, w: 2.25, h: 0.5, fontSize: 15, bold: true, color: C.text1, align: "center", objectName: "Légende " + titre });
});
T(s, "Le même professeur, le même accent européen", { x: 0.5, y: 3.88, w: 4.7, h: 0.45, fontSize: 14, italic: true, color: C.accent3, align: "center", objectName: "Même professeur" });
[["118 étudiants de l'université du Michigan", "1"], ["Chacun regarde l'une des deux vidéos", "2"], ["Ils notent son apparence, ses manières et son accent", "3"]].forEach(([t, n], i) => {
  const y = 1.45 + i * 0.95;
  pastille(s, 5.5, y + 0.12, 0.52, n, C.accent3, C.background1, 18, "Numéro " + n);
  T(s, t, { x: 6.2, y, w: 3.3, h: 0.78, fontSize: 16, color: C.text1, valign: "middle", objectName: "Texte " + n });
});
carte(s, 0.5, 4.4, 9, 0.62, C.background2, "Question");
T(s, "Vont-ils le juger pareil dans les deux vidéos ?", { x: 0.7, y: 4.4, w: 8.6, h: 0.62, fontSize: 20, bold: true, color: C.text1, align: "center", valign: "middle", objectName: "Texte question" });
notes(s, 6);

// ================= 8. RESULTATS =================
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "L'effet de halo" });
s.addText("Résultats : deux jugements opposés", { placeholder: "title" });
[["Professeur chaleureux", "+", C.accent6, C.accent1, C.text1, ["Apparence : attirante", "Manières : agréables", "Accent : agréable"], 0.5], ["Professeur froid", "−", C.background2, C.accent2, C.text1, ["Apparence : irritante", "Manières : irritantes", "Accent : irritant"], 5.1]].forEach(([titre, signe, fond, pastilleCouleur, couleur, lignes, x]) => {
  carte(s, x, 1.4, 4.4, 2.55, fond, "Carte " + titre);
  pastille(s, x + 0.2, 1.55, 0.6, signe, pastilleCouleur, signe === "+" ? C.text1 : C.background1, 26, "Signe " + titre);
  T(s, titre, { x: x + 0.95, y: 1.55, w: 3.3, h: 0.6, fontSize: 19, bold: true, color: couleur, valign: "middle", objectName: "Titre " + titre });
  T(s, puces(lignes, { paraSpaceAfter: 9 }), { x: x + 0.3, y: 2.35, w: 3.9, h: 1.5, fontSize: 18, color: couleur, valign: "top", objectName: "Résultats " + titre });
});
carte(s, 0.5, 4.15, 9, 0.9, C.text1, "Bandeau");
T(s, [{ text: "Même homme, même accent. ", options: { bold: true, color: C.accent1 } }, { text: "Et les étudiants ne se rendaient pas compte que leur impression générale changeait leur jugement." }], { x: 0.75, y: 4.15, w: 8.5, h: 0.9, fontSize: 17, color: C.background1, valign: "middle", objectName: "Texte bandeau" });
notes(s, 7);

// ================= 9. VIE ET ARCHITECTURE =================
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "L'effet de halo" });
s.addText("Dans la vie et en architecture", { placeholder: "title" });
carte(s, 0.5, 1.4, 4.4, 3.65, C.background2, "Carte exemples");
T(s, "Où le retrouve-t-on ?", { x: 0.75, y: 1.55, w: 4.0, h: 0.4, fontSize: 19, bold: true, color: C.accent3, objectName: "Titre exemples" });
T(s, puces(["La beauté : les personnes séduisantes sont jugées plus positivement (Dion et al., 1972)", "Les entretiens d'embauche et les notes à l'école", "En architecture : un beau rendu peut faire paraître un projet meilleur qu'il n'est (exemple d'application)"]), { x: 0.75, y: 2.1, w: 3.95, h: 2.85, fontSize: 15, color: C.text1, valign: "top", objectName: "Texte exemples" });
carte(s, 5.1, 1.4, 4.4, 3.65, C.background2, "Carte protection");
T(s, "Comment s'en protéger ?", { x: 5.35, y: 1.55, w: 4.0, h: 0.4, fontSize: 19, bold: true, color: C.accent3, objectName: "Titre protection" });
T(s, puces(["En être conscient", "Noter critère par critère, avec une grille", "Séparer ce qu'on voit de ce qu'on déduit", "Évaluer de façon anonyme quand c'est possible"]), { x: 5.35, y: 2.1, w: 3.95, h: 2.85, fontSize: 17, color: C.text1, valign: "top", objectName: "Texte protection" });
notes(s, 8);

// ================= 10. CONCLUSION =================
pres.addSection({ title: "Conclusion" });
s = pres.addSlide({ masterName: "SOMBRE", sectionTitle: "Conclusion" });
s.addText("Ce qu'il faut retenir", { placeholder: "title" });
["Thorndike : pionnier de la psychologie de l'apprentissage (loi de l'effet)", "L'effet de halo : un seul trait colore tout le jugement, souvent sans qu'on le sache", "À nous, futurs architectes : juger un projet sur des critères, pas sur une impression"].forEach((t, i) => {
  const y = 1.35 + i * 0.85;
  pastille(s, 0.5, y + 0.08, 0.55, String(i + 1), C.accent1, C.text1, 20, "Numéro " + (i + 1));
  T(s, t, { x: 1.3, y, w: 8.2, h: 0.72, fontSize: 18, color: C.background1, valign: "middle", objectName: "Idée " + (i + 1) });
});
T(s, "Merci ! Des questions ?", { x: 0.5, y: 3.95, w: 9, h: 0.5, fontSize: 24, bold: true, color: C.accent1, objectName: "Merci" });
T(s, "Sources : Thorndike (1920), « A Constant Error in Psychological Ratings », Journal of Applied Psychology, 4(1) · Nisbett et Wilson (1977), « The Halo Effect », Journal of Personality and Social Psychology, 35(4) · Dion, Berscheid et Walster (1972), « What is beautiful is good », JPSP, 24 · Thorndike (1898), Animal Intelligence", { x: 0.5, y: 4.55, w: 9, h: 0.6, fontSize: 10.5, color: C.accent6, valign: "top", objectName: "Sources" });
notes(s, 9);

(async () => {
  const sortie = path.join(__dirname, "..", "Thorndike_effet_de_halo.pptx");
  await pres.writeFile({ fileName: sortie });
  await applyTheme(sortie, THEME);
  console.log("OK ->", sortie);
})();

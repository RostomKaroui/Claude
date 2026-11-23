// Genere la presentation PowerPoint « Le chemin de l'ecole ».
// Usage : NODE_PATH=<dossier node_modules> node generer_pptx.js  ->  ../Chemin_de_l_ecole.pptx
const path = require("path");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require("/root/.claude/skills/synced/e25176ef-0d6b-426f-88d1-18a43a6852b2_f6f6c202-53e5-4ae9-bc09-471b71e888ab/pptx/scripts/apply_theme.js");
const NOTES = require("./notes.js");

const THEME = {
  name: "Chemin",
  headFontFace: "Cambria", bodyFontFace: "Calibri",
  colors: { dk1: "1B3A3F", lt1: "FFFFFF", dk2: "3D5A5E", lt2: "F2F7F5", accent1: "E76F51", accent2: "2A9D8F", accent3: "F4A261", accent4: "6B8F86", accent5: "264653", accent6: "BFE3DB", hlink: "2A9D8F", folHlink: "6B8F86" },
};
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "Le chemin de l'école : circulation ou socialisation ?";
pres.author = "Étudiant·e 1re année Architecture, ESAD Tunis";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

const titrePh = (couleur) => ({ placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.35, w: 9, h: 0.8, fontSize: 32, bold: true, color: couleur, align: "left", valign: "middle", margin: 0 }, text: "" } });
pres.defineSlideMaster({ title: "TITRE", background: { color: C.text1 }, objects: [
  { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 1.3, w: 5.3, h: 1.9, fontSize: 40, bold: true, color: C.background1, align: "left", valign: "bottom", margin: 0 }, text: "" } },
  { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 3.35, w: 5.1, h: 0.9, fontSize: 18, color: C.accent6, align: "left", valign: "top", margin: 0 }, text: "" } },
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
const notes = (s, i) => s.addNotes(`[${NOTES[i].minutes}] ${NOTES[i].texte}\n\nConseil : ${NOTES[i].conseil}`);
const puces = (items, o = {}) => items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1, paraSpaceAfter: 6, ...o } }));

// ============ 1. TITRE ============
pres.addSection({ title: "Introduction" });
let s = pres.addSlide({ masterName: "TITRE", sectionTitle: "Introduction" });
s.addText("Le chemin de l'école : circulation ou socialisation ?", { placeholder: "title" });
s.addText("L'enfant entre autonomie et « enfant-paquet »", { placeholder: "body" });
T(s, "Sociologie · 1re année Architecture · ESAD Tunis", { x: 0.6, y: 4.55, w: 5.5, h: 0.3, fontSize: 14, color: C.background1, objectName: "Classe" });
T(s, "Présenté par : [ton nom]", { x: 0.6, y: 4.9, w: 5.5, h: 0.3, fontSize: 14, color: C.accent3, objectName: "Auteur" });
// illustration : maison -> chemin -> école
maison(s, 6.3, 3.7, 0.9, 0.9, C.accent6, C.accent1, "Maison");
rect(s, 6.6, 4.25, 0.25, 0.35, C.text2, "Porte maison");
maison(s, 8.3, 1.4, 1.2, 1.3, C.accent3, C.accent2, "École");
rect(s, 8.75, 2.05, 0.3, 0.65, C.text1, "Porte école");
s.addShape(pres.shapes.LINE, { x: 9.3, y: 0.95, w: 0, h: 0.5, line: { color: C.background1, width: 1.5 }, objectName: "Mât" });
s.addShape(pres.shapes.RECTANGLE, { x: 9.3, y: 0.95, w: 0.32, h: 0.2, fill: { color: C.accent1 }, line: { color: C.accent1, width: 0 }, objectName: "Drapeau" });
for (let i = 0; i < 10; i++) {   // chemin en pointilles (courbe)
  const t = i / 9, x = 7.15 * (1 - t) ** 2 + 7.0 * 2 * t * (1 - t) + 8.75 * t ** 2, y = 4.4 * (1 - t) ** 2 + 2.2 * 2 * t * (1 - t) + 2.75 * t ** 2;
  ovale(s, x - 0.06, y - 0.06, 0.12, 0.12, C.accent6, "Pas " + (i + 1));
}
personnage(s, 7.45, 3.15, C.background2, C.accent1, "Enfant", 0.42);
notes(s, 0);

// ============ 2. PROBLEMATIQUE ============
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "Introduction" });
s.addText("Notre problématique", { placeholder: "title" });
[["Circulation ou socialisation ?", "Un simple trajet, ou un vrai espace social ?"], ["Des expériences sociales ?", "L'enfant y vit-il des rencontres, des découvertes ?"], ["Aventure, apprentissage, épanouissement ?", "Quel rôle joue le chemin pour l'enfant ?"], ["Un « enfant-paquet » ?", "Est-il seulement transporté dès qu'on l'amène à l'école ?"]].forEach(([q, d], i) => {
  const x = 0.5 + (i % 2) * 4.6, y = 1.4 + Math.floor(i / 2) * 1.75;
  carte(s, x, y, 4.4, 1.6, C.background2, "Question " + (i + 1));
  pastille(s, x + 0.2, y + 0.2, 0.55, String(i + 1), i === 3 ? C.accent1 : C.accent2, C.background1, 20, "Numéro " + (i + 1));
  T(s, [{ text: q, options: { bold: true, fontSize: 17, breakLine: true } }, { text: d, options: { fontSize: 14 } }], { x: x + 0.95, y: y + 0.1, w: 3.3, h: 1.4, color: C.text1, valign: "middle", objectName: "Texte question " + (i + 1) });
});
T(s, "Démarche : le chemin comme espace social · le regard de Dolto · la situation aujourd'hui", { x: 0.5, y: 4.95, w: 8.4, h: 0.3, fontSize: 12, italic: true, color: C.accent4, objectName: "Démarche" });
notes(s, 1);

// ============ 3. CIRCULATION / SOCIALISATION ============
pres.addSection({ title: "Le chemin comme espace social" });
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "Le chemin comme espace social" });
s.addText("Circulation ou socialisation ?", { placeholder: "title" });
[["CIRCULATION", C.accent5, C.background1, ["Aller d'un point A à un point B", "Le plus vite et le plus sûrement possible", "L'enfant est un usager comme un autre", "Le trajet est du temps « perdu »"], 0.5], ["SOCIALISATION", C.accent6, C.text1, ["Un temps pour rencontrer : copains, voisins, commerçants", "Un rythme lent : on s'arrête, on observe, on joue", "L'enfant apprend les règles de la rue", "Le trajet est du temps « gagné »"], 5.1]].forEach(([titre, fond, coul, lignes, x]) => {
  carte(s, x, 1.4, 4.4, 2.75, fond, "Carte " + titre);
  T(s, titre, { x: x + 0.3, y: 1.55, w: 3.5, h: 0.4, fontSize: 19, bold: true, color: coul, objectName: "Titre " + titre });
  T(s, puces(lignes), { x: x + (x > 5 ? 0.45 : 0.3), y: 2.1, w: 3.55, h: 1.95, fontSize: 15, color: coul, valign: "top", objectName: "Texte " + titre });
});
pastille(s, 4.7, 2.5, 0.6, "ou", C.accent1, C.background1, 18, "Ou");
carte(s, 0.5, 4.3, 9, 0.75, C.text1, "Bandeau");
T(s, [{ text: "Le même chemin peut être les deux : ", options: { bold: true, color: C.accent3 } }, { text: "tout dépend de la place laissée à l'enfant." }], { x: 0.75, y: 4.3, w: 8.5, h: 0.75, fontSize: 18, color: C.background1, valign: "middle", objectName: "Texte bandeau" });
notes(s, 2);

// ============ 4. ESPACE DE SOCIALISATION ============
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "Le chemin comme espace social" });
s.addText("Un espace de socialisation", { placeholder: "title" });
[["FAMILLE", "socialisation primaire", 0.5, C.background2, C.text1], ["LE CHEMIN", "espace public : premières expériences sans les parents", 3.6, C.accent1, C.text1], ["ÉCOLE", "socialisation secondaire", 6.7, C.background2, C.text1]].forEach(([t, d, x, fond, coul], i) => {
  carte(s, x, 1.4, 2.8, 1.15, fond, "Cadre " + t);
  T(s, [{ text: t, options: { bold: true, fontSize: 16, breakLine: true } }, { text: d, options: { fontSize: 13 } }], { x: x + 0.15, y: 1.4, w: 2.5, h: 1.15, color: coul, align: "center", valign: "middle", objectName: "Texte " + t });
  if (i < 2) T(s, "→", { x: x + 2.8, y: 1.7, w: 0.3, h: 0.5, fontSize: 20, bold: true, color: C.accent4, align: "center", objectName: "Flèche " + (i + 1) });
});
[["Les rencontres", "Camarades, voisins, commerçants : l'enfant découvre des personnes différentes."], ["Les règles de la rue", "Dire bonjour, laisser passer, ne pas dévisager : l'« inattention civile » (Goffman)."], ["Les repères", "Il se construit une carte mentale du quartier : lieux, couleurs, odeurs."]].forEach(([t, d], i) => {
  const x = 0.5 + i * 3.05;
  carte(s, x, 2.8, 2.9, 2.25, C.background2, "Carte " + t);
  pastille(s, x + 0.2, 2.95, 0.45, String(i + 1), C.accent2, C.background1, 16, "Numéro carte " + (i + 1));
  T(s, t, { x: x + 0.8, y: 2.95, w: 2.0, h: 0.45, fontSize: 17, bold: true, color: C.text1, valign: "middle", objectName: "Titre " + t });
  T(s, d, { x: x + 0.2, y: 3.55, w: 2.55, h: 1.4, fontSize: 14, color: C.text2, valign: "top", objectName: "Texte " + t });
});
notes(s, 3);

// ============ 5. AVENTURE / APPRENTISSAGE / EPANOUISSEMENT ============
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "Le chemin comme espace social" });
s.addText("Aventure, apprentissage, épanouissement", { placeholder: "title", options: { fontSize: 30 } });
[["Aventure", C.accent1, C.text1, ["Explorer : raccourcis, ruelles, petits défis", "Un peu de liberté loin des adultes", "Jouer en chemin"]], ["Apprentissage", C.accent2, C.background1, ["S'orienter et lire la ville", "Traverser, évaluer le danger", "Gérer son temps"]], ["Épanouissement", C.accent5, C.background1, ["Confiance en soi : « je sais y aller seul »", "Plaisir et complicité avec les copains", "Sentiment d'appartenir au quartier"]]].forEach(([t, fond, coul, lignes], i) => {
  const x = 0.5 + i * 3.05;
  carte(s, x, 1.4, 2.9, 3.0, fond, "Carte " + t);
  T(s, t, { x: x + 0.25, y: 1.55, w: 2.4, h: 0.45, fontSize: 20, bold: true, color: coul, objectName: "Titre " + t });
  T(s, puces(lignes), { x: x + 0.25, y: 2.15, w: 2.45, h: 2.15, fontSize: 15, color: coul, valign: "top", objectName: "Texte " + t });
});
carte(s, 0.5, 4.55, 9, 0.5, C.background2, "Bandeau");
T(s, "Ces trois dimensions se nourrissent entre elles.", { x: 0.7, y: 4.55, w: 8.6, h: 0.5, fontSize: 16, italic: true, bold: true, color: C.text1, align: "center", valign: "middle", objectName: "Texte bandeau" });
notes(s, 4);

// ============ 6. DOLTO ============
pres.addSection({ title: "Dolto et l'autonomie" });
s = pres.addSlide({ masterName: "SOMBRE", sectionTitle: "Dolto et l'autonomie" });
s.addText("Françoise Dolto", { placeholder: "title" });
carte(s, 0.5, 1.4, 3.3, 3.0, C.accent5, "Carte portrait");
personnage(s, 2.15, 2.15, C.background2, C.accent3, "Portrait", 0.8);
T(s, [{ text: "1908 – 1988", options: { bold: true, fontSize: 20, color: C.accent3, breakLine: true } }, { text: "Pédiatre et psychanalyste française", options: { fontSize: 15, color: C.background1 } }], { x: 0.7, y: 3.45, w: 2.9, h: 0.9, align: "center", valign: "top", objectName: "Texte portrait" });
[["Grandir, c'est devenir autonome", "Se détacher peu à peu de l'adulte, étape par étape."], ["Confiance, respect et limites", "Une éducation bienveillante, sans enfant-roi."], ["La Maison Verte (Paris, 1979)", "Les tout-petits s'y socialisent avec leurs parents, avant l'école."]].forEach(([t, d], i) => {
  const y = 1.4 + i * 1.0;
  carte(s, 4.1, y, 5.4, 0.9, C.accent5, "Idée " + (i + 1));
  pastille(s, 4.25, y + 0.2, 0.5, String(i + 1), C.accent3, C.text1, 18, "Numéro idée " + (i + 1));
  T(s, [{ text: t, options: { bold: true, fontSize: 16, breakLine: true } }, { text: d, options: { fontSize: 13 } }], { x: 4.95, y, w: 4.45, h: 0.9, color: C.background1, valign: "middle", objectName: "Texte idée " + (i + 1) });
});
carte(s, 4.1, 4.5, 5.4, 0.6, C.accent1, "Notre lecture");
T(s, [{ text: "Notre lecture : ", options: { bold: true } }, { text: "le chemin de l'école est l'un des premiers pas vers cette autonomie." }], { x: 4.3, y: 4.5, w: 5.0, h: 0.6, fontSize: 13.5, color: C.text1, valign: "middle", objectName: "Texte lecture" });
notes(s, 5);

// ============ 7. ENFANT-PAQUET ============
pres.addSection({ title: "La situation aujourd'hui" });
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "La situation aujourd'hui" });
s.addText("L'enfant-paquet", { placeholder: "title" });
carte(s, 0.5, 1.4, 4.2, 3.0, C.background2, "Carte définition");
T(s, "DÉFINITION", { x: 0.75, y: 1.55, w: 3.7, h: 0.3, fontSize: 12, bold: true, color: C.accent1, objectName: "Étiquette définition" });
T(s, [{ text: "L'enfant qu'on transporte et qu'on dépose devant la porte de l'école, ", options: { bold: true } }, { text: "sans qu'il vive quoi que ce soit en chemin." }], { x: 0.75, y: 1.9, w: 3.7, h: 1.5, fontSize: 20, color: C.text1, valign: "top", objectName: "Texte définition" });
rect(s, 0.9, 3.55, 1.2, 0.5, C.accent5, "Colis");
s.addShape(pres.shapes.LINE, { x: 1.5, y: 3.55, w: 0, h: 0.5, line: { color: C.accent3, width: 3 }, objectName: "Ruban" });
T(s, "= l'enfant transporté comme un colis", { x: 2.25, y: 3.55, w: 2.3, h: 0.5, fontSize: 13, italic: true, color: C.text2, valign: "middle", objectName: "Légende colis" });
carte(s, 4.95, 1.4, 4.55, 3.0, C.text1, "Carte chiffres");
T(s, "ANGLETERRE · ENFANTS DE 7-8 ANS QUI VONT À L'ÉCOLE SANS ADULTE", { x: 5.2, y: 1.55, w: 4.05, h: 0.5, fontSize: 12, bold: true, color: C.accent6, objectName: "Étiquette chiffres" });
T(s, "1971", { x: 5.2, y: 2.2, w: 1.5, h: 0.4, fontSize: 18, color: C.background1, align: "center", objectName: "Année 1971" });
T(s, "80 %", { x: 5.0, y: 2.55, w: 2.0, h: 0.95, fontSize: 52, bold: true, color: C.accent3, align: "center", valign: "middle", objectName: "Chiffre 1971" });
T(s, "→", { x: 6.95, y: 2.65, w: 0.6, h: 0.8, fontSize: 36, bold: true, color: C.background1, align: "center", valign: "middle", objectName: "Flèche chiffres" });
T(s, "1990", { x: 7.5, y: 2.2, w: 1.5, h: 0.4, fontSize: 18, color: C.background1, align: "center", objectName: "Année 1990" });
T(s, "9 %", { x: 7.3, y: 2.55, w: 1.9, h: 0.95, fontSize: 52, bold: true, color: C.accent1, align: "center", valign: "middle", objectName: "Chiffre 1990" });
T(s, "Hillman, Adams et Whitelegg (1990)", { x: 5.2, y: 3.75, w: 4.05, h: 0.45, fontSize: 12, italic: true, color: C.accent6, align: "center", valign: "middle", objectName: "Source chiffres" });
carte(s, 0.5, 4.55, 9, 0.55, C.accent6, "Bandeau");
T(s, "Pourtant, en Angleterre, les accidents mortels d'enfants sur la route ont presque diminué de moitié.", { x: 0.7, y: 4.55, w: 8.6, h: 0.55, fontSize: 14, bold: true, color: C.text1, align: "center", valign: "middle", objectName: "Texte bandeau" });
notes(s, 6);

// ============ 8. CAUSES / CONSEQUENCES ============
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "La situation aujourd'hui" });
s.addText("Pourquoi, et avec quelles conséquences ?", { placeholder: "title", options: { fontSize: 30 } });
[["Pourquoi on les accompagne", C.accent3, C.text1, ["La peur de la circulation et des accidents", "Les horaires de travail des parents", "La voiture, pratique : les « parents-taxis »"], 0.5], ["Ce que l'enfant perd", C.accent5, C.background1, ["Moins de rencontres avec les camarades", "Une autonomie retardée", "Un quartier moins connu"], 5.2]].forEach(([t, fond, coul, lignes, x]) => {
  carte(s, x, 1.4, 4.3, 2.55, fond, "Carte " + t);
  T(s, t, { x: x + 0.3, y: 1.55, w: 3.7, h: 0.45, fontSize: 19, bold: true, color: coul, objectName: "Titre " + t });
  T(s, puces(lignes), { x: x + 0.3, y: 2.15, w: 3.75, h: 1.7, fontSize: 16, color: coul, valign: "top", objectName: "Texte " + t });
});
pastille(s, 4.85, 2.4, 0.5, "→", C.accent1, C.background1, 22, "Flèche cause");
carte(s, 0.5, 4.15, 9, 0.95, C.background2, "Carte Tonucci");
T(s, [{ text: "Francesco Tonucci, « La ville des enfants » (Fano, 1991) : ", options: { bold: true, color: C.accent2 } }, { text: "rendre aux enfants leur autonomie en ville. Se déplacer seul aide à créer des liens avec les camarades et avec le quartier." }], { x: 0.75, y: 4.15, w: 8.5, h: 0.95, fontSize: 15, color: C.text1, valign: "middle", objectName: "Texte Tonucci" });
notes(s, 7);

// ============ 9. GRADIENT ============
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "La situation aujourd'hui" });
s.addText("Enfant-paquet ou enfant acteur ?", { placeholder: "title" });
T(s, "ENFANT-PAQUET", { x: 0.5, y: 1.35, w: 3, h: 0.3, fontSize: 13, bold: true, color: C.accent1, objectName: "Pôle paquet" });
T(s, "ENFANT ACTEUR", { x: 6.5, y: 1.35, w: 3, h: 0.3, fontSize: 13, bold: true, color: C.accent2, align: "right", objectName: "Pôle acteur" });
[["En voiture, porte à porte", "Il ne vit presque rien", C.accent1, C.text1], ["À pied avec un parent", "Il discute avec lui", C.accent3, C.text1], ["Pédibus : en groupe accompagné", "Il rencontre d'autres enfants", C.accent6, C.text1], ["Seul ou avec des copains", "Autonomie complète", C.accent5, C.background1]].forEach(([t, d, fond, coul], i) => {
  const x = 0.5 + i * 2.3;
  carte(s, x, 1.75, 2.1, 2.6, fond, "Étape " + (i + 1));
  pastille(s, x + 0.15, 1.9, 0.5, String(i + 1), coul === C.background1 ? C.accent3 : C.text1, coul === C.background1 ? C.text1 : C.background1, 18, "Numéro étape " + (i + 1));
  T(s, t, { x: x + 0.15, y: 2.55, w: 1.8, h: 0.95, fontSize: 16, bold: true, color: coul, valign: "top", objectName: "Titre étape " + (i + 1) });
  T(s, d, { x: x + 0.15, y: 3.55, w: 1.8, h: 0.7, fontSize: 14, italic: true, color: coul, valign: "top", objectName: "Texte étape " + (i + 1) });
});
carte(s, 0.5, 4.5, 9, 0.6, C.background2, "Bandeau");
T(s, "L'idéal : avancer petit à petit vers l'autonomie.", { x: 0.7, y: 4.5, w: 8.6, h: 0.6, fontSize: 17, bold: true, color: C.text1, align: "center", valign: "middle", objectName: "Texte bandeau" });
notes(s, 8);

// ============ 10. L'ARCHITECTE ============
s = pres.addSlide({ masterName: "CLAIR", sectionTitle: "La situation aujourd'hui" });
s.addText("Et l'architecte dans tout ça ?", { placeholder: "title" });
carte(s, 0.5, 1.4, 4.6, 3.65, C.background2, "Fond coupe");
T(s, "Coupe sur la rue de l'école", { x: 0.7, y: 1.5, w: 4.2, h: 0.3, fontSize: 12, bold: true, color: C.accent4, objectName: "Titre coupe" });
rect(s, 0.7, 2.3, 1.1, 1.95, C.accent5, "Bâtiment école");
for (let r = 0; r < 2; r++) for (let c = 0; c < 2; c++) rect(s, 0.85 + c * 0.45, 2.5 + r * 0.55, 0.3, 0.35, C.accent6, "Fenêtre " + r + c);
T(s, "école", { x: 0.7, y: 2.02, w: 1.1, h: 0.25, fontSize: 12, bold: true, color: C.text1, align: "center", objectName: "Étiquette école" });
rect(s, 3.6, 2.75, 1.35, 1.5, C.accent3, "Bâtiment commerces");
rect(s, 3.6, 2.75, 1.35, 0.18, C.accent1, "Auvent");
rect(s, 3.8, 3.15, 0.5, 0.6, C.accent6, "Vitrine");
T(s, "commerces", { x: 3.6, y: 2.47, w: 1.35, h: 0.25, fontSize: 12, bold: true, color: C.text1, align: "center", objectName: "Étiquette commerces" });
rect(s, 0.7, 4.25, 1.5, 0.3, C.accent3, "Trottoir gauche");
rect(s, 2.2, 4.25, 1.4, 0.3, C.text2, "Chaussée");
rect(s, 3.6, 4.25, 1.35, 0.3, C.accent3, "Trottoir droit");
rect(s, 0.7, 4.55, 4.25, 0.4, C.accent4, "Sol");
rect(s, 2.04, 3.3, 0.1, 0.95, C.text2, "Tronc");
ovale(s, 1.72, 2.55, 0.74, 0.74, C.accent2, "Feuillage");
personnage(s, 1.35, 3.85, C.background1, C.accent1, "Enfant 1", 0.28);
personnage(s, 4.6, 3.85, C.background1, C.accent1, "Enfant 2", 0.28);
rect(s, 3.7, 4.1, 0.55, 0.06, C.text1, "Banc");
rect(s, 3.75, 4.16, 0.05, 0.09, C.text1, "Pied banc 1"); rect(s, 4.15, 4.16, 0.05, 0.09, C.text1, "Pied banc 2");
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 2.42, y: 3.98, w: 0.95, h: 0.22, rectRadius: 0.06, fill: { color: C.accent1 }, line: { color: C.accent1, width: 0 }, objectName: "Voiture" });
ovale(s, 2.52, 4.15, 0.14, 0.14, C.text1, "Roue 1"); ovale(s, 3.12, 4.15, 0.14, 0.14, C.text1, "Roue 2");
T(s, puces(["Trottoirs larges et continus", "Traversées sûres, abords d'école piétons", "Arbres et ombre contre la chaleur", "Bancs et petites places pour s'arrêter", "« Yeux sur la rue » (Jane Jacobs) : commerces et fenêtres"], { paraSpaceAfter: 9 }), { x: 5.4, y: 1.5, w: 4.1, h: 3.5, fontSize: 17, color: C.text1, valign: "top", objectName: "Leviers" });
notes(s, 9);

// ============ 11. CONCLUSION ============
pres.addSection({ title: "Conclusion" });
s = pres.addSlide({ masterName: "SOMBRE", sectionTitle: "Conclusion" });
s.addText("Conclusion", { placeholder: "title" });
T(s, "Le chemin de l'école est à la fois circulation et socialisation.", { x: 0.5, y: 1.25, w: 9, h: 0.55, fontSize: 22, bold: true, color: C.accent3, objectName: "Phrase clé" });
["Il peut être un lieu d'aventure, d'apprentissage et d'épanouissement", "L'enfant devient « paquet » quand on ne lui laisse aucune place", "L'architecte peut rendre le chemin plus sûr, pour que l'enfant y soit acteur"].forEach((t, i) => {
  const y = 2.0 + i * 0.75;
  pastille(s, 0.5, y + 0.05, 0.5, String(i + 1), C.accent3, C.text1, 18, "Numéro " + (i + 1));
  T(s, t, { x: 1.25, y, w: 8.25, h: 0.6, fontSize: 18, color: C.background1, valign: "middle", objectName: "Idée " + (i + 1) });
});
T(s, "Merci ! Des questions ?", { x: 0.5, y: 4.3, w: 9, h: 0.4, fontSize: 22, bold: true, color: C.accent3, objectName: "Merci" });
T(s, "Sources : Hillman, Adams et Whitelegg, One False Move (1990) · Brami, L'Éducation selon Dolto · BnF, notice Françoise Dolto (Maison Verte, 1979) · Tonucci, La città dei bambini (projet de Fano, 1991) · Jacobs, The Death and Life of Great American Cities (1961) · cours de sociologie (cadres sociaux, Goffman)", { x: 0.5, y: 4.75, w: 9, h: 0.5, fontSize: 10, color: C.accent6, valign: "top", objectName: "Sources" });
notes(s, 10);

(async () => {
  const sortie = path.join(__dirname, "..", "Chemin_de_l_ecole.pptx");
  await pres.writeFile({ fileName: sortie });
  await applyTheme(sortie, THEME);
  console.log("OK ->", sortie);
})();

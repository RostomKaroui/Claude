// Genere la feuille de DS en PDF (1 page A4) a partir de feuille_ds.html.
// Usage : node generer_pdf.js  ->  ../Construction_generale_feuille_DS.pdf
const path = require("path");
const { chromium } = require("playwright");

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto("file://" + path.join(__dirname, "feuille_ds.html"));
  await page.evaluate(() => document.fonts.ready);
  const sortie = path.join(__dirname, "..", "Construction_generale_feuille_DS.pdf");
  await page.pdf({ path: sortie, format: "A4", printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log("OK ->", sortie);
})();

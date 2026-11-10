// Genere les deux PDF du dossier DS (A4) a partir des pages HTML produites par construire_ds.py.
// Usage : python3 construire_ds.py && node generer_pdf.js
//   -> ../Environnement_DS_entrainement.pdf  et  ../Environnement_mini_fiche_DS.pdf
const path = require("path");
const { chromium } = require("playwright");

const documents = [
  { html: "ds_entrainement.html", pdf: "Environnement_DS_entrainement.pdf", pied: "Environnement · DS blanc · 1re année Architecture, ESAD Tunis" },
  { html: "mini_fiche_ds.html", pdf: "Environnement_mini_fiche_DS.pdf", pied: "Environnement · mini fiche DS · 1re année Architecture, ESAD Tunis" },
];

(async () => {
  const browser = await chromium.launch();
  for (const d of documents) {
    const page = await browser.newPage();
    await page.goto("file://" + path.join(__dirname, d.html));
    await page.evaluate(() => document.fonts.ready);
    const sortie = path.join(__dirname, "..", d.pdf);
    await page.pdf({
      path: sortie,
      format: "A4",
      printBackground: true,
      preferCSSPageSize: true,
      displayHeaderFooter: true,
      headerTemplate: "<span></span>",
      footerTemplate:
        '<div style="width:100%;font-family:sans-serif;font-size:7.5px;color:#8a9099;padding:0 12mm;display:flex;justify-content:space-between;">' +
        "<span>" + d.pied + "</span>" +
        '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
    });
    console.log("OK ->", sortie);
  }
  await browser.close();
})();

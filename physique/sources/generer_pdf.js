// Genere la fiche de revision en PDF (A4) a partir de fiche_physique.html.
// Usage : node generer_pdf.js  ->  ../Physique_fiche_revision.pdf
const path = require("path");
const { chromium } = require("playwright");

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto("file://" + path.join(__dirname, "fiche_physique.html"));
  await page.evaluate(() => document.fonts.ready);
  const sortie = path.join(__dirname, "..", "Physique_fiche_revision.pdf");
  await page.pdf({
    path: sortie,
    format: "A4",
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: "<span></span>",
    footerTemplate:
      '<div style="width:100%;font-family:sans-serif;font-size:7.5px;color:#8a9099;padding:0 13mm;display:flex;justify-content:space-between;">' +
      "<span>Physique du bâtiment · fiche de révision · 1re année Architecture, ESAD Tunis</span>" +
      '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
  });
  await browser.close();
  console.log("OK ->", sortie);
})();

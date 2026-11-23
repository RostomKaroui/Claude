// Rend les visuels HTML en PNG haute definition (A4 paysage, ~300 dpi).
// Usage : node rendre_visuels.js visuel1_porte visuel2_dar
const path = require("path");
const { chromium } = require("playwright");

(async () => {
  const noms = process.argv.slice(2);
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1400, height: 990 }, deviceScaleFactor: 2.5 });
  const page = await ctx.newPage();
  for (const nom of noms) {
    await page.goto("file://" + path.join(__dirname, nom + ".html"));
    await page.evaluate(() => document.fonts.ready);
    const deborde = await page.evaluate(() => document.body.scrollHeight > 990 || document.body.scrollWidth > 1400);
    const sortie = path.join(__dirname, "..", nom + ".png");
    await page.screenshot({ path: sortie, clip: { x: 0, y: 0, width: 1400, height: 990 } });
    console.log(nom, "->", sortie, deborde ? "(ATTENTION : le contenu deborde)" : "");
  }
  await browser.close();
})();

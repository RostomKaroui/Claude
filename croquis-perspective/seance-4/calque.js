// calque-*.html (le dessin posé sur la photo) -> captures du cadre, pour vérifier que le croquis colle à la photo
// Lancer : NODE_PATH=$(npm root -g) node calque.js <dossier de sortie>
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const out = process.argv[2] || __dirname;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2.5 });
  for (const nom of ['voute', 'rue']) {
    await p.goto('file://' + path.resolve(__dirname, `calque-${nom}.html`));
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    const mm = 794 / 210;
    for (const [i, y0] of [[1, 30], [2, 150]]) {
      await p.screenshot({ path: path.join(out, `calque-${nom}-${i}.png`), clip: { x: 15 * mm, y: y0 * mm, width: 180 * mm, height: 120 * mm } });
    }
  }
  await b.close();
})();

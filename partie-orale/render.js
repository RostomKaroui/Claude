// Rend partie-orale.html en PDF A4 (partie-orale-rostom.pdf) et en aperçus PNG.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(__dirname, 'partie-orale.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  await p.pdf({ path: 'partie-orale-rostom.pdf', format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close();
})();

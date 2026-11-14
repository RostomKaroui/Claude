// Rend patrons-A4.html en PDF (4 pages A4, échelle 1) et en aperçus PNG.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = process.argv[2] || __dirname;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(dir, 'patrons-A4.html'));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  await p.pdf({ path: path.resolve(dir, 'patrons-A4.pdf'), width: '210mm', height: '297mm', printBackground: true });
  const pages = await p.$$('.p');
  for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: path.resolve(dir, `apercu-patrons-${i + 1}.png`) });
  await b.close();
})();

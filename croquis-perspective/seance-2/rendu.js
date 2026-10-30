// croquis-3.html -> croquis-3-A4.pdf + apercu-3.png
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(__dirname, 'croquis-3.html'));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.pdf({ path: path.resolve(__dirname, 'croquis-3-A4.pdf'), width: '210mm', height: '297mm', printBackground: true });
  await (await p.$('.p')).screenshot({ path: path.resolve(__dirname, 'apercu-3.png') });
  await b.close();
})();

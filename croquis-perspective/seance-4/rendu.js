// croquis-4-voute.html, croquis-4-rue.html -> PDF A4 + aperçus PNG
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  for (const nom of ['voute', 'rue']) {
    await p.goto('file://' + path.resolve(__dirname, `croquis-4-${nom}.html`));
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    await p.pdf({ path: path.resolve(__dirname, `croquis-4-${nom}-A4.pdf`), width: '210mm', height: '297mm', printBackground: true });
    await (await p.$('.p')).screenshot({ path: path.resolve(__dirname, `apercu-4-${nom}.png`) });
  }
  await b.close();
})();

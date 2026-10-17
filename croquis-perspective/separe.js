// Un PDF A4 par croquis, à partir de croquis.html
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + path.resolve(__dirname, 'croquis.html'));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  for (const [n, f] of [['1', 'croquis-1-A4.pdf'], ['2', 'croquis-2-A4.pdf']])
    await p.pdf({ path: path.resolve(__dirname, f), width: '210mm', height: '297mm', printBackground: true, pageRanges: n });
  await b.close();
})();

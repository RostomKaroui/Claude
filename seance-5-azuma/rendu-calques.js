// calques.html -> calques-a4.pdf (9 pages A4 à taille réelle) + aperçus PNG
// Lancer : NODE_PATH=$(npm root -g) node rendu-calques.js <dossier des aperçus>
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const out = process.argv[2] || __dirname;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1.5 });
  p.on('pageerror', e => console.log('erreur:', e.message));
  await p.goto('file://' + path.resolve(__dirname, 'calques.html')); await p.waitForTimeout(800);
  await p.pdf({ path: path.resolve(__dirname, 'calques-a4.pdf'), width: '210mm', height: '297mm', printBackground: true,
                margin: { top: 0, bottom: 0, left: 0, right: 0 }, preferCSSPageSize: true, scale: 1 });
  const pages = await p.$$('.page');
  for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: path.join(out, `calque-p${i + 1}.png`) });
  await b.close();
})();

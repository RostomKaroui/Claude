// rendu.html -> azuma-rendu-x1-5.pdf (A4 paysage, à taille réelle) + aperçus PNG
// Lancer : NODE_PATH=$(npm root -g) node rendu-carnet.js <dossier des aperçus>
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const out = process.argv[2] || __dirname;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1123, height: 794 }, deviceScaleFactor: 1.2 });
  p.on('pageerror', e => console.log('erreur:', e.message));
  await p.goto('file://' + path.resolve(__dirname, 'rendu.html')); await p.waitForTimeout(900);
  await p.pdf({ path: path.resolve(__dirname, 'azuma-rendu-x1-5.pdf'), width: '297mm', height: '210mm', printBackground: true,
                margin: { top: 0, bottom: 0, left: 0, right: 0 }, preferCSSPageSize: true, scale: 1 });
  const pages = await p.$$('.page');
  for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: path.join(out, `rendu-p${i + 1}.png`) });
  console.log('pages', pages.length);
  await b.close();
})();

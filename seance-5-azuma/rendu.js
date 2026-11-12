// index.html -> aperçus PNG (page entière + une image par vue) pour vérification
// Lancer : NODE_PATH=$(npm root -g) node rendu.js <dossier de sortie>
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const out = process.argv[2] || __dirname;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1240, height: 900 }, deviceScaleFactor: 1 });
  p.on('pageerror', e => console.log('erreur:', e.message));
  await p.goto('file://' + path.resolve(__dirname, 'index.html')); await p.waitForTimeout(600);
  await p.screenshot({ path: path.join(out, 'azuma-page.png'), fullPage: true });
  const vues = await p.$$('.vue');
  for (let i = 0; i < vues.length; i++) await vues[i].screenshot({ path: path.join(out, `azuma-v${i + 1}.png`) });
  await b.close();
})();

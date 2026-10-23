const { chromium } = require('playwright');
const fs = require('fs');
const OUT = process.env.HOME + '/work/directions/_redesign/concurrents';
const sites = [
  ['craft', 'https://craftparis.fr/fr/'],
  ['belmard', 'https://www.belmard-batiment.fr/'],
  ['costaud', 'https://www.costaudrenovation.com/'],
  ['avoltis', 'https://avoltisrenovation.com/renovation-paris/'],
  ['erema', 'https://eremabat.fr/'],
];
(async () => {
  const browser = await chromium.launch();
  const report = {};
  for (const [key, url] of sites) {
    report[key] = { url };
    for (const [vp, w, h] of [['390', 390, 844], ['1366', 1366, 768]]) {
      const ctx = await browser.newContext({ viewport: { width: w, height: h }, locale: 'fr-FR',
        userAgent: w < 500 ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' : undefined });
      const page = await ctx.newPage();
      try {
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
        await page.waitForTimeout(4000);
        await page.screenshot({ path: `${OUT}/${key}-${vp}-ecran1.png` });
        await page.screenshot({ path: `${OUT}/${key}-${vp}-page.png`, fullPage: true }).catch(()=>{});
        const info = await page.evaluate(() => {
          const vis = el => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
          const fold = [...document.querySelectorAll('a,button')].filter(vis).filter(e => e.getBoundingClientRect().top < innerHeight && e.getBoundingClientRect().bottom > 0)
            .map(e => (e.innerText || e.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 60)).filter(Boolean);
          const tel = [...document.querySelectorAll('a[href^="tel:"]')].length;
          const wa = [...document.querySelectorAll('a[href*="wa.me"],a[href*="whatsapp"]')].length;
          const forms = [...document.querySelectorAll('form')].map(f => ({ fields: [...f.querySelectorAll('input,select,textarea')].filter(i => i.type !== 'hidden').map(i => i.name || i.id || i.type).slice(0, 15) }));
          const h = [...document.querySelectorAll('h1,h2')].filter(vis).map(e => e.tagName + ': ' + e.innerText.trim().replace(/\s+/g, ' ').slice(0, 90)).slice(0, 14);
          const fonts = [...new Set([...document.querySelectorAll('h1,h2,p,a')].slice(0, 80).map(e => getComputedStyle(e).fontFamily.split(',')[0].trim()))].slice(0, 6);
          const fixed = [...document.querySelectorAll('body *')].filter(e => { const p = getComputedStyle(e).position; return (p === 'fixed' || p === 'sticky') && vis(e); }).map(e => (e.innerText || e.className || e.tagName).toString().trim().replace(/\s+/g, ' ').slice(0, 50)).slice(0, 8);
          return { title: document.title, fold, tel, wa, forms, h, fonts, fixed, height: document.body.scrollHeight };
        });
        report[key][vp] = info;
      } catch (e) { report[key][vp] = { error: String(e).slice(0, 200) }; }
      await ctx.close();
    }
  }
  fs.writeFileSync(`${OUT}/releve.json`, JSON.stringify(report, null, 2));
  await browser.close();
})();

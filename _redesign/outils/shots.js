const { chromium } = require('playwright');
const [,, base, outdir, ...paths] = process.argv;
(async () => {
  const b = await chromium.launch();
  for (const p of paths) for (const [w, h] of [[390, 844], [1366, 768]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    const errs = []; page.on('pageerror', e => errs.push(String(e)));
    await page.route(u => !u.href.startsWith(base) && !/fonts\.(googleapis|gstatic)|cdnjs/.test(u.href), r => r.abort());
    await page.goto(base + p, { waitUntil: 'networkidle' });
    await page.evaluate(() => { const c = document.getElementById('mbCookie'); if (c) c.classList.remove('is-open'); });
    await page.waitForTimeout(400);
    const name = p.replace(/\//g, '_').replace(/^_|_$/g, '') || 'home';
    await page.screenshot({ path: `${outdir}/${name}-${w}-ecran1.png` });
    const ov = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
    await page.evaluate(async () => { document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager'); for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); });
    await page.waitForTimeout(1500); await page.evaluate(async () => { await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
    await page.screenshot({ path: `${outdir}/${name}-${w}-page.png`, fullPage: true });
    console.log(p, w, 'overflow', ov, 'errors', errs.length, errs.slice(0,2));
    await ctx.close();
  }
  await b.close();
})();

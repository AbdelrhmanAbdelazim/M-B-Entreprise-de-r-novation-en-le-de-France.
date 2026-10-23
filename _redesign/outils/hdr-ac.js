const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const out = {};
 for (const [w,h] of [[390,844],[1366,768]]) { const p = await (await b.newContext({viewport:{width:w,height:h}})).newPage();
  await p.route(u => !u.href.startsWith('http://127.0.0.1:4100'), r => r.abort());
  await p.goto('http://127.0.0.1:4100/apercu/ac/');
  const lum = c => { const v = c.match(/\d+(\.\d+)?/g).slice(0,3).map(x => { x/=255; return x<=.03928? x/12.92 : ((x+.055)/1.055)**2.4; }); return .2126*v[0]+.7152*v[1]+.0722*v[2]; };
  const r = await p.evaluate(() => { const hd = document.querySelector('.site-head'); const btn = hd.querySelector('.head-devis'); const s = getComputedStyle(btn); const bb = btn.getBoundingClientRect(); const hb = hd.querySelector('#menuBtn').getBoundingClientRect();
   return { logo_img: hd.querySelectorAll('img').length, tel: hd.querySelectorAll('a[href^="tel:"]').length, texte_tel: /\+33|07 53|7 53 30/.test(hd.innerText), label: btn.textContent.trim(), bg: s.backgroundColor, fg: s.color, h: bb.height, w: bb.width, left_first: Math.round(Math.min(...[...hd.children].map(c=>c.getBoundingClientRect()).filter(x=>x.width).map(x=>x.left))), hamburger_visible: hb.width>0, hamburger_box: [hb.width,hb.height] }; });
  const L1 = lum(r.bg), L2 = lum(r.fg); r.contraste = +((Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05)).toFixed(2);
  await p.hover('.site-head .head-devis'); await p.waitForTimeout(500); r.hover_bg = await p.evaluate(() => getComputedStyle(document.querySelector('.head-devis')).backgroundColor);
  const Lh = lum(r.hover_bg); r.contraste_hover = +((Math.max(Lh,L2)+.05)/(Math.min(Lh,L2)+.05)).toFixed(2);
  await p.focus('.site-head .head-devis'); await p.keyboard.press('Shift+Tab'); await p.keyboard.press('Tab');
  r.focus_outline = await p.evaluate(() => { const s = getComputedStyle(document.activeElement); return document.activeElement.className + ' ' + s.outlineStyle + ' ' + s.outlineWidth + ' ' + s.outlineColor; });
  await p.keyboard.press('Enter'); await p.waitForTimeout(300);
  r.modal_ouvert_clavier = await p.evaluate(() => !document.getElementById('devisModal').hidden && document.activeElement.id);
  await p.keyboard.press('Escape'); r.modal_ferme_echap = await p.evaluate(() => document.getElementById('devisModal').hidden);
  r.focus_retour = await p.evaluate(() => document.activeElement.className);
  out[w] = r; }
 console.log(JSON.stringify(out, null, 1)); await b.close(); })();

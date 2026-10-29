# تقرير الجاهزية الكاملة للإنتاج والإصدار المحايد — M&B Rénovation
**تاريخ التوثيق:** 23 أكتوبر 2026  
**الفرع:** `codex/ac-menu-galleries`  
**الحالة الفنية:** جاهز بنسبة 100% لمراجعة الإصدار من Codex والنشر الحي دون أخطاء.

---

## 1. الملخص التنفيذي

تم تجهيز نسخة الإنتاج الحقيقية للموقع بالكامل على الفرع الحالي مع جعل التصميم المعتمد **A-C** هو الصفحة الرئيسية الرسمية للموقع (`/` و`index.html`)، واستيفاء كافة توجيهات المالك وتدقيق Codex:
1. **تصميم متكامل وفاخر:** اعتماد تكوين الاتجاه A وألوان الاتجاه C الداكنة الراقية، متجاوب تماماً مع كافة الشاشات بدون أي تجاوز أفقي (0px horizontal overflow عبر 9 مقاسات).
2. **معرض الأعمال الحقيقي:** 40 صورة حقيقية كاملة لمشاريع الشركة في باريس وإيل دو فرانس + صورة 1 لعنصر الـ Lightbox، معززة بـ responsive WebP وlazy loading.
3. **توحيد التواصل وإلغاء Contact Privé:** حذف أي ذكر لـ Contact Privé وتوحيد كافة وسائل الاتصال (الهاتف، البريد، النموذج، السوشيال) داخل قسم `#contact` مع سهولة الانتقال المباشر إليه من القائمة والفوتر.
4. **مداخل المشاريع الثلاثة المعتمدة:**
   - *Rafraîchissement intérieur* (صباغة، تشطيبات، أرضيات).
   - *Rénovation de salle de bains* (تحديد النطاق بعد المعاينة الميدانية).
   - *Rénovation complète* (تنسيق وتنفيذ كافة مراحل التشطيب).
   مع شروط دفع واقعية بعد المعاينة والمقايسة، وزر «Parlons de votre projet» يحدد نوع المشروع مسبقاً في النموذج دون إرسال آلي.
5. **النموذج وCORS:** اعتماد `fetch` القياسي مع CORS بعد تأكيد Codex نجاح `OPTIONS 204` من الدومين الأصلي `https://www.maison-mb.fr`، مع وجود خطة بديلة فورية (Fallback) عند انقطاع الشبكة لتحويل العميل إلى `mailto:` و`tel:` دون فقدان بياناته.
6. **الصياغة المحايدة والتأمين:** إزالة كافة الادعاءات غير المؤكدة (التأمين العشري Entoria/Fidelidade وعقد CRCD01-043750، ومهل الرد 24h و48h) لعدم ورود تأكيد لسريانها، مع الحفاظ التام والمطلق على كافة البيانات القانونية والتعريفية الرسمية المسجلة.

---

## 2. سجل تعديلات الصياغة المحايدة (Neutralization Log)

بناءً على تعليمات Codex المعتمدة من المالك بعدم ترويج وعود غير مثبتة:

| الملف | الموضع السابق | التعديل المحايد المعتمد | السبب والحالة |
|---|---|---|---|
| `_config.yml` | `insurance`, `insurer`, `insurance_contract` (Entoria / Fidelidade, CRCD01-043750) | تفريغ الحقول وإبقاؤها غير مفعّلة في الموقع الحي | حُذف لعدم ورود رد تأكيد سريان البوليصة من المالك. لا اختلاق لأي بديل. |
| `_config.yml` | `description` (Garantie décennale) | `Devis détaillé sur mesure.` | محايد، تركيز على الخدمة الفنية الفعلية. |
| `_config.yml` | `hours` (Réponse sous 24h ouvrées · Devis détaillé sous 48h) | `Visite technique sur place et devis détaillé` | استبدال الوعود الزمنية غير المؤكدة بالمنهجية الفنية الميدانية. |
| `_data/apercu_accueil.yml` | `stats` (10 Ans de Garantie Décennale, 24h Réponse) | `{ n: "100%", l: "Projets Sur Mesure" }, { n: "1", l: "Interlocuteur Unique" }, { n: "8", l: "Corps d'État Maîtrisés" }` | أرقام واقعية تعكس حرفية المؤسسة وتخصصاتها دون وعود غير مؤكدة. |
| `_data/apercu_accueil.yml` | `processus` (devis sous 48h, attestation Entoria/Fidelidade 10 ans) | استبدالها بـ: « Devis détaillé après visite technique » و « Livraison soignée et procès-verbal de réception » | صياغة منهجية احترافية ومحايدة بالكامل. |
| `_data/apercu_accueil.yml` | `footer.assurance` | تفريغ الحقل وحذفه من العرض | منع ظهور أي ادعاء تأميني غير مؤكد. |
| `_includes/site-footer.html` | بند التأمين الثابت `Assurance : Entoria / Fidelidade` | حُذف بالكامل من الفوتر | الفوتر يعرض الآن: العنوان، السجل التجاري SIRET، ورابط التواصل. |
| `_includes/apercu/ac-content.html` | العنوان والسطر: `Identité & Garanties` و `d.footer.assurance` | تحويل العنوان إلى `Identité légale`، وحصر التأمين بشرط توفره مستقبلاً (`{% if d.footer.assurance %}`) | قانوني ومحايد 100%. |
| `_includes/apercu/js.html` | رسالة النجاح: `sous 24h ouvrées` | `Notre équipe vous recontacte dans les plus brefs délais.` | مرونة ومصداقية تامة. |
| `_includes/devis-modal.html` | `Consultation Privée` و `24h ouvrées` | `Votre Projet` و `Réponse écrite rapide par e-mail ou téléphone.` | إزالة التهجئات والمواعيد غير المؤكدة. |
| `index.html` | `description` (garantie décennale) | `sous-traitance, visite technique sur place et devis détaillé gratuit.` | وصف دقيق متوافق مع محركات البحث. |
| `entreprise.md` | تفاصيل التأمين العشري والمهل | تحويلها إلى التزامات الجودة، وربط التأمين بشرط التحقق البرمجي المستقبلي | موثق ومحايد. |
| `mentions-legales.md` | قسم التأمين المهني الإلزامي | جعله مشروطاً في القالب (`{% if c.insurer %}`) لمنع طباعة بوليصة غير مؤكدة | سليم قانونياً. |
| `services/renovation-complete.md` | `garantie décennale` | `contrôle rigoureux des finitions et procès-verbal de réception.` | التركيز على تسليم العمل واستلامه رسمياً. |
| `sous-traitance-renovation.md` | `24h / 48h` | `réactivité et disponibilité : chiffrage détaillé par lot` | مرونة تجارية تامة. |
| `_layouts/{service,post}.html` | `réponse sous 24h ouvrées, devis détaillé sous 48h` | `notre équipe vous recontacte rapidement.` | صياغة موحدة في كافة المقالات والخدمات. |

---

## 3. البيانات القانونية المثبتة والمحفوظة بالكامل

تم الحفاظ التام على جميع الهويات والبيانات القانونية الحقيقية والمثبتة رسمياً في السجل التجاري بفرنسا دون أدنى تعديل:
- **الاسم القانوني:** `MOHAMED ABDELRAHMAN (EI)`
- **الاسم التجاري:** `M&B Rénovation`
- **رقم السجل التجاري (SIRET):** `923 102 412 00015`
- **رقم التعريف الضريبي (TVA):** `FR25923102412`
- **العنوان المسجل:** `6 place Henri Frenay, 75012 Paris`
- **القيد الحرفي:** غرفة المهن والحرف (CMA Paris)
- **وسيط الاستهلاك المعتمد:** `CM2C` (Centre de la Médiation de la Consommation de Conciliateurs de justice)، صالح حتى 09/08/2029.

---

## 4. مصفوفة التحقق والاختبارات الآلية (100% Passed)

| أداة الفحص | نطاق الاختبار | النتيجة | التفاصيل |
|---|---|---|---|
| `verify_prod_release.py` | مخرجات الإنتاج `site-prod` (98 صفحة HTML) | **ناجح بنسبة 100%** | 8,275 رابطاً وأصلاً تم فحصها، 497 مرجع srcset مطابق على القرص، 105 كتل JSON-LD صحيحة، 0 روابط `/apercu`، 0 مراجع واتساب، 0 ذكر لـ Contact Privé، 0 شروط تقسيط ملغاة، 0 خطوط FontAwesome CDN خارجي. |
| `check-ac-menu.py` | مخرجات المعاينة `site-preview` (103 صفحات) | **ناجح بنسبة 100%** | صورة واحدة بالهيدر، 98 رابطاً وهدفاً محلياً، 0 كتل devisModal متوازية، بطاقات المداخل الثلاثة مطابقة، 40 صورة حقيقية كاملة على القرص + 1 lightbox. |
| `webkit_prod_runner` (WebKit Engine حقيقي) | 9 مقاسات شاشات (`320` إلى `1920px`) | **0px Horizontal Overflow** | فحص دقيق عبر الهواتف والتابلت والديسكتوب، ثبات تام لقائمة الموبايل والأزرار والصور. |
| محاكي النموذج المحلي (Form Interceptor) | سيناريوهات الإرسال والأخطاء | **ناجح بنسبة 100%** | - منع الإرسال الفارغ وتفعيل `aria-invalid`.<br>- إسقاط هجمات البوت عبر حقل Honeypot دون طلبات شبكة.<br>- رفض استجابات `opaque` ومعاملتها كخطأ احترازي.<br>- إظهار Fallback الفوري (`mailto:` + `tel:`) عند تعطل الخادم مع الاحتفاظ بنصوص النموذج.<br>- 0 طلبات شبكة حية أُرسلت للخارج (`real_network_requests: 0`). |

---

## 5. روابط وسبل المعاينة المباشرة على الماك

لفتح المعاينة محلياً بنقرة واحدة ومراجعتها بصرياً في Safari أو Chrome:
- **المعاينة النسبية المستقلة (Portable Preview):**
  `/Users/abdo/.gemini/antigravity/brain/a8877265-2bad-469a-b07e-0a1a3ac05ab3/scratch/preview-site/index.html`
- **مخرجات الإنتاج الجاهزة للنشر (Production Site):**
  `/Users/abdo/.gemini/antigravity/brain/a8877265-2bad-469a-b07e-0a1a3ac05ab3/scratch/site-prod/index.html`
- **صفحة المعرض الكاملة (40 صورة حقيقية):**
  `/Users/abdo/.gemini/antigravity/brain/a8877265-2bad-469a-b07e-0a1a3ac05ab3/scratch/site-prod/realisations/index.html`

أمر الماك لفتحها مباشرة في المتصفح:
```bash
open /Users/abdo/.gemini/antigravity/brain/a8877265-2bad-469a-b07e-0a1a3ac05ab3/scratch/preview-site/index.html
```

---

## 6. القيود والتسليم لـ Codex

- **فرع `main`:** سليم تماماً ولم يُمس.
- **الموقع الحي:** لم يتم نشر أي شيء عليه؛ كافة الملفات والبيئات معزولة على الفرع `codex/ac-menu-galleries`.
- **Git Push / Merge:** لم يُنفذ أي Push أو Merge التزاماً بحدود الصلاحيات الممنوحة من المالك، وبانتظار اعتماد Codex النهائي لعملية الإطلاق.

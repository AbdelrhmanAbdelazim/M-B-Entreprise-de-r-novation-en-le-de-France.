# تسليم Antigravity — معاينة M&B A-C
التوجيه الأحدث للمالك: «استخدم Antigravity». Codex أوقف كتابة واجهة الموقع بعد حفظ المسودة التالية، ولا يوجد كاتب آخر مصرح به لهذه الشريحة. Devin استلم التكليف ثم نام لنفاد رصيده المجاني؛ لا توقظه أو تشترِ أو تنشئ تكليفًا مكررًا.
## نقطة البداية
- العمل حصريًا داخل /Users/abdo/MB-Renovation/codex-ac-menu-galleries، فرع codex/ac-menu-galleries.
- أصل الفرع devin/redesign-directions عند 5c7f2def1f2d8dcb50ab798ad7c1465e905b466a.
- main ثابت عند 8909697d920da75f140e97dec29e16bc04d244f3؛ لا merge ولا deploy ولا تغيير production/DNS.
- اقرأ REDESIGN.md؛ الأقسام القديمة تاريخية، والتصميم الأول في PR24 مرفوض. المعتمد أساسًا للمعاينة هو تركيب A بألوان C وصورة inspiration الجديدة، وليس اعتماد نشر.
## المطلوب النهائي
- حافظ على A-C العاجي/الفحمي/الشمبانيا وصورة hero الإلهامية الموسومة بوضوح بأنها ليست عمل M&B.
- الرئيسية دون شبكات صور الأعمال؛ الوصول للصور باختيار Portfolio / Réalisations / L’Envers du Décor. استخدم /realisations/#portfolio و#chantiers وصفحات المشاريع الموجودة؛ لا تحذف أصول الصور أو تغيّر نسبتها.
- زر Menu ظاهر على الموبايل والكمبيوتر؛ قائمة كاملة مستوحاة من _redesign/references/owner-menu-reference.jpg، بألوان الموقع الحالي، وليس الخلفية القديمة.
- القائمة تشمل الروابط الحقيقية: الرئيسية، الأعمال، كواليس العمل، المراحل، الخدمات الثماني، مناطق باريس وإيل دو فرانس، الشركة، المقاولة من الباطن، المدونة، الرأي، الترشيح، طلب عرض السعر والروابط القانونية. لا اختراع خدمات أو شهادات أو أعمال.
- لا شعار أو هاتف أعلى الصفحة أو القائمة. زر Demander un devis يبقى بلون شامبانيا متناسق. لا WhatsApp في معاينة A-C.
- النصوص التسويقية والبيانات الموجودة لا تُعاد كتابتها دون المالك. M&B شركة تنفيذ rénovation وليست architecte أو مصممًا. العبارات الملتبسة الموجودة في main موثقة تاريخيًا ولم تُصحح دون موافقة.
- نطاق التنفيذ A-C فقط؛ لا تطبيق التصميم على باقي الصفحات الآن. وجهات القائمة الحالية تحتفظ بشكلها القديم؛ أخبر المالك بهذا القيد ولا تدّع توحيدها.
## المسودة المحفوظة — لم تُختبر في متصفح بعد
- _apercu/ac.html: إزالة تكرار صور portfolio/chantiers/realisations وإضافة مدخلين نصيين للأعمال، مع بقاء hero.
- _includes/apercu/ac-menu.html: dialog native كامل وروابط وأقسام details للخدمات والمناطق.
- _includes/apercu/ac.css: تنسيق القائمة والمدخلين، دون تغيير ألوان التصميم.
- _includes/apercu/js.html: الفرع الشرطي page.detailed_menu يعزل native dialog عن معاينات A/B/C؛ إغلاق/Escape وتركيز أصلي، والحفاظ على قفل التمرير عند الانتقال إلى نموذج العرض.
- _redesign/outils/check-ac-menu.py: فحص المخرجات المبنية للصور والروابط والمعاينات القديمة، لم يُشغّل بعد لغياب البناء.
## التحقق المطلوب قبل اعتبارها مختبرة
1. ابنِ Jekyll فعليًا بإعداد _config.yml,_config.apercu.yml في مجلد خارج المستودع؛ apercu_sans_envoi=true. لا إرسال نموذج حقيقي أو نداء webhook أو تتبع أو نشر.
2. افحص 390 و1366 و320px: زر القائمة، فتح/إغلاق/Escape، عودة التركيز، حصر Tab داخل dialog وخلفية inert، فتح تفاصيل الخدمات والمناطق، التمرير الطويل وإظهار كل الروابط.
3. افحص الانتقال من Menu إلى طلب العرض وإغلاق النموذج، scroll lock وعدم تعطل Tab، البيانات الاصطناعية فقط example.invalid، إثبات عدم الإرسال.
4. شغّل python3 _redesign/outils/check-ac-menu.py BUILD_DIR وافحص الروابط والصور وعدم WhatsApp. لا مجرد CSS لإخفاء الصور المحمّلة.
5. افحص صورة hero والكلمة التوضيحية، عدم logo/tel بالهيدر، عدم overflow وحجم أهداف اللمس. التقط صور desktop/mobile للرئيسية وللقائمة.
6. حافظ على A/B/C القديمة. بناء الإنتاج دون apercu، وتحقق أنه لا ينشر preview أو وثائق _redesign.
## عائق بيئة البناء المعروف
Ruby 2.6 موجود. جرى تثبيت اعتمادات محلية معزولة في outputs/mb-site-build-gems تحت مساحة Codex؛ لا تغيير macOS.
- Jekyll 3.9.5 لم يكتمل: آخر رسالة تطلب i18n 1.14.8 المتوافق مع Ruby 2.6 (latest يحتاج 3.1).
- ffi 1.17.0-x86_64-darwin مثبت مع Liquid4 وkramdown2 وsass3.7 وغيرها؛ لا تفترض اكتمال Jekyll.
- فحص syntax لـJS عبر Liquid+node --check نجح؛ git diff --check نجح. لا بناء ولا browser ولا links test مكتملة.
- لا تغيّر النظام أو بيانات المستخدم لتجاوز العائق؛ استخدم dependencies محلية أو بيئة معزولة معتمدة.
## الحفظ والتسليم
حدّث REDESIGN.md بعد كل خطوة: المنجز/الجاري/المتبقي، القرار وسببه، آخر commit معروف، حالة مسودة/مختبر/انتظار موافقة/merge. commit وpush للفرع codex فقط بعد الخطوات الموثقة. لا force-push. سلّم صور المعاينة ونتائج الأوامر الفعلية والقيود؛ لا تعتبر noindex خصوصية أو رابط localhost صالحًا للهاتف خارج الماك.
لا شراء/اشتراك/تفعيل AI credits أو API key مدفوع أو تغيير permissions أو auto-approval. استخدم الحساب والخطة الحالية فقط؛ إذا تطلب تسجيل الدخول أو إذن جهاز، اطلب المالك. لا تتجاوز sandbox.
VS Code يملك تطبيق M&B OS بمجلد مختلف؛ لا تلمس ملفاته. عمليات Claude/n8n/live خارج النطاق تمامًا.

## État du lancement officiel
Antigravity CLI 1.4.6 vérifié par SHA512, démarré en sandbox depuis ce worktree. Une seule consigne initiale fournie ; son exécution n’est pas confirmée. Démarrage non connecté puis écran initial. Une touche Enter a été refusée par la revue automatique car elle pourrait poursuivre l’authentification ; ne pas contourner cette décision. Le gérant doit terminer la connexion/écran initial. Aucune tâche achevée annoncée.

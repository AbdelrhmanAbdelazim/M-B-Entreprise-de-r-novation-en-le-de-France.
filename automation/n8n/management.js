// Pure operator policy. No transports, secrets, customer sends, publication or ad actions.
function mgPayload(r){try{return JSON.parse(r?.payload||'{}');}catch{return {};}}
function mgSafe(s){return String(s??'').replace(/\b(?:sk-(?:proj-|ant-)?[A-Za-z0-9_-]{12,}|Bearer\s+\S+|(?:api[_-]?key|password|access_token)\s*[:=]\s*\S+)/gi,'[REDACTED]').slice(0,1800);}
function mgArabic(s){return String(s||'').replace(/[٠-٩]/g,c=>String('٠١٢٣٤٥٦٧٨٩'.indexOf(c))).replace(/[۰-۹]/g,c=>String('۰۱۲۳۴۵۶۷۸۹'.indexOf(c))).replace(/[ًٌٍَُِّْـ]/g,'').replace(/[أإآ]/g,'ا').trim();}
function mgCommand(text){
 const s=mgArabic(text),aliases={'المهام':'/queue','اعرض المهام':'/queue','قائمة المهام':'/queue','حالة النظام':'/status','حاله النظام':'/status','تقرير الادارة':'/report','تقرير':'/report','العملاء':'/clients','اعرض العملاء':'/clients','الفرص المهمة':'/hot','الفرص المهمه':'/hot'};
 const t=aliases[s]||s.replace(/^اعرض (?:تفاصيل )?المهمة\s+(\d+)$/,'/task $1').replace(/^اعرض (?:تفاصيل )?المهمه\s+(\d+)$/,'/task $1');
 const [word,...args]=t.split(/\s+/);return {cmd:word.toLowerCase().replace(/@\w+$/,''),args,text:t};
}
function mgAuthorized(update,owner){const m=update?.message;return !!m&&Number.isSafeInteger(update.update_id)&&!m.forward_origin&&!m.forward_from&&!m.via_bot&&String(m.chat?.id)===String(owner)&&String(m.from?.id)===String(owner)&&m.chat?.type==='private'&&m.from?.is_bot!==true;}
function mgPending(q){const hidden=new Set(['action','inbox','agent_log','agent_session','operator_command','integration_report']);return q.filter(t=>t.task_key&&!hidden.has(t.type)&&!['done','published','rejected','cancelled'].includes(t.status));}
function mgBrief(q,leads,clients,journal,now){
 const day=new Date(now).toLocaleString('sv-SE',{timeZone:'Europe/Paris'}).slice(0,10),onDay=x=>String(x||'').slice(0,10)===day;
 const prospects=q.filter(r=>r.type==='prospect'),pending=mgPending(q),review=pending.filter(t=>['needs_review','needs_attention','uncertain'].includes(t.status));
 const sent=leads.filter(l=>onDay(l.date_envoi)),reply=leads.filter(l=>onDay(l.date_reponse)),errors=journal.filter(l=>l.resultat==='erreur'&&onDay(l.date));
 const integrations=q.filter(t=>t.type==='integration'&&t.status!=='done');
 return ['📊 إدارة M&B — '+day+' (Europe/Paris)',`📋 مهام معلقة: ${pending.length} | للمراجعة: ${review.length}`,`🔎 سجلات prospects: ${prospects.length} | اكتُشفت اليوم: ${prospects.filter(p=>onDay(p.created_at)).length}`,`📤 اتصال أول مسجل اليوم: ${sent.length} | متابعات: ${leads.filter(l=>onDay(l.date_relance)).length}`,`💬 ردود مسجلة اليوم: ${reply.length} | اهتمام مؤكد بتصنيف وارد: ${reply.filter(l=>l.statut==='interesse').length}`,`🔥 HOT: ${prospects.filter(t=>t.priority==='HOT').length} — ملاءمة تجارية؛ ليست دليل اهتمام أو رد`,`👥 عملاء مسجلون: ${clients.length} | محتوى للمراجعة: ${q.filter(t=>t.type==='content'&&t.status==='needs_review').length}`,`⚠️ أخطاء مسجلة اليوم: ${errors.length} | تكاملات تحتاج وصولًا: ${integrations.length}`,'النشر والإعلانات: لا إجراء من هذا الأمر. غياب بيانات Analytics لا يعني صفر نتائج.'].join('\n');
}
function mgTaskDetail(t){const p=mgPayload(t);return [`📋 المهمة #${t.id}`,`النوع: ${t.type} | ${t.priority} | ${t.status}`,`المسؤول: ${t.owner} | المصدر: ${t.source}`,`أُنشئت: ${t.created_at} | الموعد: ${t.due_at}`,`التالي: ${mgSafe(t.next_action)}`,p.from?'من: '+mgSafe(p.from):'',p.subject?'الموضوع: '+mgSafe(p.subject):'',p.summary?'الملخص: '+mgSafe(p.summary):'',p.email?'البريد: '+mgSafe(p.email):'',p.title?'الطلب: '+mgSafe(p.title):'',p.instruction?'التعليمات: '+mgSafe(p.instruction):'',p.result?'النتيجة الفعلية: '+mgSafe(p.result):'',p.error?'الخطأ: '+mgSafe(p.error):'',p.reply_draft?'مسودة فقط، لم تُرسل:\n'+mgSafe(p.reply_draft):'','لا يُستنتج اكتمال التنفيذ من الموافقة أو تصنيف HOT.'].filter(Boolean).join('\n').slice(0,3500);}
function mgCompletion(t){const p=mgPayload(t);return t.type==='agent_task'&&p.turn_status==='completed'&&!!p.turn_id&&!!p.session_id&&typeof p.result==='string'&&!!p.result.trim();}
function mgProspectBlocked(t,q,leads,blacklist){const p=mgPayload(t),mail=s=>String(s||'').toLowerCase().trim(),email=mail(p.email),domain=email.split('@')[1];const ls=leads.filter(l=>mail(l.email)===email);
 if(ls.length!==1||!email||ls.some(l=>Number(l.id)===79||l.date_envoi||l.date_reponse||l.date_relance||['stop','pas_interesse','erreur','interesse'].includes(l.statut)))return true;
 if(blacklist.some(b=>mail(b.email)===email||(!['gmail.com','outlook.com','hotmail.fr','yahoo.fr'].includes(domain)&&mail(b.email).split('@')[1]===domain)))return true;
 return q.some(r=>r.type==='action'&&(r.task_key==='send:outreach:'+p.company||r.task_key==='send:followup:'+p.company||JSON.stringify(mgPayload(r)).toLowerCase().includes(email)));
}
function mgOperator(text,data,context){
 const {cmd,args}=mgCommand(text),{queue:q=[],leads=[],clients=[],journal=[],blacklist=[]}=data,now=context.now;
 const reply=s=>({op:'reply',reply:mgSafe(s).slice(0,3500)}); // Task/report outputs are separately bounded below.
 if(context.authorized!==true)return {op:'deny'};
 const full=s=>({op:'reply',reply:String(s).slice(0,3500)});
 if(cmd==='/queue')return full('📋 المهام المعلقة ('+mgPending(q).length+') — أول 20 حسب الأولوية:\n'+mgPending(q).sort((a,b)=>({HOT:0,WARM:1,COLD:2}[a.priority]??3)-({HOT:0,WARM:1,COLD:2}[b.priority]??3)||a.id-b.id).slice(0,20).map(t=>`#${t.id} ${t.priority} ${t.type} — ${t.status} / ${t.owner}`).join('\n')+'\n/task ID للتفاصيل. لا تشمل القائمة سجلات الإرسال الداخلية.');
 if(cmd==='/clients')return full('👥 العملاء (أحدث 15):\n'+clients.slice().sort((a,b)=>b.id-a.id).slice(0,15).map(c=>'#'+c.id+' '+mgSafe(c.nom)+' — '+c.statut+(c.avis==='oui'?' ⭐':'')).join('\n')+(clients.length?'':'لا توجد سجلات عملاء.'));
 if(cmd==='/report')return full(mgBrief(q,leads,clients,journal,now));
 if(cmd==='/status')return full('🩺 حالة مبنية على السجلات، وليست فحصًا حيًا لكل API:\n'+journal.slice().sort((a,b)=>String(b.date).localeCompare(String(a.date))).slice(0,6).map(l=>`${l.workflow}: ${l.resultat} @ ${l.date}`).join('\n')+'\n'+q.filter(t=>t.type==='integration').map(t=>mgSafe(t.task_key)+': '+t.status).join('\n')+'\nللأرقام والتفاصيل: /report. الاتصالات الخارجية غير المتاحة لا تُفترض سليمة.');
 if(cmd==='/hot')return full('🔥 HOT = ملاءمة شراكة، لا تعني اهتمامًا مؤكدًا.\n'+q.filter(t=>['prospect','inbound_sales'].includes(t.type)&&t.priority==='HOT').slice().sort((a,b)=>b.id-a.id).slice(0,12).map(t=>{const p=mgPayload(t),l=leads.find(l=>String(l.email).toLowerCase()===String(p.email).toLowerCase());return `#${t.id} ${mgSafe(p.entreprise||p.company||p.subject||'-')} — ${t.status} | اتصال: ${l?.date_envoi||'غير مسجل'} | رد: ${l?.date_reponse||'غير مسجل'}`;}).join('\n'));
 if(cmd==='/task'&&/^#?\d+$/.test(args[0]||'')&&args.length===1){const t=q.find(t=>String(t.id)===args[0].replace('#',''));return t?full(mgTaskDetail(t)):reply('المهمة غير موجودة. استخدم /queue.');}
 const actions=['approve','reject','done','qualify','defer'];const action=cmd.slice(1);
 if(!actions.includes(action))return null;
 const t=q.find(t=>String(t.id)===String(args[0]).replace('#',''));if(!t)return reply('المهمة غير موجودة. استخدم /queue.');
 if(q.filter(r=>r.task_key===t.task_key).length!==1)return reply('سجلات متعارضة للمهمة؛ لن يتغير أي سجل.');
 const p=mgPayload(t),key=context.command_key;
 if(['inbox','agent_log','agent_session','operator_command','integration','integration_report'].includes(t.type))return reply('هذا سجل تقني أو تكامل؛ لا يُغلق أو يُعتمد كدليل اتصال بواسطة أمر إداري.');
 if(key&&journal.some(j=>String(j.details).includes('command_key='+key+';')))return reply('سبق تسجيل هذا الأمر؛ لا تعديل مكرر. استخدم /task '+t.id);
 if(t.type==='action'||t.type==='publication'||['running','reserved','uncertain','submitting'].includes(t.status))return reply('عملية محجوزة أو تسليم غير محسوم: لا يمكن إعادة ضبطها أو إعلان اكتمالها يدويًا.');
 if(action==='done'){
  if(t.status==='done')return reply('المهمة مسجلة مكتملة بالفعل. /task '+t.id+' يعرض الدليل المتاح؛ لم تتغير حالتها.');
  if(!mgCompletion(t))return reply('لم تُغلق المهمة: لا يوجد دليل تنفيذ موثق. الموافقة أو كتابة /done لا تثبت الإنجاز.');
 }
 if(['done','published','rejected','cancelled'].includes(t.status))return reply('المهمة مغلقة؛ لا إعادة فتح تلقائية أو إعادة تنفيذ.');
 const update={...t,last_action:now};
 if(action==='approve'){
  if(t.type==='prospect'&&(t.priority==='COLD'||mgProspectBlocked(t,q,leads,blacklist)))return reply('الموافقة محجوبة: تحقق من التأهيل، lead79، الاتصال السابق، الرد، blacklist ومنع التكرار.');
  if(t.type==='content'&&(!q.some(r=>r.type==='quality_review'&&mgPayload(r).target===t.task_key)||q.some(r=>r.type==='quality_review'&&mgPayload(r).target===t.task_key&&r.status!=='done')))return reply('يلزم اكتمال مراجعة جودة المحتوى قبل الموافقة.');
  update.status=t.type==='prospect'?'approved':t.type==='content'?'approved_draft':['quality_review','sales_review'].includes(t.type)?'ready':['inbound_sales','inbound_hr'].includes(t.type)?'approved_for_human_reply':'approved';
  update.next_action='موافقة بشرية مسجلة؛ لا رسالة أو نشر من هذا الأمر؛ تتحقق الوحدة المختصة مجددًا.';
  update.payload=JSON.stringify({...p,reviewed_by:context.actor,reviewed_at:now,...(t.type==='content'?{publication_approval:{revision:metricoolRevision(p),approved_by:context.actor,approved_at:now}}:{}),...(t.type==='prospect'?{qualified_by:context.actor,auto_approved:false}:{})});
 }else if(action==='reject'){update.status='rejected';update.next_action='رفض بشري؛ لا إرسال أو تنفيذ تلقائي';}
 else if(action==='done'){update.status='done';update.next_action='أُثبت اكتمال turn ونتيجته؛ لا إعادة تنفيذ';}
 else if(action==='qualify'){
  const grade=String(args[1]||'').toUpperCase();if(t.type!=='prospect'||!['HOT','WARM','COLD'].includes(grade))return reply('الصيغة: /qualify ID HOT|WARM|COLD لفرصة تجارية.');
  update.priority=grade;update.status='needs_review';update.payload=JSON.stringify({...p,grade,qualified_by:context.actor,qualified_at:now});update.next_action='تأهيل بشري؛ يلزم /approve قبل الاتصال الأول';
 }else if(action==='defer'){
  const due=args.slice(1,3).join(' ');if(!/^\d{4}-\d{2}-\d{2} ([01]\d|2[0-3]):[0-5]\d$/.test(due))return reply('الصيغة: /defer ID YYYY-MM-DD HH:MM (Europe/Paris)');update.status='deferred';update.due_at=due+':00';update.next_action='يُراجع عند الموعد؛ لا إرسال تعويضي تلقائي';
 }
 const columns=['task_key','type','priority','source','owner','status','created_at','last_action','next_action','due_at','payload'];
 return {op:'queue_update',row:Object.fromEntries(columns.map(k=>[k,String(update[k]??'')])),expected_last_action:t.last_action,expected_status:t.status,command_key:key||'',pending_reply:'✅ سُجل '+cmd+' للمهمة #'+t.id+' بعد حفظها. لا إرسال عميل أو منشور من هذا الأمر.'};
}
function mgRecruitment(subject){return /\bcandidature\b|\bcurriculum vitae\b|\brecrutement\b|\bdemande\s+(?:de?\s+|d['’])?(?:stage|alternance)\b|^alternance\b|طلب تدريب|بحث عن عمل/i.test(String(subject||''));}

function mgTelegramText(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}

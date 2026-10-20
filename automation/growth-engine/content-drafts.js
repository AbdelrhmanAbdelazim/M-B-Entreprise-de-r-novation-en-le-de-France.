// Draft adaptation only. This function never schedules, uploads, publishes or grants permission.
function growthContentDrafts(content,key){
 const caption=String(content.caption||''),cta=String(content.cta||'Contactez M&B Rénovation : https://www.maison-mb.fr/'),tags=[...new Set(String(content.hashtags||'').match(/#[\p{L}\p{N}_]+/gu)||[])];
 const base=[caption,cta].filter(Boolean).join('\n\n'),make=(channel,text,format,extra={})=>({idempotency_key:key+':'+channel,channel,format,text,publication_ready:false,human_approval_required:true,account_permission_verified:false,owned_media_approval_required:true,scheduling_owner:'existing Metricool schedule only after authorization',...extra});
 return {facebook:make('facebook',[base,tags.slice(0,5).join(' ')].join('\n\n').slice(0,5000),'image_or_video'),instagram:make('instagram',[base,tags.slice(0,5).join(' ')].join('\n\n').slice(0,2200),'image_or_reel'),threads:make('threads',base.slice(0,500),'short_text'),linkedin:make('linkedin',[base,tags.slice(0,3).join(' ')].join('\n\n').slice(0,3000),'professional_post'),tiktok:make('tiktok',[base,tags.slice(0,5).join(' ')].join('\n\n').slice(0,2200),'short_video',{script:content.video_script||null}),youtube_shorts:make('youtube_shorts',base.slice(0,5000),'short_video',{title:String(content.titre||'').slice(0,100),script:content.video_script||null}),pinterest:make('pinterest',base.slice(0,500),'image_or_video_pin',{title:String(content.titre||'').slice(0,100),board_authorization_required:true}),google_business_profile:make('google_business_profile',base.slice(0,1500),'business_update')};
}
function growthAdaptContentRows(rows){
 // A generated batch alone does not prove that an approved content brief was fulfilled.
 rows=rows.filter(item=>item.json?.type!=='content_brief'||item.json.status!=='done');
 const assets=new Map();const adapted=rows.map(item=>{const r=item.json;if(r?.type!=='content')return item;const p=JSON.parse(r.payload);const asset={...p,social_drafts:growthContentDrafts(p,r.task_key)};assets.set(r.task_key,asset);return {json:{...r,payload:JSON.stringify(asset)}};});
 return adapted.map(item=>{if(item.json?.type!=='quality_review')return item;const p=JSON.parse(item.json.payload),asset=assets.get(p.target);return asset?{json:{...item.json,owner:'OpenAI',payload:JSON.stringify({...p,content:asset})}}:item;});
}

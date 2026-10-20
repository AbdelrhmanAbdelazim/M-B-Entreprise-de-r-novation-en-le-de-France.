// Preparation only: no network, rendering, upload, publishing, API key or spend.
function mbVideoDraft(content,key){
 const script=content.video_script||{},text=v=>String(v||'').slice(0,700);
 const candidates=['realisation-sejour-parquet.jpg','realisation-peinture-parquet.jpg'].map(name=>({url:'https://www.maison-mb.fr/images/realisations/'+name,provenance:'existing company website repository',rights_verified:false,approved_for_this_video:false,http_verified:false}));
 const overlay=(name,value,time,duration,y,size,color='#FFFFFF')=>({type:'text',name,track:3,time,duration,x:'50%',y,width:'82%',height:'20%',text:text(value),font_family:'Arial',font_size:size,font_weight:'700',fill_color:color,x_alignment:'50%',y_alignment:'50%'});
 const source={output_format:'mp4',width:1080,height:1920,frame_rate:30,duration:36,fill_color:'#102438',elements:[
  ...candidates.map((asset,i)=>({type:'image',name:'Project-'+(i+1),track:1,time:i*18,duration:18,source:asset.url,x:'50%',y:'48%',width:'100%',height:'65%',fit:'cover'})),
  overlay('Brand','M&B RÉNOVATION',0,36,'10%',58,'#D4AF37'),
  overlay('Hook',script.hook||content.titre,0,6,'77%',48),
  ...(Array.isArray(script.points)?script.points.slice(0,3):[]).map((point,i)=>overlay('Point-'+(i+1),point,6+i*8,8,'77%',42)),
  overlay('CTA',content.cta||'Demandez une visite : maison-mb.fr',30,6,'77%',40,'#D4AF37'),
  overlay('Location','Paris & Île-de-France • maison-mb.fr',0,36,'92%',30,'#D4AF37')
 ]};
 return {idempotency_key:key+':vertical-video:v1',status:'blocked_authorization_and_media_review',provider:'creatomate',render_enabled:false,publish_enabled:false,spending_authorized:false,render_id:null,mp4_url:null,source,media_candidates:candidates,
  script:{language:'fr',writer_primary:'Claude',actual_model:content.model||'unknown',hook:text(script.hook),points:(Array.isArray(script.points)?script.points:[]).map(text),cta:text(content.cta)},
  quality_review:{owner:'OpenAI',status:'pending',must_review:['facts','services','script','media_rights','privacy','no_false_before_after','no_price_or_date_promise']},
  targets:['instagram_reels','tiktok','youtube_shorts','facebook_reels'],calendar_owner:'existing W10 Content Queue; Metricool scheduled items untouched',
  optional_runway:{enabled:false,api_verified:false,credit_balance:null,task_id:null,reason:'Google login is not API authorization; generation and spending remain disabled'},
  retry:{render_submit:'never retry an uncertain submission',status_poll_only_after_known_render_id:true},failure_routing:'W0',approval_required:true};
}
function mbVideoRows(rows){
 const assets=new Map();const out=rows.map(item=>{const r=item.json;if(r?.type!=='content')return item;const p=JSON.parse(r.payload);const asset={...p,video_draft:p.video_draft||mbVideoDraft(p,r.task_key)};assets.set(r.task_key,asset);return {json:{...r,payload:JSON.stringify(asset)}};});
 return out.map(item=>{if(item.json?.type!=='quality_review')return item;const p=JSON.parse(item.json.payload),asset=assets.get(p.target);return asset?{json:{...item.json,owner:'OpenAI',payload:JSON.stringify({...p,content:asset,video_review_required:true})}}:item;});
}

from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '<!-- PLATINUM_TOEFL_AUTH_GUARD -->'

guard = r'''
<!-- PLATINUM_TOEFL_AUTH_GUARD -->
<style id="platinum-auth-guard-style">html{visibility:hidden!important}</style>
<style id="platinum-legacy-gate-hide">#pa32-gate,.pa32-switch{display:none!important}</style>
<script type="module">
import {createClient} from 'https://esm.sh/@supabase/supabase-js@2';
const sb=createClient('https://yqgqylzfveiennyprsip.supabase.co','sb_publishable_uZ1Oyk5hnQfjkJFfvdIW3A_zZmEhHYv');
const LEGACY_ACTIVE='platinum-v32-active-student';
const LEGACY_SUFFIX='@students.platinumacademy.invalid';
const reveal=()=>{document.documentElement.style.visibility='visible';document.getElementById('platinum-auth-guard-style')?.remove();};
const deny=async()=>{try{await sb.auth.signOut()}catch{} location.replace('./student-login.html');};
function usernameFromSession(session){
  const email=String(session?.user?.email||'').toLowerCase();
  return email.endsWith(LEGACY_SUFFIX)?email.slice(0,-LEGACY_SUFFIX.length):'';
}
function syncLegacyProfile(session,row){
  const username=usernameFromSession(session);
  if(!username) return false;
  const fullName=String(row?.full_name||username).trim()||username;
  let reload=false;
  try{
    if(sessionStorage.getItem(LEGACY_ACTIVE)!==username){
      sessionStorage.setItem(LEGACY_ACTIVE,username);
      reload=true;
    }
    const key='platinum-v32-profile:'+username;
    let currentName='';
    try{currentName=JSON.parse(localStorage.getItem(key)||'null')?.name||''}catch{}
    if(currentName!==fullName){
      localStorage.setItem(key,JSON.stringify({name:fullName,created:new Date().toISOString(),source:'supabase'}));
      reload=true;
    }
  }catch{}
  return reload;
}
async function verify(){
  try{
    const {data:{session}}=await sb.auth.getSession();
    if(!session) return deny();
    const {data,error}=await sb.rpc('toefl_student_access');
    if(error) return deny();
    const row=Array.isArray(data)?data[0]:data;
    if(!row||!row.allowed) return deny();
    if(syncLegacyProfile(session,row)){
      location.reload();
      return;
    }
    reveal();
  }catch(e){
    return deny();
  }
}
await verify();
setInterval(async()=>{
  try{
    const {data:{session}}=await sb.auth.getSession();
    if(!session) return deny();
    const {data,error}=await sb.rpc('toefl_student_access');
    const row=Array.isArray(data)?data[0]:data;
    if(error||!row||!row.allowed) return deny();
    syncLegacyProfile(session,row);
  }catch{await deny();}
},60000);
</script>
'''

if marker in s:
    start = s.index(marker)
    end_tag = '</script>'
    end = s.find(end_tag, start)
    if end == -1:
        raise SystemExit('Existing auth guard is malformed: closing </script> not found')
    end += len(end_tag)
    s = s[:start] + guard + s[end:]
    print('Guard updated')
else:
    if '</head>' not in s:
        raise SystemExit('Could not find </head> in index.html')
    s = s.replace('</head>', guard + '\n</head>', 1)
    print('Guard injected')

hub_start = '<!-- PLATINUM_TOOLS_HUB_START -->'
hub_end = '<!-- PLATINUM_TOOLS_HUB_END -->'
hub = r'''
<!-- PLATINUM_TOOLS_HUB_START -->
<style id="platinum-tools-hub-style">
.platinum-hub-source{display:none!important}
#platinum-tools-hub-launcher{position:fixed;right:16px;bottom:16px;z-index:19000;border:0;border-radius:999px;padding:12px 18px;background:linear-gradient(135deg,#b45309,#7c2d12);color:#fff;font:700 14px/1.2 Tahoma,Arial,sans-serif;box-shadow:0 10px 28px rgba(0,0,0,.24);cursor:pointer;direction:rtl}
#platinum-tools-hub-launcher:hover{transform:translateY(-1px)}
#platinum-tools-hub-overlay[hidden]{display:none!important}
#platinum-tools-hub-overlay{position:fixed;inset:0;z-index:300000;background:rgba(15,23,42,.68);backdrop-filter:blur(4px);display:flex;align-items:center;justify-content:center;padding:18px;direction:rtl;font-family:Tahoma,Arial,sans-serif}
#platinum-tools-hub-panel{width:min(980px,100%);max-height:92vh;overflow:auto;background:#fff;color:#1f2937;border-radius:22px;box-shadow:0 30px 80px rgba(0,0,0,.34);padding:22px}
#platinum-tools-hub-head{display:flex;align-items:center;justify-content:space-between;gap:14px;border-bottom:1px solid #eadbcf;padding-bottom:14px;margin-bottom:14px}
#platinum-tools-hub-title{margin:0;font-size:22px;font-weight:800;color:#7c2d12}
#platinum-tools-hub-subtitle{margin:5px 0 0;color:#6b7280;font-size:13px}
#platinum-tools-hub-close{border:1px solid #e3c7b1;background:#fff;color:#7c2d12;border-radius:10px;padding:9px 12px;font-weight:700;cursor:pointer;white-space:nowrap}
#platinum-tools-hub-search{width:100%;box-sizing:border-box;border:1px solid #dcc7b7;border-radius:12px;padding:11px 13px;margin:0 0 16px;background:#fffaf6;color:#1f2937;outline:none}
#platinum-tools-hub-search:focus{border-color:#b45309;box-shadow:0 0 0 3px rgba(180,83,9,.12)}
.platinum-hub-section{margin:16px 0 20px}
.platinum-hub-section-title{font-size:15px;font-weight:800;color:#7c2d12;margin:0 0 9px;display:flex;align-items:center;gap:7px}
.platinum-hub-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.platinum-hub-card{border:1px solid #ead8c9;background:linear-gradient(180deg,#fff,#fffaf6);border-radius:14px;padding:12px 13px;color:#334155;text-align:right;cursor:pointer;min-height:58px;font-weight:700;line-height:1.45;box-shadow:0 2px 8px rgba(124,45,18,.05)}
.platinum-hub-card:hover{border-color:#c56d2a;background:#fff4e9;transform:translateY(-1px)}
#platinum-tools-hub-empty{padding:24px;text-align:center;color:#6b7280;background:#f8fafc;border-radius:12px}
@media(max-width:760px){#platinum-tools-hub-overlay{padding:10px;align-items:flex-end}#platinum-tools-hub-panel{max-height:88vh;border-radius:20px 20px 0 0;padding:16px}.platinum-hub-grid{grid-template-columns:1fr 1fr}#platinum-tools-hub-launcher{right:12px;bottom:12px;padding:11px 15px}}
@media(max-width:430px){.platinum-hub-grid{grid-template-columns:1fr}#platinum-tools-hub-title{font-size:19px}}
</style>
<button id="platinum-tools-hub-launcher" type="button" hidden>🧪 المختبرات والأدوات</button>
<div id="platinum-tools-hub-overlay" hidden>
  <div id="platinum-tools-hub-panel" role="dialog" aria-modal="true" aria-labelledby="platinum-tools-hub-title">
    <div id="platinum-tools-hub-head">
      <div><h2 id="platinum-tools-hub-title">🧪 مركز المختبرات والأدوات</h2><p id="platinum-tools-hub-subtitle">كل الاختبارات والمختبرات واللوحات في مكان واحد.</p></div>
      <button id="platinum-tools-hub-close" type="button">إغلاق ×</button>
    </div>
    <input id="platinum-tools-hub-search" type="search" placeholder="ابحث عن اختبار أو مختبر أو أداة..." autocomplete="off">
    <div id="platinum-tools-hub-content"></div>
  </div>
</div>
<script id="platinum-tools-hub-script">
(()=>{'use strict';
const launcher=document.getElementById('platinum-tools-hub-launcher');
const overlay=document.getElementById('platinum-tools-hub-overlay');
const closeBtn=document.getElementById('platinum-tools-hub-close');
const search=document.getElementById('platinum-tools-hub-search');
const content=document.getElementById('platinum-tools-hub-content');
if(!launcher||!overlay||!closeBtn||!search||!content)return;
const order=['الاختبارات والمحاكاة','مهارات اللغة والتدريب','المتابعة والإدارة','المختبرات والأدوات'];
const icons={'الاختبارات والمحاكاة':'🏁','مهارات اللغة والتدريب':'🎧','المتابعة والإدارة':'📊','المختبرات والأدوات':'🧪'};
let entries=[];
function category(text){
  const t=String(text||'').toLowerCase();
  if(/إدارة|لوحة|تقدم|حضور|attendance|admin|dashboard|تقارير|طلاب|مجموعات|progress/.test(t))return 'المتابعة والإدارة';
  if(/اختبار|محاكاة|exam|mock|quiz|assessment|test/.test(t))return 'الاختبارات والمحاكاة';
  if(/listening|استماع|reading|قراءة|structure|grammar|قواعد|vocab|مفردات|writing|كتابة|نطق|pronunciation|مهارة/.test(t))return 'مهارات اللغة والتدريب';
  return 'المختبرات والأدوات';
}
function collect(){
  const nodes=[...document.querySelectorAll('[id^="pa"][id$="-open"]')].filter(el=>{
    if(!(el instanceof HTMLElement)||el.closest('#platinum-tools-hub-overlay'))return false;
    const cs=getComputedStyle(el);
    return !el.hidden&&cs.display!=='none'&&cs.visibility!=='hidden'&&cs.position==='fixed';
  });
  entries=nodes.map(el=>{
    const label=(el.textContent||el.getAttribute('aria-label')||el.id).replace(/\s+/g,' ').trim();
    el.classList.add('platinum-hub-source');
    return {el,label,category:category(label+' '+el.id)};
  });
  launcher.hidden=entries.length===0;
  render('');
}
function render(query){
  const q=String(query||'').trim().toLowerCase();
  content.replaceChildren();
  const visible=entries.filter(x=>!q||x.label.toLowerCase().includes(q)||x.el.id.toLowerCase().includes(q));
  if(!visible.length){const empty=document.createElement('div');empty.id='platinum-tools-hub-empty';empty.textContent=q?'لا توجد نتيجة مطابقة للبحث.':'لا توجد أدوات عائمة لعرضها.';content.append(empty);return;}
  for(const name of order){
    const items=visible.filter(x=>x.category===name);
    if(!items.length)continue;
    const section=document.createElement('section');section.className='platinum-hub-section';
    const h=document.createElement('h3');h.className='platinum-hub-section-title';h.textContent=icons[name]+' '+name;
    const grid=document.createElement('div');grid.className='platinum-hub-grid';
    for(const item of items){
      const b=document.createElement('button');b.type='button';b.className='platinum-hub-card';b.textContent=item.label;b.dataset.target=item.el.id;
      b.addEventListener('click',()=>{overlay.hidden=true;search.value='';render('');setTimeout(()=>item.el.click(),0)});
      grid.append(b);
    }
    section.append(h,grid);content.append(section);
  }
}
function open(){render(search.value);overlay.hidden=false;setTimeout(()=>search.focus(),0)}
function close(){overlay.hidden=true;search.value='';render('')}
launcher.addEventListener('click',open);
closeBtn.addEventListener('click',close);
overlay.addEventListener('click',e=>{if(e.target===overlay)close()});
search.addEventListener('input',()=>render(search.value));
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!overlay.hidden)close()});
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',collect,{once:true});else collect();
setTimeout(collect,600);
setTimeout(collect,1800);
})();
</script>
<!-- PLATINUM_TOOLS_HUB_END -->
'''

if hub_start in s:
    start = s.index(hub_start)
    end = s.find(hub_end, start)
    if end == -1:
        raise SystemExit('Existing tools hub is malformed: end marker not found')
    end += len(hub_end)
    s = s[:start] + hub.strip() + s[end:]
    print('Tools hub updated')
else:
    if '</body>' not in s:
        raise SystemExit('Could not find </body> in index.html')
    s = s.replace('</body>', hub.strip() + '\n</body>', 1)
    print('Tools hub injected')

# Lightweight build checks: one auth marker, one hub pair, one launcher, and the source-hiding class.
checks = {
    'auth guard': s.count(marker) == 1,
    'hub start': s.count(hub_start) == 1,
    'hub end': s.count(hub_end) == 1,
    'hub launcher': s.count('id="platinum-tools-hub-launcher"') == 1,
    'hub overlay': s.count('id="platinum-tools-hub-overlay"') == 1,
    'source hide class': '.platinum-hub-source{display:none!important}' in s,
    'body close': '</body>' in s,
}
failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise SystemExit('Injection validation failed: ' + ', '.join(failed))
print('Injection validation passed')

p.write_text(s, encoding='utf-8')

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

p.write_text(s, encoding='utf-8')

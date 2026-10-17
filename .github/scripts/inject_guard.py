from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = 'PLATINUM_TOEFL_AUTH_GUARD'

if marker in s:
    print('Guard already present')
    raise SystemExit(0)

guard = r'''
<!-- PLATINUM_TOEFL_AUTH_GUARD -->
<style id="platinum-auth-guard-style">html{visibility:hidden!important}</style>
<script type="module">
import {createClient} from 'https://esm.sh/@supabase/supabase-js@2';
const sb=createClient('https://yqgqylzfveiennyprsip.supabase.co','sb_publishable_uZ1Oyk5hnQfjkJFfvdIW3A_zZmEhHYv');
const reveal=()=>{document.documentElement.style.visibility='visible';document.getElementById('platinum-auth-guard-style')?.remove();};
const deny=async()=>{try{await sb.auth.signOut()}catch{} location.replace('./student-login.html');};
async function verify(){
  try{
    const {data:{session}}=await sb.auth.getSession();
    if(!session) return deny();
    const {data,error}=await sb.rpc('toefl_student_access');
    if(error) return deny();
    const row=Array.isArray(data)?data[0]:data;
    if(!row||!row.allowed) return deny();
    reveal();
  }catch(e){
    return deny();
  }
}
await verify();
setInterval(async()=>{
  try{
    const {data,error}=await sb.rpc('toefl_student_access');
    const row=Array.isArray(data)?data[0]:data;
    if(error||!row||!row.allowed) await deny();
  }catch{await deny();}
},60000);
</script>
'''

if '</head>' not in s:
    raise SystemExit('Could not find </head> in index.html')

s = s.replace('</head>', guard + '\n</head>', 1)
p.write_text(s, encoding='utf-8')
print('Guard injected')

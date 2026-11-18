import base64,hashlib,hmac,json,os,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
MANAGE=ROOT/'selfhost/manage.py'

def env(path):
 return dict(line.split('=',1) for line in path.read_text().splitlines() if line and not line.startswith('#'))

class BootstrapTests(unittest.TestCase):
 def invoke(self,*args):
  return subprocess.run([sys.executable,str(MANAGE),*args],capture_output=True,text=True)
 def init(self,p):
  p.mkdir()
  creds=p/'credentials-input.txt';creds.write_text('DOCKER_CLOUD_USERNAME=synthetic\nDOCKER_CLOUD_PAT=synthetic-cloud-access-token\n')
  return self.invoke('init','--instance-dir',str(p),'--callback-url','https://api.example.com','--frontend-url','https://app.example.com','--docker-cloud-credentials',str(creds))
 def test_auth_tokens_are_signed_and_use_one_secret(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'new';r=self.init(p);self.assertEqual(r.returncode,0,r.stderr);v=env(p/'.env')
   self.assertEqual(v['JWT_SECRET'],v['SUPABASE_JWT_SECRET'])
   for key,role in [('ANON_KEY','anon'),('SUPABASE_ANON_KEY','anon'),('SERVICE_ROLE_KEY','service_role'),('SUPABASE_SERVICE_ROLE_KEY','service_role')]:
    a,b,c=v[key].split('.');claims=json.loads(base64.urlsafe_b64decode(b+'='*(-len(b)%4)));self.assertEqual(claims['role'],role)
    expected=base64.urlsafe_b64encode(hmac.new(v['JWT_SECRET'].encode(),(a+'.'+b).encode(),hashlib.sha256).digest()).decode().rstrip('=');self.assertEqual(c,expected)
 def test_encryption_lengths_match_supabase_bootstrap(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'new';self.init(p);v=env(p/'.env');self.assertEqual(len(v['REALTIME_DB_ENC_KEY']),16);self.assertEqual(len(v['VAULT_ENC_KEY']),32)
 def test_source_build_tags_and_browser_proxy_origin(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'new';self.init(p);v=env(p/'.env');self.assertEqual(v['API_IMAGE'],'kortix-v2-api:local');self.assertEqual(v['FRONTEND_IMAGE'],'kortix-v2-frontend:local');self.assertEqual(v['GATEWAY_IMAGE'],'kortix-v2-gateway:local');self.assertEqual(v['SUPABASE_PUBLIC_URL'],'https://app.example.com/supabase');self.assertEqual(v['DEFAULT_MEMORY_GB'],'4')
 def test_private_directory_remains_traversable_by_owner(self):
  if os.name=='nt':self.skipTest('Native Windows ACLs are outside supported production platform')
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'new';self.init(p);self.assertEqual(p.stat().st_mode&0o777,0o700)
 def test_full_template_defines_the_database_and_auth_services(self):
  text=(ROOT/'selfhost/compose.template.yml').read_text()
  for service in ['supabase-db','supabase-auth','supabase-kong','kortix-api','frontend','llm-gateway']:
   self.assertIn('\n  '+service+':',text)
 def test_unmanaged_existing_instance_is_not_reconfigured(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'existing';p.mkdir();(p/'.env').write_text('PRESERVE_ME=synthetic-value\n');r=self.invoke('init','--instance-dir',str(p));self.assertNotEqual(r.returncode,0);self.assertEqual((p/'.env').read_text(),'PRESERVE_ME=synthetic-value\n')
 def test_production_rejects_private_ip_and_route_suffix(self):
  with tempfile.TemporaryDirectory() as d:
   for i,url in enumerate(['https://127.0.0.2','https://10.0.0.1','https://api.example.com/v1/health']):
    r=self.invoke('init','--instance-dir',str(Path(d)/str(i)),'--callback-url',url);self.assertNotEqual(r.returncode,0,url)
 def test_stock_auto_updater_is_not_started(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'new';self.init(p);v=json.loads((p/'docker-compose.reachability.yml').read_text());self.assertIn('upstream-updater-disabled',v['services']['kortix-updater']['profiles'])

if __name__=='__main__':unittest.main()

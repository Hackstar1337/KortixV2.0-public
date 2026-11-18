#!/usr/bin/env python3
"""Verify source provenance, Docker integration payload and private-file exclusions."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent.parent

def verify(root=ROOT):
 data=json.loads((root/'selfhost/source-manifest.json').read_text())
 if data['upstream_revision']!='1f58c106d02140c4b050c539904d9410b438ab5f':raise ValueError('Unsupported upstream source revision')
 for item in data['integration_files']:
  path=root/item['path']
  if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Source manifest mismatch: '+item['path'])
 for required in ['LICENSE','UPSTREAM-WHITE-LABEL-LICENSE.md','apps/api/Dockerfile','apps/web/package.json','apps/llm-gateway/Dockerfile','apps/cli/src/self-host/assets/kortix-compose.yml','selfhost/manage.py','selfhost/build.sh','selfhost/Dockerfile.frontend']:
  if not (root/required).is_file():raise ValueError('Required distribution file missing: '+required)
 for path in root.rglob('*'):
  rel=path.relative_to(root)
  if any(part in ('.git','.runtime','.work','node_modules','__pycache__') for part in rel.parts):continue
  if path.is_file() and (path.name=='.env' or (path.name.startswith('.env.') and not path.name.endswith(('.example','.template','.sample')))):raise ValueError('Operational env file in distribution: '+str(rel))
 print(json.dumps({'status':'passed','integration_files':len(data['integration_files']),'upstream_revision':data['upstream_revision'],'checks':['payload integrity','required source/build/install files','operational env exclusions']}))
 return data

if __name__=='__main__':
 try:verify()
 except (ValueError,OSError,KeyError) as error:print('Source verification failed: '+str(error),file=sys.stderr);sys.exit(1)

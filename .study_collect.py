import json
import re
import subprocess
from pathlib import Path

repo = "mikkokallio/research-setup"
base = Path('study_data/snapshot_2026-03-01')
(base / 'raw').mkdir(parents=True, exist_ok=True)
(base / 'artifacts').mkdir(parents=True, exist_ok=True)
(base / 'logs').mkdir(parents=True, exist_ok=True)

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=False, encoding='utf-8', errors='ignore')

runs_cmd = ['gh','-R',repo,'run','list','--workflow','experiment.yml','--limit','20','--json','databaseId,displayTitle,status,conclusion,createdAt,updatedAt,headSha,event,url']
runs_res = run(runs_cmd)
if runs_res.returncode != 0:
    raise SystemExit(runs_res.stderr or runs_res.stdout)
runs = json.loads(runs_res.stdout)
(base / 'runs.json').write_text(json.dumps(runs, indent=2), encoding='utf-8')

completed_runs = [r for r in runs if r.get('status') == 'completed']

for run_item in completed_runs:
    run_id = str(run_item['databaseId'])
    run_dir = base / 'raw' / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    view_cmd = [
        'gh','-R',repo,'run','view',run_id,
        '--json','databaseId,displayTitle,status,conclusion,createdAt,updatedAt,headSha,event,url,jobs'
    ]
    view = run(view_cmd)
    if view.returncode == 0:
        (run_dir / 'run_view.json').write_text(view.stdout, encoding='utf-8')
    else:
        (run_dir / 'run_view_error.txt').write_text((view.stderr or view.stdout), encoding='utf-8')

    api_cmd = ['gh','api',f'repos/{repo}/actions/runs/{run_id}/artifacts']
    api = run(api_cmd)
    if api.returncode == 0:
        (run_dir / 'artifacts_manifest.json').write_text(api.stdout, encoding='utf-8')
        try:
            manifest = json.loads(api.stdout)
            for art in manifest.get('artifacts', []):
                if art.get('expired'):
                    continue
                art_name = art.get('name')
                if not art_name:
                    continue
                out_dir = base / 'artifacts' / run_id
                out_dir.mkdir(parents=True, exist_ok=True)
                dl_cmd = ['gh','-R',repo,'run','download',run_id,'-n',art_name,'-D',str(out_dir)]
                run(dl_cmd)
        except Exception as exc:
            (run_dir / 'artifact_parse_error.txt').write_text(str(exc), encoding='utf-8')
    else:
        (run_dir / 'artifacts_manifest_error.txt').write_text((api.stderr or api.stdout), encoding='utf-8')

    run_view_path = run_dir / 'run_view.json'
    if run_view_path.exists():
        try:
            rv = json.loads(run_view_path.read_text(encoding='utf-8'))
            for job in rv.get('jobs', []):
                if job.get('conclusion') == 'failure':
                    job_id = str(job.get('databaseId'))
                    job_name = re.sub(r'[^a-zA-Z0-9_-]+', '_', job.get('name', 'job'))
                    log_path = base / 'logs' / f'run_{run_id}__job_{job_id}__{job_name}.log'
                    log_cmd = ['gh','-R',repo,'run','view',run_id,'--job',job_id,'--log']
                    lg = run(log_cmd)
                    if lg.returncode == 0:
                        log_path.write_text(lg.stdout, encoding='utf-8', errors='ignore')
                    else:
                        log_path.write_text((lg.stderr or lg.stdout), encoding='utf-8', errors='ignore')
        except Exception as exc:
            (run_dir / 'run_view_parse_error.txt').write_text(str(exc), encoding='utf-8')

print(f"Collected data for {len(completed_runs)} completed runs into {base}")

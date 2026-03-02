import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

base = Path('study_data/snapshot_2026-03-01')
runs = json.loads((base / 'runs.json').read_text(encoding='utf-8'))


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return None


def read_text(path: Path):
    try:
        return path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return None


def file_info(path: Path):
    if not path.exists():
        return None
    return {
        'path': str(path).replace('\\', '/'),
        'size_bytes': path.stat().st_size,
    }


def parse_error_signatures(log_text: str):
    if not log_text:
        return []
    signatures = []
    patterns = [
        r"##\[error\](.+)",
        r"\bRuntimeError:\s*(.+)",
        r"\bIndentationError:\s*(.+)",
        r"\bJSONDecodeError:\s*(.+)",
        r"\bError:\s*(.+)",
        r"\bERROR:\s*(.+)",
    ]
    for pat in patterns:
        for m in re.finditer(pat, log_text):
            msg = re.sub(r"\s+", " ", m.group(1).strip())
            if msg and msg not in signatures:
                signatures.append(msg)
    return signatures[:25]


def extract_split_data(run_artifacts_dir: Path):
    out = {}
    split_plan_path = run_artifacts_dir / 'split_plan.json'
    split_plan = read_json(split_plan_path)
    if split_plan:
        slices = split_plan.get('slices', [])
        out['split_plan'] = {
            'slice_count': len(slices),
            'slice_ids': [s.get('id') for s in slices],
            'slice_titles': [s.get('title') for s in slices],
            'integration_notes': split_plan.get('integration_notes'),
            'file': file_info(split_plan_path),
        }

    slices_dir = run_artifacts_dir / 'slices'
    if slices_dir.exists():
        slice_files = sorted([p for p in slices_dir.glob('slice_*.md')])
        out['slices'] = []
        for p in slice_files:
            text = read_text(p) or ''
            first_lines = '\n'.join(text.splitlines()[:8])
            out['slices'].append({
                'file': file_info(p),
                'preview': first_lines,
            })

    stage_timing = read_json(run_artifacts_dir / 'stage_timing_split.json')
    if stage_timing:
        out['stage_timing_split'] = stage_timing

    usage_split = read_json(run_artifacts_dir / 'usage_split.json')
    if usage_split:
        out['usage_split'] = usage_split

    run_manifest = read_json(run_artifacts_dir / 'run_manifest.json')
    if run_manifest:
        out['run_manifest'] = run_manifest

    splitter_raw = run_artifacts_dir / 'splitter_raw.txt'
    if splitter_raw.exists():
        raw_text = read_text(splitter_raw) or ''
        out['splitter_raw'] = {
            'file': file_info(splitter_raw),
            'tail': '\n'.join(raw_text.splitlines()[-25:]),
        }

    return out


def extract_implement_data(run_artifacts_dir: Path):
    out = {}

    stage_impl = read_json(run_artifacts_dir / 'stage_timing_implement_and_test.json')
    if stage_impl:
        out['stage_timing_implement_and_test'] = stage_impl

    run_summary = read_json(run_artifacts_dir / 'run_summary.json')
    if run_summary:
        out['run_summary'] = run_summary

    deploy_info = read_json(run_artifacts_dir / 'deploy_info.json')
    if deploy_info:
        out['deploy_info'] = deploy_info

    # Agentic subtree may or may not exist depending on artifact unpack layout
    for root in [run_artifacts_dir, run_artifacts_dir / 'agentic', run_artifacts_dir / 'work' / 'agentic']:
        if not root.exists():
            continue

        logs = sorted(root.glob('logs/*.txt')) if (root / 'logs').exists() else []
        timings = sorted(root.glob('timings/*.json')) if (root / 'timings').exists() else []
        usages = sorted(root.glob('usage/*.json')) if (root / 'usage').exists() else []
        patches = sorted(root.glob('patches/*.patch')) if (root / 'patches').exists() else []
        summaries = sorted(root.glob('summaries/*.json')) if (root / 'summaries').exists() else []

        if logs or timings or usages or patches or summaries:
            out['agentic_files'] = {
                'root': str(root).replace('\\', '/'),
                'logs': [file_info(p) for p in logs],
                'timings': [read_json(p) for p in timings],
                'usage': [read_json(p) for p in usages],
                'patches': [file_info(p) for p in patches],
                'summaries': [read_json(p) for p in summaries],
            }
            break

    return out

report = {
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'snapshot_root': str(base).replace('\\', '/'),
    'run_count_total': len(runs),
    'run_count_completed': sum(1 for r in runs if r.get('status') == 'completed'),
    'runs': [],
}

all_error_signatures = Counter()

for run in runs:
    run_id = str(run['databaseId'])
    raw_dir = base / 'raw' / run_id
    art_dir = base / 'artifacts' / run_id

    run_entry = {
        'run_id': run['databaseId'],
        'status': run.get('status'),
        'conclusion': run.get('conclusion'),
        'created_at': run.get('createdAt'),
        'updated_at': run.get('updatedAt'),
        'head_sha': run.get('headSha'),
        'event': run.get('event'),
        'url': run.get('url'),
    }

    run_view = read_json(raw_dir / 'run_view.json')
    if run_view:
        jobs = []
        for job in run_view.get('jobs', []):
            failed_steps = [
                {
                    'name': s.get('name'),
                    'number': s.get('number'),
                    'conclusion': s.get('conclusion'),
                }
                for s in (job.get('steps') or [])
                if s.get('conclusion') == 'failure'
            ]
            jobs.append({
                'id': job.get('databaseId'),
                'name': job.get('name'),
                'status': job.get('status'),
                'conclusion': job.get('conclusion'),
                'started_at': job.get('startedAt'),
                'completed_at': job.get('completedAt'),
                'failed_steps': failed_steps,
                'url': job.get('url'),
            })

            if job.get('conclusion') == 'failure':
                log_name = f"run_{run_id}__job_{job.get('databaseId')}__{re.sub(r'[^a-zA-Z0-9_-]+', '_', job.get('name','job'))}.log"
                log_path = base / 'logs' / log_name
                log_text = read_text(log_path)
                sigs = parse_error_signatures(log_text or '')
                if sigs:
                    for sig in sigs:
                        all_error_signatures[sig] += 1
                job['error_signatures'] = sigs
                job['log_file'] = file_info(log_path)

        run_entry['jobs'] = jobs

    manifest = read_json(raw_dir / 'artifacts_manifest.json')
    if manifest:
        run_entry['artifact_manifest'] = {
            'total_count': manifest.get('total_count'),
            'artifacts': [
                {
                    'id': a.get('id'),
                    'name': a.get('name'),
                    'size_in_bytes': a.get('size_in_bytes'),
                    'expired': a.get('expired'),
                    'created_at': a.get('created_at'),
                    'updated_at': a.get('updated_at'),
                    'expires_at': a.get('expires_at'),
                }
                for a in manifest.get('artifacts', [])
            ],
        }

    if art_dir.exists():
        run_entry['extracted_split_data'] = extract_split_data(art_dir)
        run_entry['extracted_implement_deploy_data'] = extract_implement_data(art_dir)

    report['runs'].append(run_entry)

report['error_signature_frequency'] = [
    {'signature': sig, 'count': count}
    for sig, count in all_error_signatures.most_common()
]

out_file = Path('study_data/study_snapshot_2026-03-01.json')
out_file.parent.mkdir(parents=True, exist_ok=True)
out_file.write_text(json.dumps(report, indent=2), encoding='utf-8')
print(f'Wrote {out_file} with {len(report["runs"])} runs')

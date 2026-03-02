import argparse
import json
import os
import re
import subprocess
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


def parse_usage(raw_text: str):
    patterns = {
        "prompt_tokens": [r"prompt[_\s-]*tokens\s*[:=]\s*(\d+)", r"input[_\s-]*tokens\s*[:=]\s*(\d+)"],
        "completion_tokens": [r"completion[_\s-]*tokens\s*[:=]\s*(\d+)", r"output[_\s-]*tokens\s*[:=]\s*(\d+)"],
        "total_tokens": [r"total[_\s-]*tokens\s*[:=]\s*(\d+)"],
    }

    result = {"prompt_tokens": None, "completion_tokens": None, "total_tokens": None}
    for key, regex_list in patterns.items():
        for regex in regex_list:
            match = re.search(regex, raw_text, flags=re.IGNORECASE)
            if match:
                result[key] = int(match.group(1))
                break

    return result


@dataclass
class CmdResult:
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False
    elapsed_seconds: int = 0


def run_cmd(cmd, cwd=None, timeout_seconds=None, heartbeat_label=None, heartbeat_every_seconds=30):
    start = time.time()
    with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=True) as out_tmp, tempfile.NamedTemporaryFile(
        mode="w+", encoding="utf-8", delete=True
    ) as err_tmp:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            text=True,
            stdout=out_tmp,
            stderr=err_tmp,
        )

        last_heartbeat_mark = -1
        timed_out = False

        while True:
            code = process.poll()
            elapsed = int(time.time() - start)
            if heartbeat_label and elapsed // heartbeat_every_seconds != last_heartbeat_mark:
                last_heartbeat_mark = elapsed // heartbeat_every_seconds
                print(f"[agentic] heartbeat label={heartbeat_label} elapsed_sec={elapsed}", flush=True)

            if code is not None:
                break

            if timeout_seconds is not None and elapsed >= timeout_seconds:
                timed_out = True
                process.kill()
                process.wait()
                break

            time.sleep(1)

        out_tmp.flush()
        err_tmp.flush()
        out_tmp.seek(0)
        err_tmp.seek(0)
        stdout_text = out_tmp.read()
        stderr_text = err_tmp.read()
        final_elapsed = int(time.time() - start)

        if timed_out:
            return CmdResult(
                returncode=124,
                stdout=stdout_text,
                stderr=stderr_text,
                timed_out=True,
                elapsed_seconds=final_elapsed,
            )

        return CmdResult(
            returncode=process.returncode,
            stdout=stdout_text,
            stderr=stderr_text,
            timed_out=False,
            elapsed_seconds=final_elapsed,
        )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--condition", required=True)
    parser.add_argument("--run-key", required=True)
    parser.add_argument("--k", type=int, required=True)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--slices-dir", required=True)
    parser.add_argument("--split-plan", required=False)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    slice_timeout_seconds = int(os.getenv("COPILOT_SLICE_TIMEOUT_SEC", "420"))

    out_dir = Path(args.out_dir)
    logs_dir = out_dir / "logs"
    usage_dir = out_dir / "usage"
    timings_dir = out_dir / "timings"
    patches_dir = out_dir / "patches"
    summary_dir = out_dir / "summaries"
    for directory in [logs_dir, usage_dir, timings_dir, patches_dir, summary_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    spec_text = read_text(Path(args.spec))

    if args.condition == "k3":
        work_items = []
        split_plan = None
        if args.split_plan and Path(args.split_plan).exists():
            try:
                split_plan = json.loads(read_text(Path(args.split_plan)))
            except Exception:
                split_plan = None

        if isinstance(split_plan, dict) and isinstance(split_plan.get("slices"), list):
            shared_context = split_plan.get("shared_context")
            if not isinstance(shared_context, dict):
                shared_context = {}
            shared_context.setdefault("critical_contracts", [])
            shared_context.setdefault("cross_slice_assumptions", [])

            for index in range(1, args.k + 1):
                slice_id = f"slice_{index}"
                item = next((s for s in split_plan.get("slices", []) if s.get("id") == slice_id), None)
                if item is None:
                    raise RuntimeError(f"Missing {slice_id} in split plan")

                payload = {
                    "slice_index": index,
                    "slice_id": slice_id,
                    "slice": item,
                    "shared_context": shared_context,
                    "spec_reference": args.spec,
                    "run_context": {
                        "run_key": args.run_key,
                        "condition": args.condition,
                        "k": args.k,
                    },
                }
                work_items.append((index, json.dumps(payload, indent=2)))
        else:
            for index in range(1, args.k + 1):
                slice_path = Path(args.slices_dir) / f"slice_{index}.md"
                work_items.append((index, read_text(slice_path)))
    else:
        work_items = [(1, spec_text)]

    for index, slice_text in work_items:
        print(f"[agentic] starting slice {index}/{len(work_items)}", flush=True)
        start_epoch = int(time.time())
        start_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        prompt = f"""
You are coding agent #{index} for run {args.run_key}.
Apply ONLY the work described below to this repository.

Rules:
    - Clean-room requirement: treat `apps/web` and `apps/api` as empty targets that must be created from scratch for this run.
    - Use only the work package/spec context below as product requirements.
    - Do not reuse or depend on previous app scaffold code, examples, or prior run outputs.
- Modify files directly in the current workspace.
- Keep changes minimal and consistent.
- Do not add unrelated features.
- You may run local build/test commands as needed.
- You may dynamically re-order tasks inside this slice to maximize progress when blocked.
- Prefer authoring tests early, even if some cannot pass yet.
- If execution is blocked by missing dependencies, still write deferred tests and mark assumptions clearly in test names/messages.
- Run all tests/checks that are runnable now; defer only blocked ones.
- If a task is blocked, continue with independent contract-first or mock/stub-based work instead of waiting.
- At the end, print a short JSON object only:
    {{"slice_index": {index}, "summary": "...", "changed_files": ["..."], "tests_authored": ["..."], "tests_ran": ["..."], "tests_deferred": ["..."]}}

Work package (authoritative; includes slice object and minimal shared context):
{slice_text}
""".strip()

        cmd = [
            "copilot",
            "--allow-all",
            "--no-ask-user",
            "--model",
            args.model,
            "-p",
            prompt,
        ]

        print(f"[agentic] invoking copilot for slice {index} with timeout {slice_timeout_seconds}s", flush=True)
        result = run_cmd(
            cmd,
            timeout_seconds=slice_timeout_seconds,
            heartbeat_label=f"slice_{index}:primary",
        )
        raw = (result.stdout or "") + "\n" + (result.stderr or "")
        if result.timed_out:
            raw = (
                raw
                + f"\nTIMEOUT: Copilot call exceeded {slice_timeout_seconds} seconds for slice {index}.\n"
            )
        if result.returncode != 0:
            error_blob = raw.lower()
            if "interactive mode to enable this model" in error_blob:
                fallback_cmd = [
                    "copilot",
                    "--allow-all",
                    "--no-ask-user",
                    "--model",
                    "gpt-4.1",
                    "-p",
                    prompt,
                ]
                fallback_result = run_cmd(
                    fallback_cmd,
                    timeout_seconds=slice_timeout_seconds,
                    heartbeat_label=f"slice_{index}:fallback_gpt41",
                )
                fallback_raw = (fallback_result.stdout or "") + "\n" + (fallback_result.stderr or "")
                if fallback_result.returncode != 0:
                    fallback_cmd = [
                        "copilot",
                        "--allow-all",
                        "--no-ask-user",
                        "-p",
                        prompt,
                    ]
                    fallback_result = run_cmd(
                        fallback_cmd,
                        timeout_seconds=slice_timeout_seconds,
                        heartbeat_label=f"slice_{index}:fallback_default_model",
                    )
                    fallback_raw = (fallback_result.stdout or "") + "\n" + (fallback_result.stderr or "")
            else:
                fallback_cmd = [
                    "copilot",
                    "--allow-all",
                    "--no-ask-user",
                    "--model",
                    "gpt-4.1",
                    "-p",
                    prompt,
                ]
                fallback_result = run_cmd(
                    fallback_cmd,
                    timeout_seconds=slice_timeout_seconds,
                    heartbeat_label=f"slice_{index}:fallback_gpt41",
                )
                fallback_raw = (fallback_result.stdout or "") + "\n" + (fallback_result.stderr or "")
            raw = (
                "PRIMARY_CMD_STDOUT:\n"
                + (result.stdout or "")
                + "\nPRIMARY_CMD_STDERR:\n"
                + (result.stderr or "")
                + "\nFALLBACK_CMD_STDOUT:\n"
                + (fallback_result.stdout or "")
                + "\nFALLBACK_CMD_STDERR:\n"
                + (fallback_result.stderr or "")
            )
            result = fallback_result
        (logs_dir / f"slice_{index}_copilot_output.txt").write_text(raw, encoding="utf-8")

        diff_res = run_cmd(["git", "diff", "--", "."])
        patch_path = patches_dir / f"slice_{index}.patch"
        patch_path.write_text(diff_res.stdout or "", encoding="utf-8")

        changed_res = run_cmd(["git", "diff", "--name-only", "--", "."])
        changed_files = [line.strip() for line in (changed_res.stdout or "").splitlines() if line.strip()]

        if changed_files:
            run_cmd(["git", "add", "."])
            run_cmd(["git", "commit", "-m", f"agentic slice {index} ({args.run_key})"])

        json_start = raw.find("{")
        json_end = raw.rfind("}")
        summary_payload = {
            "slice_index": index,
            "summary": "No JSON summary found in Copilot output",
            "changed_files": changed_files,
            "exit_code": result.returncode,
        }
        if json_start != -1 and json_end != -1 and json_end > json_start:
            try:
                summary_payload = json.loads(raw[json_start : json_end + 1])
                summary_payload.setdefault("slice_index", index)
                summary_payload.setdefault("changed_files", changed_files)
                summary_payload.setdefault("exit_code", result.returncode)
            except Exception:
                pass

        (summary_dir / f"slice_{index}_summary.json").write_text(json.dumps(summary_payload, indent=2), encoding="utf-8")

        usage_payload = {
            "stage": "implement_slice",
            "slice_index": index,
            "run_key": args.run_key,
            "model": args.model,
            "condition": args.condition,
            "token_usage": parse_usage(raw),
            "cost": {
                "currency": "USD",
                "amount": None,
            },
            "raw_output_file": str((logs_dir / f"slice_{index}_copilot_output.txt").as_posix()),
            "notes": "Token usage parsed best-effort from CLI output.",
        }
        (usage_dir / f"slice_{index}_usage.json").write_text(json.dumps(usage_payload, indent=2), encoding="utf-8")

        end_epoch = int(time.time())
        end_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        timing_payload = {
            "stage": "implement_slice",
            "slice_index": index,
            "run_key": args.run_key,
            "start_epoch": start_epoch,
            "end_epoch": end_epoch,
            "start_iso": start_iso,
            "end_iso": end_iso,
            "duration_seconds": end_epoch - start_epoch,
        }
        (timings_dir / f"slice_{index}_timing.json").write_text(json.dumps(timing_payload, indent=2), encoding="utf-8")

        if result.returncode != 0:
            raise RuntimeError(f"Copilot coding step failed for slice {index}. See logs/slice_{index}_copilot_output.txt")

        print(
            f"[agentic] completed slice {index}/{len(work_items)} elapsed_sec={result.elapsed_seconds}",
            flush=True,
        )


if __name__ == "__main__":
    main()

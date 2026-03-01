import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--stage", required=True)
    args = parser.parse_args()

    payload = {
        "stage": args.stage,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metrics": {
            "duration_ms": 0,
            "status": "ok",
        },
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

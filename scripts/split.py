import argparse
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, required=True)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    k = max(args.k, 1)
    spec_path = Path(args.spec)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    content = spec_path.read_text(encoding="utf-8")
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    if not paragraphs:
        paragraphs = [content]

    slices = [[] for _ in range(k)]
    for idx, para in enumerate(paragraphs):
        slices[idx % k].append(para)

    for i, slice_paras in enumerate(slices, start=1):
        slice_path = out_dir / f"slice_{i}.md"
        body = "\n\n".join(slice_paras)
        slice_path.write_text(body, encoding="utf-8")

    (out_dir / "slices.txt").write_text("\n".join(p.name for p in out_dir.glob("slice_*.md")), encoding="utf-8")


if __name__ == "__main__":
    main()

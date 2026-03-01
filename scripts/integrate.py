import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slices", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    slices_dir = Path(args.slices)
    out_path = Path(args.out)
    slice_files = sorted(slices_dir.glob("slice_*.md"))

    parts = []
    for slice_file in slice_files:
        content = slice_file.read_text(encoding="utf-8")
        parts.append(f"# {slice_file.name}\n\n{content}")

    out_path.write_text("\n\n".join(parts), encoding="utf-8")


if __name__ == "__main__":
    main()

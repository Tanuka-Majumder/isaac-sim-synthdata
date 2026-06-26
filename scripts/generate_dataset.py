from __future__ import annotations

import argparse
from pathlib import Path

from synthetic_inspection.config import load_config
from synthetic_inspection.pipeline import generate_dataset


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate synthetic inspection data.")
    parser.add_argument("--config", default="configs/dataset.yaml")
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--mode", choices=["procedural", "isaac"], default="procedural")
    parser.add_argument("--output", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    output = generate_dataset(config, samples=args.samples, mode=args.mode, output_dir=args.output)
    print(f"Dataset written to {Path(output).resolve()}")


if __name__ == "__main__":
    main()

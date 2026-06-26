from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from synthetic_inspection.training import train_segmentation_model


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a segmentation model.")
    parser.add_argument("--config", default="configs/training.yaml")
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--output", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    dataset = args.dataset or config["dataset"]["root"]
    output = args.output or config["output"]["model_dir"]
    model_path = train_segmentation_model(config, dataset, output)
    print(f"Model written to {model_path.resolve()}")


if __name__ == "__main__":
    main()


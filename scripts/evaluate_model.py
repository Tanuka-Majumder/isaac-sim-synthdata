from __future__ import annotations

import argparse
import json
from pathlib import Path

from synthetic_inspection.metrics import summarize_detection_annotations


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate COCO-style annotation outputs.")
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--ground-truth", required=True)
    parser.add_argument("--output", default="outputs/evaluation_metrics.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metrics = summarize_detection_annotations(args.predictions, args.ground_truth)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()


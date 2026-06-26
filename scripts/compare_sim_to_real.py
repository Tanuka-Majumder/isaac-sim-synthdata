from __future__ import annotations

import argparse
import json

from synthetic_inspection.metrics import compare_metric_files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare synthetic and real validation metrics.")
    parser.add_argument("--synthetic-metrics", required=True)
    parser.add_argument("--real-metrics", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(compare_metric_files(args.synthetic_metrics, args.real_metrics), indent=2))


if __name__ == "__main__":
    main()


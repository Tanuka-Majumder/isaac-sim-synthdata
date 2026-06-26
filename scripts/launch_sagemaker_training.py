from __future__ import annotations

import argparse

from synthetic_inspection.cloud_training import launch_sagemaker_training


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Launch SageMaker training for the inspection model.")
    parser.add_argument("--config", default="configs/aws.example.yaml")
    parser.add_argument("--entry-point", default="scripts/train_model.py")
    parser.add_argument("--source-dir", default=".")
    parser.add_argument("--wait", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    job_name = launch_sagemaker_training(
        config_path=args.config,
        training_entry_point=args.entry_point,
        source_dir=args.source_dir,
        wait=args.wait,
    )
    print(f"Started SageMaker training job: {job_name}")


if __name__ == "__main__":
    main()

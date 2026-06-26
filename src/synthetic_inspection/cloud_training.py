from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_cloud_config(path: str | Path) -> dict[str, Any]:
    config = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    if not isinstance(config, dict):
        raise ValueError("Cloud configuration must be a YAML mapping.")
    return config


def launch_sagemaker_training(
    config_path: str | Path,
    training_entry_point: str = "scripts/train_model.py",
    source_dir: str = ".",
    wait: bool = False,
) -> str:
    try:
        from sagemaker.pytorch import PyTorch
    except ImportError as exc:
        raise RuntimeError("Install cloud dependencies with: pip install -e .[cloud]") from exc

    config = load_cloud_config(config_path)
    dataset = config["dataset"]
    sagemaker_config = config["sagemaker"]
    input_uri = f"s3://{dataset['s3_bucket']}/{dataset['s3_prefix'].strip('/')}"

    estimator = PyTorch(
        entry_point=training_entry_point,
        source_dir=source_dir,
        role=sagemaker_config["role_arn"],
        framework_version="2.1.0",
        py_version="py310",
        instance_count=int(sagemaker_config["instance_count"]),
        instance_type=sagemaker_config["instance_type"],
        output_path=sagemaker_config["output_path"],
        hyperparameters={
            "config": "configs/training.yaml",
            "dataset": "/opt/ml/input/data/train",
            "output": "/opt/ml/model",
        },
    )
    estimator.fit({"train": input_uri}, wait=wait)
    return estimator.latest_training_job.name


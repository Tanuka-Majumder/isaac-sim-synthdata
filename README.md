# Synthetic Data Generation and Domain Randomization with NVIDIA Isaac Sim

This project builds a reproducible synthetic-data pipeline for robotic surface-defect inspection. It creates randomized Isaac Sim inspection scenes, exports paired RGB/depth/segmentation data, versions datasets for cloud training, and trains/evaluates semantic segmentation models.

The code is designed to run in two modes:

- `procedural`: generates deterministic RGB/depth/mask samples with the same dataset contract used by the Isaac Sim export path. This is useful for local development, CI, and pipeline validation.
- `isaac`: uses NVIDIA Isaac Sim APIs when run inside an Isaac Sim Python environment.

## Project Layout

```text
configs/                         Experiment configuration files
docs/                            Architecture and project documentation
scripts/                         CLI entry points
src/synthetic_inspection/         Reusable pipeline package
tests/                           Unit tests for non-Isaac logic
```

## Documentation

- [Architecture](docs/architecture.md)
- [Technical overview](docs/technical_overview.md)
- [GitHub readiness checklist](docs/github_readiness.md)

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev,train,cloud]"
python scripts/generate_dataset.py --config configs/dataset.yaml --samples 16 --mode procedural
python scripts/evaluate_model.py --predictions outputs/dataset/annotations/instances.json --ground-truth outputs/dataset/annotations/instances.json
pytest
```

## Generate Synthetic Data

Procedural generation:

```powershell
python scripts/generate_dataset.py --config configs/dataset.yaml --samples 100 --mode procedural --output outputs/dataset
```

Inside Isaac Sim:

```powershell
python scripts/generate_dataset.py --config configs/dataset.yaml --samples 1000 --mode isaac --output data/generated/inspection_v1
```

Each generated dataset contains:

- `rgb/*.png`
- `depth/*.npy`
- `masks/*.png`
- `annotations/instances.json`
- `manifest.json`

## Train Segmentation Model

```powershell
python scripts/train_model.py --config configs/training.yaml --dataset data/generated/inspection_v1 --output models/segmentation_v1
```

## Compare Synthetic and Real Evaluation Splits

```powershell
python scripts/compare_sim_to_real.py --synthetic-metrics outputs/synthetic_metrics.json --real-metrics outputs/real_metrics.json
```

## Upload Dataset to S3

```powershell
python scripts/upload_to_s3.py --dataset data/generated/inspection_v1 --bucket surface-defect-inspection-datasets --prefix inspection/inspection_v1
```

## Launch SageMaker Training

```powershell
python scripts/launch_sagemaker_training.py --config configs/aws.example.yaml
```


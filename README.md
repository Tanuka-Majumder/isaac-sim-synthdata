# Synthetic Data Generation and Domain Randomization with NVIDIA Isaac Sim

This project implements a reproducible synthetic-data pipeline for robotic surface-defect inspection. It randomizes inspection-scene conditions, exports paired RGB/depth/segmentation data, versions datasets for cloud training, and provides training/evaluation utilities for semantic segmentation models.

The repository is structured as an end-to-end engineering project: configuration-driven data generation, a consistent dataset contract, local validation, model training, evaluation, S3 upload, SageMaker launch support, documentation, and CI.

## What This Demonstrates

- Synthetic-data pipeline design for robotic inspection workflows
- Domain randomization across lighting, camera pose, material properties, and defect geometry
- Dataset export with RGB images, depth arrays, semantic masks, COCO-style annotations, and manifest metadata
- Reproducible command-line workflows for generation, training, evaluation, and cloud handoff
- Testable Python package structure with CI coverage for non-Isaac logic

The code is designed to run in two modes:

- `procedural`: generates deterministic RGB/depth/mask samples with the same dataset contract used by the Isaac Sim export path. This is useful for local development, CI, and pipeline validation.
- `isaac`: uses NVIDIA Isaac Sim APIs when run inside an Isaac Sim Python environment.

## Repository Structure

```text
configs/                         Experiment configuration files
docs/                            Architecture and project documentation
scripts/                         CLI entry points
src/synthetic_inspection/         Reusable pipeline package
tests/                           Unit tests for non-Isaac logic
```

Generated datasets, trained model weights, local environments, and cache files are intentionally excluded from version control.

## Documentation

- [Architecture](docs/architecture.md)
- [Technical overview](docs/technical_overview.md)

## Quick Start

Install the package with development dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

Run tests and generate a small validation dataset:

```powershell
pytest
python scripts/generate_dataset.py --config configs/dataset.yaml --samples 16 --mode procedural
python scripts/evaluate_model.py --predictions outputs/dataset/annotations/instances.json --ground-truth outputs/dataset/annotations/instances.json
```

Install optional training and cloud dependencies when needed:

```powershell
pip install -e ".[train,cloud]"
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

## Validation

The project includes unit tests for configuration loading, deterministic randomization, and dataset generation:

```powershell
pytest -q
```

The GitHub Actions workflow in `.github/workflows/ci.yml` runs the same test suite on each push and pull request.

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

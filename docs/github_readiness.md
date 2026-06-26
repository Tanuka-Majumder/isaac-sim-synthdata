# GitHub Readiness Checklist

This repository is intended to be reviewed as a complete project without committing generated datasets or trained model artifacts.

## Included

- Source package under `src/synthetic_inspection`
- Command-line scripts under `scripts`
- Configuration files under `configs`
- Unit tests under `tests`
- Project README
- Architecture and technical overview documentation
- CI workflow for automated tests

## Excluded

- Generated datasets
- Trained model weights
- Local virtual environments
- Python cache directories
- Cloud credentials

## Recommended Review Flow

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
python scripts/generate_dataset.py --config configs/dataset.yaml --samples 8 --mode procedural
```

The generated files are written under `outputs/`, which is intentionally ignored by Git.


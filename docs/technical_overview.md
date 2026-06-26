# Technical Overview

## Problem

Robotic defect inspection models often need labeled examples of surface scratches, dents, stains, and similar manufacturing defects. Collecting and labeling real images can be expensive, especially when defects are rare or safety-critical.

This project addresses that gap with a configurable synthetic-data pipeline that randomizes scene conditions and exports supervised segmentation data.

## Implementation Highlights

- Config-driven scene and randomization parameters in YAML.
- Deterministic procedural generation path for local validation and tests.
- Isaac Sim execution path for simulation-backed rendering.
- Dataset exporter with RGB images, depth arrays, semantic masks, COCO-style annotations, and manifest metadata.
- Baseline PyTorch segmentation training script.
- Evaluation utility for comparing synthetic and real validation metrics.
- S3 upload and SageMaker training launch scripts for cloud workflows.
- Unit tests covering configuration loading, randomization, and dataset generation.

## Engineering Decisions

The repository keeps rendering, exporting, training, evaluation, and cloud operations in separate modules. This makes the code easier to test locally and easier to extend when adding new defect types, assets, or camera configurations.

The procedural generation mode is included so the data contract can be validated without requiring Isaac Sim on every development machine or CI runner. The Isaac-specific path remains isolated in `isaac_scene.py`.

## Extension Points

- Add production USD assets for inspection parts and fixtures.
- Add Replicator annotators for instance segmentation and surface normals.
- Add additional material randomization presets for metal, plastic, and coated surfaces.
- Replace the baseline segmentation model with DeepLabV3, Mask2Former, or a custom inspection model.
- Add experiment tracking through MLflow, Weights & Biases, or SageMaker Experiments.


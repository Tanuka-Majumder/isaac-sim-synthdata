from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_coco_annotations(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def category_counts(coco: dict[str, Any]) -> dict[int, int]:
    counts: dict[int, int] = {}
    for annotation in coco.get("annotations", []):
        category_id = int(annotation["category_id"])
        counts[category_id] = counts.get(category_id, 0) + 1
    return counts


def annotation_recall(predictions: dict[str, Any], ground_truth: dict[str, Any]) -> float:
    gt_count = len(ground_truth.get("annotations", []))
    if gt_count == 0:
        return 1.0
    pred_count = len(predictions.get("annotations", []))
    return min(1.0, pred_count / gt_count)


def summarize_detection_annotations(
    predictions_path: str | Path,
    ground_truth_path: str | Path,
) -> dict[str, Any]:
    predictions = load_coco_annotations(predictions_path)
    ground_truth = load_coco_annotations(ground_truth_path)
    return {
        "prediction_annotations": len(predictions.get("annotations", [])),
        "ground_truth_annotations": len(ground_truth.get("annotations", [])),
        "annotation_recall_estimate": annotation_recall(predictions, ground_truth),
        "prediction_category_counts": category_counts(predictions),
        "ground_truth_category_counts": category_counts(ground_truth),
    }


def compare_metric_files(synthetic_path: str | Path, real_path: str | Path) -> dict[str, Any]:
    synthetic = json.loads(Path(synthetic_path).read_text(encoding="utf-8"))
    real = json.loads(Path(real_path).read_text(encoding="utf-8"))
    synthetic_score = float(
        synthetic.get("mean_iou", synthetic.get("annotation_recall_estimate", 0.0))
    )
    real_score = float(real.get("mean_iou", real.get("annotation_recall_estimate", 0.0)))
    gap = synthetic_score - real_score
    return {
        "synthetic_score": synthetic_score,
        "real_score": real_score,
        "sim_to_real_gap": gap,
        "sim_to_real_gap_percent": gap * 100.0,
    }

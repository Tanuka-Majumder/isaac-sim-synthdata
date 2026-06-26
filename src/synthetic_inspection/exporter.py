from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from random import Random
from typing import Any

import numpy as np
from PIL import Image, ImageDraw

from .randomization import DomainSample


CLASS_TO_ID = {"background": 0, "scratch": 1, "dent": 2, "stain": 3}


class DatasetExporter:
    def __init__(self, output_dir: str | Path, resolution: tuple[int, int] = (640, 480)) -> None:
        self.output_dir = Path(output_dir)
        self.width, self.height = resolution
        self.rgb_dir = self.output_dir / "rgb"
        self.depth_dir = self.output_dir / "depth"
        self.mask_dir = self.output_dir / "masks"
        self.annotation_dir = self.output_dir / "annotations"
        for directory in [self.rgb_dir, self.depth_dir, self.mask_dir, self.annotation_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        self.images: list[dict[str, Any]] = []
        self.annotations: list[dict[str, Any]] = []
        self._annotation_id = 1

    def export_procedural_sample(self, sample_id: int, sample: DomainSample, seed: int) -> dict[str, str]:
        rng = Random(seed + sample_id)
        base = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        color = [int(channel * 255) for channel in sample.surface["color"]]
        base[:, :] = color
        noise = np.random.default_rng(seed + sample_id).normal(0, 9, base.shape)
        rgb = np.clip(base + noise, 0, 255).astype(np.uint8)

        mask = Image.new("L", (self.width, self.height), 0)
        draw_mask = ImageDraw.Draw(mask)
        rgb_image = Image.fromarray(rgb, mode="RGB")
        draw_rgb = ImageDraw.Draw(rgb_image)

        defect_classes = ["scratch", "dent", "stain"]
        for _ in range(sample.defects["count"]):
            cls = rng.choice(defect_classes)
            x = rng.randint(40, self.width - 80)
            y = rng.randint(40, self.height - 80)
            length = sample.defects["length_px"]
            width = sample.defects["width_px"]
            if cls == "scratch":
                bbox = [x, y, length, max(2, width)]
                shape = [x, y, x + length, y + max(2, width)]
            elif cls == "dent":
                radius = max(8, width * 3)
                bbox = [x - radius, y - radius, radius * 2, radius * 2]
                shape = [x - radius, y - radius, x + radius, y + radius]
            else:
                stain_w = max(18, length // 2)
                stain_h = max(12, width * 4)
                bbox = [x, y, stain_w, stain_h]
                shape = [x, y, x + stain_w, y + stain_h]

            class_id = CLASS_TO_ID[cls]
            draw_mask.rectangle(shape, fill=class_id)
            draw_rgb.rectangle(shape, fill=(160, 45, 40) if cls != "dent" else (75, 75, 80))
            self.annotations.append(
                {
                    "id": self._annotation_id,
                    "image_id": sample_id,
                    "category_id": class_id,
                    "bbox": [int(v) for v in bbox],
                    "area": int(bbox[2] * bbox[3]),
                    "iscrowd": 0,
                    "segmentation": [],
                }
            )
            self._annotation_id += 1

        depth = np.full((self.height, self.width), sample.camera["distance"], dtype=np.float32)
        rgb_path = self.rgb_dir / f"{sample_id:06d}.png"
        mask_path = self.mask_dir / f"{sample_id:06d}.png"
        depth_path = self.depth_dir / f"{sample_id:06d}.npy"
        rgb_image.save(rgb_path)
        mask.save(mask_path)
        np.save(depth_path, depth)

        self.images.append(
            {
                "id": sample_id,
                "file_name": str(rgb_path.relative_to(self.output_dir)),
                "width": self.width,
                "height": self.height,
            }
        )
        return {"rgb": str(rgb_path), "mask": str(mask_path), "depth": str(depth_path)}

    def write_annotations(self) -> Path:
        payload = {
            "images": self.images,
            "annotations": self.annotations,
            "categories": [
                {"id": class_id, "name": name}
                for name, class_id in CLASS_TO_ID.items()
                if name != "background"
            ],
        }
        path = self.annotation_dir / "instances.json"
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path

    def write_manifest(self, config: dict[str, Any], samples: list[DomainSample]) -> Path:
        manifest = {
            "config": config,
            "sample_count": len(samples),
            "samples": [asdict(sample) for sample in samples],
        }
        path = self.output_dir / "manifest.json"
        path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return path

from __future__ import annotations

from pathlib import Path
from typing import Any

from tqdm import trange

from .config import ProjectConfig
from .exporter import DatasetExporter
from .isaac_scene import InspectionScene
from .randomization import DomainRandomizer, DomainSample


def camera_resolution(config: dict[str, Any]) -> tuple[int, int]:
    resolution = config.get("scene", {}).get("camera", {}).get("resolution", [640, 480])
    return int(resolution[0]), int(resolution[1])


def generate_dataset(
    config: ProjectConfig,
    samples: int,
    mode: str = "procedural",
    output_dir: str | Path | None = None,
) -> Path:
    destination = Path(output_dir) if output_dir is not None else config.output_dir
    randomizer = DomainRandomizer(config.raw, seed=config.seed)
    scene = InspectionScene(config.raw, mode=mode)
    scene.initialize()
    exporter = DatasetExporter(destination, resolution=camera_resolution(config.raw))

    generated_samples: list[DomainSample] = []
    for sample_id in trange(1, samples + 1, desc="Generating samples"):
        sample = randomizer.sample()
        scene.apply_randomization(sample)
        scene.render_sample(sample_id, sample, destination)
        if mode == "procedural":
            exporter.export_procedural_sample(sample_id, sample, config.seed)
        generated_samples.append(sample)

    exporter.write_annotations()
    exporter.write_manifest(config.raw, generated_samples)
    return destination

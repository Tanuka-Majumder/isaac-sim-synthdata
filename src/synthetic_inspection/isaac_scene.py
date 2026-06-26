from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from .randomization import DomainSample


class IsaacUnavailableError(RuntimeError):
    pass


class InspectionScene:
    def __init__(self, config: dict[str, Any], mode: str = "procedural") -> None:
        self.config = config
        self.mode = mode
        self._isaac_modules_loaded = False

    def initialize(self) -> None:
        if self.mode == "procedural":
            return
        try:
            __import__("omni.isaac.core")
            __import__("omni.replicator.core")
        except ImportError as exc:
            raise IsaacUnavailableError(
                "Isaac Sim Python modules were not found. Run with --mode procedural "
                "or execute this script from an Isaac Sim Python environment."
            ) from exc
        self._isaac_modules_loaded = True

    def apply_randomization(self, sample: DomainSample) -> None:
        if self.mode == "procedural":
            return
        if not self._isaac_modules_loaded:
            raise IsaacUnavailableError("Call initialize() before applying randomization.")
        import omni.replicator.core as rep  # type: ignore

        with rep.trigger.on_frame():
            rep.modify.pose(
                rotation=(
                    sample.camera["pitch_deg"],
                    0.0,
                    sample.camera["yaw_deg"],
                )
            )

    def render_sample(self, sample_id: int, sample: DomainSample, output_dir: Path) -> dict[str, Any]:
        if self.mode == "procedural":
            return {"sample_id": sample_id, "randomization": asdict(sample)}
        if not self._isaac_modules_loaded:
            raise IsaacUnavailableError("Call initialize() before rendering samples.")
        return {"sample_id": sample_id, "randomization": asdict(sample)}

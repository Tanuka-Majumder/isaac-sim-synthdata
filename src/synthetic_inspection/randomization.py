from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Any


@dataclass(frozen=True)
class DomainSample:
    lighting: dict[str, float]
    camera: dict[str, float]
    surface: dict[str, Any]
    defects: dict[str, Any]


class DomainRandomizer:
    def __init__(self, config: dict[str, Any], seed: int = 42) -> None:
        self.config = config
        self.rng = Random(seed)

    def sample(self) -> DomainSample:
        randomization = self.config.get("randomization", {})
        return DomainSample(
            lighting={
                "intensity": self._range(randomization, "lighting", "intensity"),
                "color_temperature": self._range(
                    randomization, "lighting", "color_temperature"
                ),
                "x_jitter": self._range(randomization, "lighting", "position_jitter"),
                "y_jitter": self._range(randomization, "lighting", "position_jitter"),
            },
            camera={
                "yaw_deg": self._range(randomization, "camera", "yaw_deg"),
                "pitch_deg": self._range(randomization, "camera", "pitch_deg"),
                "distance": self._range(randomization, "camera", "distance"),
            },
            surface={
                "roughness": self._range(randomization, "surface", "roughness"),
                "metallic": self._range(randomization, "surface", "metallic"),
                "color": self.rng.choice(randomization.get("surface", {}).get("color", [[0.5, 0.5, 0.5]])),
            },
            defects={
                "count": self._integer_range(randomization, "defects", "count"),
                "length_px": self._integer_range(randomization, "defects", "length_px"),
                "width_px": self._integer_range(randomization, "defects", "width_px"),
            },
        )

    def _range(self, root: dict[str, Any], group: str, key: str) -> float:
        spec = root.get(group, {}).get(key, {"min": 0.0, "max": 1.0})
        return self.rng.uniform(float(spec["min"]), float(spec["max"]))

    def _integer_range(self, root: dict[str, Any], group: str, key: str) -> int:
        spec = root.get(group, {}).get(key, {"min": 0, "max": 1})
        return self.rng.randint(int(spec["min"]), int(spec["max"]))


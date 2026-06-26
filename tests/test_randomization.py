from synthetic_inspection.randomization import DomainRandomizer


def test_randomizer_is_repeatable() -> None:
    config = {
        "randomization": {
            "lighting": {
                "intensity": {"min": 1, "max": 1},
                "color_temperature": {"min": 2, "max": 2},
                "position_jitter": {"min": 0, "max": 0},
            },
            "camera": {
                "yaw_deg": {"min": 0, "max": 0},
                "pitch_deg": {"min": 0, "max": 0},
                "distance": {"min": 1, "max": 1},
            },
            "surface": {
                "roughness": {"min": 0.5, "max": 0.5},
                "metallic": {"min": 0.2, "max": 0.2},
                "color": [[0.1, 0.2, 0.3]],
            },
            "defects": {
                "count": {"min": 1, "max": 1},
                "length_px": {"min": 10, "max": 10},
                "width_px": {"min": 3, "max": 3},
            },
        }
    }
    sample = DomainRandomizer(config, seed=7).sample()
    assert sample.lighting["intensity"] == 1
    assert sample.camera["distance"] == 1
    assert sample.defects["count"] == 1


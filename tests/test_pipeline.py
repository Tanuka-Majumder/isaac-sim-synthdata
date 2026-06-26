from synthetic_inspection.config import load_config
from synthetic_inspection.pipeline import generate_dataset


def test_generate_procedural_dataset(tmp_path) -> None:
    config = load_config("configs/dataset.yaml")
    output = generate_dataset(config, samples=2, mode="procedural", output_dir=tmp_path)
    assert (output / "rgb" / "000001.png").exists()
    assert (output / "depth" / "000001.npy").exists()
    assert (output / "masks" / "000001.png").exists()
    assert (output / "annotations" / "instances.json").exists()
    assert (output / "manifest.json").exists()

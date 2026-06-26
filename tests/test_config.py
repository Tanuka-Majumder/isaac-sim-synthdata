from synthetic_inspection.config import load_config


def test_load_dataset_config() -> None:
    config = load_config("configs/dataset.yaml")
    assert config.seed == 42
    assert config.output_dir.as_posix() == "outputs/dataset"


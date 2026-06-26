from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def train_segmentation_model(config: dict[str, Any], dataset_root: str | Path, output_dir: str | Path) -> Path:
    try:
        import torch
        from torch import nn
        from torch.utils.data import DataLoader
        from torchvision import transforms
    except ImportError as exc:
        raise RuntimeError("Install training dependencies with: pip install -e .[train]") from exc

    from PIL import Image

    class MaskDataset(torch.utils.data.Dataset):
        def __init__(self, root: Path) -> None:
            self.rgb_paths = sorted((root / "rgb").glob("*.png"))
            self.mask_dir = root / "masks"
            self.transform = transforms.Compose(
                [
                    transforms.Resize(tuple(config["training"]["image_size"])),
                    transforms.ToTensor(),
                ]
            )

        def __len__(self) -> int:
            return len(self.rgb_paths)

        def __getitem__(self, index: int) -> tuple[Any, Any]:
            rgb_path = self.rgb_paths[index]
            image = Image.open(rgb_path).convert("RGB")
            mask = Image.open(self.mask_dir / rgb_path.name).resize(
                tuple(config["training"]["image_size"]),
                resample=Image.Resampling.NEAREST,
            )
            return self.transform(image), torch.as_tensor(list(mask.getdata()), dtype=torch.long).reshape(
                tuple(config["training"]["image_size"])
            )

    root = Path(dataset_root)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    dataset = MaskDataset(root)
    if len(dataset) == 0:
        raise ValueError(f"No training images found under {root / 'rgb'}")

    device_name = config["training"].get("device", "auto")
    device = "cuda" if device_name == "auto" and torch.cuda.is_available() else "cpu"
    loader = DataLoader(dataset, batch_size=int(config["training"]["batch_size"]), shuffle=True)
    num_classes = int(config["dataset"]["num_classes"])
    model = nn.Sequential(
        nn.Conv2d(3, 16, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.Conv2d(16, num_classes, kernel_size=1),
    ).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=float(config["training"]["learning_rate"]))
    criterion = nn.CrossEntropyLoss()

    history: list[dict[str, float]] = []
    for epoch in range(int(config["training"]["epochs"])):
        total_loss = 0.0
        for images, masks in loader:
            images = images.to(device)
            masks = masks.to(device)
            optimizer.zero_grad()
            logits = model(images)
            loss = criterion(logits, masks)
            loss.backward()
            optimizer.step()
            total_loss += float(loss.detach().cpu())
        history.append({"epoch": epoch + 1, "loss": total_loss / max(1, len(loader))})

    torch.save(model.state_dict(), output / "model.pt")
    (output / "history.json").write_text(json.dumps(history, indent=2), encoding="utf-8")
    return output / "model.pt"


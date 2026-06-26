from __future__ import annotations

from pathlib import Path


def upload_directory_to_s3(local_root: str | Path, bucket: str, prefix: str) -> list[str]:
    try:
        import boto3
    except ImportError as exc:
        raise RuntimeError("Install cloud dependencies with: pip install -e .[cloud]") from exc

    root = Path(local_root)
    if not root.exists():
        raise FileNotFoundError(f"Dataset directory does not exist: {root}")

    client = boto3.client("s3")
    uploaded: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        key = f"{prefix.rstrip('/')}/{relative}"
        client.upload_file(str(path), bucket, key)
        uploaded.append(f"s3://{bucket}/{key}")
    return uploaded


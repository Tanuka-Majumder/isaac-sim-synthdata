from __future__ import annotations

import argparse

from synthetic_inspection.cloud import upload_directory_to_s3


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload a generated dataset to S3.")
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--prefix", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    uploaded = upload_directory_to_s3(args.dataset, args.bucket, args.prefix)
    print(f"Uploaded {len(uploaded)} files.")


if __name__ == "__main__":
    main()


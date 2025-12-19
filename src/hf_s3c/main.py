import logging

import os
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

import huggingface_hub  # noqa: F401
import s3impleclient as s3c

s3c.configure_logging(logging.INFO)
s3c.patch_all()

import argparse

from hf_s3c.download import add_download_parser
from hf_s3c.upload import add_upload_parser

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hf-s3c",
        description="huggingface-cli-like tool accelerated by S3impleClient",
        epilog="See 'hf-s3c <command> --help' for more information about a specific command.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    add_download_parser(subparsers)
    add_upload_parser(subparsers)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

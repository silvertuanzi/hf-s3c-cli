from argparse import _SubParsersAction
from pathlib import Path

def add_upload_parser(subparsers: _SubParsersAction):
    p = subparsers.add_parser(
        "upload",
        help="Upload files or folders to the Hugging Face Hub using S3impleClient acceleration",
    )

    p.add_argument(
        "repo_id",
        help="ID of the repo to download from (e.g. `username/repo-name`).",
    )

    p.add_argument(
        "local_path",
        nargs="?",
        type=Path,
        default=Path("."),
        help="Local file or folder to upload. Defaults to current directory. Unlike hf cli, Wildcard patterns are not supported here.",
    )

    p.add_argument(
        "path_in_repo",
        nargs="?",
        help="Path in the repositoryPath of the file or folder in the repo. Defaults to the relative path of the file or folder.",
    )

    p.add_argument(
        "--repo-type",
        choices=["model", "dataset", "space"],
        default="model",
        help="Type of the repo to upload to (e.g. `dataset`). Defaults to 'model'."
    )

    p.add_argument(
        "--include", 
        action="append",
        help="Glob patterns to match files to upload.",
    )

    p.add_argument(
        "--exclude", 
        action="append",
        help="Glob patterns to exclude from files to upload.",
    )

    p.set_defaults(func=cmd_upload)


def cmd_upload(args):
    from huggingface_hub import upload_file, upload_folder

    local_path: Path = args.local_path
    path_in_repo = args.path_in_repo

    common_kwargs = dict(
        repo_id=args.repo_id,
        repo_type=args.repo_type,
    )

    if local_path.is_file():
        if path_in_repo:
            repo_path = Path(path_in_repo)
        else:
            repo_path = Path(local_path.name)

        upload_file(
            path_or_fileobj=str(local_path),
            path_in_repo=repo_path.as_posix(),
            **common_kwargs,
        )

    else:
        if path_in_repo is None:
            repo_dir = local_path.name
        else:
            repo_dir = path_in_repo

        upload_folder(
            folder_path=str(local_path),
            path_in_repo=repo_dir,
            allow_patterns=args.include,
            ignore_patterns=args.exclude,
            **common_kwargs,
        )

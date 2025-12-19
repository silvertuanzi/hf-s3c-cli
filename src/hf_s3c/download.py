from argparse import _SubParsersAction

def add_download_parser(subparsers: _SubParsersAction):
    p = subparsers.add_parser(
        "download",
        help="Download files from the Hugging Face Hub using S3impleClient acceleration",
    )

    p.add_argument(
        "repo_id",
        help="ID of the repo to download from (e.g. `username/repo-name`).",
    )
    p.add_argument(
        "filenames", 
        nargs="*",
        help="Files to download (e.g. `config.json`, `data/metadata.jsonl`).",
    )

    p.add_argument(
        "--repo-type",
        choices=["model", "dataset", "space"],
        default="model",
        help="Type of repo to download from (defaults to 'model').",
    )

    p.add_argument(
        "--include", 
        action="append",
        help="Glob patterns to match files to download.",
    )

    p.add_argument(
        "--exclude", 
        action="append",
        help="Glob patterns to exclude from files to download.",
    )

    p.add_argument(
        "--local-dir",
        help="If set, the downloaded file will be placed under this directory. Check out https://huggingface.co/docs/huggingface_hub/guides/download#download-files-to-local-folder for more details.",
    )
    
    p.add_argument(
        "--revision",
        default=None,
        help="An optional Git revision id which can be a branch name, a tag, or a commit hash."
    )

    p.set_defaults(func=cmd_download)

def cmd_download(args):
    from huggingface_hub import hf_hub_download, snapshot_download

    common_kwargs = dict(
        repo_id=args.repo_id,
        repo_type=args.repo_type,
        revision=args.revision,
    )

    use_local_dir = args.local_dir is not None

    if args.filenames and not (args.include or args.exclude):
        for filename in args.filenames:
            kwargs = dict(
                filename=filename,
                **common_kwargs,
            )

            if use_local_dir:
                kwargs["local_dir"] = args.local_dir

            path = hf_hub_download(**kwargs)
            print(path)

    else:
        kwargs = dict(
            allow_patterns=args.include,
            ignore_patterns=args.exclude,
            **common_kwargs,
        )

        if use_local_dir:
            kwargs["local_dir"] = args.local_dir

        path = snapshot_download(**kwargs)
        print(path)

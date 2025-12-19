# Huggingface-cli accelerate by S3impleClient

A CLI tool similar to huggingface-cli, but use [S3impleClient](https://github.com/KohakuBlueleaf/S3impleClient) for accelerating download/upload.

## Install

Upstream has [Attribute Error](https://github.com/KohakuBlueleaf/S3impleClient/issues/1), so install my fork version first:
```
pip install git+https://github.com/silvertuanzi/S3impleClient.git
```
Then install the CLI:
```
pip install git+https://github.com/silvertuanzi/hf-s3c-cli.git
```

### Install as a command use uv tool

Alternatively, you can use `uv tool` (similar to `pipx`) to install this repo:
```
uv tool install git+https://github.com/silvertuanzi/hf-s3c-cli.git --with git+https://github.com/silvertuanzi/S3impleClient.git
```

## Usage

Not recommend to use it as a python module. Don't import it in `.py` codes. Only use it as a cli tool.
If you want to use in `.py` codes, use [S3impleClient itself](https://github.com/KohakuBlueleaf/S3impleClient) directly.

```
hf-s3c download repo_id [filenames ...]
hf-s3c upload repo_id [local_path] [path_in_repo]
```
Use it similar to hf-cli. 
For more details, use
```
hf-s3c download --help
hf-s3c upload --help
```
[S3impleClient](https://github.com/KohakuBlueleaf/S3impleClient) accelerates uploads and downloads without using HF_XET, which otherwise consumes a lot of CPU and disk.
It cannot patch XET uploads/downloads, so this CLI automatically sets `HF_HUB_DISABLE_XET=1`.

## Limitations

1. Manage authentication is not implemented.
	- To download from a private repo or upload files, you need to run `hf auth login` first.
	- Once your token is stored in `$HF_HOME/token`, you can use `hf-s3c` for upload/download.
	- The `HF_TOKEN` environment variable should also work, but it has not been fully tested.
2. This repo only implement download and upload. For repo management or other features, use the original huggingface-cli.
3. The argument below are all not supported:
	- download:
		- `--revision`: not fully tested
		- `--cache-dir`, `--token`: use env variables can do the same things
		- `--force-download`, `--quiet`, `--max-workers`
	- upload:
		- `--private`: not support creating new repo, so ignore it
		- `--token`: use env variables can do the same things
		- `--revision`, `--delete`, `--commit-message`, `--commit-description`, `--create-pr`, `--every`, `--quiet`
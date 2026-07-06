"""Clone official Kubernetes and Terraform docs."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from src.config import load_settings, root_path


def git(args: list[str], cwd: Path | None = None) -> None:
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr.strip() or r.stdout.strip())


def clone_or_update(url: str, dest: Path, sparse: list[str]) -> None:
    if dest.exists() and (dest / ".git").exists():
        print(f"Updating {dest.name}...")
        git(["pull", "--ff-only"], dest)
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"Cloning {dest.name}...")
    git(["clone", "--depth", "1", "--filter=blob:none", "--sparse", url, str(dest)])
    git(["sparse-checkout", "init", "--cone"], dest)
    git(["sparse-checkout", "set", *sparse], dest)


def main() -> None:
    settings = load_settings()
    paths = settings["paths"]
    clone_or_update(
        settings["doc_sources"]["kubernetes"]["repo_url"],
        root_path(paths["raw_kubernetes"]),
        ["content/en/docs"],
    )
    clone_or_update(
        settings["doc_sources"]["terraform"]["repo_url"],
        root_path(paths["raw_terraform"]),
        ["content/terraform"],
    )
    print("Doc repos ready under data/raw/")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

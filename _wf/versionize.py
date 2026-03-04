#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

import git
from tomlkit import dumps
from tomlkit import parse


def bump_patch(v: str) -> str:
    v = v.lstrip("v")
    m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", v)
    if not m:
        raise ValueError(f"Unsupported version format: {v!r} (expected X.Y.Z)")
    major, minor, patch = map(int, m.groups())
    return f"{major}.{minor}.{patch + 1}"


def main() -> None:
    cur = Path.cwd()
    pyproject_file = cur / "pyproject.toml"
    data = parse(pyproject_file.read_text(encoding="utf-8"))

    version = str(data["project"]["version"]).strip()
    version_changed = 0

    repo = git.Repo(cur)
    tags = {str(t) for t in repo.tags}

    # consider both "vX.Y.Z" and "X.Y.Z"
    if f"v{version}" in tags or version in tags:
        version = bump_patch(version)
        data["project"]["version"] = version
        pyproject_file.write_text(dumps(data), encoding="utf-8")
        version_changed = 1

    # GitHub Actions outputs
    print(f"versiontag=v{version}")
    print(f"version_changed={version_changed}")


if __name__ == "__main__":
    main()

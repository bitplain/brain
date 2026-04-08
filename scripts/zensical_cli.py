#!/usr/bin/env python3

from __future__ import annotations

import platform
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen


VERSION = "0.0.32"
ASSETS = {
    ("linux", "x86_64"): "zensical-0.0.32-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    ("linux", "aarch64"): "zensical-0.0.32-cp310-abi3-manylinux_2_17_aarch64.manylinux2014_aarch64.whl",
    ("darwin", "x86_64"): "zensical-0.0.32-cp310-abi3-macosx_10_12_x86_64.whl",
    ("darwin", "arm64"): "zensical-0.0.32-cp310-abi3-macosx_11_0_arm64.whl",
    ("windows", "x86_64"): "zensical-0.0.32-cp310-abi3-win_amd64.whl",
}

REPO_ROOT = Path(__file__).resolve().parent.parent
CACHE_ROOT = REPO_ROOT / ".tools" / "zensical" / VERSION


def normalize_platform() -> tuple[str, str]:
    if sys.platform.startswith("linux"):
        system = "linux"
    elif sys.platform == "darwin":
        system = "darwin"
    elif sys.platform in {"win32", "cygwin"}:
        system = "windows"
    else:
        raise SystemExit(f"Unsupported platform: {sys.platform}")

    machine = platform.machine().lower()
    aliases = {
        "amd64": "x86_64",
        "x86-64": "x86_64",
        "arm64": "aarch64" if system == "linux" else "arm64",
    }
    machine = aliases.get(machine, machine)

    key = (system, machine)
    if key not in ASSETS:
        supported = ", ".join(f"{name}/{arch}" for name, arch in sorted(ASSETS))
        raise SystemExit(
            f"Unsupported platform or architecture: {system}/{machine}. Supported targets: {supported}"
        )

    return key


def download_file(url: str, destination: Path) -> None:
    request = Request(url, headers={"User-Agent": "brain-zensical-bootstrap/1.0"})
    with urlopen(request) as response, destination.open("wb") as output:
        shutil.copyfileobj(response, output)


def ensure_zensical() -> Path:
    platform_key = normalize_platform()
    asset_name = ASSETS[platform_key]
    wheel_path = CACHE_ROOT / asset_name
    extract_dir = CACHE_ROOT / "extracted"
    marker = extract_dir / "zensical" / "__main__.py"

    if marker.exists():
        return extract_dir

    CACHE_ROOT.mkdir(parents=True, exist_ok=True)

    if not wheel_path.exists():
        url = f"https://github.com/zensical/zensical/releases/download/v{VERSION}/{asset_name}"
        print(f"Downloading Zensical {VERSION} for {platform_key[0]}/{platform_key[1]}...")
        temp_path = wheel_path.with_suffix(".download")
        download_file(url, temp_path)
        temp_path.replace(wheel_path)

    temp_extract_dir = CACHE_ROOT / "extracted.tmp"
    if temp_extract_dir.exists():
        shutil.rmtree(temp_extract_dir)
    temp_extract_dir.mkdir(parents=True, exist_ok=True)

    print("Extracting Zensical...")
    with zipfile.ZipFile(wheel_path) as archive:
        archive.extractall(temp_extract_dir)

    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    temp_extract_dir.replace(extract_dir)

    if not marker.exists():
        raise SystemExit("Zensical bootstrap completed, but the extracted package is incomplete.")

    return extract_dir


def run_zensical(arguments: list[str]) -> int:
    extract_dir = ensure_zensical()
    env = dict(**os_environ(), PYTHONPATH=compose_pythonpath(extract_dir))
    command = [sys.executable, "-m", "zensical", *arguments]
    return subprocess.call(command, cwd=REPO_ROOT, env=env)


def os_environ() -> dict[str, str]:
    import os

    return os.environ.copy()


def compose_pythonpath(extract_dir: Path) -> str:
    import os

    current = os.environ.get("PYTHONPATH")
    if current:
        return f"{extract_dir}{os.pathsep}{current}"
    return str(extract_dir)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/zensical_cli.py <bootstrap|zensical args...>", file=sys.stderr)
        return 1

    if sys.argv[1] == "bootstrap":
        extract_dir = ensure_zensical()
        print(f"Zensical {VERSION} is ready in {extract_dir}")
        return 0

    return run_zensical(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())

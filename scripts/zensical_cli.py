#!/usr/bin/env python3

from __future__ import annotations

import platform
import json
import os
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
DEPENDENCIES = [
    ("click", "8.1.8"),
    ("deepmerge", "2.0"),
    ("markdown", "3.7"),
    ("pygments", "2.20.0"),
    ("pymdown-extensions", "10.21.2"),
]


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


def next_stale_path(path: Path) -> Path:
    candidate = path.with_name(f"{path.name}.stale-root")
    index = 2
    while candidate.exists():
        candidate = path.with_name(f"{path.name}.stale-root-{index}")
        index += 1
    return candidate


def dependency_marker_path(extract_dir: Path) -> Path:
    return extract_dir / ".deps_installed"


def dependency_module_name(package_name: str) -> str:
    aliases = {
        "pymdown-extensions": "pymdownx",
    }
    if package_name in aliases:
        return aliases[package_name]
    return package_name.replace("-", "_")


def dependency_missing(extract_dir: Path) -> bool:
    for package_name, _ in DEPENDENCIES:
        module_name = dependency_module_name(package_name)
        if not (extract_dir / module_name).exists():
            return True
    # Zensical loads YAML config; wheels are platform-specific, not pure-any.
    if not (extract_dir / "yaml").exists():
        return True
    return not dependency_marker_path(extract_dir).exists()


def download_dependency_wheel(package_name: str, version: str, destination: Path) -> None:
    metadata_url = f"https://pypi.org/pypi/{package_name}/{version}/json"
    request = Request(metadata_url, headers={"User-Agent": "brain-zensical-bootstrap/1.0"})
    with urlopen(request) as response:
        metadata = json.load(response)

    candidates = [
        file_info["url"]
        for file_info in metadata["urls"]
        if file_info["packagetype"] == "bdist_wheel" and file_info["filename"].endswith("none-any.whl")
    ]
    if not candidates:
        raise SystemExit(f"Could not find a pure Python wheel for {package_name}=={version}.")

    download_file(candidates[0], destination)


def install_dependencies(extract_dir: Path) -> None:
    deps_cache = CACHE_ROOT / "deps"
    deps_cache.mkdir(parents=True, exist_ok=True)

    for package_name, version in DEPENDENCIES:
        wheel_path = deps_cache / f"{package_name}-{version}.whl"
        if not wheel_path.exists():
            print(f"Downloading dependency {package_name}=={version}...")
            temp_path = wheel_path.with_suffix(".download")
            download_dependency_wheel(package_name, version, temp_path)
            temp_path.replace(wheel_path)

        with zipfile.ZipFile(wheel_path) as archive:
            archive.extractall(extract_dir)

    if not (extract_dir / "yaml").exists():
        print("Installing PyYAML (required for zensical.toml)...")
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-q",
                "pyyaml",
                "--target",
                str(extract_dir),
            ],
            check=True,
        )

    dependency_marker_path(extract_dir).write_text("ok\n", encoding="utf-8")


def replace_directory(source: Path, destination: Path) -> None:
    if not destination.exists():
        source.replace(destination)
        return

    try:
        shutil.rmtree(destination)
    except PermissionError:
        stale_dir = next_stale_path(destination)
        destination.replace(stale_dir)

    source.replace(destination)


def prepare_runtime_paths() -> None:
    for path, recreate in ((REPO_ROOT / ".cache", True), (REPO_ROOT / "site", False)):
        if path.exists() and not os.access(path, os.W_OK | os.X_OK):
            path.replace(next_stale_path(path))
        if recreate and not path.exists():
            path.mkdir(parents=True, exist_ok=True)


def ensure_zensical() -> Path:
    platform_key = normalize_platform()
    asset_name = ASSETS[platform_key]
    wheel_path = CACHE_ROOT / asset_name
    extract_dir = CACHE_ROOT / "extracted"
    marker = extract_dir / "zensical" / "__main__.py"

    if marker.exists() and not dependency_missing(extract_dir):
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

    print("Installing Zensical dependencies...")
    install_dependencies(temp_extract_dir)

    replace_directory(temp_extract_dir, extract_dir)

    if not marker.exists():
        raise SystemExit("Zensical bootstrap completed, but the extracted package is incomplete.")

    return extract_dir


def run_zensical(arguments: list[str]) -> int:
    prepare_runtime_paths()
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

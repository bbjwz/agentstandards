from __future__ import annotations

import argparse
import shutil
import tempfile
import zipfile
from pathlib import Path

VERSION = "0.1.0"


def _zip_tree(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source).as_posix())


def build(root: Path, output: Path) -> list[Path]:
    output.mkdir(parents=True, exist_ok=True)
    artifacts: list[Path] = []
    with tempfile.TemporaryDirectory(prefix="agentstandards-release-") as temp_name:
        temp = Path(temp_name)
        extension = temp / "extension"
        extension.mkdir()
        for name in ["extension.yml", "config-template.yml", "LICENSE", "README.md"]:
            shutil.copy2(root / name, extension / name)
        for name in ["commands", "runtime"]:
            shutil.copytree(
                root / name,
                extension / name,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
        (extension / "scripts").mkdir(parents=True)
        for runtime in ["bash", "powershell", "python"]:
            shutil.copytree(root / "scripts" / runtime, extension / "scripts" / runtime)
        extension_zip = output / f"agentstandards-{VERSION}.zip"
        _zip_tree(extension, extension_zip)
        artifacts.append(extension_zip)

        preset = temp / "preset"
        shutil.copytree(root / "presets" / "agentstandards-gate", preset)
        shutil.copy2(root / "LICENSE", preset / "LICENSE")
        preset_zip = output / f"agentstandards-gate-{VERSION}.zip"
        _zip_tree(preset, preset_zip)
        artifacts.append(preset_zip)

        bundle = temp / "bundle"
        shutil.copytree(root / "bundles" / "agentstandards", bundle)
        shutil.copy2(root / "LICENSE", bundle / "LICENSE")
        bundle_zip = output / f"agentstandards-bundle-{VERSION}.zip"
        _zip_tree(bundle, bundle_zip)
        artifacts.append(bundle_zip)
    return artifacts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("dist"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    for artifact in build(root, args.output.resolve()):
        print(artifact)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

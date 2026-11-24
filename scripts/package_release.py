#!/usr/bin/env python3
"""Build an offline, reproducible single-skill ZIP and its checksum."""
import argparse
import hashlib
from pathlib import Path
import re
import zipfile

FILES = ("SKILL.md", "LICENSE", "README.md", "SECURITY.md", "CHANGELOG.md", "CONTRIBUTING.md")
DIRECTORIES = ("agents", "assets", "references", "scripts", "tests", "examples")


def build(version, destination):
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        raise ValueError("version must have the form 1.0.1")
    root = Path(__file__).resolve().parents[1]
    selected = [root / name for name in FILES]
    for name in DIRECTORIES:
        selected.extend(p for p in (root / name).rglob("*") if p.is_file()
                        and "__pycache__" not in p.parts and p.suffix != ".pyc")
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    archive = destination / f"migrant-pl-{version}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as bundle:
        for path in sorted(selected, key=lambda p: p.relative_to(root).as_posix()):
            if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                raise ValueError("package files must stay inside the skill directory")
            name = "migrant-pl/" + path.relative_to(root).as_posix()
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            data = path.read_bytes()
            if path.suffix in (".md", ".py", ".yaml", ".yml"):
                data = data.replace(b"\r\n", b"\n")
            bundle.writestr(entry, data)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (destination / "SHA256SUMS.txt").write_text(f"{digest}  {archive.name}\n", encoding="utf-8", newline="\n")
    return archive, digest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", required=True, type=Path)
    options = parser.parse_args()
    archive, digest = build(options.version, options.output)
    print(f"{archive.name}: sha256:{digest}")

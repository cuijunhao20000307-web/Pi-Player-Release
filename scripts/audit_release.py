#!/usr/bin/env python3
"""Inspect publicly distributed Pi Player install bundles before release.

This tool does not remove GPL/source archives or rewrite existing release assets.
"""
import io
from pathlib import Path, PurePosixPath
import sys
import tarfile
import zipfile

BASE = Path(__file__).resolve().parent.parent
PACKAGE_DIR = BASE / "packages"
REQUIRED_SOURCES = {
    "licenses/pi-player/source.tar.gz",
    "licenses/sys-tune/source.tar.gz",
    "licenses/libtesla/source.tar.gz",
}
SOURCE_EXTS = (".c", ".cc", ".cpp", ".h", ".hpp", ".rs", ".go", ".java", ".py", ".ts", ".tsx", ".js")
SENSITIVE = {
    ".env", ".env.local", ".env.production", "id_rsa", "id_ed25519",
    "credentials.json", "service-account.json", "secrets.json",
    ".npmrc", ".pypirc", ".netrc", "known_hosts",
}
SENSITIVE_SUFFIXES = (".pem", ".p12", ".pfx", ".key", ".keystore")
MAX_ARCHIVE_ITEMS = 30000

def unsafe_path(name):
    normalized = name.replace("\\", "/")
    path = PurePosixPath(normalized)
    return path.is_absolute() or ".." in path.parts or "\x00" in name

def sensitive_path(name):
    parts = PurePosixPath(name.replace("\\", "/")).parts
    low = [p.lower() for p in parts]
    return (".git" in low or ".ssh" in low or ".aws" in low or
            any(p in SENSITIVE or p.startswith(".env.") for p in low) or
            any(p.endswith(SENSITIVE_SUFFIXES) for p in low))

def audit_names(names, label, allow_license_sources=False):
    errors = []
    for name in names:
        if unsafe_path(name):
            errors.append(f"{label}: unsafe archive path: {name}")
        if sensitive_path(name):
            errors.append(f"{label}: sensitive-looking path: {name}")
        normalized = name.replace("\\", "/").lower()
        if not allow_license_sources and normalized.endswith(SOURCE_EXTS) and not normalized.startswith("licenses/"):
            errors.append(f"{label}: unexpected loose source file: {name}")
    return errors

def run():
    packages = sorted(PACKAGE_DIR.glob("*.zip"))
    if not packages:
        raise RuntimeError("No ZIP package found in packages/")
    errors = []
    for package in packages:
        with zipfile.ZipFile(package) as z:
            bad = z.testzip()
            if bad:
                errors.append(f"{package.name}: unreadable ZIP member: {bad}")
            names = z.namelist()
            if len(names) > MAX_ARCHIVE_ITEMS:
                errors.append(f"{package.name}: unexpectedly large number of entries")
            errors += audit_names(names, package.name)
            missing = REQUIRED_SOURCES.difference(names)
            if missing:
                errors.append(f"{package.name}: missing required published-source archive(s): {sorted(missing)}")
            for path in REQUIRED_SOURCES.intersection(names):
                try:
                    payload = z.read(path)
                    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as tar:
                        members = tar.getmembers()
                        if not members or len(members) > MAX_ARCHIVE_ITEMS:
                            errors.append(f"{path}: empty or excessive tar members")
                        errors += audit_names((m.name for m in members), path, allow_license_sources=True)
                        if any(m.issym() or m.islnk() for m in members):
                            errors.append(f"{path}: links found in bundled source archive; review manually")
                except (tarfile.TarError, OSError, EOFError) as exc:
                    errors.append(f"{path}: invalid source archive ({type(exc).__name__})")
            print(f"Audited {package.name}: {len(names)} ZIP items, {len(REQUIRED_SOURCES.intersection(names))} published source archives")
    if errors:
        for err in errors[:30]:
            print("FAIL:", err, file=sys.stderr)
        raise SystemExit(f"Release audit failed: {len(errors)} issue(s)")
    print("PASS: no unexpected loose source files or common secret-file paths detected")
    print("NOTE: bundled pi-player/sys-tune/libtesla source archives remain public; license review is still required.")

if __name__ == "__main__":
    run()

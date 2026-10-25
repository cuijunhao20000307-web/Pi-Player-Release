#!/usr/bin/env python3
"""Publish already-verified installation files from this release-only repository."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import urllib.error
import urllib.parse
import urllib.request
import zipfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def check_nacp(data, title, version):
    if data[16:20] != b"NRO0":
        raise RuntimeError("Invalid NRO/OVL header")
    offset = struct.unpack_from("<I", data, 0x18)[0]
    if data[offset:offset + 4] != b"ASET":
        raise RuntimeError("Missing NRO assets header")
    start, size = struct.unpack_from("<QQ", data, offset + 24)
    nacp = data[offset + start:offset + start + size]
    name = nacp[:512].split(b"\0", 1)[0].decode()
    actual_version = nacp[0x3060:0x3070].split(b"\0", 1)[0].decode()
    if (name, actual_version) != (title, version):
        raise RuntimeError(f"Metadata mismatch: {name} {actual_version}")


def asset_name(url):
    name = urllib.parse.urlparse(url).path.rsplit("/", 1)[-1]
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
        raise RuntimeError("Invalid release asset filename")
    return name


def verify():
    version = json.loads(Path("version.json").read_text())
    history = json.loads(Path("versions.json").read_text())
    if not history or history[0] != version or version["channel"] != "stable":
        raise RuntimeError("Version index does not match current stable release")
    if not re.fullmatch(r"\d+\.\d+\.\d+", version["version"]):
        raise RuntimeError("Invalid stable version")
    package_name = asset_name(version["download_url"])
    package = Path("packages") / package_name
    payload = package.read_bytes()
    if digest(payload) != version["sha256"] or len(payload) != version["size"]:
        raise RuntimeError("Installation package checksum or size mismatch")
    with zipfile.ZipFile(package) as archive:
        if archive.testzip() is not None:
            raise RuntimeError("Installation ZIP is damaged")
        for name in ("licenses/pi-player/source.tar.gz", "licenses/sys-tune/source.tar.gz",
                     "licenses/libtesla/source.tar.gz", "atmosphere/contents/4200000000000000/exefs.nsp"):
            if not archive.read(name):
                raise RuntimeError(f"Missing installation file: {name}")
        nro = archive.read("switch/piplayer/piplayer.nro")
        overlay = archive.read("switch/.overlays/piplayer-overlay.ovl")
        check_nacp(nro, "Pi Player", version["version"])
        check_nacp(overlay, "Piplayer", version["version"])
    preview = Path("assets/startup.gif").read_bytes()
    if preview[:6] not in (b"GIF87a", b"GIF89a"):
        raise RuntimeError("Invalid startup GIF")
    files = {
        package_name: (payload, "application/zip"),
        asset_name(version["nro_url"]): (nro, "application/octet-stream"),
        asset_name(version["preview_url"]): (preview, "image/gif"),
    }
    checksums = "".join(f"{digest(files[name][0])}  {name}\n" for name in sorted(files))
    if Path("SHA256SUMS.txt").read_text() != checksums:
        raise RuntimeError("Published checksum file does not match release assets")
    files["SHA256SUMS.txt"] = (checksums.encode(), "text/plain")
    print(f"Verified {version['version']}: ZIP, NRO/OVL metadata, licenses, GIF and all checksums")
    return version, files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    version, files = verify()
    if args.verify_only:
        return
    repository = os.environ["GITHUB_REPOSITORY"]
    commit = os.environ["GITHUB_SHA"]
    token = os.environ["GH_TOKEN"]
    api = f"https://api.github.com/repos/{repository}"

    def request(method, url, data=None, content_type="application/json", allow_missing=False):
        if isinstance(data, dict):
            data = json.dumps(data).encode()
        req = urllib.request.Request(url, data=data, method=method, headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": content_type,
            "X-GitHub-Api-Version": "2022-11-28",
        })
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if allow_missing and error.code == 404:
                return None
            raise RuntimeError(f"GitHub {method} failed with HTTP {error.code}") from None

    tag = version["version"]
    body = Path(f"RELEASE_{tag}.md").read_text()
    release = request("GET", f"{api}/releases/tags/{tag}", allow_missing=True)
    if release is None:
        release = request("POST", f"{api}/releases", {
            "tag_name": tag, "target_commitish": commit,
            "name": f"Pi Player {tag} 正式版", "draft": True,
            "prerelease": False, "body": body,
        })
    for name, (payload, content_type) in files.items():
        expected = "sha256:" + digest(payload)
        existing = next((a for a in release["assets"] if a["name"] == name), None)
        if existing:
            if existing.get("digest") != expected or existing["size"] != len(payload):
                raise RuntimeError(f"Existing asset differs; refusing to replace {name}")
            continue
        url = f"https://uploads.github.com/repos/{repository}/releases/{release['id']}/assets?name={urllib.parse.quote(name)}"
        uploaded = request("POST", url, payload, content_type)
        if uploaded["size"] != len(payload) or uploaded.get("digest") != expected:
            raise RuntimeError(f"Upload verification failed: {name}")
        print(f"Uploaded and verified: {name}")
    published = request("PATCH", f"{api}/releases/{release['id']}", {
        "draft": False, "prerelease": False, "make_latest": "true", "body": body,
    })
    print("Published stable release: " + published["html_url"])


if __name__ == "__main__":
    main()

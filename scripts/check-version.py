#!/usr/bin/env python3
"""Detect the latest Proton Authenticator version from the download page.

Outputs just the version string (e.g. 1.1.4-1) to stdout, or exits with
code 1 if detection fails.
"""

import re
import sys
import urllib.request

DOWNLOAD_PAGE = "https://proton.me/download/authenticator"
BASE_URL = "https://proton.me/download/authenticator/linux"
VERSION_RE = re.compile(r'ProtonAuthenticator-([\d]+\.[\d]+\.[\d]+-[\d]+)\.x86_64\.rpm')


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def get_latest_version() -> tuple[str, str] | tuple[None, None]:
    try:
        html = fetch(DOWNLOAD_PAGE)
        matches = VERSION_RE.findall(html)
        if matches:
            version = matches[0]
            url = f"{BASE_URL}/ProtonAuthenticator-{version}.x86_64.rpm"
            return version, url
    except Exception as e:
        print(f"Error fetching download page: {e}", file=sys.stderr)

    return None, None


def main() -> None:
    version, url = get_latest_version()
    if not version:
        print("Could not detect latest version from Proton download page.", file=sys.stderr)
        print(f"Manually check: {DOWNLOAD_PAGE}", file=sys.stderr)
        sys.exit(1)

    print(f"VERSION={version}")
    print(f"URL={url}")


if __name__ == "__main__":
    main()

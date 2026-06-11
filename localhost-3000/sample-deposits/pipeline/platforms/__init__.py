"""Platform-specific scaffolding for new journals.

A "platform" is a hosting convention (WAC Clearinghouse, OJS, etc.). Each
platform knows how to:
  - recognize URLs that belong to it
  - generate a per-journal downloader.py + journal.py + depositor.json

Adding a new platform = adding a new module here and registering it in
the `PLATFORMS` list.
"""
from __future__ import annotations

from . import wac, ojs, bepress, janeway, unknown


# Order matters: detection.detect() walks this list and the first hit wins.
# Put the most specific (most-distinctive-signal) platforms first;
# `unknown` is the fallback. Bepress comes before WAC/OJS because the
# `bepress_citation_*` meta tag signature is uniquely strong.
PLATFORMS = [bepress.PLATFORM, wac.PLATFORM, ojs.PLATFORM, janeway.PLATFORM, unknown.PLATFORM]

PLATFORM_BY_KEY = {p.key: p for p in PLATFORMS}
if len(PLATFORM_BY_KEY) != len(PLATFORMS):
    duplicate_keys = [p.key for p in PLATFORMS if sum(1 for q in PLATFORMS if q.key == p.key) > 1]
    raise ValueError(f"Duplicate platform keys in PLATFORMS: {sorted(set(duplicate_keys))}")


def by_key(key: str):
    """Look up a Platform by its key. Returns the unknown platform on miss."""
    return PLATFORM_BY_KEY.get(key, unknown.PLATFORM)

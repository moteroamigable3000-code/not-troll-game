"""Regenerate NotTrollGDX/assets/levels.json from backend/levels.py.

backend/levels.py is the single source of truth for level data (used by the
web/backend build). The Android/desktop (libGDX) build reads a static JSON
copy with the same schema but Y-coordinates shifted by GROUND_LIFT. Run this
script after editing backend/levels.py so both builds stay in sync:

    python scripts/gen_android_levels.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "backend"))

from levels import level_count, level_meta, shifted_level  # noqa: E402

OUTPUT_PATH = REPO_ROOT / "NotTrollGDX" / "assets" / "levels.json"


def main() -> None:
    data = {
        "levels": [shifted_level(i) for i in range(level_count())],
        "meta": level_meta(),
    }
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"Wrote {level_count()} levels to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

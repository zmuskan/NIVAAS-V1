from __future__ import annotations

import logging
import sys

from elt.common.config import Settings
from elt.sources.osm.pipeline import run_osm_pipeline


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
    )

    try:
        settings = Settings.from_env()
        result = run_osm_pipeline(settings)

        print()
        print("NIVAAS OSM INGESTION")
        print("--------------------")
        print(f"Fetched:    {result.fetched}")
        print(f"Normalized: {result.normalized}")
        print(f"Skipped:    {result.skipped}")
        print(f"Persisted:  {result.persisted}")

        return 0

    except Exception:
        logging.exception("OSM ingestion failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

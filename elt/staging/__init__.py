"""
Entry point for the NIVAAS staging pipeline.
"""

from __future__ import annotations

import sys

from elt.staging.pipeline import StagingPipeline


def main() -> int:

    pipeline = StagingPipeline()

    try:
        stats = pipeline.run()
    except Exception as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 1

    stats.print_summary()

    return 0


if __name__ == "__main__":
    sys.exit(main())

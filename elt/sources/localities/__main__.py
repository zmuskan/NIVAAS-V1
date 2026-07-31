from __future__ import annotations

import logging

from elt.common.config import Settings
from elt.sources.localities.pipeline import run_locality_pipeline


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def main() -> None:
    settings = Settings.from_env()

    result = run_locality_pipeline(settings)

    print()
    print("NIVAAS LOCALITY INGESTION")
    print("-------------------------")
    print(f"Requested:          {result.requested}")
    print(f"Resolved:           {result.resolved}")
    print(f"Unresolved:         {len(result.unresolved)}")
    print(f"Rejected by QA:     {len(result.rejected)}")
    print(f"Amenities assigned: {result.amenities_assigned}")

    if result.unresolved:
        print()
        print("Unresolved localities:")

        for name in result.unresolved:
            print(f"  - {name}")

    if result.rejected:
        print()
        print("Rejected by geometry QA:")

        for name in result.rejected:
            print(f"  - {name}")


if __name__ == "__main__":
    main()

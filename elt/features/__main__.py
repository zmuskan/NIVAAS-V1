from __future__ import annotations

import logging

from elt.common.config import Settings
from elt.features.locality import run_locality_feature_pipeline


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
    )

    settings = Settings.from_env()

    result = run_locality_feature_pipeline(settings)

    print()
    print("NIVAAS LOCALITY FEATURE ENGINEERING")
    print("-----------------------------------")
    print(
        f"Localities processed: {result.localities_processed}"
    )
    print(
        f"Features written:     {result.features_written}"
    )


if __name__ == "__main__":
    main()

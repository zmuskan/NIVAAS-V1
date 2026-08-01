from elt.features.locality import (
    AMENITY_TYPES,
    CALCULATION_VERSION,
    FeaturePipelineResult,
)


def test_expected_amenity_types() -> None:
    assert set(AMENITY_TYPES) == {
        "restaurant",
        "hospital",
        "school",
        "supermarket",
        "park",
        "gym",
        "bus_stop",
        "metro_station",
    }


def test_amenity_types_are_unique() -> None:
    assert len(AMENITY_TYPES) == len(set(AMENITY_TYPES))


def test_calculation_version_exists() -> None:
    assert CALCULATION_VERSION


def test_pipeline_result() -> None:
    result = FeaturePipelineResult(
        localities_processed=9,
        features_written=171,
    )

    assert result.localities_processed == 9
    assert result.features_written == 171

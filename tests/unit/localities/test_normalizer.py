from elt.sources.localities.normalizer import (
    normalize_candidate,
    select_boundary,
)
from elt.sources.localities.registry import TargetLocality


TARGET = TargetLocality("HSR Layout")


def valid_candidate() -> dict:
    return {
        "osm_type": "relation",
        "osm_id": 12345,
        "lat": "12.9116",
        "lon": "77.6389",
        "geojson": {
            "type": "Polygon",
            "coordinates": [
                [
                    [77.63, 12.90],
                    [77.65, 12.90],
                    [77.65, 12.92],
                    [77.63, 12.90],
                ]
            ],
        },
    }


def test_normalizes_polygon_candidate() -> None:
    result = normalize_candidate(TARGET, valid_candidate())

    assert result is not None
    assert result.name == "HSR Layout"
    assert result.city == "Bengaluru"
    assert result.state == "Karnataka"
    assert result.source == "OpenStreetMap"
    assert result.source_type == "relation"
    assert result.source_id == 12345
    assert result.boundary_quality == "osm_boundary"


def test_accepts_multipolygon() -> None:
    candidate = valid_candidate()
    candidate["geojson"]["type"] = "MultiPolygon"

    assert normalize_candidate(TARGET, candidate) is not None


def test_rejects_node() -> None:
    candidate = valid_candidate()
    candidate["osm_type"] = "node"

    assert normalize_candidate(TARGET, candidate) is None


def test_rejects_point_geometry() -> None:
    candidate = valid_candidate()
    candidate["geojson"] = {
        "type": "Point",
        "coordinates": [77.6389, 12.9116],
    }

    assert normalize_candidate(TARGET, candidate) is None


def test_rejects_location_outside_bengaluru() -> None:
    candidate = valid_candidate()
    candidate["lat"] = "28.6139"
    candidate["lon"] = "77.2090"

    assert normalize_candidate(TARGET, candidate) is None


def test_rejects_missing_osm_id() -> None:
    candidate = valid_candidate()
    del candidate["osm_id"]

    assert normalize_candidate(TARGET, candidate) is None


def test_select_boundary_skips_invalid_candidates() -> None:
    invalid = valid_candidate()
    invalid["osm_type"] = "node"

    result = select_boundary(
        TARGET,
        [invalid, valid_candidate()],
    )

    assert result is not None
    assert result.source_id == 12345


def test_select_boundary_returns_none_when_unresolved() -> None:
    invalid = valid_candidate()
    invalid["geojson"] = None

    assert select_boundary(TARGET, [invalid]) is None

from elt.sources.osm.normalizer import normalize_element


def test_normalizes_node() -> None:
    element = {
        "type": "node",
        "id": 123,
        "lat": 12.9716,
        "lon": 77.5946,
        "tags": {
            "amenity": "hospital",
            "name": "Example Hospital",
        },
    }

    result = normalize_element(element)

    assert result is not None
    assert result.osm_type == "node"
    assert result.osm_id == 123
    assert result.name == "Example Hospital"
    assert result.amenity_type == "hospital"
    assert result.latitude == 12.9716
    assert result.longitude == 77.5946


def test_normalizes_way_using_center() -> None:
    element = {
        "type": "way",
        "id": 456,
        "center": {
            "lat": 12.95,
            "lon": 77.60,
        },
        "tags": {
            "leisure": "park",
            "name": "Example Park",
        },
    }

    result = normalize_element(element)

    assert result is not None
    assert result.osm_type == "way"
    assert result.latitude == 12.95
    assert result.longitude == 77.60


def test_normalizes_relation_using_center() -> None:
    element = {
        "type": "relation",
        "id": 789,
        "center": {
            "lat": 12.98,
            "lon": 77.61,
        },
        "tags": {
            "shop": "supermarket",
            "name": "Example Market",
        },
    }

    result = normalize_element(element)

    assert result is not None
    assert result.osm_type == "relation"
    assert result.amenity_type == "supermarket"


def test_rejects_invalid_latitude() -> None:
    element = {
        "type": "node",
        "id": 123,
        "lat": 120,
        "lon": 77,
        "tags": {
            "amenity": "school",
            "name": "Bad Coordinates School",
        },
    }

    assert normalize_element(element) is None


def test_rejects_invalid_longitude() -> None:
    element = {
        "type": "node",
        "id": 123,
        "lat": 12,
        "lon": 200,
        "tags": {
            "amenity": "school",
        },
    }

    assert normalize_element(element) is None


def test_rejects_unknown_category() -> None:
    element = {
        "type": "node",
        "id": 123,
        "lat": 12,
        "lon": 77,
        "tags": {
            "amenity": "bank",
        },
    }

    assert normalize_element(element) is None


def test_uses_deterministic_name_for_unnamed_element() -> None:
    element = {
        "type": "node",
        "id": 999,
        "lat": 12.9,
        "lon": 77.5,
        "tags": {
            "amenity": "hospital",
        },
    }

    result = normalize_element(element)

    assert result is not None
    assert result.name == "Unnamed hospital"


def test_builds_address() -> None:
    element = {
        "type": "node",
        "id": 321,
        "lat": 12.9,
        "lon": 77.5,
        "tags": {
            "amenity": "restaurant",
            "name": "Example Restaurant",
            "addr:housenumber": "42",
            "addr:street": "MG Road",
            "addr:suburb": "Central Bengaluru",
            "addr:city": "Bengaluru",
            "addr:postcode": "560001",
        },
    }

    result = normalize_element(element)

    assert result is not None
    assert result.address == (
        "42 MG Road, Central Bengaluru, Bengaluru, 560001"
    )


def test_rejects_missing_osm_id() -> None:
    element = {
        "type": "node",
        "lat": 12.9,
        "lon": 77.5,
        "tags": {
            "amenity": "hospital",
        },
    }

    assert normalize_element(element) is None

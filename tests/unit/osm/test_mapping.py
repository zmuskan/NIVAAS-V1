from elt.sources.osm.mapping import map_osm_category


def test_maps_hospital() -> None:
    assert map_osm_category({"amenity": "hospital"}) == "hospital"


def test_maps_clinic_to_hospital() -> None:
    assert map_osm_category({"amenity": "clinic"}) == "hospital"


def test_maps_school() -> None:
    assert map_osm_category({"amenity": "school"}) == "school"


def test_maps_restaurant() -> None:
    assert map_osm_category({"amenity": "restaurant"}) == "restaurant"


def test_maps_supermarket() -> None:
    assert map_osm_category({"shop": "supermarket"}) == "supermarket"


def test_maps_park() -> None:
    assert map_osm_category({"leisure": "park"}) == "park"


def test_maps_gym() -> None:
    assert (
        map_osm_category({"leisure": "fitness_centre"})
        == "gym"
    )


def test_maps_bus_stop() -> None:
    assert map_osm_category({"highway": "bus_stop"}) == "bus_stop"


def test_maps_metro_station() -> None:
    assert (
        map_osm_category(
            {
                "railway": "station",
                "station": "subway",
            }
        )
        == "metro_station"
    )


def test_rejects_unknown_category() -> None:
    assert map_osm_category({"amenity": "bank"}) is None

from elt.sources.localities.registry import TARGET_LOCALITIES


def test_registry_is_not_empty() -> None:
    assert TARGET_LOCALITIES


def test_registry_contains_core_localities() -> None:
    names = {target.name for target in TARGET_LOCALITIES}

    assert "HSR Layout" in names
    assert "Koramangala" in names
    assert "Indiranagar" in names
    assert "Whitefield" in names


def test_target_names_are_unique() -> None:
    names = [target.name for target in TARGET_LOCALITIES]

    assert len(names) == len(set(names))


def test_all_targets_are_bengaluru_karnataka() -> None:
    for target in TARGET_LOCALITIES:
        assert target.city == "Bengaluru"
        assert target.state == "Karnataka"


def test_registry_has_thirteen_localities() -> None:
    localities = [
        target
        for target in TARGET_LOCALITIES
        if target.area_type == "locality"
    ]

    assert len(localities) == 13


def test_registry_has_two_corridors() -> None:
    corridors = [
        target
        for target in TARGET_LOCALITIES
        if target.area_type == "corridor"
    ]

    assert len(corridors) == 2

    names = {target.name for target in corridors}

    assert names == {
        "Sarjapur Road",
        "Bannerghatta Road",
    }


def test_search_names_start_with_canonical_name() -> None:
    for target in TARGET_LOCALITIES:
        assert target.search_names[0] == target.name


def test_search_names_are_unique_per_target() -> None:
    for target in TARGET_LOCALITIES:
        assert len(target.search_names) == len(
            set(target.search_names)
        )


def test_locality_minimum_areas_are_positive() -> None:
    for target in TARGET_LOCALITIES:
        if target.area_type == "locality":
            assert target.min_area_km2 > 0


def test_known_aliases_are_registered() -> None:
    targets = {
        target.name: target
        for target in TARGET_LOCALITIES
    }

    assert "Jayanagara" in targets["Jayanagar"].search_aliases
    assert "Electronics City" in targets["Electronic City"].search_aliases
    assert "Sadashiva Nagar" in targets["Sadashivanagar"].search_aliases

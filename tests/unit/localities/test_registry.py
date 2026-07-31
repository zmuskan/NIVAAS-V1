from elt.sources.localities.registry import TARGET_LOCALITIES


def test_registry_is_not_empty() -> None:
    assert TARGET_LOCALITIES


def test_registry_contains_core_localities() -> None:
    names = {locality.name for locality in TARGET_LOCALITIES}

    assert "HSR Layout" in names
    assert "Koramangala" in names
    assert "Indiranagar" in names
    assert "Whitefield" in names


def test_locality_names_are_unique() -> None:
    names = [locality.name for locality in TARGET_LOCALITIES]

    assert len(names) == len(set(names))


def test_all_localities_are_bengaluru_karnataka() -> None:
    for locality in TARGET_LOCALITIES:
        assert locality.city == "Bengaluru"
        assert locality.state == "Karnataka"

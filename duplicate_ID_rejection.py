import pytest
from lost_item import LostItem
from lost_found_system import LostFoundSystem

def test_duplicate_id_preserves_original_item():
    system = LostFoundSystem()
    original = LostItem(101, "Laptop", "Electronics", "Library")
    duplicate = LostItem(101, "Backpack", "Personal", "Cafeteria")

    assert system.add_item(original) is True
    assert system.add_item(duplicate) is False
    assert system.get_item_count() == 1

    stored = system.search_item(101)
    assert stored.get_name() == "Laptop"
    assert stored.get_location() == "Library"

    #What it verifies: Confirms that LostItem.__eq__ identifies equality solely by ID and that add_item() returns False on a duplicate ID while leaving the first item intact.
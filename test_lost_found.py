"""
Pytest test suite for LostItem and LostFoundSystem.
Covers Part B Mission 1 (independent + AI-assisted tests) and Mission 2 verification.
"""

import pytest
from lost_item import LostItem
from lost_found_system import LostFoundSystem


# =========================================================
# PART B - MISSION 1A: FOUR INDEPENDENT TESTS (Normal Ops)
# =========================================================

def test_register_item():
    # Setup
    system = LostFoundSystem()
    item = LostItem(101, "Laptop", "Electronics", "Library")

    # Invoke
    added = system.add_item(item)

    # Analyze
    assert added is True
    assert system.get_item_count() == 1
    assert str(item) == "101 | Laptop | Electronics | Library | Lost"


def test_search_existing_item():
    # Setup
    system = LostFoundSystem()
    item1 = LostItem(101, "Laptop", "Electronics", "Library")
    item2 = LostItem(102, "Water Bottle", "Personal", "Cafeteria")
    system.add_item(item1)
    system.add_item(item2)

    # Invoke
    found = system.search_item(102)
    missing = system.search_item(999)

    # Analyze
    assert found is not None
    assert found.get_name() == "Water Bottle"
    assert missing is None


def test_mark_item_claimed():
    # Setup
    system = LostFoundSystem()
    item = LostItem(101, "Laptop", "Electronics", "Library")
    system.add_item(item)

    # Invoke
    changed = system.claim_item(101)

    # Analyze
    assert changed is True
    assert item.get_status() == "Claimed"


def test_save_and_load_valid_records():
    # Setup
    system = LostFoundSystem()
    system.add_item(LostItem(101, "Laptop", "Electronics", "Library"))
    item2 = LostItem(102, "Water Bottle", "Personal", "Cafeteria")
    item2.mark_claimed()
    system.add_item(item2)
    filename = "test_valid_items.txt"

    # Invoke
    saved_count = system.save_items(filename)
    new_system = LostFoundSystem()
    loaded_count = new_system.load_items(filename)

    # Analyze
    assert saved_count == 2
    assert loaded_count == 2
    assert new_system.search_item(101).get_status() == "Lost"
    assert new_system.search_item(102).get_status() == "Claimed"


# =========================================================
# PART B - MISSION 1B: FIVE CHALLENGING EDGE-CASE TESTS
# =========================================================

def test_duplicate_item_id():
    # Setup
    system = LostFoundSystem()
    item1 = LostItem(101, "Laptop", "Electronics", "Library")
    item2 = LostItem(101, "Phone", "Electronics", "Gym")

    # Invoke
    first_add = system.add_item(item1)
    second_add = system.add_item(item2)

    # Analyze
    assert first_add is True
    assert second_add is False
    assert system.get_item_count() == 1
    assert system.search_item(101).get_name() == "Laptop"


def test_invalid_item_id_and_empty_fields():
    # Setup & Invoke & Analyze
    with pytest.raises(ValueError):
        LostItem(0, "Laptop", "Electronics", "Library")

    with pytest.raises(ValueError):
        LostItem(-5, "Laptop", "Electronics", "Library")

    with pytest.raises(ValueError):
        LostItem("101", "Laptop", "Electronics", "Library")

    with pytest.raises(ValueError):
        LostItem(101, "   ", "Electronics", "Library")

    with pytest.raises(ValueError):
        LostItem(101, "Laptop, Pro", "Electronics", "Library")


def test_claim_already_claimed():
    # Setup
    system = LostFoundSystem()
    item = LostItem(101, "Laptop", "Electronics", "Library")
    system.add_item(item)
    first_claim = system.claim_item(101)

    # Invoke
    second_claim = system.claim_item(101)

    # Analyze
    assert first_claim is True
    assert second_claim is False
    assert item.get_status() == "Claimed"


def test_missing_file_preserves_records():
    # Setup
    system = LostFoundSystem()
    system.add_item(LostItem(101, "Laptop", "Electronics", "Library"))

    # Invoke
    loaded_count = system.load_items("non_existent_file_xyz.txt")

    # Analyze
    assert loaded_count == 0
    assert system.get_item_count() == 1
    assert system.search_item(101) is not None


def test_load_corrupted_records_skipped():
    # Setup
    filename = "test_corrupted_items.txt"
    with open(filename, "w") as file:
        file.write("101,Laptop,Electronics,Library,Lost\n")
        file.write("bad_id,Book,Stationery,Hall,Lost\n")
        file.write("-4,Pen,Stationery,Hall,Lost\n")
        file.write("102,Incomplete,Record\n")
        file.write("103,Keys,Personal,Lab,UnknownStatus\n")
        file.write("101,Duplicate,Electronics,Lab,Lost\n")
        file.write("104,Jacket,Clothing,Auditorium,Claimed\n")

    system = LostFoundSystem()

    # Invoke
    loaded_count = system.load_items(filename)

    # Analyze
    assert loaded_count == 2
    assert system.get_item_count() == 2
    assert system.search_item(101).get_name() == "Laptop"
    assert system.search_item(104).get_status() == "Claimed"


# =========================================================
# PART B - MISSION 2: INTERROGATION ROOM VERIFICATION TESTS
# =========================================================

def test_items_equal_by_id():
    # Case 1: Two LostItem objects with the same ID but different names
    item_a = LostItem(101, "Laptop", "Electronics", "Library")
    item_b = LostItem(101, "Backpack", "Personal", "Cafeteria")
    assert item_a == item_b


def test_double_claim_returns_false():
    # Case 2: Claiming an already claimed item returns False
    item = LostItem(101, "Laptop", "Electronics", "Library")
    assert item.mark_claimed() is True
    assert item.mark_claimed() is False


def test_load_file_twice():
    # Case 3: Loading the same file twice replaces records rather than doubling
    filename = "test_reload_items.txt"
    system = LostFoundSystem()
    system.add_item(LostItem(101, "Laptop", "Electronics", "Library"))
    system.add_item(LostItem(102, "Calculator", "Electronics", "Room 204"))
    system.save_items(filename)

    first_load = system.load_items(filename)
    second_load = system.load_items(filename)

    assert first_load == 2
    assert second_load == 2
    assert system.get_item_count() == 2
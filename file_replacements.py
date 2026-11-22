import pytest
from lost_item import LostItem
from lost_found_system import LostFoundSystem

def test_file_reload_replacement_and_missing_file_recovery(tmp_path):
    records_file = tmp_path / "items.txt"
    records_file.write_text(
        "101,Laptop,Electronics,Library,Lost\n"
        "102,Calculator,Electronics,Room 204,Claimed\n"
    )

    system = LostFoundSystem()
    system.add_item(LostItem(999, "Old Item", "Other", "Storage"))

    # Valid load replaces existing in-memory records
    assert system.load_items(str(records_file)) == 2
    assert system.search_item(999) is None
    assert system.get_item_count() == 2

    # Repeated load of the same file does not duplicate items
    assert system.load_items(str(records_file)) == 2
    assert system.get_item_count() == 2

    # Missing file returns 0 and preserves current in-memory records
    missing_path = tmp_path / "does_not_exist.txt"
    assert system.load_items(str(missing_path)) == 0
    assert system.get_item_count() == 2
    assert system.search_item(101) is not None

    #What it verifies: Confirms that valid loads cleanly replace old records (preventing record doubling on repeated loads) while a FileNotFoundError returns 0 and leaves current records intact.
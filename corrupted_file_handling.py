import pytest
from lost_item import LostItem
from lost_found_system import LostFoundSystem

def test_load_corrupted_and_duplicate_records(tmp_path):
    bad_file = tmp_path / "corrupted.txt"
    bad_file.write_text(
        "101,Laptop,Electronics,Library,Lost\n"
        "\n"
        "abc,Book,Stationery,Hall,Lost\n"
        "-3,Pen,Stationery,Hall,Lost\n"
        "102,MissingFields,Electronics\n"
        "103,Keys,Personal,Lab,Pending\n"
        "101,DuplicateInFile,Electronics,Gym,Claimed\n"
        "104,Jacket,Clothing,Auditorium,Claimed\n"
    )

    system = LostFoundSystem()
    loaded_count = system.load_items(str(bad_file))

    assert loaded_count == 2
    assert system.get_item_count() == 2
    assert system.search_item(101).get_name() == "Laptop"
    assert system.search_item(101).get_status() == "Lost"
    assert system.search_item(104).get_status() == "Claimed"

    #What it verifies: Confirms that load_items() safely skips corrupted lines and intra-file duplicate IDs without crashing, loading only valid unique records.
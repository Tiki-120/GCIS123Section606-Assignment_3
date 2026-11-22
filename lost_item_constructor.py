import pytest
from lost_item import LostItem
from lost_found_system import LostFoundSystem


def test_lost_item_boundaries_and_invalid_inputs():
    # Boundary: 1 is the smallest valid positive integer ID
    valid_boundary = LostItem(1, "Key", "Personal", "Lobby")
    assert valid_boundary.get_id() == 1

    # Invalid IDs: zero, negative, string, and bool (since isinstance(True, int) is True in Python)
    with pytest.raises(ValueError):
        LostItem(0, "Key", "Personal", "Lobby")
    with pytest.raises(ValueError):
        LostItem(-10, "Key", "Personal", "Lobby")
    with pytest.raises(ValueError):
        LostItem("101", "Key", "Personal", "Lobby")
    with pytest.raises(ValueError):
        LostItem(True, "Key", "Personal", "Lobby")

    # Invalid text fields: empty, whitespace-only, or containing commas
    with pytest.raises(ValueError):
        LostItem(2, "   ", "Personal", "Lobby")
    with pytest.raises(ValueError):
        LostItem(2, "Key, Silver", "Personal", "Lobby")




    #What it verifies: Confirms that 1 is accepted as the lower ID boundary while 0, negative numbers, non-integers (including bool, which is a subclass of int in Python), whitespace-only strings, and comma-containing strings raise ValueError.
import pytest
from lost_item import LostItem
from lost_found_system import LostFoundSystem

def test_repeated_claim_actions_and_missing_id():
    system = LostFoundSystem()
    item = LostItem(105, "Headphones", "Electronics", "Gym")
    system.add_item(item)

    # First claim succeeds and changes status
    assert system.claim_item(105) is True
    assert item.get_status() == "Claimed"

    # Second claim on already-claimed item returns False without altering state
    assert system.claim_item(105) is False
    assert item.get_status() == "Claimed"

    # Claiming an ID that does not exist returns False
    assert system.claim_item(999) is False

    #What it verifies: Ensures claim_item() and mark_claimed() return True only when a state transition from "Lost" to "Claimed" actually occurs, returning False for repeated claims or unknown IDs.
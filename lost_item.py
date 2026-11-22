"""
Defines the LostItem class for the Campus Lost & Found application.
"""

STATUS_LOST = "Lost"
STATUS_CLAIMED = "Claimed"


class LostItem:
    """
    Represents a single lost or claimed item on campus.
    """
    __slots__ = ["__id", "__name", "__category", "__location", "__status"]

    def __init__(self, item_id, name, category, location):
        if type(item_id) != int or item_id <= 0:
            raise ValueError("Item ID must be a positive integer.")
        if type(name) != str or name.strip() == "" or "," in name:
            raise ValueError("Item name must be non-empty and contain no commas.")
        if type(category) != str or category.strip() == "" or "," in category:
            raise ValueError("Category must be non-empty and contain no commas.")
        if type(location) != str or location.strip() == "" or "," in location:
            raise ValueError("Location must be non-empty and contain no commas.")

        self.__id = item_id
        self.__name = name.strip()
        self.__category = category.strip()
        self.__location = location.strip()
        self.__status = STATUS_LOST

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_category(self):
        return self.__category

    def get_location(self):
        return self.__location

    def get_status(self):
        return self.__status

    def mark_claimed(self):
        """
        Changes status from Lost to Claimed and returns True.
        Returns False without modifying if already Claimed.
        """
        if self.__status == STATUS_LOST:
            self.__status = STATUS_CLAIMED
            return True
        return False

    def __str__(self):
        return (
            str(self.__id) + " | "
            + self.__name + " | "
            + self.__category + " | "
            + self.__location + " | "
            + self.__status
        )

    def __eq__(self, other):
        if type(self) == type(other):
            return self.__id == other.__id
        return False
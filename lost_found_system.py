"""
Manages the collection of LostItem records and file persistence.
"""

from lost_item import LostItem, STATUS_LOST, STATUS_CLAIMED


class LostFoundSystem:
    """
    Manages registering, searching, claiming, displaying, saving, and loading items.
    """
    __slots__ = ["__items"]

    def __init__(self):
        self.__items = []

    def get_item_count(self):
        return len(self.__items)

    def add_item(self, item):
        """
        Adds a LostItem and returns True; returns False if its ID already exists.
        """
        for existing in self.__items:
            if existing == item:
                return False
        self.__items.append(item)
        return True

    def search_item(self, item_id):
        """
        Returns matching LostItem by ID, or None if not found.
        """
        for item in self.__items:
            if item.get_id() == item_id:
                return item
        return None

    def claim_item(self, item_id):
        """
        Claims the matching item; returns True only if status changes, else False.
        """
        item = self.search_item(item_id)
        if item is None:
            return False
        return item.mark_claimed()

    def display_items(self):
        """
        Displays every item using its __str__ representation.
        """
        if len(self.__items) == 0:
            print("No items registered.")
        else:
            for item in self.__items:
                print(item)

    def save_items(self, filename):
        """
        Saves comma-separated records to filename and returns the count saved.
        """
        with open(filename, "w") as file:
            for item in self.__items:
                line = (
                    str(item.get_id()) + ","
                    + item.get_name() + ","
                    + item.get_category() + ","
                    + item.get_location() + ","
                    + item.get_status() + "\n"
                )
                file.write(line)
        return len(self.__items)

    def load_items(self, filename):
        """
        Loads items from a comma-separated file, replacing current records if file exists.
        Skips invalid IDs, missing fields, invalid statuses, and duplicate IDs.
        If file is missing, prints an error, preserves current records, and returns 0.
        """
        try:
            loaded_items = []
            with open(filename, "r") as file:
                for line in file:
                    stripped = line.strip()
                    if stripped == "":
                        continue
                    parts = stripped.split(",")
                    if len(parts) != 5:
                        continue

                    id_str = parts[0].strip()
                    name = parts[1].strip()
                    category = parts[2].strip()
                    location = parts[3].strip()
                    status = parts[4].strip()

                    if status != STATUS_LOST and status != STATUS_CLAIMED:
                        continue

                    try:
                        item_id = int(id_str)
                        item = LostItem(item_id, name, category, location)
                        if status == STATUS_CLAIMED:
                            item.mark_claimed()
                    except ValueError:
                        continue

                    is_duplicate = False
                    for existing in loaded_items:
                        if existing == item:
                            is_duplicate = True
                            break

                    if not is_duplicate:
                        loaded_items.append(item)

            self.__items = loaded_items
            return len(self.__items)

        except FileNotFoundError:
            print("Error: File not found! 0 records loaded.")
            return 0
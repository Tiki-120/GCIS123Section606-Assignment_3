class LostItem:
    # Use __slots__ to restrict class attributes to private slots
    __slots__ = ["__id", "__name", "__category", "__location", "__status"]

    # Define a constructor __init__() that initializes the attributes
    def __init__(self, item_id, name, category, location):
        if not isinstance(item_id, int) or isinstance(item_id, bool) or item_id <= 0:
            raise ValueError("Item ID must be a positive integer.")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name cannot be empty.")

        if not isinstance(category, str) or not category.strip():
            raise ValueError("Category cannot be empty.")

        if not isinstance(location, str) or not location.strip():
            raise ValueError("Location cannot be empty.")

        self.__id = item_id
        self.__name = name.strip()
        self.__category = category.strip()
        self.__location = location.strip()
        self.__status = "Lost"

    # Create getter methods to retrieve the values of all attributes
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

    # Mark item as Claimed if currently Lost; return True if changed, else False
    def mark_claimed(self):
        if self.__status == "Lost":
            self.__status = "Claimed"
            return True
        return False

    # Define the __str__() method to display item details in a user-friendly format
    def __str__(self):
        return f"{self.__id} | {self.__name} | {self.__category} | {self.__location} | {self.__status}"

    # Define __eq__() and __ne__() methods to compare two LostItem objects based on their ID
    def __eq__(self, other):
        if type(self) == type(other):
            return self.__id == other.__id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    # Define __hash__() so LostItem objects can be used in sets/dictionaries
    def __hash__(self):
        return hash(self.__id)

    # Create a method named display() to print item details
    def display(self):
        print(self.__str__())


# Write a main() function for quick standalone testing
def main():
    item1 = LostItem(101, "Laptop", "Electronics", "Library")
    item2 = LostItem(102, "Water Bottle", "Personal", "Cafeteria")

    print("Displaying items:")
    item1.display()
    item2.display()

    print("\nClaiming item 101:")
    print("First claim:", item1.mark_claimed())
    print("Second claim:", item1.mark_claimed())
    item1.display()

    item_dict = {
        item1.get_id(): item1,
        item2.get_id(): item2
    }

    print("\nItem IDs in dictionary:")
    for item_id in item_dict:
        print(item_id)


if __name__ == "__main__":
    main()
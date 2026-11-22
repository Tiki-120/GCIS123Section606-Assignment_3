"""
Main interactive menu program for the Campus Lost & Found application.
"""

from lost_item import LostItem
from lost_found_system import LostFoundSystem

MENU_REGISTER = 1
MENU_SEARCH = 2
MENU_CLAIM = 3
MENU_DISPLAY = 4
MENU_SAVE = 5
MENU_LOAD = 6
MENU_EXIT = 7


def print_menu():
    print("\n--- Campus Lost & Found ---")
    print("1 - Register Lost Item")
    print("2 - Search for Item")
    print("3 - Claim an Item")
    print("4 - Display All Items")
    print("5 - Save Records")
    print("6 - Load Records")
    print("7 - Exit")


def handle_register(system):
    try:
        item_id = int(input("Enter item ID: "))
    except ValueError:
        print("Error: Item ID must be a positive integer.")
        return

    name = input("Enter item name: ")
    category = input("Enter item category: ")
    location = input("Enter location found: ")

    try:
        new_item = LostItem(item_id, name, category, location)
    except ValueError as err:
        print("Error:", err)
        return

    if system.add_item(new_item):
        print("Item registered successfully!")
    else:
        print("Error: Item ID", item_id, "already exists!")


def handle_search(system):
    try:
        item_id = int(input("Enter item ID to search: "))
    except ValueError:
        print("Error: Item ID must be an integer.")
        return

    found = system.search_item(item_id)
    if found is not None:
        print("Item Found!")
        print(found)
    else:
        print("Item not found.")


def handle_claim(system):
    try:
        item_id = int(input("Enter item ID to claim: "))
    except ValueError:
        print("Error: Item ID must be an integer.")
        return

    existing = system.search_item(item_id)
    if existing is None:
        print("Error: Item ID", item_id, "not found.")
    elif system.claim_item(item_id):
        print("Item", item_id, "successfully marked as Claimed!")
    else:
        print("Item is already claimed. No changes made.")


def handle_save(system):
    filename = input("Enter filename to save (e.g., items.txt): ").strip()
    if filename == "":
        print("Error: Filename cannot be empty.")
        return
    count = system.save_items(filename)
    print(count, "records saved successfully!")


def handle_load(system):
    filename = input("Enter filename to load (e.g., items.txt): ").strip()
    if filename == "":
        print("Error: Filename cannot be empty.")
        return
    count = system.load_items(filename)
    if count > 0:
        print(count, "records loaded successfully!")


def main():
    system = LostFoundSystem()
    while True:
        print_menu()
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid choice. Please enter a number from 1 to 7.")
            continue

        if choice == MENU_REGISTER:
            handle_register(system)
        elif choice == MENU_SEARCH:
            handle_search(system)
        elif choice == MENU_CLAIM:
            handle_claim(system)
        elif choice == MENU_DISPLAY:
            system.display_items()
        elif choice == MENU_SAVE:
            handle_save(system)
        elif choice == MENU_LOAD:
            handle_load(system)
        elif choice == MENU_EXIT:
            print("Thank you for using Campus Lost & Found! Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1 to 7.")


if __name__ == "__main__":
    main()
"""
Inventory Management System.

This module provides basic functions to manage a simple inventory system,
including adding, removing, loading, and saving stock data.
It has been cleaned and secured using static analysis tools (Pylint, Bandit, Flake8).
"""
import json
import logging
from datetime import datetime

# FIX: E501 - Line wrapped
# Initialize logging for better error/warning reporting
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Global variable
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """
    Adds a specified quantity of an item to the inventory.
    Uses 'logs' to track the operation history.

    :param item: Name of the item (str or compatible type).
    :param qty: Quantity to add (int).
    :param logs: List to append log messages to.
    """
    if logs is None:
        logs = []

    if not item:
        logging.warning("Attempted to add item with no name.")
        return

    # Input validation for quantity
    if not isinstance(qty, int) or qty < 0:
        # FIX: E501 - Line wrapped
        logging.error(
            "Invalid quantity %s provided for item %s.", qty, item
        )
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item, qty):
    """
    Removes a specified quantity of an item from the inventory.
    If stock drops to zero or less, the item is removed from stock_data.

    :param item: Name of the item to remove.
    :param qty: Quantity to remove (int).
    """
    try:
        # Check if item is in stock_data and has sufficient quantity before removal
        if stock_data.get(item, 0) >= qty:
            stock_data[item] -= qty
            if stock_data[item] <= 0:
                del stock_data[item]
                # FIX: E501 - Line wrapped
                logging.info(
                    "Item %s removed from stock (quantity dropped to 0 or less).",
                    item
                )
        else:
            # FIX: E501 - Line wrapped
            logging.warning(
                "Attempted to remove %s of %s, but only %s in stock.",
                qty, item, stock_data.get(item, 0)
            )
    except KeyError:
        logging.error("Attempted to remove non-existent item: %s.", item)


def get_qty(item):
    """
    Retrieves the current stock quantity for an item.

    :param item: Name of the item.
    :return: Current quantity (int).
    """
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Loads inventory data from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            # W0603: Required to reassign the global variable
            global stock_data
            stock_data = json.loads(f.read())
        logging.info("Inventory data loaded from %s.", file)
    except FileNotFoundError:
        # FIX: E501 - Line wrapped
        logging.error(
            "Load file not found: %s. Starting with empty stock.", file
        )
    except json.JSONDecodeError:
        # FIX: E501 - Line wrapped
        logging.error(
            "Error decoding JSON from %s. Starting with empty stock.", file
        )


def save_data(file="inventory.json"):
    """Saves the current inventory data to a JSON file."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            # Use indent for better JSON readability
            f.write(json.dumps(stock_data, indent=4))
        logging.info("Inventory data saved to %s.", file)
    except IOError as e:
        # FIX: E501 - Line wrapped
        logging.critical("Error saving data to %s: %s", file, e)


def print_data():
    """Prints a report of all items and their quantities."""
    print("--- Items Report ---")
    if not stock_data:
        print("Inventory is empty.")
        return
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


def check_low_items(threshold=5):
    """
    Returns a list of items whose stock quantity is below the given threshold.

    :param threshold: The quantity level considered 'low'.
    :return: A list of item names.
    """
    # FIX: E501 - Line wrapped
    return [
        item for item, qty in stock_data.items() if qty < threshold
    ]


def main():
    """Main execution block for the inventory system demonstration."""
    inventory_logs = []

    add_item("apple", 10, inventory_logs)
    add_item("banana", 2, inventory_logs)
    add_item("grape", 4, inventory_logs)
    # The following line is handled/ignored gracefully due to input validation in add_item
    add_item(123, "ten", inventory_logs)  # Fixed comment spacing

    remove_item("apple", 3)
    remove_item("orange", 1)  # Handled by KeyError in remove_item

    print(f"Apple stock: {get_qty('apple')}")

    print(f"Low items (threshold 5): {check_low_items()}")

    save_data()
    load_data()
    print_data()

    print("\n--- Inventory Logs ---")
    for log in inventory_logs:
        print(log)


if __name__ == "__main__":
    main()
# FIX: C0304/W292 - Final newline added
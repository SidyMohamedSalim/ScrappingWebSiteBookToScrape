from categories import *
from book import *
import json


def get_data_books():
    """
    Fetches and prints detailed information about books from all categories.

    This function:
    1. Retrieves all book categories.
    2. Collects links to all books within these categories.
    3. Gathers detailed information about each book.

    The final result is returned as a structured list of book details.
    """
    categories = get_categories()  # Fetch all categories
    links_books_categories = get_all_links_books_categories(categories)  # Get all book links for each category
    infos_books_categories = get_all_infos_books_categories(links_books_categories)  # Get detailed info for each book
    return infos_books_categories  # return the detailed book info


def save_infos_books_in_file(infos_books_categories):
    with open("data_books.json", "w") as f:
        json.dump(infos_books_categories, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    infos_books_categories = get_data_books()
    save_infos_books_in_file(infos_books_categories)

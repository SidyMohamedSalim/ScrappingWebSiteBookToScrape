from categories import *
from book import *


def get_data_books():
    """
    Fetches and prints detailed information about books from all categories.

    This function:
    1. Retrieves all book categories.
    2. Collects links to all books within these categories.
    3. Gathers detailed information about each book.

    The final result is printed as a structured list of book details.
    """
    categories = get_categories()  # Fetch all categories
    links_books_categories = get_all_links_books_categories(categories)  # Get all book links for each category
    infos_books_categories = get_all_infos_books_categories(links_books_categories)  # Get detailed info for each book
    pprint(infos_books_categories)  # Print the detailed book info


if __name__ == "__main__":
    get_data_books()

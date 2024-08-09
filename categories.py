from pprint import pprint
import constants
from bs4 import BeautifulSoup
import requests

from scraping.booktosrape.book import get_book_infos


def get_categories():
    """
    Fetches all book categories from the base URL defined in constants.

    Returns:
        list: A list of tuples containing the category name and the link to the category.
    """
    print("Start fetching categories...")
    r = requests.get(constants.BASE_URL)
    if r.status_code != 200:
        print("Error fetching the categories...")
        return

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(r.content, features="html.parser")
    aside_content = soup.find("aside").find_next("ul")

    if not aside_content:
        return get_categories()

    categories = []
    for category in aside_content.find_all("a"):
        value = category.get_text(strip=True)
        href: str = category.get("href")
        link = f"{constants.BASE_URL}/{href}"
        categories.append((value, link))

    # Exclude the 'Books' category
    categories = [category for category in categories if str(category[0]).lower() != "books"]

    return categories


def get_books_page_category(url_category, category_name, page_number=1):
    """
    Fetches all book links from a single page of a given category.

    Args:
        url_category (str): The URL of the category page.
        category_name (str): The name of the category.
        page_number (int, optional): The page number to fetch. Defaults to 1.

    Returns:
        list: A list of links to individual book pages on the current category page.
    """
    retry = 0
    max_retry = 3
    print(f"Fetching {category_name} page {page_number}...")

    books_category_page = []

    if page_number != 1:
        url_category = url_category.replace("index.html", f"page-{page_number}.html")

    r = requests.get(url_category)
    soup = BeautifulSoup(r.content, "html.parser")

    books_section = soup.find("ol")
    if not books_section and retry > max_retry:
        retry += 1
        return get_books_page_category(url_category, category_name=category_name)

    if books_section:
        articles = books_section.find_all("article")
        for section in articles:
            a = section.find_next("a")
            href: str = a.get("href")
            href_array = href.split("/")
            link_book = f"{constants.BASE_URL}/catalogue/{href_array[-2]}/{href_array[-1]}"
            books_category_page.append(link_book)

    return books_category_page


def get_all_links_books_for_one_category(url_category, category_name):
    """
    Fetches all book links for a given category across all pages.

    Args:
        url_category (str): The URL of the category.
        category_name (str): The name of the category.

    Returns:
        list: A list of all book links for the category.
    """
    all_links_books_category = []
    page_number = 1
    while True:
        books_category_page = get_books_page_category(url_category, category_name, page_number)
        if not books_category_page:
            break
        all_links_books_category.extend(books_category_page)
        page_number += 1

    return all_links_books_category


def get_all_links_books_categories(categories: list):
    """
    Fetches all book links for the first three categories.

    Args:
        categories (list): A list of category tuples containing category names and URLs.

    Returns:
        list: A list of tuples, each containing a category name and a list of book links.
    """
    links_books_categories = []
    for category in categories:
        category_name = category[0]
        category_link = category[1]
        links_books = get_all_links_books_for_one_category(category_link, category_name)
        links_books_categories.append((category_name, links_books))

    return links_books_categories


def get_all_infos_books_by_one_category(links_books_category: list):
    """
    Fetches information for all books in a given category.

    Args:
        links_books_category (list): A tuple containing the category name and a list of book links.

    Returns:
        tuple: A tuple containing the category name and a list of dictionaries with book information.
    """
    category_name = links_books_category[0]
    links_books = links_books_category[1]
    infos_books = []

    for link_book in links_books:
        book_infos = get_book_infos(link_book)
        infos_books.append(book_infos)

    return (category_name, infos_books)


def get_all_infos_books_categories(links_books_categories: list):
    """
    Fetches information for all books across all categories.

    Args:
        links_books_categories (list): A list of tuples, each containing a category name and a list of book links.

    Returns:
        list: A list of tuples, each containing a category name and a list of book information dictionaries.
    """
    all_infos_books_categories = []

    for links_books_category in links_books_categories:
        infos_books_category = get_all_infos_books_by_one_category(links_books_category)
        all_infos_books_categories.append(infos_books_category)

    return all_infos_books_categories


def main():

    categories = get_categories()
    links_books_categories = get_all_links_books_categories(categories)
    pprint(links_books_categories)


if __name__ == "__main__":
    main()

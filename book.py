from pprint import pprint
import constants
from bs4 import BeautifulSoup
import requests


def get_book_infos(url_book):
    """
    Fetches detailed information about a specific book from the given URL.

    Args:
        url_book (str): The URL of the book page to fetch information from.

    Returns:
        list: A list of tuples containing book details, such as title, description, and other specific information.
    """
    print(f"Start fetching {url_book}...")
    book_infos = []

    r = requests.get(url_book)
    if r.status_code != 200:
        # Retry fetching the book information if the request fails
        return get_book_infos(url_book)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(r.content, "html.parser")
    content = soup.find("div", id="content_inner")

    # Fetch the book title
    title = content.find_next("h1").get_text()
    book_infos.append(("title", title))

    # Fetch the book description
    description = content.find_next("div", id="product_description").find_next('p').get_text()
    book_infos.append(("description", description))

    # Fetch additional book details from the table
    details_book_section = content.find_next("table", class_="table table-striped")
    if details_book_section:
        for detail in details_book_section.find_all("tr"):
            name_info_book = str(detail.find_next("th").get_text())
            value_info_book = str(detail.find_next("td").get_text())
            book_infos.append((name_info_book, value_info_book))

    return book_infos


def main():
    book_infos = get_book_infos(
        f"{constants.BASE_URL}/catalogue/a-spys-devotion-the-regency-spies-of-london-1_3/index.html")
    pprint(book_infos)


if __name__ == "__main__":
    main()

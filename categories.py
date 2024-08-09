from pprint import pprint
import constants
from bs4 import BeautifulSoup
import requests


def get_categories():
    print("start fetching categories...")
    r = requests.get(constants.BASE_URL)
    if r.status_code != 200:
        print("Erreur...")
        return

    soul = BeautifulSoup(r.content, features="html.parser")
    aside_content = soul.find("aside").find_next("ul")

    if not aside_content:
        get_categories()

    categories = []
    for categorie in aside_content.find_all("a"):
        value = categorie.get_text(strip=True)
        href: str = categorie.get("href")
        link = f"{constants.BASE_URL}/{href}"
        categories.append((value, link))
    categories = [categorie for categorie in categories if str(categorie[0]).lower() != "books" ]
    return categories


def get_books_page_categorie(url_categorie, categorie_name, page_number=1):
    retry = 0
    max_retry = 3
    print(f"fetching {categorie_name} page {page_number} ...")

    books_categorie_page = []

    if page_number != 1:
        url_categorie = url_categorie.replace("index.html", f"page-{page_number}.html")

    r = requests.get(url_categorie)
    soul = BeautifulSoup(r.content, "html.parser")

    books_section = soul.find("ol")
    if not books_section and retry > max_retry:
        retry += 1
        get_books_page_categorie(url_categorie,categorie_name=categorie_name)

    if books_section:
        songs_article = books_section.find_all("article")
        for section in songs_article:
            a = section.find_next("a")
            href: str = a.get("href")
            href_array = href.split("/")
            link_book = f"{constants.BASE_URL}/catalogue/{href_array[-2]}/{href_array[-1]}"
            books_categorie_page.append(link_book)

    return books_categorie_page


def get_all_links_books_for_one_categorie(url_categorie, categorie_name):
    all_links_books_categorie = []
    page_number = 1
    while True:
        books_categorie_page = get_books_page_categorie(url_categorie ,categorie_name ,page_number)
        if not books_categorie_page:
            break
        all_links_books_categorie.extend(books_categorie_page)
        page_number += 1

    return all_links_books_categorie


def get_all_links_books_categories(categories:list):
    links_books_categories = []
    for categorie in categories[:3]:
        categorie_name = categorie[0]
        categorie_link = categorie[1]
        links_books = get_all_links_books_for_one_categorie(categorie_link,categorie_name)
        links_books_categories.append((categorie_name,links_books))

    return links_books_categories



def main():
    categories = get_categories()
    links_books_categories = get_all_links_books_categories(categories)
    pprint(links_books_categories)


if __name__ == "__main__":
    main()

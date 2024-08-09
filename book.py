from pprint import pprint
import constants
from bs4 import BeautifulSoup
import requests


def get_book_infos(url_book):
    print(f"start fetching {url_book} ... ")
    book_infos = []
    r = requests.get(url_book)
    if r.status_code != 200:
        get_book_infos(url_book)

    soul = BeautifulSoup(r.content,"html.parser")
    content = soul.find("div",id="content_inner")
    title = content.find_next("h1").get_text()
    book_infos.append(("title",title))
    description = content.find_next("div",id="product_description").find_next('p').get_text()
    book_infos.append(("description",description))
    details_book_section =  content.find_next("table",class_="table table-striped")
    if details_book_section:
        for detail in details_book_section.find_all("tr"):
            name_info_book = str(detail.find_next("th").get_text())
            value_info_book = str(detail.find_next("td").get_text())
            book_infos.append((name_info_book,value_info_book))

    return book_infos


def main():
    book_infos = get_book_infos(f"{constants.BASE_URL}/catalogue/a-spys-devotion-the-regency-spies-of-london-1_3/index.html")
    print(book_infos)


if __name__ == "__main__":
    main()

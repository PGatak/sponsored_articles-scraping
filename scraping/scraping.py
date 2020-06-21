from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from start_urls import all_start_urls

from common.db import create_connection
from common.db import (
    services,
    articles,
    urls
)
from matchers import match_tags

UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
)

TIMEOUT = 30


connection = create_connection()

session = requests.Session()
session.headers.update({"User-agent": UA})


def extract_urls(text, service_name, current_url):
    urls = []
    bs = BeautifulSoup(text, "lxml")
    links = bs.find_all("a")
    for link in links:
        article_url = link.attrs.get("href", "")
        if article_url and not article_url.startswith("#"):
            article_url = urljoin(current_url, article_url)
            record = {"article_url": article_url, "service_name": service_name}
            urls.append(record)
    return urls


if __name__ == "__main__":
    services.add_services(connection, all_start_urls)
    urls.add_start_urls(connection, all_start_urls)

    urls = urls.get_start_urls(connection)
    # print([dict(r) for r in urls])


    while urls:
        task = urls.pop(0)
        # print(task)
        current_url = task["start_url_name"]
        service_name = task["service_name"]
        extracted_urls = []

        try:
            response = session.get(current_url, timeout=TIMEOUT)
            extracted_urls = extract_urls(response.text,
                                          service_name,
                                          current_url)
        except Exception as e:
            print(e)
            continue

    for new_article in extracted_urls:
        url = new_article['article_url']
        if articles.is_article_old(connection, new_article):
            print("old", url)
            continue

        created = articles.add_article(connection, new_article)

        # article is new
        try:
            print("GET", url)
            response = session.get(url, timeout=(3, TIMEOUT))
            soup = BeautifulSoup(response.text, "lxml")
            tags = match_tags(soup.find("body").text)
            if tags:
                print("|______> MATCHED", tags)
                articles.add_article_tags(
                    connection, created["article_id"], tags)
        except Exception as e:
            print(e)
            continue

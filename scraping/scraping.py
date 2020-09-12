from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

from start_urls import all_start_urls
from db import (create_connection,
                articles as articles_api,
                services as services_api,
                urls as urls_api)
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
            record = {"article_url": article_url,
                      "service_name": service_name}
            urls.append(record)

    return urls


if __name__ == "__main__":
    services_api.add_services(connection, all_start_urls)
    urls_api.add_start_urls(connection, all_start_urls)
    urls = urls_api.get_start_urls(connection)

    while urls:
        task = urls.pop(0)
        current_url = task["start_url_name"]
        service_name = task["service_name"]
        extracted_urls = []
        response = None

        try:
            response = session.get(current_url, timeout=TIMEOUT)
        except requests.exceptions.RequestException as e:
            print(e)
            continue
        if not response.ok:
            continue

        try:
            extracted_urls = extract_urls(response.text,
                                          service_name,
                                          current_url)
        except Exception as e:
            # catching all exceptions to continue anyway
            print(e)
            continue

        for new_article in extracted_urls:
            url = new_article['article_url']

            if articles_api.is_article_old(connection, new_article):
                print("old", url)
                continue

            if ("/sport/" or "koronawirus" or "/ogloszenia/") in url:
                continue

            created = articles_api.add_article(connection, new_article)

            # article is new
            try:
                print("GET", url)
                response = session.get(url, timeout=(3, TIMEOUT))
                soup = BeautifulSoup(response.text, "lxml")
                tags = match_tags(soup.find("body").text)
                if tags:
                    print("|______> MATCHED", tags)
                    articles_api.add_article_tags(
                        connection, created["article_id"], tags)
            except Exception as e:
                print(e)
                continue

import requests
from bs4 import BeautifulSoup
from collections import namedtuple

import setup


def get_description(art_name):
    response = requests.get(
        url="https://en.wikipedia.org/wiki/" + art_name,
    )

    if not response:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    description = soup.find(id="bodyContent").find_all("p")[1].text
    if len(description) > 500:
        description = description[:500] + "..."

    return description

auth_url = "https://www.wikiart.org/en/Api/2/login?accessCode={}&secretCode={}"\
    .format(setup.api_access_key, setup.api_secret_key)

session_key = requests.get(auth_url).json()["SessionKey"]


def get_search_results(art_name):
    url = "https://www.wikiart.org/en/api/2/PaintingSearch?term={}&imageFormat=Large&authSessionKey={}"\
        .format(art_name, session_key)

    response_json = requests.get(url).json()

    ShortDescription = namedtuple("ShortDescription", "id image")

    return list(map(lambda element: ShortDescription(element["id"], element["image"]), response_json["data"][:10]))


if __name__ == "__main__":
    print(get_search_results("The scream"))

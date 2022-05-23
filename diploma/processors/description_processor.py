import requests
from bs4 import BeautifulSoup


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


if __name__ == "__main__":
    print(get_description("The scream"))

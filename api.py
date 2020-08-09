import logging
import random
import string
from typing import Union

from flask import Flask, request, redirect

logger = logging.getLogger()

app = Flask(__name__)

# {"short_url1": "url1", "short_url2": "url2"}
url_map = {}

CHARACTER_CHOICES = string.ascii_letters+string.digits
SHORT_URL_LENGTH = 5


def get_random_string(choices: Union[list, tuple, str], length: int) -> str:
    return "".join(random.choices(choices, k=length))


def shorten_url(url: str, short_url: str="") -> str:
    global url_map

    og_short_url = short_url

    # very smart collision checker in 3 lines
    short_url = og_short_url + get_random_string(CHARACTER_CHOICES, SHORT_URL_LENGTH)
    i = 0
    while url_map.get(short_url, ""):
        i += 1
        logger.warn(f"---------- Detected collision {i} times")
        short_url = og_short_url + get_random_string(CHARACTER_CHOICES, SHORT_URL_LENGTH)

    return short_url


def lengthen_url(short_url: str) -> str:
    return url_map.get(short_url, "")


class URLMapping:
    def __init__(self, url: str, short_url: str, strict: bool):
        self.url = url
        self.short_url = short_url
        self.strict = strict

    @staticmethod
    def create(url: str, short_url: str="", strict: bool=True):
        if strict and short_url and short_url in url_map:
            raise KeyError(f"short_url {short_url} already assigned")

        if not strict and short_url and short_url in url_map:
            short_url = shorten_url(url, short_url)
        else:
            short_url = shorten_url(url) if not short_url else short_url

        return URLMapping(url=url, short_url=short_url, strict=strict)

@app.route("/api", methods=["POST"])
def create_short_url():
    global url_map
    payload = request.json

    try:
        url = payload["url"]
    except KeyError as e:
        message = "key `url` not found in payload"
        logger.error(message)
        return {"error": message}, 400

    strict = payload.get("strict", True)
    short_url = payload.get("short_url", "")

    try:
        url_mapping = URLMapping.create(url, short_url, strict)
    except KeyError as e:
        return {"error": f"{e}. Please use strict=false for getting a random id appended"}, 409

    url_map[url_mapping.short_url] = url_mapping.url

    return {"url": url_mapping.url, "short_url": url_mapping.short_url}


@app.route("/<short_url>")
def redirect_url(short_url):
    url = lengthen_url(short_url)

    if not url:
        return {"error": f"{short_url} not found"}, 404

    return redirect(url)


if __name__ == "__main__":
    app.run(debug=True)

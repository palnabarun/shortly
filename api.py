import logging
import random
import string

from flask import Flask, request, redirect

logger = logging.getLogger()

app = Flask(__name__)

url_map = {}

CHARACTER_CHOICES = string.ascii_letters+string.digits
SHORT_URL_LENGTH = 5


def shorten_url(url: str) -> str:
    global url_map

    # very smart collision checker in 3 lines
    random_id = "".join(random.choices(CHARACTER_CHOICES, k=SHORT_URL_LENGTH))
    i = 0
    while url_map.get(random_id, ""):
        i += 1
        logger.warn(f"---------- Detected collision {i} times")
        random_id = "".join(random.choices(CHARACTER_CHOICES, k=SHORT_URL_LENGTH))

    return random_id


def lengthen_url(short_url: str) -> str:
    return url_map.get(short_url, "")


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

    short_url = shorten_url(url)
    url_map[short_url] = url

    return {"url": url, "short_url": short_url}


@app.route("/<short_url>")
def redirect_url(short_url):
    url = lengthen_url(short_url)

    if not url:
        return {"error": f"{short_url} not found"}, 404

    return redirect(url)


if __name__ == "__main__":
    app.run(debug=True)

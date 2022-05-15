import requests
import numpy as np
from modules import util

base_url = r"https://www.googleapis.com/customsearch/v1?"


def get_image(key_word):
    search_results = _image_search(key_word)
    image, file_ext = _select_image(search_results)
    return image, file_ext


def _image_search(key_word):
    key = "key={}".format(util.get_key("image"))
    engine_id = "cx={}".format(util.get_key("engine_id"))
    search_type = "searchType=image"
    num_results = "num=10"
    query = "q={}".format(key_word)
    query_url = "{}{}&{}&{}&{}&{}".format(base_url, key, engine_id, search_type, num_results, query)
    response = requests.get(query_url)
    if "items" in response.json():
        return [result["link"] for result in response.json()["items"]]
    else:
        print(response.json())
        return None


def _select_image(image_links):
    np.random.shuffle(image_links)
    for link in image_links:
        file_ext = link.strip().split(".")[-1].lower()
        if file_ext != "png" and file_ext != "jpg" and file_ext != "jpeg":
            continue
        response = requests.get(link)
        if response.status_code != 200:
            continue
        image = response.content
        return image, file_ext
    return None

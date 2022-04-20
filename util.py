import os
from dotenv import load_dotenv
import requests
import numpy as np

load_dotenv()
API_KEY = os.getenv("API_KEY")
ENGINE_ID = os.getenv("ENGINE_ID")
SEARCH_TYPE = "image"
NUMBER = 10
FILE_TYPE = 'png'


def get_decade(year):
    return int(year / 10) * 10


def query2image(query):
    google_image_api = r"https://www.googleapis.com/customsearch/v1?key={}&cx={}&searchType={}&fileType={}&num={}&q={}" \
        .format(API_KEY, ENGINE_ID, SEARCH_TYPE, FILE_TYPE,NUMBER, query)
    response = requests.get(google_image_api)
    if "items" in response.json():
        result = response.json()["items"]
        choice = np.random.choice(len(result))
        image_link = result[choice]['link']
        return image_link
    else:
        print(response.json())

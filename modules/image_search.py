from dotenv import load_dotenv
from collections import defaultdict, Counter
from PIL import Image
import os
import requests
from . import movie_scrape
from . import smart_query
import numpy as np

load_dotenv()
API_KEY = os.getenv("API_KEY")
ENGINE_ID = os.getenv("ENGINE_ID")
SEARCH_TYPE = "image"
NUMBER = 10
FILE_TYPE_1, FILE_TYPE_2, FILE_TYPE_3 = "png", "jpg", "jpeg"
CWD = os.getcwd()
IMG_FOLDER = "img/"

# this dictionary is used to determine the search query for a given
# input. 'None' indicates that we don't want to search for an image for this
# input. An empty string, "", indicates that we want to search for an image,
# but don't want to append anything to the query.
SEARCH_MAP = {
    "birth": {
        "date": " visual",
        "location": " landscape"
        # "location": None # Will change later because the video animation can only support 2 pictures
    },
    "childhood": {
        "start_year": "time magazine person of the year",
        "end_year": None,
        "location": "",
        "language": None
    },
    "school": {
        "start_year": None,
        "end_year": None,
        "name": " logo",
        "location": ""
    },
    "previous_home": {
        "start_year": None,
        "end_year": None,
        "location": " landscape"
    },
    "previous_work": {
        "start_year": None,
        "end_year": None,
        "name": " logo",
        "position": " job picture",
    },
    "wedding": {
        "spouse_name": None,
        "wedding_date": None,
        "location": " landscape"
    },
    "current_status": {
        "age": None,
        "location": "",
        "occupation": " job picture",
        "company": " logo"
    },
    "children": {
        "number": None,
        "child_name": "baby clipart",
        "birth_date": None,
        "location": " landscape"
    },
    "death": {
        "death_data": " visual death",
        "age": None,
        "location": None
    },
}


def google_img_search(key_word):
    print(key_word)
    # only searching for PNGs for right now
    # if "calendar" in key_word:
    # google_image_api = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={ENGINE_ID}&searchType={SEARCH_TYPE}&num={NUMBER}&fileType={FILE_TYPE_1}&q={key_word}"
    google_image_api = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={ENGINE_ID}&searchType={SEARCH_TYPE}&num={NUMBER}&q={key_word}"
    # else:
    #     google_image_api = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={ENGINE_ID}&searchType={SEARCH_TYPE}&num={NUMBER}&q={key_word}"

    response = requests.get(google_image_api)
    if "items" in response.json():
        return response.json()["items"]
    else:
        print(response.json())
    # resp_idx = None

    # wikipedia images seems to be an issue. also, some links end in ".svg.png" and are an issue
    # for i in range(len(imgs)):
    #     curr_link = imgs[i]["link"]
    #     if (".svg" not in curr_link) and (".gif" not in curr_link) and ("wiki" not in curr_link):
    #         resp_idx = i
    #         break

    # return response.json()["items"][resp_idx]["link"]


def save_image(images, name):
    image_links = [img["link"] for img in images]
    np.random.shuffle(image_links)
    for link in image_links:
        file_ext = link.strip().split(".")[-1].lower()
        if file_ext != "png" and file_ext != "jpg" and file_ext != "jpeg":
            continue
        response = requests.get(link)
        if response.status_code != 200:
            continue

        print("SAVING IMAGE")
        is_exist = os.path.exists(os.path.join(CWD, IMG_FOLDER))
        if not is_exist:
            os.makedirs(os.path.join(CWD, IMG_FOLDER))
        file_path = os.path.join(CWD, f"img/{name}.{file_ext}")
        file = open(file_path, "wb")
        file.write(response.content)
        file.close()

        # Check if image is grayscale and if so, convert to RGB
        # (Addresses issue with moviepy library)
        try:
            print("save", link)
            img = Image.open(file_path)
        except:
            print("remove", link)
            os.remove(file_path)
            continue

        if img.mode in ["1", "L", "P"]:
            # Known grayscale image, so convert
            rgbimg = Image.new("RGB", img.size)
            rgbimg.paste(img)
            rgbimg.save(file_path, format=img.format)
        break

    return file_path


def delete_all_images():
    is_exist = os.path.exists(os.path.join(CWD, IMG_FOLDER))
    if is_exist:
        for filename in os.listdir(os.path.join(CWD, IMG_FOLDER)):
            f = os.path.join(CWD, IMG_FOLDER, filename)
            os.remove(f)


#
# returns the query we'd like to perform and image search
#
def get_search_params(event_dict, event, sub_event):
    to_append = SEARCH_MAP[event][sub_event]
    if to_append is None:
        return None
    sub_event_str = event_dict[event][sub_event]
    # fix school logo search by adding location onto 
    if event == "school" and sub_event == "name":
        to_append += f" {event_dict['school']['location']}"
    elif event == "children" and sub_event == "child_name":
        sub_event_str = ""
    elif event == "childhood" and sub_event == "language":
        language = event_dict["childhood"]["language"]

    return sub_event_str + to_append


# input looks like
# [
#    { "birth": { "date": "xxx", "location": "xxx" }},
#    { "school": { "name": "xxx", "start_year": "xxx", "end_year": "xxx" }},
# ]

# output looks like
# [
#    { "birth": ["path/to/file.png"] },
#    { "school": ["path/to/file2.png", "path/to/file3.png"] }
# ]

def image_search(data):
    # delete the file in the folder
    delete_all_images()
    # use counter to keep track of multiple events -> ex. school, work, etc.
    counter = Counter()
    result = []
    for _dict in data:
        # skip name
        if "name" in _dict:
            continue
        # init output
        output_dict = defaultdict(list)
        for event, val in _dict.items():
            counter[event] += 1
            keys = list(val.keys())
            for sub_event in keys:
                search_str = val[sub_event]
                query = smart_query.construct_query(_dict, event, sub_event)
                query_str = get_search_params(_dict, event, sub_event)
                if query_str is None:
                    continue

                # do query seach using google api
                print("query")
                print(query + "\n")
                images = google_img_search(query)
                if not images:
                    continue
                file_path = save_image(images, f"{event}_{sub_event}_{counter[event]}")
                output_dict[f"{event}_{counter[event]}"].append(file_path)

                # do movie search
                if event == "birth" and sub_event == "date":
                    year = int(search_str.split(",")[-1].strip())
                    movie = movie_scrape.find_movie(year)
                    val["movie"] = movie
                    images = google_img_search(movie + " poster")
                    file_path = save_image(images, f"{event}_{movie}_{counter[event]}")
                    output_dict[f"{event}_{counter[event]}"].append(file_path)

        result.append(output_dict)

    return result

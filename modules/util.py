import os
from PIL import Image
from dotenv import load_dotenv
import json

# configs
CWD = os.getcwd()
IMG_FOLDER = "img/"

# load various key from env file
load_dotenv()
MAP_API_KEY = os.getenv("MAP_API")
IMAGE_SEARCH_API_KEY = os.getenv("IMAGE_API")
ENGINE_ID = os.getenv("ENGINE_ID")

# load keywords from json
with open("./major_events.json", "r", encoding="utf-8") as json_file:
    major_events = json.load(json_file)
with open("./switches.json", "r", encoding="utf-8") as json_file:
    switches = json.load(json_file)
with open("./landmarks.json", "r", encoding="utf-8") as json_file:
    landmarks = json.load(json_file)


def get_landmarks():
    return landmarks


def get_major_event(decade):
    if decade in major_events:
        return major_events[decade]
    return None


def get_switches():
    return switches


def get_key(key_name):
    if key_name.lower() == "map":
        return MAP_API_KEY
    elif key_name.lower() == "image":
        return IMAGE_SEARCH_API_KEY
    elif key_name.lower() == "engine_id":
        return ENGINE_ID
    else:
        return None


def get_decade(year):
    decade = int(int(year) / 10) * 10
    return str(decade) + "s"


def delete_all_images():
    is_exist = os.path.exists(os.path.join(CWD, IMG_FOLDER))
    if is_exist:
        for filename in os.listdir(os.path.join(CWD, IMG_FOLDER)):
            f = os.path.join(CWD, IMG_FOLDER, filename)
            os.remove(f)


def save_image(image, file_ext, name):
    print("SAVING IMAGE: {}".format(name))
    is_exist = os.path.exists(os.path.join(CWD, IMG_FOLDER))
    if not is_exist:
        os.makedirs(os.path.join(CWD, IMG_FOLDER))
    file_path = os.path.join(CWD, f"img/{name}.{file_ext}")
    with open(file_path, "wb") as image_file:
        image_file.write(image)
    try:
        img = Image.open(file_path)
    except:
        print("FAILED: image removed")
        os.remove(file_path)
        return None

    if img.mode in ["1", "L", "P"]:
        # Known grayscale image, so convert
        rgbimg = Image.new("RGB", img.size)
        rgbimg.paste(img)
        rgbimg.save(file_path, format=img.format)
    print("SUCCESS")

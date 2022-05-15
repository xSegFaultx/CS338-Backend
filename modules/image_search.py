from collections import defaultdict, Counter
from modules import movie_scrape
from modules import smart_query, google_custom_search, map_generator, util

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


def _generate_image(event_dict, event, sub_event):
    query, gen_method = smart_query.construct_query(event_dict, event, sub_event)
    if gen_method == "search":
        image, file_ext = google_custom_search.get_image(query)
        if image:
            return image, file_ext
    elif gen_method == "map":
        city, state, country = query
        image = map_generator.generate_single_location_map(city, state, country)
        if image:
            return image, "png"
    return None, None


def image_search(data):
    # delete the file in the folder
    util.delete_all_images()
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
                if not util.get_switches()[event][sub_event]:
                    continue
                image, file_ext = _generate_image(_dict, event, sub_event)
                if not image:
                    continue
                file_path = util.save_image(image, file_ext, f"{event}_{sub_event}_{counter[event]}")
                output_dict[f"{event}_{counter[event]}"].append(file_path)

                # do movie search
                """
                if event == "birth" and sub_event == "date":
                    year = int(search_str.split(",")[-1].strip())
                    movie = movie_scrape.find_movie(year)
                    val["movie"] = movie
                    images = google_img_search(movie + " poster")
                    file_path = save_image(images, f"{event}_{movie}_{counter[event]}")
                    output_dict[f"{event}_{counter[event]}"].append(file_path)
                """

        result.append(output_dict)

    return result

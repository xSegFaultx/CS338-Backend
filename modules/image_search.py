from collections import defaultdict, Counter
from modules import movie_scrape
from modules import smart_query, google_custom_search, map_generator, util


def _generate_image(event_dict, event, sub_event):
    query, gen_method = smart_query.construct_query(event_dict, event, sub_event)
    if gen_method == "search":
        image, file_ext = google_custom_search.get_image(query)
        if image:
            return image, file_ext
    elif gen_method == "map":
        state, country = query
        image = map_generator.generate_single_location_map(state, country)
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
                if _dict[event][sub_event] is None:
                    continue
                if _dict[event][sub_event] == "":
                    continue
                if not util.get_switches()[event][sub_event]:
                    continue
                image, file_ext = _generate_image(_dict, event, sub_event)
                if not image:
                    continue
                file_path = util.save_image(image, file_ext, f"{event}_{sub_event}_{counter[event]}")
                output_dict[f"{event}_{counter[event]}"].append(file_path)

                # do movie search
                if event == "birth" and sub_event == "date":
                    year = int(_dict[event][sub_event])
                    movie = movie_scrape.find_movie(year)
                    val["movie"] = movie
                    image, file_ext = google_custom_search.get_image(movie + " poster")
                    file_path = util.save_image(image, file_ext, f"{event}_{movie}_{counter[event]}")
                    output_dict[f"{event}_{counter[event]}"].append(file_path)

        result.append(output_dict)
    return result

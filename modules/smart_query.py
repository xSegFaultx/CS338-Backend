import sys
from modules import util
import numpy as np


def construct_query(event_dict, event, sub_event):
    print("-------------------------------")
    print(event_dict[event])
    print(event_dict[event][sub_event])
    print(event)
    print(sub_event)
    print("-------------------------------")
    constructor = getattr(sys.modules["modules.smart_query"], "{}_{}_query".format(event, sub_event))
    query = constructor(event_dict[event][sub_event])
    return query


def birth_date_query(date):
    # expected input format: Month DD, YYYY
    year = date.split(",")[-1].strip()
    decade = util.get_decade(year)
    query = "{} infant portrait".format(decade)
    return query, "search"


def _landmark_query(location):
    state, country = location.split(",")
    state = state.lower().strip()
    if country.strip().lower() == "usa":
        landmarks = util.get_landmarks()
        if state.lower() in landmarks:
            landmark = np.random.choice(landmarks[state.lower()])
        else:
            landmark = "{} landmarks".format(state)
        return landmark
    else:
        query = "{} landmarks".format(country.strip().lower())
    return query


def _map_query(location):
    city, state, country = location.split(",")
    return city.strip(), state.strip(), country.strip()


def _event_query(date):
    decade = util.get_decade(date)
    events = util.get_major_event(decade)
    if not events:
        event = "images of " + decade
        return event
    if len(events) == 1:
        event = events[0]
    elif len(events) > 1:
        event = np.random.choice(events)
    else:
        event = "images of " + decade
    return event


def birth_location_query(location):
    # expect input format: State, Country
    return _landmark_query(location), "search"


def childhood_location_query(location):
    # expect input format: City, State, Country
    city, state, country = _map_query(location)
    return [city, state, country], "map"


def childhood_start_year_query(date):
    # expect input format: YYYY
    return _event_query(date), "search"


def childhood_end_year_query(date):
    # expect input format: YYYY
    return _event_query(date), "search"


def school_name_query(name):
    return name + " logo", "search"


def school_start_year_query(date):
    # expect input format: YYYY
    return _event_query(date), "search"


def school_location_query(location):
    # expect input format: City, State, Country
    _, state, country = location.split(",")
    return _landmark_query("{}, {}".format(state.strip(), country.strip())), "search"


def previous_work_name_query(name):
    return name + " company logo", "search"


def previous_work_position_query(name):
    return name + "at work", "search"


def current_status_location_query(location):
    # expect input format: City, State, Country
    _, state, country = location.split(",")
    return _landmark_query("{}, {}".format(state.strip(), country.strip())), "search"


def current_status_occupation_query(name):
    return name + "at work", "search"


def current_status_company_query(name):
    return name + " company logo", "search"


def wedding_location_query(location):
    # expect input format: City, State, Country
    _, state, country = location.split(",")
    return _landmark_query("{}, {}".format(state.strip(), country.strip())), "search"

import sys
from . import util


def construct_query(event_dict, event, sub_event):
    print("-------------------------------")
    print(event_dict[event])
    print(event_dict[event][sub_event])
    print(event)
    print(sub_event)
    print("-------------------------------")
    constructor = getattr(sys.modules["smart_query"], "{}_{}_query".format(event, sub_event))
    query = constructor(event_dict[event][sub_event])
    return query


def birth_date_query(date):
    year = date.split(",")[-1].strip()
    decade = util.get_decade(year)
    query = "{} infant portrait".format(decade)
    return query


def _location_query(location):
    state, country = location.split(",")
    if country.strip().lower() == "usa":
        return "USA"
    else:
        query = "{} landmarks".format(country.strip().lower())
    return query


def birth_location_query(location):
    return _location_query(location)


def childhood_location_query(location):
    return _location_query(location)

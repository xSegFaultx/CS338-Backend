import requests
from geopy.geocoders import Nominatim
from modules import util
from geopy import distance

loc = Nominatim(user_agent="GetLoc")
base_url = r"https://maps.googleapis.com/maps/api/staticmap?"


# convert city name to longitude and latitude
def _city2ll(city):
    location = loc.geocode(city)
    latitude, longitude = location.latitude, location.longitude
    return latitude, longitude


def generate_single_location_map(city, state, country):
    location = "{}, {}, {}".format(city, state, country)
    latitude, longitude = _city2ll(location)
    format_state = "+".join(state.strip().split())
    format_country = "+".join(country.strip().split())
    center = "center={}+State,{}".format(format_state, format_country)
    size = "size=800x800"
    map_type = "maptype=roadmap"
    markers = "markers=color:red%7Clabel:%7C{},{}".format(latitude, longitude)
    key = "key={}".format(util.get_key("map"))
    query_url = "{}{}&{}&{}&{}&{}".format(base_url, center, size, map_type, markers, key)
    response = requests.get(query_url)
    if response.status_code == 200:
        map_image = response.content
        return map_image
    else:
        print(response)
        return None

# 155.91127558836405   7
# 31.930454905421847    8
# center_coord = (latitude, longitude)
# city_coord = (latitude_2, longitude_2)
# coord_distance = distance.distance(center_coord, city_coord).miles

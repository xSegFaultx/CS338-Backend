from bs4 import BeautifulSoup
import requests
import unicodedata

# Movie URL
url = "https://www.the-numbers.com/movies/#tab=year"

# To fix 403 problem
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
# Request and extract the text part 
source = requests.get(url, headers=headers).text

# Using BeautifulSoup to convert text into a BeautifulSoup object
soup = BeautifulSoup(source, 'lxml')

# Find all popular movies
def find_all_movie():
    # Init variables
    movies = {}
    movie_name = False
    curr_year = None
    end_year = 1899

    # For each of the td tag in the HTML file
    for data in soup.find_all("td"):
        try:
            # Check whether the data we have is a year or movie name
            if data.b.a.text.isdigit():
                curr_year = int(data.b.a.text)
                movie_name = True
            elif movie_name:
                movies[curr_year] = unicodedata.normalize("NFKD", data.b.a.text).strip()
                movie_name = False
                # We reach the end
                if curr_year == end_year:
                    break

        except:
            continue

    return movies


def find_movie(year:int):
    match_year = False

    # For each of the td tag in the HTML file
    for data in soup.find_all("td"):
        try:
            # Check if we find the year that we try to search
            if data.b.a.text.isdigit() and int(data.b.a.text) == year:
                match_year = True
            elif match_year:
                return unicodedata.normalize("NFKD", data.b.a.text).strip()
        except:
            continue
    return None
movie = find_movie(1968)



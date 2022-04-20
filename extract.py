from util import *
import requests
import os

num2themes = ['music', 'movies', 'sports', 'fashion', 'food', 'technology']
themes2num = {}
for index, theme in enumerate(num2themes):
    themes2num[theme] = index
theme_query = [r'most popular music genre in {}s',
               r'most influential movies in {}s',
               r'sports moments in {}s',
               r'fashion show in {}s',
               r'most famous food in {}s',
               r'technology in {}s'
               ]


def get_theme_image(theme, birth_year):
    decade = get_decade(int(birth_year)) + 20
    theme_num = themes2num[theme]
    query = "_".join(theme_query[theme_num].format(decade).split())
    image_link = query2image(query)
    response = requests.get(image_link)
    if response.status_code != 200:
        return -1
    if not os.path.exists('./images'):
        os.makedirs('./images')
    with open("./images/theme.png", 'wb') as image_file:
        image_file.write(response.content)
    return 0


# testing
get_theme_image('music', '1995')

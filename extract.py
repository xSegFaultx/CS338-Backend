from util import *

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
    query = theme_query[theme_num].format(decade)
    return query2image(query)




import requests
from bs4 import BeautifulSoup
# ca_movie_urls = ["http://www.fantasy-sky.com/ContentList.aspx?section=002&category=0020{}".format(i) for i in range(1, 5)]

# response = requests.get(ca_movie_urls, cookies={'COOKIE_LANGUAGE': 'en'})
# soup = BeautifulSoup(response.text)
# movie_titles = [i.text for i in soup.select(".movies-name")]
# print(movie_titles)


requests_url = "http://www.fantasy-sky.com/ContentList.aspx"
en_cookie = {
    'COOKIE_LANGUAGE': 'en'
}
movie_name_cs = '.movies-name'
ca_movie_title = []
for i in range(1, 5):
    query_string_paramenters = {
        'section': '002',
        'category': '0020{}'.format(i)
    }
    response = requests.get(requests_url, params=query_string_paramenters, cookies=en_cookie)
    soup = BeautifulSoup(response.text)
    movie_name = [e.text for e in soup.select(movie_name_cs)]
    ca_movie_title += movie_name

print(ca_movie_title)
print(len(ca_movie_title))


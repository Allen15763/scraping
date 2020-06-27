# !pip install -U BeautifulSoup4   !=給每一電腦能解讀
#html scraping
import requests
from bs4 import BeautifulSoup


def get_moive_data(moive_url):

    movie_title_cs = 'h1'
    movie_poster_cs = '.poster img'
    movie_rating_cs = 'strong span'
    movie_genre_cs = '.subtext a'
    movie_cast_cs = '.primary_photo+ td a' 
    response = requests.get(moive_url)
    response_text = response.text  #<class 'str'>
    soup = BeautifulSoup(response_text, "html.parser") #換成soup type  <class 'bs4.BeautifulSoup'> html段for移除警告
    moive_title = soup.select(movie_title_cs)[0].text.replace('\xa0', ' ').strip()
    moive_poster = soup.select(movie_poster_cs)[0].get('src')
    moive_rating = float(soup.select(movie_rating_cs)[0].text)
    moive_genre = [e.text for e in soup.select(movie_genre_cs)]
    moive_release_date = moive_genre.pop()
    moive_cast = [e.text.strip() for e in soup.select(movie_cast_cs)]
    moive_data = {
        'moiveTitle' : moive_title,
        'moivePoster' : moive_poster,
        'moiveRatinf' : moive_rating,
        'moiveGenre' : moive_genre,
        'moiveCast'    : moive_cast
    }
    return moive_data

print(get_moive_data("https://www.imdb.com/title/tt7286456"))



#command
# print(soup.find("h1"))
# print(type(soup.find("h1")))
# print(soup.find("h1").text)
# print(soup.select("strong span"))
# print(float(soup.select("strong span")[0].text))

#response
# <h1 class="">復仇者聯盟：終局之戰 <span id="titleYear">(<a href="/year/2019/">2019</a>)</span> </h1>
# <class 'bs4.element.Tag'>
# 復仇者聯盟：終局之戰 (2019) 
# [<span itemprop="ratingValue">8.5</span>]
# 8.5

# command
# print(len(soup.find_all("img")))
# print(soup.find_all("img")[2])
# print(soup.find_all("img")[2].get("alt"))
# print(soup.find_all("img")[2].get("src"))

# response
# <img class="pro_logo" src="https://m.media-amazon.com/images/G/01/imdb/IMDbConsumerSiteProTitleViews/images/logo/pro_logo_dark-3176609149._CB455053166_.png"/>
# None
# https://m.media-amazon.com/images/G/01/imdb/IMDbConsumerSiteProTitleViews/images/logo/pro_logo_dark-3176609149._CB455053166_.png
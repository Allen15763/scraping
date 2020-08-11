# !pip install -U BeautifulSoup4   !=給每一電腦能解讀
#html scraping
import requests
from bs4 import BeautifulSoup

def get_movie_data(search_movie_title):
    result_text_cs = '.result_text > a'
    movie_title_cs = 'h1'
    movie_poster_cs = '.poster img'
    movie_rating_cs = 'strong span'
    movie_genre_cs = '.subtext a'
    movie_cast_cs = '.primary_photo+ td a' 
    # 1st request and parse: movie_url

    query_string_parameters = {
        'q': search_movie_title,
        'ref_': 'nv_sr_sm'
    }
    request_url = 'https://www.imdb.com/find'
    response = requests.get(request_url, params=query_string_parameters)
    soup = BeautifulSoup(response.text, "html.parser") #其資料型態</a> </td> <td class="result_text"> <a href="/title/tt7286456/?ref_=fn_al_tt_1" >Joker</a>
    result_text_hrefs = [e.get('href') for e in soup.select(result_text_cs)] #取得搜尋結果，print得知相近者為list中第一項
    movie_href = result_text_hrefs[0]
    movie_url = 'https://www.imdb.com' + movie_href # = movie_url = 'https//www.imdb.com{}'.format(movie_href) 

    # 2nd request and parse:movie_data
    response_data = requests.get(movie_url)
    response_text = response_data.text  #<class 'str'>
    soup = BeautifulSoup(response_text, "html.parser") #換成soup type  <class 'bs4.BeautifulSoup'> html段for移除警告
    movie_title = soup.select(movie_title_cs)[0].text.replace('\xa0', ' ').strip()
    movie_poster = soup.select(movie_poster_cs)[0].get('src')
    movie_rating = float(soup.select(movie_rating_cs)[0].text)
    movie_genre = [e.text for e in soup.select(movie_genre_cs)]
    movie_release_date = movie_genre.pop()
    movie_cast = [e.text.strip() for e in soup.select(movie_cast_cs)]
    movie_data = {
        'movieTitle' : movie_title,
        'moviePoster' : movie_poster,
        'movieRatinf' : movie_rating,
        'movieGenre' : movie_genre,
        'movieCast'    : movie_cast
    }
    return movie_data

print(get_movie_data('avengers: endgame'))
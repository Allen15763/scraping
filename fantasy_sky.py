
import requests
from bs4 import BeautifulSoup
import pandas as pd
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
    ca_movie_title += movie_name #避免用append造成重複巢狀

print(ca_movie_title)
print(len(ca_movie_title))

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
        's': 'tt',
        'ttype': 'ft',
        'ref_': 'fn_ft'
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
        'movieRating' : movie_rating,
        'movieGenre' : movie_genre,
        'movieCast'    : movie_cast
    }
    return movie_data

ca_imdb_movie_data =[]
for ca_movie in ca_movie_title:
    try:
        imdb_movie_data = get_movie_data(ca_movie)
        ca_imdb_movie_data.append(imdb_movie_data)
        imdb_movie_title = imdb_movie_data['movieTitle']
        imdb_movie_rating = imdb_movie_data['movieRating']
        print('{} 的IMDB評等為 {}'.format(imdb_movie_title, imdb_movie_rating))
    except:
        print('在擷取 {} 的電影資訊時產生錯誤'.format(ca_movie))

movie_titles, movie_ratings =[], []
for movie_data in ca_imdb_movie_data:
    movie_titles.append(movie_data['movieTitle'])
    movie_ratings.append(movie_data['movieRating'])
max_movie_rating = max(movie_ratings)
print(max_movie_rating)
best_rated_indice = []
for idx, rating in enumerate(movie_ratings):
    if rating == max_movie_rating:
        print('位於 {} 位置的平等是最高的'.format(idx))
        best_rated_indice.append(idx)
best_movie_index = best_rated_indice[0]
print(movie_titles[best_movie_index])

#pd.DataFrame(ca_imdb_movie_data)
ca_movie_df = pd.DataFrame()
ca_movie_df['movie_title'] = movie_titles  #這邊直接帶入是字典的值
ca_movie_df['movie_rating'] = movie_ratings
print(ca_movie_df.sort_values('movie_rating', ascending=False))
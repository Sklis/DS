import os
import streamlit as st
from dotenv import load_dotenv
from typing import List, Set, Optional, Any
from api.omdb import OMDBApi
from recsys import ContentBaseRecSys

TOP_K = 5
load_dotenv()

API_KEY = os.getenv("API_KEY")
MOVIES = os.getenv("MOVIES")
DISTANCE = os.getenv("DISTANCE")
# print("250",MOVIES)

omdbapi = OMDBApi(API_KEY)

recsys = ContentBaseRecSys(
    movies_dataset_filepath=MOVIES,
    distance_filepath=DISTANCE,
)


st.sidebar.title("Краткое руководство пользование сервисом")
st.sidebar.info(
    """
    1. Выберите  фильм.
    2. Выберите интересующий жанр фильма
    3. Выберите желаемый рейтинг фильма (1 до 10) 
    4. Нажмите кнопку "Показать рекомендации"
    5. Смотрите рекомендации
    """
)


st.sidebar.info(
    """
    e-mail: bav-td@yandex.ru,
    arrecsus@student.21-school.ru
    Intensive Parallel 21 TGU_DS_0423(DS. 103)
    Tribe Mercury
    08.08.2023
    """  
)    


st.markdown(
    """
    <style>
    body {
        background-color: #FF00BF;
    }
    h1 {
        color: #0022FF;
        text-align: center;
    }
    .btn-primary {
        background-color: #FAF600;
        color: #F01088;
    }    
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='text-align: center; color: green;'>Сервис рекомендации фильмов </h1>",
    unsafe_allow_html=True)

selected_movie = st.selectbox(
    "Выберите фильм:",
    recsys.get_title()
)
#  -----------------
poster = omdbapi.get_posters([selected_movie]) 
st.image(poster[0])
# -----------------------------------
selected_genre = st.selectbox('Фильтр по жанру', ['', *recsys.get_genres()])
selected_rating = st.text_input('Фильтр по рейтингу')

if selected_rating:
    try:
        selected_rating = float(selected_rating)
        if selected_rating < 0 or selected_rating > 10:
            st.warning('Введи число от 0 до 10')
            selected_rating = 0.0
    except ValueError:
        selected_rating = 0.0
        st.warning('Введи число от 0 до 10 ')
else:
    selected_rating = 0.0

if st.button('Показать рекомендации', key='show_recommendation', help='Click to show recommendations', 
             on_click=None, args=None, kwargs=None):
    st.write("Рекомендуемые фильмы:")
    if selected_genre or selected_rating:
        filtered_movies = recsys.filter_movies(genres=selected_genre, rating=float(selected_rating))
        recommended_movie_names = recsys.recommendation(selected_movie, top_k=TOP_K, movies=filtered_movies)
    else:
        recommended_movie_names = recsys.recommendation(selected_movie, top_k=TOP_K)
    if len(recommended_movie_names) == 0:
        st.subheader("Фильмы не найдены:((()))")
    else:
        if len(recommended_movie_names) < 5:
            top_k = len(recommended_movie_names)
        else:
            top_k = TOP_K
        recommended_movie_posters = omdbapi.get_posters(recommended_movie_names)
        movies_col = st.columns(top_k)

        for index, col in enumerate(movies_col):
            with col:
                st.subheader(recommended_movie_names[index])
                st.image(recommended_movie_posters[index])
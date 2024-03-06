import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=6e83e12a0e7302a71237990ef196ec4f".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data["poster_path"]


def recommend(movie, recommend_movie_posters=None):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movie_list:
        # fetch poster from api
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


movies_dict = pickle.load(open("movie_dict.pkl","rb"))
# movies_dict = movies_dict["title"].values
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl","rb"))

st.title("Movie Recommender System")
selected_movie = st.selectbox(
    'Type or select a movie from the dropdown',
    # ('Email', 'Home phone', 'Mobile phone'))
    movies["title"].values)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)

    col1, col2, col3,col4,col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])


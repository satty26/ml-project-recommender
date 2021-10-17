import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=a4ed6b9a006c448d9b382bd6a5e764fa&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    rec_movies = []
    rec_posters = []
    movie_index = movies[movies['title'] == movie].index[0]
    similar_movies = sorted(list(enumerate(sim[movie_index])),reverse=True,key=lambda x:x[1])[1:6]
    for i in similar_movies:
        movie_id = movies.iloc[i[0]].movie_id
        rec_posters.append(fetch_poster(movie_id))
        rec_movies.append(movies.iloc[i[0]].title)
    return rec_movies,rec_posters

movies_list = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_list)

sim = pickle.load(open('sim.pkl','rb'))
st.title('Movie Recommender System')

selected_movie = st.selectbox('Search the movie you wish to find similar movies to', movies['title'].values)

if st.button('Recommend'):
    recs,recs_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recs[0])
        st.image(recs_posters[0])
    with col2:
        st.text(recs[1])
        st.image(recs_posters[1])
    with col3:
        st.text(recs[2])
        st.image(recs_posters[2])
    with col4:
        st.text(recs[3])
        st.image(recs_posters[3])
    with col5:
        st.text(recs[4])
        st.image(recs_posters[4])


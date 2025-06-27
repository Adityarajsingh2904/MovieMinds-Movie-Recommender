import pickle
import streamlit as st
import requests
import os


# Load API key from environment or Streamlit secrets
TMDB_API_KEY = os.getenv("TMDB_API_KEY") or st.secrets.get("TMDB_API_KEY", None)
if not TMDB_API_KEY:
    st.error("TMDB_API_KEY not set. Set it as an environment variable or in .streamlit/secrets.toml.")
    st.stop()

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/200x300?text=No+Image"

    data = response.json()
    poster_path = data.get("poster_path")
    if not poster_path:
        return "https://via.placeholder.com/200x300?text=No+Image"

    return f"https://image.tmdb.org/t/p/w500/{poster_path}"


def recommend(movie):
    if movie not in movies["title"].values:
        st.error("Selected movie not found in the dataset.")
        return [], []

    index = movies[movies["title"] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1],
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)


    return recommended_movie_names, recommended_movie_posters


# UI
st.header("🎬 Movie Recommender System")

model_dir = "model"
movie_file = os.path.join(model_dir, "movie_list.pkl")
sim_file = os.path.join(model_dir, "similarity.pkl")

if os.path.exists(movie_file) and os.path.exists(sim_file):
    movies = pickle.load(open(movie_file, "rb"))
    similarity = pickle.load(open(sim_file, "rb"))
else:
    st.error("Model files not found. Ensure movie_list.pkl and similarity.pkl exist in the 'model' folder.")
    st.stop()

movie_list = movies["title"].values
selected_movie = st.selectbox("🎥 Type or select a movie", movie_list)

if st.button("Show Recommendation"):
    names, posters = recommend(selected_movie)
    if names and posters:
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])

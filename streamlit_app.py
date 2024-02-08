import pandas as pd
import streamlit as st
import pickle
import requests

# Set page configuration
st.set_page_config(
    page_title='CineSelect',
    page_icon=':clapper:',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# Add custom CSS to set the background color to black and customize fonts and colors
st.markdown(
    """
    <style>
    body {
        background-color: #000000; /* Set background color to black, change to #0000FF for blue */
        color: #000000; /* Set text color to white */
        font-family: 'Arial', sans-serif;
        background-image: url('https://example.com/your-background-image.jpg'); /* Add your background image URL here */
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .st-eb {
        color: #FFD700;  /* Set button text color to gold */
    }
    </style>
    """,
    unsafe_allow_html=True
)
def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=c182c97b3388df4f39fe9ba74b8fa29a&append_to_response=videos'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w342/" + data['poster_path']  # Reduced poster size


def recommend(selected_movie):
    movie_index = movie[movie['title'] == selected_movie].index[0]
    distances = similars[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movie_posters = []  # Corrected variable name
    for i in movies_list:
        movie_id = movie.iloc[i[0]].movie_id
        recommended_movies.append(movie.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movie_posters  # Corrected return values


# Load data from pickle files
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movie = pd.DataFrame(movie_dict)
similars = pickle.load(open('similars.pkl', 'rb'))


# Title and description
st.title('Movie Recommender')
st.write("Discover movies similar to the ones you love! Enter the name of a movie, and we'll recommend similar ones.")


# Select a movie from the dropdown
selected_movie_name = st.selectbox('Select a movie', movie['title'].values, help="Choose a movie for recommendations", key="movie_dropdown")

# Create a button to recommend movies
if st.button("Recommend!", key="recommend_button"):
    st.subheader('Recommended Movies:')
    st.write("Please wait while we find movies similar to '{}'...".format(selected_movie_name))

    # Perform recommendations
    names, posters = recommend(selected_movie_name)

    # Center-align text
    st.text(" ")  # Add some space

    col1, col2, col3, col4, col5 = st.columns(5)

    for i in range(len(posters)):
        if i % 5 == 0:
            with col1:
                st.image(posters[i], caption=f"{names[i]}", width=300, use_column_width=True)
        elif i % 5 == 1:
            with col2:
                st.image(posters[i], caption=f"{names[i]}", width=200, use_column_width=True)
        elif i % 5 == 2:
            with col3:
                st.image(posters[i], caption=f"{names[i]}", width=200, use_column_width=True)
        elif i % 5 == 3:
            with col4:
                st.image(posters[i], caption=f"{names[i]}", width=200, use_column_width=True)
        elif i % 5 == 4:
            with col5:
                st.image(posters[i], caption=f"{names[i]}", width=200, use_column_width=True)

import streamlit as st
import pickle
import pandas as pd
import requests

# Load movie data and similarity matrix
movies_list = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_list)  # Assuming movies_list is a dictionary with 'title' key
similarity = pickle.load(open('similarity.pkl', 'rb'))
api_key = '913e725d220d2e9fdc97751685922966'

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #FF4B4B, #FF6A6A);
            color: #fff;
            font-family: 'Arial', sans-serif;
        }

        .title {
            font-size: 50px;
            font-weight: bold;
            text-align: center;
            color: #FFF;
            text-shadow: 3px 3px 5px rgba(0,0,0,0.3);
            margin-top: 30px;
        }

        .subtitle {
            font-size: 26px;
            text-align: center;
            margin-top: -20px;
            color: #f0f0f0;
        }

        .recommend-text {
            color: #FFEB3B;
            font-weight: bold;
            font-size: 20px;
            text-align: center;
            margin-top: 30px;
        }

        .movie-title {
            color: #FF4B4B;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            margin-top: 10px;
        }

        .contact {
            font-size: 18px;
            text-align: center;
            margin-top: 50px;
            color: #f0f0f0;
            font-weight: bold;
        }

        .contact a {
            color: #FFEB3B;
            text-decoration: none;
            padding: 5px;
            font-weight: bold;
        }

        .contact a:hover {
            color: #FF6A6A;
        }

        .movie-card {
            background-color: rgba(255, 255, 255, 0.3);
            border-radius: 10px;
            overflow: hidden;
            width: 180px;
            text-align: center;
            padding: 10px;
            transition: transform 0.3s ease;
            margin: 0 15px;  /* Added margin between each card */
        }

        .movie-card:hover {
            transform: scale(1.05);
            box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
        }

        .movie-card img {
            width: 100%;
            border-radius: 5px;
        }

        .movie-container {
            display: flex;
            justify-content: center;
            gap: 20px;  /* Adjusted gap for spacing between posters */
            flex-wrap: wrap;  /* Allow wrapping to the next row if there are more posters */
            margin-top: 30px;
        }
    </style>
""", unsafe_allow_html=True)


def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}')
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return f'https://image.tmdb.org/t/p/w185/{data["poster_path"]}'
    else:
        return "https://via.placeholder.com/185"  # Placeholder if no poster is found


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Assuming 'movie_id' column exists in `movies`
        recommended.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended, recommended_posters


# Streamlit app title
st.markdown('<h1 class="title">🎬 Movie Recommender</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Get Personalized Movie Recommendations Instantly</p>', unsafe_allow_html=True)

# Dropdown for movie selection
selected_movie_name = st.selectbox("Select a Movie", movies['title'].values)

# Button to get recommendations
if st.button('Get Recommendations'):
    names, posters = recommend(selected_movie_name)
    st.markdown('<p class="recommend-text">Top Movie Recommendations for You:</p>', unsafe_allow_html=True)

    # Create a flex container to display the movies horizontally
    st.markdown('<div class="movie-container">', unsafe_allow_html=True)

    # Display the movie posters with spacing
    for idx in range(len(names)):
        st.markdown(f"""
            <div class="movie-card">
                <img src="{posters[idx]}" alt="{names[idx]}">
                <p class="movie-title">{names[idx]}</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Select a movie and click on 'Get Recommendations' to discover new movies!")

# Contact information section
st.markdown("""
    <div class="contact">
        <p>Stay Connected: <br>
            <a href="https://www.facebook.com/wail.luffi" target="_blank">Facebook</a> | 
            <a href="https://github.com/zerarka-mohmamed-wail" target="_blank">GitHub</a>
        </p>
    </div>
""", unsafe_allow_html=True)

import streamlit as st
import pickle
import pandas as pd
import requests
from datetime import datetime
import urllib.parse
import gdown
import os

# --- Authentication check ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- Simulate DOB from Aadhaar ---
def dob(aadhaar_number):
    fake_dob = "2005-04-01"  # Placeholder
    return datetime.strptime(fake_dob, "%Y-%m-%d")

# --- Fetch movie poster + rating from TMDB ---
def fetch_movie_data(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url).json()
        poster_url = f"https://image.tmdb.org/t/p/w500/{data['poster_path']}" if data.get('poster_path') else "https://via.placeholder.com/200"
        rating = round(data.get('vote_average', 0), 1)
        return poster_url, rating
    except:
        return "https://via.placeholder.com/200", 0

# recommend function
def recommend(movie):
    if movie not in movies['title'].values:
        st.error("Movie not found! Please select a valid movie.")
        return [], [], [], []

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies, posters, links, ratings = [], [], [], []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster, rating = fetch_movie_data(movie_id)

        recommended_movies.append(title)
        posters.append(poster)
        links.append(f"https://www.themoviedb.org/movie/{movie_id}")
        ratings.append(rating)

    return recommended_movies, posters, links, ratings

# --- Load data from Google Drive ---
movie_dict_url = 'https://drive.google.com/uc?export=download&id=1CPfXFmfsF-hOihHBbFTdlkFUOVPoyrcY'
similarity_url = 'https://drive.google.com/uc?export=download&id=1D0er_IZCdzK4QRbPXIlOQ4iDCIGzEMTW'

movie_dict_path = 'movie_dict.pkl'
similarity_path = 'similarity.pkl'

try:
    if not os.path.exists(movie_dict_path):
        gdown.download(movie_dict_url, movie_dict_path, quiet=False)
    if not os.path.exists(similarity_path):
        gdown.download(similarity_url, similarity_path, quiet=False)

    movie_dict = pickle.load(open(movie_dict_path, 'rb'))
    similarity = pickle.load(open(similarity_path, 'rb'))
    movies = pd.DataFrame(movie_dict)
except Exception as e:
    st.error(f"Error loading movie data: {e}")
    movies = pd.DataFrame()

# Age verification
if not st.session_state["authenticated"]:
    st.image("https://wes.eletsonline.com/assets/images/haridwar-logo-500.png", caption="Haridwar University", width=200)
    st.markdown('<h1 style="color:blue;">Haridwar University</h1>', unsafe_allow_html=True)
    st.markdown('<h1 style="color:red; font-size:30px;">End-To-End Project</h1>', unsafe_allow_html=True)
    st.markdown('<h1 style="color:green; font-size:20px;">Movie Recommender System</h1>', unsafe_allow_html=True)
    st.text("Please verify your age before proceeding.")

    aadhaar_number = st.text_input("Enter your Aadhaar Card Number:", max_chars=12)
    if st.button("Verify Age"):
        if len(aadhaar_number) == 12 and aadhaar_number.isdigit():
            dob_value = dob(aadhaar_number)
            age = (datetime.today() - dob_value).days // 365

            if age >= 18:
                st.success("Access Granted!")
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error(f"Access Denied! You are only {age} years old. You must be 18+ to access this system.")
        else:
            st.warning("Invalid Aadhaar Number! Please enter a valid 12-digit Aadhaar number.")

    st.markdown("""
        <div style="color:black; font-size:10px; margin:0; padding:0;">
            Developed By: SHIV SONKER and SHOBHIT SAURABH [B.TECH CSE 2ND YEAR]
        </div>
        <div style="color:black; font-size:15px; margin:0; padding:0;">
            Mentored By:
        </div>
        <div style="color:black; font-size:15px; margin:0; padding:0;">
            MRINALINEE SINGH (MAM)
        </div>
        <div style="color:black; font-size:15px; margin:0; padding:0;">
            VIKALP TYAGI (SIR)
        </div>
        <div style="color:black; font-size:15px; margin:0; padding:0;">
            NARAYAN JEE (SIR)
        </div>
        <div style="color:black; font-size:10px; margin:0; padding:0;">
            DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING
        </div>
    """, unsafe_allow_html=True)

else:
    st.image("https://wes.eletsonline.com/assets/images/haridwar-logo-500.png", caption="Haridwar University", width=200)
    st.markdown('<h1 style="color:blue;">Haridwar University</h1>', unsafe_allow_html=True)
    st.markdown('<h1 style="color:red; font-size:30px;">End-To-End Project</h1>', unsafe_allow_html=True)
    st.markdown('<h1 style="color:green;">Movie Recommendation System</h1>', unsafe_allow_html=True)

    st.markdown("""
        <style>
        .stSelectbox>div>div>div>div {
            color: green;
            font-size: 18px;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    if not movies.empty:
        selected_movie_name = st.selectbox('🎬 Select a movie to get recommendations:', movies['title'].values)
        mood = st.selectbox("🎭 Choose your mood (optional):", ["None", "Happy", "Sad","Thriller"])

        if st.button('Recommend'):
            names, posters, links, ratings = recommend(selected_movie_name)

            if names:
                st.markdown("<h3 style='color:purple;'>Recommended Movies:</h3>", unsafe_allow_html=True)

                for row in range(2):
                    cols = st.columns(5)
                    for i, col in enumerate(cols):
                        idx = row * 5 + i
                        if idx < len(names):
                            with col:
                                st.image(posters[idx], width=180)
                                st.markdown(f"<p style='font-size:16px; font-weight:bold;'>{names[idx]}</p>", unsafe_allow_html=True)
                                st.markdown(f"<p style='font-size:14px;'>⭐ Rating: {ratings[idx]}</p>", unsafe_allow_html=True)
                                st.markdown(f"[More Info]({links[idx]})", unsafe_allow_html=True)
                                st.caption(f"🤖 Why recommended: Similar to '{selected_movie_name}'")

                total_time = len(names) * 2
                st.info(f"🕒 Estimated watch time: {total_time} hours")

                share_text = f"Check out these movies I found using this awesome recommender: {', '.join(names)}"
                share_link = f"https://api.whatsapp.com/send?text={urllib.parse.quote(share_text)}"
                st.markdown(f"[📤 Share on WhatsApp]({share_link})", unsafe_allow_html=True)
            else:
                st.warning("No movies recommended. Try selecting a different movie.")

    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()

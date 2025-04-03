import streamlit as st
import pickle
import pandas as pd
import requests
from datetime import datetime

# for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False


# date of birth find karne ke liye
def dob(aadhaar_number):
    fdob = "2005-04-01"  # fake dob, format specify karne ke liye
    return datetime.strptime(fdob, "%Y-%m-%d")


def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url).json()
        if 'poster_path' in data and data['poster_path']:
            return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    except:
        return None  # agar api nhi find out hua to none return karega
    return None


def recommend(movie):
    if movie not in movies['title'].values:
        st.error("Movie not found! Please select a valid movie.")
        return [], [], []

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]

    if not movies_list:
        st.error("No recommendations available!")
        return [], [], []

    recommended_movies, recommended_movies_posters, movie_links = [], [], []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id) or "No poster available")
        movie_links.append(f"https://www.themoviedb.org/movie/{movie_id}")

    return recommended_movies, recommended_movies_posters, movie_links


# uploaded files se data read kerega
try:
    movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movies = pd.DataFrame(movie_dict)
except Exception as e:
    st.error(f"Error loading movie data: {e}")
    movies = pd.DataFrame()
#  Navigation
if not st.session_state["authenticated"]:
    # page 1 pr age verification ke liye
    st.image("https://wes.eletsonline.com/assets/images/haridwar-logo-500.png", caption="Haridwar University",
             width=200)
    st.markdown('<h1 style="color:blue;">Haridwar University</h1>', unsafe_allow_html=True)
    st.markdown('<h1 style="color:red; font-size:30px;">End To End Project</h1>', unsafe_allow_html=True)
    st.markdown('<h1 style="color:black; font-size:20px;">Home Page</h1>', unsafe_allow_html=True)
    st.markdown('<h1 style="color:green; font-size:20px;">Movie Recommender System</h1>', unsafe_allow_html=True)
    st.text("First Verify Your Age")

    # aadhar card se age validate karne ke liye
    aadhaar_number = st.text_input("Enter your Aadhaar Card Number:", max_chars=12)
    if st.button("Verify Age"):
        if len(aadhaar_number) == 12 and aadhaar_number.isdigit():
            dob = dob(aadhaar_number)
            age = (datetime.today() - dob).days // 365

            if age >= 18:
                st.text("Access Granted!")
                st.session_state["authenticated"] = True  # ye user ko validation dega
                st.rerun()
            else:
                st.error(f"Access Denied! You are only {age} years old. You must be 18+ to access this system.")
        else:
            st.warning("Invalid Aadhaar Number! Please enter a valid 12-digit Aadhaar number.")

else:
    st.image("https://wes.eletsonline.com/assets/images/haridwar-logo-500.png", caption="Haridwar University",
             width=300)
    st.markdown('<h1 style="color:blue;">Haridwar University</h1>', unsafe_allow_html=True)
    st.markdown('<h1 style="color:red; font-size:30px;">End To End Project</h1>', unsafe_allow_html=True)
    st.markdown('<h1 style="color:green;">Movie Recommendation System</h1>', unsafe_allow_html=True)

    if not movies.empty:
        selected_movie_name = st.selectbox('Select a movie to get recommendations:', movies['title'].values)

        if st.button('Recommend'):
            names, posters, links = recommend(selected_movie_name)

            if names:
                cols = st.columns(len(names))
                                                   #name and poster fetch karne ke liye
                for i, col in enumerate(cols):
                    with col:
                        st.text(names[i])
                        st.markdown(f"[More Info]({links[i]})")
                        if posters[i] != "No poster available":
                            st.image(posters[i], width=200)
                        else:
                            st.text("No poster available")

            else:
                st.warning("No movies recommended. Try selecting a different movie.")

    if st.button("Logout"):
        st.session_state["authenticated"] = False  # Logout function
        st.rerun()  # fir se start karega




# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 11:53:00 2025

@author: Akriti
    """
import streamlit as st
import os
import pandas as pd
from PIL import Image

# ---- Page Config ----
st.set_page_config(page_title="Moodify 🎵", layout="wide", initial_sidebar_state="expanded")

# ---- Load Dataset ----
data_path = "data1.csv"  # Ensure this file exists in the correct path
if os.path.exists(data_path):
    data = pd.read_csv(data_path)
else:
    st.error("⚠️ Error: Dataset not found! Please check the file path.")
    data = pd.DataFrame()

# ---- Custom CSS for Dark Theme with Neon Accents ----
st.markdown(
    """
    <style>
        body {
            background-color: #121212;
            color: #EAEAEA;
        }
        .block-container {
            padding: 32px !important;
        }
        .stApp {
            background-color: #121212;
        }
        .stSidebar {
            background-color: #1E1E1E !important;
            padding: 20px !important;
            font-size: 20px !important;
            color: #EAEAEA !important;
            border-right: 2px solid #444;
        }
        .stSidebar div, .stSidebar label, .stSidebar span {
            color: #EAEAEA !important;
            font-size: 18px !important;
        }
        h1, h2, h3, h4, h5, h6 {
            font-size: 30px !important;
            font-weight: bold !important;
            color: #00A6FF;
            text-align: center;
        }
        .stButton>button {
            font-size: 18px !important;
            font-weight: bold;
            background: linear-gradient(45deg, #00A6FF, #8A2BE2);
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            margin: 5px;
            width: 100%;
            border: none;
        }
        .stButton>button:hover {
            background: linear-gradient(45deg, #FF007F, #8A2BE2);
            box-shadow: 0px 0px 10px #FF007F;
        }
        .top-song-container {
            background-color: #1E1E1E;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            box-shadow: 0px 0px 10px #00A6FF;
        }
    </style>
    """, unsafe_allow_html=True
)

# ---- Sidebar Navigation ----
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Recommendations", "Top Charts", "Music Hub", "Podcast"])

# ---- Sidebar Filters ----
st.sidebar.title("🎭 Filters")
mood = st.sidebar.selectbox("Select Mood", ["All", "Happy", "Sad", "Energetic", "Calm"])
year = st.sidebar.slider("Select Year", int(data["year"].min()), int(data["year"].max()), step=1)
popularity = st.sidebar.slider("Minimum Popularity", 0, 100, 50)

# ---- Home Page Content ----
st.markdown("""
    <h1 style="text-align: center; font-size: 50px; font-weight: bold; color: #8A2BE2;">
        🎶 Moodify - Home Page
    </h1>
""", unsafe_allow_html=True)

st.markdown("<p style='color: #EAEAEA; font-size: 24px; font-weight: bold; text-align: center;'>Welcome to Moodify, where music meets emotion!</p>", unsafe_allow_html=True)

# ---- Search Bar ----
st.markdown("""
    <h2 style='color: #FF007F; font-weight: bold; font-size: 26px; text-align: center;'>🔍 Search for a song or artist</h2>
""", unsafe_allow_html=True)

search_query = st.text_input("Search by song or artist", "").strip()

# Filter dataset based on search query (only song name and artist)
if search_query:
    search_results = data[
        data["name"].str.contains(search_query, case=False, na=False) |
        data["artists"].str.contains(search_query, case=False, na=False)
    ].nlargest(5, 'popularity')  # Get top 5 most popular results
else:
    search_results = pd.DataFrame()  # Empty DataFrame if no search query

# ---- Display Top 5 Search Results ----
st.markdown("<h3 style='color: #00A6FF; text-align: center;'>🎶 Top 5 Search Results</h3>", unsafe_allow_html=True)

if not search_results.empty:
    for _, row in search_results.iterrows():
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 10px; background-color: #1E1E1E; margin-bottom: 10px;">
            <p style="color: #FF007F; font-size: 20px; font-weight: bold;">🎵 {row['name']}</p>
            <p style="color: #EAEAEA;">🎤 {row['artists']}</p>
            <p style="color: #8A2BE2;">🔥 Popularity: {row['popularity']}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("<p style='color: #FF007F; text-align: center;'>No matching results found.</p>", unsafe_allow_html=True)

# ---- Genre Selection ----
st.markdown("""
    <h2 style='color: #EAEAEA; font-weight: bold; font-size: 28px; text-align: left;'>🎵 Explore your genres</h2>
""", unsafe_allow_html=True)

if not data.empty and 'genre' in data.columns:
    genres = data['genre'].unique()
    cols = st.columns(len(genres))
    
    selected_genre = None
    for i, genre in enumerate(genres):
        with cols[i]:
            if st.button(genre, key=genre):
                selected_genre = genre
                
    if selected_genre:
        st.markdown(f"<h3 style='color:#FF007F; font-size: 24px; font-weight: bold;'>🎧 Top Song in {selected_genre}</h3>", unsafe_allow_html=True)
        top_song = data[data['genre'] == selected_genre].nlargest(1, 'popularity')
        for _, row in top_song.iterrows():
            st.markdown(f"<p style='color: #FFFFFF; font-size: 20px;'><b>🎵 {row['name']}</b> - {row['artists']}</p>", unsafe_allow_html=True)
            st.markdown(f"""
    <style>
        .pearl-white {{
            color: #FDFDFD; /* Pearl White color */
        }}
    </style>
    <b class='pearl-white'>🎤 Artist:</b> <span class='pearl-white'>{row['artists']}</span><br>
    <b class='pearl-white'>📅 Release Year:</b> <span class='pearl-white'>{row['year']}</span><br>
    <b class='pearl-white'>🔥 Popularity:</b> <span class='pearl-white'>{row['popularity']}</span>
""", unsafe_allow_html=True)

            st.audio("Sample.mp3")


# ---- Next in Queue (3 songs) ----
        next_songs = data[data['genre'] == selected_genre].nlargest(4, 'popularity').iloc[1:4]  # Get next 3 songs
        
        if not next_songs.empty:
            st.markdown(f"<h3 style='color:#00A6FF; font-size: 22px; font-weight: bold;'>🎶 Next in Queue for {selected_genre}</h3>", unsafe_allow_html=True)
            for _, song in next_songs.iterrows():
                st.markdown(f"""
                <div style="padding: 10px; border-radius: 10px; background-color: #1E1E1E; margin-bottom: 10px;">
                    <p style="color: #FF007F; font-size: 18px; font-weight: bold;">🎵 {song['name']}</p>
                    <p style="color: #EAEAEA;">🎤 {song['artists']}</p>
                    <p style="color: #8A2BE2;">🔥 Popularity: {song['popularity']}</p>
                </div>
                """, unsafe_allow_html=True)

# ---- Display Filtered Songs ----
# Center the icon above the title
st.image("SM.png", width=30)
st.markdown("""
    <div style="text-align: center;">
        <h1 style="color: #00A6FF; margin-top: 5px;"> 🎧Moodify Song Recommendations</h1>
    </div>
    <br><br> <!-- Adding space between the title and song list -->
""", unsafe_allow_html=True)


#st.image("SM.png", width=30)
#st.markdown("<h1 style='color: #00A6FF; display: inline;'>🎧 Moodify Song Recommendations</h1>", unsafe_allow_html=True)
#<br><br> <!-- Adding space between the title and song list -->
#""", unsafe_allow_html=True)

filtered_data = data[data["popularity"] >= popularity]
filtered_data = filtered_data[filtered_data["year"] == year]

if not filtered_data.empty:
    for _, row in filtered_data.head(10).iterrows():
        col1, col2 = st.columns([1, 4])  

        with col1:
            st.image("DP.png", width=120)

        with col2:
            st.markdown(f"<div class='song-title' style='color: #FF007F; font-size: 22px; font-weight: bold;'>{row['name']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='song-artist' style='color: #EAEAEA;'>🎤 {row['artists']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='song-popularity' style='color: #8A2BE2;'>🔥 Popularity: {row['popularity']}</div>", unsafe_allow_html=True)

        st.markdown("<hr style='border-color: #00A6FF;'>", unsafe_allow_html=True)
else:
    st.write("No songs found.")

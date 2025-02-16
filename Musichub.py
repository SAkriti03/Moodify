# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 19:45:42 2025

@author: Akriti
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ---- Page Configuration ----
st.set_page_config(page_title="🎵 Moodify - Music Hub & Recommendations", layout="wide")

# ---- Initialize Session State ----
if "playlist" not in st.session_state:
    st.session_state["playlist"] = []
if "queue" not in st.session_state:
    st.session_state["queue"] = []
if "user_id" not in st.session_state:
    st.session_state["user_id"] = "guest"
if "mood_history" not in st.session_state:
    st.session_state["mood_history"] = []


# ---- Custom Styling ----
st.markdown(
    """
    <style>
        body { background-color: #121212; color: #EAEAEA; }
        .stApp { background-color: #121212; }
        .stTitle { color: #8A2BE2; font-size: 36px; text-align: center; font-weight: bold; }
        .stDataFrame { background-color: #1e1e1e; color: #EAEAEA; border-radius: 10px; }
        table { width: 100%; border-radius: 10px; }
        th { background-color: #FF007F; color: white; font-size: 18px; padding: 10px; text-align: left; }
        td { background-color: #222; color: #EAEAEA; padding: 10px; font-size: 16px; border-bottom: 1px solid #444; }
        .stRedText { color: #8A2BE2; font-size: 22px; font-weight: bold; }
        .custom-label { color: #FF007F; font-size: 20px; font-weight: bold; display: block; margin-bottom: 5px; }
        .stButton > button { background: linear-gradient(to right, #00A6FF, #8A2BE2); color: white; border: none; padding: 10px; border-radius: 5px; }
        .stButton > button:hover { background: linear-gradient(to right, #FF007F, #8A2BE2); box-shadow: 0px 0px 10px #FF007F; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Load Dataset ----
@st.cache_data
def load_data():
    return pd.read_csv("data1.csv")

data = load_data()

st.markdown("<h1 class='stTitle'>🔥 Moodify - Music Hub</h1>", unsafe_allow_html=True)

# ---- Smart Playlist Generator ----
# ---- Smart Playlist Generator ----
if st.button("🎵 Generate Smart Playlist"):
    if not data.empty:
        recommendations = data.sample(5)[["name", "artists", "year", "popularity"]]
        st.markdown("<h3 class='stRedText'>🎶 Smart Playlist Recommendations:</h3>", unsafe_allow_html=True)
        st.dataframe(recommendations.set_index("name").style.set_properties(**{'background-color': '#1e1e1e', 'color': '#EAEAEA'}))
# ---- Mood-Based Song Recommendations ----
st.markdown("<p class='custom-label'>🎧 Select Mood:</p>", unsafe_allow_html=True)
mood = st.selectbox(" ", ["Chill", "Happy", "Energetic", "Sad"], label_visibility="collapsed")

mood_mapping = {
    "Chill": (0.2, 0.5),
    "Happy": (0.6, 1.0),
    "Energetic": (0.7, 1.0),
    "Sad": (0.0, 0.3)
}

if {"valence", "energy"}.issubset(data.columns):
    filtered_songs = data[
        (data["valence"].between(mood_mapping[mood][0], mood_mapping[mood][1])) & 
        (data["energy"] > 0.5)
    ].sample(min(5, len(data)))

    st.markdown(f"<h3 class='stRedText'>🎶 {mood} Mood Songs:</h3>", unsafe_allow_html=True)
    st.dataframe(filtered_songs[['name', 'artists', 'year', 'popularity', 'valence']]
                 .style.set_properties(**{'background-color': '#1e1e1e', 'color': '#EAEAEA'}))
    
# ---- Mood Tracking ----
if st.session_state["mood_history"]:
    st.markdown("<h3 class='stRedText'>📈 Mood Trend</h3>", unsafe_allow_html=True)
    
    mood_mapping = {"Chill": 1, "Happy": 2, "Energetic": 3, "Sad": 0}
    mood_numeric = [mood_mapping[m] for m in st.session_state["mood_history"]]
    
    mood_df = pd.DataFrame({"Mood": mood_numeric, "Time": range(1, len(mood_numeric) + 1)})
    fig, ax = plt.subplots()
    ax.plot(mood_df["Time"], mood_df["Mood"], marker='o', linestyle='-', color='#FF007F')
    ax.set_xlabel("Time")
    ax.set_ylabel("Mood Level")
    ax.set_title("Your Mood Trend Over Time")
    
    # Fix: Ensure yticks and labels are properly set
    yticks = list(mood_mapping.values())
    ax.set_yticks(yticks)
    ax.set_yticklabels([key for key in mood_mapping])  # Set proper y-axis labels
    plt.xticks(rotation=45)
    st.pyplot(fig)
# ---- Trending Songs & Featured Artists ----
col1, col2 = st.columns(2)
with col1:
    st.markdown("<h3 class='stRedText'>🔥 Trending Songs</h3>", unsafe_allow_html=True)
    top_songs = data.sort_values(by="popularity", ascending=False).head(10)
    st.dataframe(top_songs[["name", "artists", "year", "popularity"]]
                 .style.set_properties(**{'background-color': '#1e1e1e', 'color': '#EAEAEA'}))

with col2:
    st.markdown("<h3 class='stRedText'>🌟 Featured Artists</h3>", unsafe_allow_html=True)
    top_artists = data["artists"].explode().value_counts().head(5)
    st.write(top_artists)

# ---- User Playlist Section ----
st.markdown("<h1 class='stTitle'>🎵 My Playlist</h1>", unsafe_allow_html=True)

st.markdown("<span class='custom-label'>🎼 Enter Song Name</span>", unsafe_allow_html=True)
song_name = st.text_input("", key="song_name")

st.markdown("<span class='custom-label'>🎤 Enter Artist Name</span>", unsafe_allow_html=True)
artist_name = st.text_input("", key="artist_name")

if st.button("➕ Add to Playlist"):
    if song_name and artist_name:
        st.session_state["playlist"].append({"Song": song_name, "Artist": artist_name})
        st.success(f"Added '{song_name}' by {artist_name} to your playlist!")

st.markdown("<h3 class='stRedText'>🎶 Your Playlist:</h3>", unsafe_allow_html=True)
st.dataframe(pd.DataFrame(st.session_state["playlist"]).style.set_properties(**{'background-color': '#1e1e1e', 'color': '#EAEAEA'}))
# ---- Social Sharing ----
if st.button("🔗 Share My Playlist"):
    st.text(f"Share this playlist link: moodify.com/playlist/{st.session_state['user_id']}")


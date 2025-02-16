# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 00:03:06 2025

@author: Akriti
"""
import streamlit as st

# ---- Page Configuration ----
st.set_page_config(page_title="🎥 Watch Video - Moodify", layout="wide")

# Custom CSS for black background
st.markdown(
    """
    <style>
        body {
            background-color: black;
            color: white;
        }
        .block-container {
            padding: 20px !important;
            background-color: black;
        }
        h1 {
            text-align: center;
            color: red;
        }
    </style>
    """, unsafe_allow_html=True
)

st.markdown("<h1>🎥 Enjoy the Music Videos</h1>", unsafe_allow_html=True)

# List of YouTube video URLs
videos = [
    "https://www.youtube.com/watch?v=LhYRD0XmzOU",
    "https://www.youtube.com/watch?v=edIctUyd4RQ",
    "https://www.youtube.com/watch?v=8_hc2WqYqT8",
    "https://www.youtube.com/watch?v=Tuw8hxrFBH8",
    "https://www.youtube.com/watch?v=UwGSgJytufY",
    "https://www.youtube.com/watch?v=DEo742BF8eo",
    "https://www.youtube.com/watch?v=ZNsPYmkSPeI",
    "https://www.youtube.com/watch?v=W0DM5lcj6mw"
    
]

# Display videos in a grid (3 per row)
for i in range(0, len(videos), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(videos):
            with cols[j]:
                st.video(videos[i + j])
#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(
    page_title="Movie Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

def set_theme(is_dark_mode):
    if is_dark_mode:
        css = """
        <style>
        .stApp {
            background-color: #111111;
            color: #EEEEEE;
        }

        div[data-testid="stToggle"] * {
            color: #EEEEEE !important;
        }
        </style>
        """
    else:
        css = """
        <style>
        .stApp {
            background-color: #FFFFFF;
            color: #000000;
        }

        div[data-testid="stToggle"] * {
            color: #000000 !important;
        }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

# --- Title and Theming Toggle Aligned Top-Right ---
col_left, col_right = st.columns([3, 1])

with col_left:
    st.title("🎥 Movie Dashboard")

with col_right:
    st.markdown(
        "<p style='font-size:16px; margin-bottom:0.5rem;'>🌓 <strong>Select Theme</strong></p>",
        unsafe_allow_html=True
    )
    is_dark_mode = st.toggle("🌙 Dark Mode", value=False)

# Apply theme
set_theme(is_dark_mode)

# --- Layout ---
col1, col2 = st.columns([1, 2])
col3, col4 = st.columns([2, 2])
col5, col6 = st.columns([1, 1])

# --- Top Donuts Section (Average Rating and Movie Count) ---
with col1:
    st.subheader("Average Rating")
    st.empty()  # Placeholder for donut chart

    st.subheader("Movie Count")
    st.empty()  # Placeholder for donut chart

# --- Yearly Trend Section (Movie Count + Avg Rating over Time) ---
with col2:
    st.subheader("Movie Trends Over Time")
    st.empty()  # Placeholder for line/bar chart

# --- Interactive Genre Panel ---
with col3:
    st.subheader("🎬 Genre Explorer")
    selected_genre = st.selectbox("Select Genre", options=[])  # To be populated dynamically
    st.markdown("**Most Rated Movie:** [Placeholder]")
    st.markdown("**Average Rating:** [Placeholder]")

# --- Top Movies Section ---
with col4:
    st.subheader("⭐ Top Rated Movies")
    st.empty()  # Placeholder for horizontal bar chart or stat display


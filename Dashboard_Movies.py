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

# --- Custom Theme Styling ---
def set_theme(mode):
    if mode == "Dark Mode":
        css = """
        <style>
        body, .stApp {
            background-color: #111111;
            color: #EEEEEE;
        }
        .stRadio > div[role="radiogroup"] > label {
            color: #EEEEEE !important;
            opacity: 1.0 !important;
        }
        </style>
        """
    else:
        css = """
        <style>
        body, .stApp {
            background-color: #FFFFFF;
            color: #000000;
        }
        .stRadio > div[role="radiogroup"] > label {
            color: #000000 !important;
            opacity: 1.0 !important;
        }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

# --- Title and Theming Toggle ---
st.title("🎥 Movie Data Visualisation Dashboard")
theme = st.radio("Select Theme", ["Light Mode", "Dark Mode"], horizontal=True)
set_theme(theme)

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


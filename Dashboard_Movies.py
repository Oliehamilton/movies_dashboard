#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Set Up Data ---
movies_df = pd.read_csv('movies_cleaned_3.csv')
@st.cache_data
def load_data():
    return pd.read_csv("movies_cleaned_3.csv")

movies_df = load_data()

# --- Page Config ---
st.set_page_config(
    page_title="Movie Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Title ---
st.title("🎥 Movie Dashboard")

# --- Force Dark Mode Styling ---
dark_mode_css = """
<style>
body {
    background-color: #111111;
    color: #EEEEEE;
}
.stApp {
    background-color: #111111;
}
</style>
"""
st.markdown(dark_mode_css, unsafe_allow_html=True)

# --- Layout ---
col1, col2 = st.columns([1, 2])
col3, col4 = st.columns([2, 2])
col5, col6 = st.columns([1, 1])

# --- Interactive Year Selection ---
years = ['All'] + sorted(movies_df['release_year_from_date'].dropna().unique().astype(int).tolist())
selected_year = st.selectbox("Filter by Year", years)

# --- Filter the Data ---
if selected_year == 'All':
    filtered_df = movies_df.copy()
else:
    filtered_df = movies_df[movies_df['release_year_from_date'] == selected_year]

# --- Calculate Metrics ---
average_rating = round(filtered_df['mean_rating'].mean(), 2)
movie_count = filtered_df['movieId'].nunique()

# --- Top Donuts Section ---
with col1:
    st.subheader("Average Rating")
    fig_rating = go.Figure(data=[go.Pie(
        labels=["Rating", ""],
        values=[average_rating, 5 - average_rating],
        hole=0.7,
        marker_colors=['#66C2A5', '#222222'],
        textinfo='none'
    )])
    fig_rating.update_layout(
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        height=200,
        annotations=[dict(text=f"{average_rating}", x=0.5, y=0.5, font_size=24, showarrow=False)]
    )
    st.plotly_chart(fig_rating, use_container_width=True)

    st.subheader("Movie Count")
    fig_count = go.Figure(data=[go.Pie(
        labels=["Movies", ""],
        values=[movie_count, movie_count * 0.1],  # Just to create the visual donut
        hole=0.7,
        marker_colors=['#FC8D62', '#222222'],
        textinfo='none'
    )])
    fig_count.update_layout(
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        height=200,
        annotations=[dict(text=str(movie_count), x=0.5, y=0.5, font_size=24, showarrow=False)]
    )
    st.plotly_chart(fig_count, use_container_width=True)
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


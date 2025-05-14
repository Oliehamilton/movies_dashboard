#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

# --- Top Donuts Section (Average Rating and Movie Count) ---
average_rating = 4.0
movie_count = 5

# --- Donut Chart for Average Rating ---
with col1:
    st.subheader("Average Rating")
    fig_rating = go.Figure(data=[go.Pie(
        values=[average_rating, 5 - average_rating],
        hole=0.6,
        marker_colors=["#FFD700", "#333333"],
        textinfo='none'
    )])
    fig_rating.update_layout(
        showlegend=False,
        annotations=[dict(text=f"{average_rating:.1f}", x=0.5, y=0.5, font_size=20, showarrow=False)],
        margin=dict(t=0, b=0, l=0, r=0),
        height=200
    )
    st.plotly_chart(fig_rating, use_container_width=True)

# --- Donut Chart for Movie Count ---
with col1:
    st.subheader("Movie Count")
    fig_count = go.Figure(data=[go.Pie(
        values=[movie_count, max(10, movie_count + 1) - movie_count],
        hole=0.6,
        marker_colors=["#1f77b4", "#333333"],
        textinfo='none'
    )])
    fig_count.update_layout(
        showlegend=False,
        annotations=[dict(text=str(movie_count), x=0.5, y=0.5, font_size=20, showarrow=False)],
        margin=dict(t=0, b=0, l=0, r=0),
        height=200
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


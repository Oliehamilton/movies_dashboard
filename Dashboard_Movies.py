#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Cache Data Load ---
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

# --- Title ---
st.title("🎥 Movie Dashboard")

# --- Interactive Year Selection ---
years = ['All'] + sorted(movies_df['release_year_from_date'].dropna().unique().astype(int).tolist(), reverse=True)

# --- Layout ---
col1, col2 = st.columns([1, 2])
with col1:
    selected_year = st.selectbox("Filter by Year", years)
col3, col4 = st.columns([2, 2])

# --- Filter the Data ---
if selected_year == 'All':
    filtered_df = movies_df.copy()
else:
    filtered_df = movies_df[movies_df['release_year_from_date'] == selected_year]

# --- Calculate Metrics ---
average_rating = round(filtered_df['mean_rating'].mean(), 2)
movie_count = filtered_df['movieId'].nunique()

# --- Donut Charts (Average Rating & Movie Count) ---
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
        values=[movie_count, movie_count * 0.1],  # Fake offset for donut effect
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

    # Year range slider
    all_years = movies_df['release_year_from_date'].dropna().astype(int)
    year_min, year_max = int(all_years.min()), int(all_years.max())
    selected_range = st.slider("Select Year Range", year_min, year_max, (year_min, year_max))

    # Filter and summarise data
    df_filtered = movies_df[
        (movies_df['release_year_from_date'].astype(int) >= selected_range[0]) &
        (movies_df['release_year_from_date'].astype(int) <= selected_range[1])
    ]

    summary = (
        df_filtered.groupby('release_year_from_date')
        .agg(movie_count=('title', 'count'), average_rating=('mean_rating', 'mean'))
        .reset_index()
        .rename(columns={'release_year_from_date': 'Year'})
        .sort_values('Year')
    )

    # Create base figure
    fig = go.Figure()

    # Add bar chart for movie count
    fig.add_trace(go.Bar(
        x=summary['Year'],
        y=summary['movie_count'],
        name='Number of Movies',
        marker_color='#7BAFD4',
        yaxis='y1',
        hovertemplate='Year: %{x}<br>Movies: %{y}<extra></extra>'
    ))

    # Add line chart for average rating
    fig.add_trace(go.Scatter(
        x=summary['Year'],
        y=summary['average_rating'],
        name='Average Rating',
        mode='lines+markers',
        line=dict(color='#9F7AEA', width=2),
        yaxis='y2',
        hovertemplate='Year: %{x}<br>Avg Rating: %{y:.2f}<extra></extra>'
    ))

    # Update layout for dual axis
    fig.update_layout(
        title='Movie Count and Average Rating per Year',
        xaxis=dict(title='Year'),
        yaxis=dict(
            title='Number of Movies',
            titlefont=dict(color='#7BAFD4'),
            tickfont=dict(color='#7BAFD4')
        ),
        yaxis2=dict(
            title='Average Rating',
            overlaying='y',
            side='right',
            titlefont=dict(color='#9F7AEA'),
            tickfont=dict(color='#9F7AEA'),
            range=[0, 10]
        ),
        legend=dict(x=0.01, y=0.99),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#EEEEEE'),
        margin=dict(t=60, b=40, l=60, r=60)
    )

    st.plotly_chart(fig, use_container_width=True)

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


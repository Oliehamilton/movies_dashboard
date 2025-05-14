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

# --- Cache Data Load ---
@st.cache_data
def load_data():
    return pd.read_csv("movies_cleaned_3.csv")

movies_df = load_data()

# --- Plot 3 Genre Frequency Preparation ---

# Identify genre columns
genre_cols = movies_df.columns[9:27]

# Summarise genre counts per year in long format
df_genre_year = movies_df[['release_year_from_date'] + list(genre_cols)].copy()

genre_year_counts = (
    df_genre_year
    .groupby('release_year_from_date')[genre_cols]
    .sum()
    .reset_index()
    .melt(id_vars='release_year_from_date', var_name='genre_columns', value_name='movie_count')
    .rename(columns={'release_year_from_date': 'year'})
)

# Ensure numeric types
genre_year_counts['year'] = genre_year_counts['year'].astype(int)
genre_year_counts['movie_count'] = genre_year_counts['movie_count'].astype(int)

# Genre colour palette
genre_colors = {
    "Drama": "#4E79A7", "Comedy": "#F28E2B", "Action": "#E15759", "Adventure": "#76B7B2",
    "Thriller": "#59A14F", "Horror": "#EDC948", "Romance": "#B07AA1", "Crime": "#FF9DA7",
    "Fantasy": "#9C755F", "Animation": "#BAB0AC", "Musical": "#8CD17D", "Sci-Fi": "#499894",
    "Children": "#D37295", "Mystery": "#FABFD2", "War": "#B6992D", "Film-Noir": "#5C5C5C"
}

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
    st.subheader("Movie Production and Quality Over Time")

    # Radio toggle
    metric = st.radio("Select Metric", ["Movie Count per Year", "Average Rating per Year"], horizontal=True)

    # Prepare summary
    summary = (
        movies_df.dropna(subset=['release_year_from_date', 'mean_rating'])
        .copy()
    )
    summary['Year'] = summary['release_year_from_date'].astype(int)

    grouped = (
        summary.groupby('Year')
        .agg(movie_count=('title', 'count'), average_rating=('mean_rating', 'mean'))
        .reset_index()
        .sort_values('Year')
    )

    # Plot
    fig = go.Figure()

    if metric == "Movie Count per Year":
        fig.add_trace(go.Bar(
            x=grouped['Year'],
            y=grouped['movie_count'],
            name='Number of Movies',
            marker_color='#7BAFD4',
            hovertemplate='Year: %{x}<br>Movies: %{y}<extra></extra>'
        ))
        fig.update_layout(
            title='Movie Count per Year',
            yaxis_title='Number of Movies'
        )

    else:
        fig.add_trace(go.Scatter(
            x=grouped['Year'],
            y=grouped['average_rating'],
            name='Average Rating',
            mode='lines+markers',
            line=dict(color='#9F7AEA', width=2),
            hovertemplate='Year: %{x}<br>Avg Rating: %{y:.2f}<extra></extra>'
        ))
        fig.update_layout(
            title='Average Rating per Year',
            yaxis_title='Average Rating',
            #yaxis=dict(range=[0, 10])
        )

    # Universal layout tweaks
    fig.update_layout(
        xaxis_title='Year',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#EEEEEE'),
        margin=dict(t=60, b=40, l=60, r=60)
    )

    st.plotly_chart(fig, use_container_width=True)

# --- Interactive Genre Panel ---
with col3:
    st.subheader("🎬 Movie Trends Over Time")

    # Define year range from the data
    min_year = genre_year_counts['year'].min()
    max_year = genre_year_counts['year'].max()

    # Year slider
    selected_year = st.slider("Select Year", min_year, max_year, max_year)

    # Filter and summarise top 10 genres up to selected year
    filtered = genre_year_counts[genre_year_counts['year'] <= selected_year]
    summary = (
        filtered.groupby('genre_columns')['movie_count']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .head(10)
    )

    # Plot bar chart with custom genre colours
    fig = px.bar(
        summary,
        x='movie_count',
        y='genre_columns',
        orientation='h',
        title=f"Top 10 Genres Up to {selected_year}",
        color='genre_columns',
        color_discrete_map=genre_colors,
        labels={'movie_count': 'Number of Movies', 'genre_columns': 'Genre'}
    )

    fig.update_layout(
        yaxis=dict(categoryorder='total ascending'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#EEEEEE'),
        margin=dict(t=60, b=40, l=60, r=60)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Genre dropdown populated from top genres at selected year
    #st.markdown("#### ℹ️ Genre Info")
    #selected_genre = st.selectbox("Select Genre", options=summary['genre_columns'].tolist())

# --- Top Movies Section ---
with col4:
    st.subheader("⭐ Top Rated Movies")

    # --- Year Block Setup ---
    min_year = int(movies_df['release_year_from_date'].min())
    max_year = int(movies_df['release_year_from_date'].max())

    year_blocks = [(start, start + 4) for start in range(min_year, max_year + 1, 5)]
    block_labels = [f"{start}–{end}" for start, end in year_blocks]
    label_to_range = dict(zip(block_labels, year_blocks))

    # Add "All Years" at the end
    block_labels.append("All Years")

    # --- Selector ---
    selected_label = st.radio("Select 5-Year Block", block_labels, horizontal=True)

    if selected_label == "All Years":
        filtered = movies_df[movies_df['rating_count'] >= 30]
    else:
        year_start, year_end = label_to_range[selected_label]
        filtered = movies_df[
            (movies_df['release_year_from_date'] >= year_start) &
            (movies_df['release_year_from_date'] <= year_end) &
            (movies_df['rating_count'] >= 30)
        ]

    # --- Top Movies ---
    top_movies = filtered.sort_values('mean_rating', ascending=False).head(5)

    if top_movies.empty:
        st.warning(f"No movies found with ≥30 ratings in {selected_label}.")
    else:
        pastel_palette = [
            "#bcb6f6", "#a0c4ff", "#ffd6a5", "#caffbf", "#ffadad",
            "#fdffb6", "#d0bdf4", "#ffc6ff", "#9bf6ff", "#bdb2ff"
        ]
        color_map = {title: pastel_palette[i % len(pastel_palette)] for i, title in enumerate(top_movies['title'])}

        fig = px.bar(
            top_movies.sort_values('mean_rating'),
            x='mean_rating',
            y='title',
            orientation='h',
            title=f"Top 10 Movies by Average Rating ({selected_label})",
            labels={'mean_rating': 'Average Rating', 'title': 'Movie'},
            color='title',  # use each movie as a color group
            color_discrete_map=color_map
        )

        fig.update_traces(marker_line_color='black', marker_line_width=1)
        fig.update_layout(
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#EEEEEE'),
            xaxis=dict(range=[0, 5]),
            yaxis=dict(categoryorder='total ascending'),
            margin=dict(t=60, b=40, l=60, r=60)
        )

        st.plotly_chart(fig, use_container_width=True)

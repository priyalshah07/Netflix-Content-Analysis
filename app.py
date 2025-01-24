#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 21:12:12 2025

@author: priyalshah
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="Netflix Content Analysis",
    page_icon="🎬",
    layout="wide"
)

# Title and description
st.title("Netflix Content Analysis - Data Analysis and Visualization")
st.markdown("An analysis of Netflix's movie catalog exploring various trends and patterns")

# Loading the data
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_data.csv")
    return df

try:
    netflix_df = load_data()
    st.success("Data loaded successfully!")
except:
    st.error("Error: Please ensure netflix_data.csv is in the same directory")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")

# Year range filter
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(netflix_df['release_year'].min()),
    max_value=int(netflix_df['release_year'].max()),
    value=(1990, 2023)
)

# Genre filter
genres = ['All'] + list(netflix_df['genre'].unique())
selected_genre = st.sidebar.selectbox("Select Genre", genres)

# Filter data based on selections
filtered_df = netflix_df[
    (netflix_df['release_year'].between(year_range[0], year_range[1]))
]

if selected_genre != 'All':
    filtered_df = filtered_df[filtered_df['genre'] == selected_genre]

# Main content
st.header("Data Analysis")

# Create two columns for layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Movie Duration Distribution")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.histplot(data=filtered_df[filtered_df['type'] == 'Movie'], 
                x='duration', 
                bins=30, 
                color='lightblue')
    plt.title('Distribution of Movie Durations')
    plt.xlabel('Duration (minutes)')
    plt.ylabel('Count')
    st.pyplot(fig1)
    plt.close()

with col2:
    st.subheader("Content by Genre")
    genre_counts = filtered_df['genre'].value_counts()
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    genre_counts.plot(kind='bar')
    plt.title('Content Distribution by Genre')
    plt.xlabel('Genre')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

# Top 10 countries producing content
st.subheader("Top 10 Countries Producing Content")
country_counts = filtered_df['country'].value_counts().head(10)
total_content = country_counts.sum()
percentages = (country_counts / total_content) * 100

fig3, ax3 = plt.subplots(figsize=(12, 6))
bars = plt.bar(country_counts.index, country_counts.values)
plt.title('Top 10 Countries Producing Content')
plt.xlabel('Country')
plt.ylabel('Number of Titles')
plt.xticks(rotation=45, ha='right')

# Add percentage labels
for bar in bars:
    height = bar.get_height()
    percentage = (height / total_content) * 100
    plt.text(bar.get_x() + bar.get_width()/2, height,
             f'{percentage:.1f}%',
             ha='center', va='bottom')

plt.tight_layout()
st.pyplot(fig3)
plt.close()

# Distribution of movie durations across genres
st.subheader("Movie Duration Distribution by Genre")
fig4, ax4 = plt.subplots(figsize=(12, 6))
sns.boxplot(x='genre', y='duration', data=filtered_df[filtered_df['type'] == 'Movie'])
plt.xticks(rotation=90)
plt.title('Distribution of Movie Durations by Genre')
plt.xlabel('Genre')
plt.ylabel('Duration (minutes)')
plt.tight_layout()
st.pyplot(fig4)
plt.close()

# Scatter plot of release year vs cast size
st.subheader("Relationship between Release Year and Cast Size")
filtered_df['cast_count'] = filtered_df['cast'].str.split(',').str.len()

fig5, ax5 = plt.subplots(figsize=(12, 6))
plt.scatter(filtered_df['release_year'], filtered_df['cast_count'], alpha=0.5)
plt.title('Relationship between Release Year and Cast Size')
plt.xlabel('Release Year')
plt.ylabel('Number of Cast Members')
plt.grid(True)

# Calculate and display correlation coefficient
correlation = filtered_df['release_year'].corr(filtered_df['cast_count'])
plt.text(0.95, 0.95, f'Correlation: {correlation:.2f}', 
         transform=plt.gca().transAxes, ha='right', va='top')

plt.tight_layout()
st.pyplot(fig5)
plt.close()

# Word cloud of movie titles
st.subheader("Common Words in Movie Titles")
selected_genre_titles = filtered_df[filtered_df['genre'] == selected_genre]['title'] if selected_genre != 'All' else filtered_df['title']

try:
    from wordcloud import WordCloud
    
    # Create word cloud
    wordcloud = WordCloud(width=800, height=400, 
                         background_color='white').generate(' '.join(selected_genre_titles))
    
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Most Common Words in {selected_genre if selected_genre != "All" else "All"} Movie Titles')
    st.pyplot(fig4)
    plt.close()
except ImportError:
    st.warning("WordCloud package not installed. Please install it to see the word cloud visualization.")

# Data table
st.subheader("Raw Data Explorer")
st.dataframe(filtered_df)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit")

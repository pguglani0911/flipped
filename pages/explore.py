import streamlit as st
import pandas as pd
import os
import ast
import kagglehub

# 1. DATA LOADING (Cached for speed)
@st.cache_data
def load_explore_data():
    # Download/Path setup
    path = kagglehub.dataset_download("pooriamst/best-books-ever-dataset")
    csv_path = os.path.join(path, "books_1.Best_Books_Ever.csv")
    
    # We only load what we need to keep the app fast
    df = pd.read_csv(csv_path, usecols=['title', 'author', 'rating', 'description', 'genres', 'coverImg'])
    
    # Clean genres from string "[Art, Fiction]" to a Python list
    df['genres_list'] = df['genres'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
    return df

books_df = load_explore_data()

# 2. HEADER
st.title(" Explore Books")
st.write("Browse the collection or search for your next favorite read.")

# 3. SEARCH & BROWSE UI
# We put these in columns to look like a pro search bar
col1, col2 = st.columns([2, 1])

with col1:
    search_query = st.text_input("🔍 Search by title or author", placeholder="e.g. The Great Gatsby")

with col2:
    # Get unique genres for the dropdown
    all_genres = sorted(list(set([genre for sublist in books_df['genres_list'] for genre in sublist])))
    selected_genre = st.selectbox("📖 Browse Genre", ["All"] + all_genres)

st.divider()

# 4. FILTERING LOGIC
filtered_df = books_df.copy()

# Filter by Search
if search_query:
    filtered_df = filtered_df[
        filtered_df['title'].str.contains(search_query, case=False, na=False) |
        filtered_df['author'].str.contains(search_query, case=False, na=False)
    ]

# Filter by Genre
if selected_genre != "All":
    filtered_df = filtered_df[filtered_df['genres_list'].apply(lambda x: selected_genre in x)]

# 5. DISPLAY RESULTS (Grid View)
st.write(f"Showing {min(len(filtered_df), 20)} of {len(filtered_df)} books")

# Show top 20 results to keep the page snappy
for idx, row in filtered_df.head(20).iterrows():
    with st.container(border=True):
        c1, c2 = st.columns([1, 4])
        with c1:
            st.image(row['coverImg'], use_container_width=True)
        with c2:
            st.subheader(row['title'])
            st.write(f"**{row['author']}** | {row['rating']} ⭐")
            st.caption(", ".join(row['genres_list'][:5])) # Show first 5 genres
            st.write(row['description'][:300] + "...")
            
            # THE ADD BUTTON
            if st.button("Add to TBR", key=f"exp_{idx}"):
                new_book = pd.DataFrame([{
                    "title": row['title'],
                    "author": row['author'],
                    "cover": row['coverImg'],
                    "status": "TBR",
                    "rating": 0,
                    "review": ""
                }])
                
                # Save to your CSV
                file_exists = os.path.exists("my_books.csv")
                new_book.to_csv("my_books.csv", mode='a', index=False, header=not file_exists)
                st.toast(f"Added {row['title']} to your TBR!")
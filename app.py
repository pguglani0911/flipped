import streamlit as st
import kagglehub
import pandas as pd
import os
import ast

# 1. SETUP & CONFIG (Must be the very first Streamlit command)
st.set_page_config(page_title="flipped", layout="wide")

st.title("flipped")

@st.cache_data
def load_data():
    path = kagglehub.dataset_download("pooriamst/best-books-ever-dataset")
    csv_path = os.path.join(path, "books_1.Best_Books_Ever.csv")
    df = pd.read_csv(csv_path, usecols=['title', 'author', 'rating', 'description', 'genres', 'coverImg'])
    df['genres_list'] = df['genres'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
    return df

books_df = load_data()

# 2. STATS DASHBOARD (Shows at the very top)
if os.path.exists("my_books.csv"):
    df_saved = pd.read_csv("my_books.csv")
    tbr_count = len(df_saved[df_saved['status'] == 'TBR'])
    read_count = len(df_saved[df_saved['status'] == 'Finished'])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Books Read", read_count)
    col2.metric("Want to Read", tbr_count)
    avg_rating = df_saved['rating'].mean() if 'rating' in df_saved and read_count > 0 else 0
    col3.metric("Avg Rating", f"{avg_rating:.1f} ⭐" if avg_rating > 0 else "N/A")
    st.divider()

# 3. SIDEBAR FILTERS
st.sidebar.title(" Filters")
all_genres = books_df['genres_list'].explode().value_counts()
top_genres = ["All Genres"] + all_genres.index[:50].tolist()
selected_genre = st.sidebar.selectbox("Genre", top_genres)

# 4. MAIN UI - SEARCH

search_query = st.text_input("Search 50k+ books...", placeholder="Type a title or author...")

# 5. FILTERING LOGIC
filtered_df = books_df.copy()
if selected_genre != "All Genres":
    filtered_df = filtered_df[filtered_df['genres_list'].apply(lambda x: selected_genre in x)]

if search_query:
    filtered_df = filtered_df[
        filtered_df['title'].str.contains(search_query, case=False, na=False) |
        filtered_df['author'].str.contains(search_query, case=False, na=False)
    ]

# 6. DISPLAY RESULTS & SAVE LOGIC
st.write(f"Found {len(filtered_df)} books")

for idx, row in filtered_df.head(15).iterrows():
    with st.container(border=True):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(row['coverImg'], use_container_width=True)
        with col2:
            st.subheader(row['title'])
            st.write(f"**{row['author']}** | {row['rating']} ⭐")
            st.write(row['description'][:250] + "...")
            
            # --- THE CORRECT SAVE LOGIC INSIDE THE LOOP ---
            if st.button("Add to TBR", key=f"add_{idx}"):
                new_book = {
                    "title": row['title'],
                    "author": row['author'],
                    "cover": row['coverImg'],
                    "status": "TBR",
                    "rating": 0
                }
                new_df = pd.DataFrame([new_book])
                
                # This creates the file if it doesn't exist, or appends if it does
                new_df.to_csv("my_books.csv", mode='a', index=False, header=not os.path.exists("my_books.csv"))
                st.success(f"Added {row['title']} to your shelf!")
                st.rerun() # Refresh to update the Stats Dashboard at the top!
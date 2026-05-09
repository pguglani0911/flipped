import streamlit as st
import pandas as pd
import os


st.title("flipped")
st.set_page_config(page_title="My Bookshelf", layout="wide")

st.title("My Bookshelf")

if os.path.exists("my_books.csv"):
    df = pd.read_csv("my_books.csv")
    finished_books = df[df['status'] == 'Finished'].copy()
    
    if not finished_books.empty:
        # --- SEARCH & STATS ---
        col_a, col_b = st.columns([3, 1])
        with col_a:
            shelf_search = st.text_input("🔍 Search your library...", placeholder="Title or Author")
        with col_b:
            st.metric("Books Completed", len(finished_books))
            
        if shelf_search:
            finished_books = finished_books[
                finished_books['title'].str.contains(shelf_search, case=False, na=False) |
                finished_books['author'].str.contains(shelf_search, case=False, na=False)
            ]

        st.divider()

        # --- THE GRID WITH REVIEWS ---
        cols = st.columns(3) 
        for idx, (_, row) in enumerate(finished_books.iterrows()):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.image(row['cover'], use_container_width=True)
                    st.subheader(row['title'])
                    st.write(f"**By:** {row['author']}")
                    
                    # Display Rating if it exists
                    rating = row.get('rating', 0)
                    st.write(f"Rating: {int(rating) * '⭐' if rating > 0 else 'Unrated'}")
                    
                    # THE REVIEW SECTION
                    # We use an expander so the review doesn't make the box too tall
                    with st.expander("📝 View My Review"):
                        review_text = row.get('review', "No review written yet.")
                        if pd.isna(review_text) or review_text == "":
                            st.info("You haven't written a review for this book yet.")
                        else:
                            st.write(f"*{review_text}*")
                            
    else:
        st.info("Your shelf is empty! Finish a book from your TBR list.")
else:
    st.warning("No library data found.")
import streamlit as st
import pandas as pd
from datetime import datetime
import os
import streamlit as st

st.title("flipped")
# --- INITIALIZATION SAFETY NET ---
if "search_results" not in st.session_state:
    st.session_state.search_results = [] # Initialize as empty list if it doesn't exist

st.title("Write a Review")

# 1. Load your existing data
if os.path.exists("my_books.csv"):
    df = pd.read_csv("my_books.csv")
    
    # Only show books that are currently marked as 'TBR'
    tbr_list = df[df['status'] == 'TBR']['title'].tolist()
    
    if tbr_list:
        # 2. Select Book to Review
        selected_book = st.selectbox("Which book did you finish?", tbr_list)
        
        # 3. Review Inputs
        col1, col2 = st.columns(2)
        with col1:
            finish_date = st.date_input("When did you finish it?", datetime.now())
        with col2:
            rating = st.slider("Rating", 1, 5, 3)
            
        review_text = st.text_area("What did you think?", placeholder="Write your review here...")
        is_reread = st.checkbox("Was this a reread?")

        if st.button("Post Review"):
            # 4. Update the CSV
            # Find the row for this book and update its status and add review info
            df.loc[df['title'] == selected_book, 'status'] = 'Finished'
            df.loc[df['title'] == selected_book, 'rating'] = rating
            df.loc[df['title'] == selected_book, 'review'] = review_text
            df.loc[df['title'] == selected_book, 'date'] = str(finish_date)
            
            df.to_csv("my_books.csv", index=False)
            st.balloons()
            st.success(f"Review for '{selected_book}' posted!")
    else:
        st.info("No books in your TBR! Go to the home page to add some.")
else:
    st.error("You haven't added any books yet!")
import streamlit as st
import pandas as pd
import os

st.title("flipped")
st.set_page_config(page_title="My TBR", layout="wide")
st.title(" My To-Be-Read List")

if os.path.exists("my_books.csv"):
    df = pd.read_csv("my_books.csv")
    
    # Filter for books that are still 'TBR'
    tbr_books = df[df['status'] == 'TBR']
    
    if not tbr_books.empty:
        cols = st.columns(4)
        for idx, (original_idx, row) in enumerate(tbr_books.iterrows()):
            with cols[idx % 4]:
                with st.container(border=True):
                    st.image(row['cover'], use_container_width=True)
                    st.write(f"**{row['title']}**")
                    st.caption(row['author'])
                    
                    # THE "MARK AS READ" BUTTON
                    if st.button("Mark as Read ✅", key=f"read_{original_idx}"):
                        # Update the status in the MAIN dataframe using the original index
                        df.at[original_idx, 'status'] = 'Finished'
                        
                        # Save the updated dataframe back to CSV
                        df.to_csv("my_books.csv", index=False)
                        
                        st.toast(f"Moved '{row['title']}' to Bookshelf!")
                        st.rerun() # Refresh page to move the book out of sight
    else:
        st.info("Your TBR list is empty! Add books from the Home page.")
else:
    st.warning("No library found yet.")
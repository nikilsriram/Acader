import streamlit as st

pg = st.navigation([
    st.Page("layout.py", title="Layout"),
    st.Page("frontend.py", title="Home", url_path="/frontend"),
    st.Page("test.py", title="Test", url_path='/test'),
    st.Page("flashcards.py", title="Flashcards", url_path="/flashcars")
])

pg.run()
import streamlit as st
from inject_analytics import inject_ga

st.set_page_config(
    page_title="Acader",
    page_icon="./gem.jpeg",  # Optional: adds a browser tab favicon
)
inject_ga()

pg = st.navigation([
    st.Page("layout.py", title="Layout"),
    st.Page("frontend.py", title="Home", url_path="/frontend"),
    st.Page("test.py", title="Test", url_path='/test'),
    st.Page("flashcards.py", title="Flashcards", url_path="/flashcars"),
    st.Page("loading.py", title="Loading", url_path="/loading"),
    st.Page("notes.py", title="Notes", url_path="/notes"),
    st.Page("app.py", title="Login", url_path="/login"),
    st.Page("aboutme.py", title="About Me", url_path="/aboutme"),
    st.Page("progresstracker.py", title="Progress Tracker", url_path="/progress"),
    st.Page("faq.py", title="Frequently Asked Questions", url_path="/faq"),
    st.Page("contact.py", title="Contact Us", url_path="/contact")
])

pg.run()
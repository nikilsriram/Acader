import os
import streamlit as st
import streamlit.components.v1 as components

# 1. Keep this at the absolute top so Streamlit reads it first
st.set_page_config(
    page_title="Acader",
    page_icon="./gem.jpeg", 
)

# 2. Pull your tracking ID from your Hyperlift Environment panel
ga_id = os.getenv("GA_TRACKING_ID", "G-H5SWDVDRZB")

if ga_id:
    # 3. This safely pushes the GA tracking script directly into the page rendering layer
    components.html(f"""
    <!-- Google Analytics -->
    <script async src="https://googletagmanager.com{ga_id}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{ga_id}');
    </script>
    """, height=0, width=0)

# 4. Your multi-page setup runs perfectly below
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

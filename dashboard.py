import streamlit as st

pg = st.navigation([
    st.Page("frontend.py", title="Home"),
    st.Page("output.py", title="Test"),
])

pg.run()
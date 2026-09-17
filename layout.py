import streamlit as st

# Load CSS
with open("style.css") as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Load HTML
with open("layout.html") as f:
    html = f.read()

st.html(html)
import base64
import streamlit as st

st.markdown("""
<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">
""", unsafe_allow_html=True)


st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

with open("style.css", "r", encoding="utf-8") as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

with open("hi.jpeg", "rb") as f:
    image = base64.b64encode(f.read()).decode()

with open("layout.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace('src="./hi.jpeg"', f'src="data:image/jpeg;base64,{image}"')

st.html(html)
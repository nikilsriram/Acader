import streamlit as st

st.write(st.session_state.notes)
st.page_link("app.py", label='go to app')
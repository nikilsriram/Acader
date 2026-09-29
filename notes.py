import streamlit as st
if not st.session_state.get("user_id"):
    st.warning("Please log in to view this page.")
    st.page_link("app.py", label="Go to Login")
    st.stop()  # Instantly halts execution of the rest of the page code


st.write(st.session_state.notes)
st.page_link("app.py", label='go to app')
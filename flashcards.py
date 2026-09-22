import streamlit as st

def show_my_flashcards(data):
    st.write("### Your Generated Flashcards:")

    for key in data:
        st.write(f"**Key:** {key}")
        st.write(f"Content: {data[key]}")
        st.markdown("---")


if "flashcards" in st.session_state:
    show_my_flashcards(st.session_state.flashcards)
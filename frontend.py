import streamlit as st
from main import generate_test_from_image, generate_flashcards_from_image, generate_notes_from_image
from flashcards import show_my_flashcards

st.title("Acader")

if "camera_active" not in st.session_state:
    st.session_state.camera_active = False


if st.button("Take a Photo"):
    st.session_state.camera_active = True


if st.session_state.camera_active:
    picture = st.camera_input("Take a picture")

    if picture:
        st.image(picture)

        if st.button("Generate Test using Photo"):
            result = generate_test_from_image(picture)
            st.write(result)
        
        if st.button("Generate Comprehensive Review Notes using Photo"):
            result = generate_notes_from_image(picture)
            st.write(result)


uploaded_file = st.file_uploader(
    "Upload your notes",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    st.image(uploaded_file)

    if st.button("Generate Test using Uploaded File"):
        result = generate_test_from_image(uploaded_file)
        st.write(result)

    if st.button("Generate Flashcards using Uploaded File"):
        result = generate_flashcards_from_image(uploaded_file)

        st.session_state.flashcards = result

        st.success("Flashcards generated!")


    if st.button("Generate Comprehensive Review Notes using Photo"):
                result = generate_notes_from_image(uploaded_file)
                st.write(result)
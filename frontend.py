import streamlit as st
from main import generate_test_from_image

st.title("Acader")

picture = st.camera_input(
    "Take a picture"
)

uploaded_file = st.file_uploader(
    "Upload your notes",
    type=["jpg", "jpeg", "png"]
)



if uploaded_file:
    st.image(uploaded_file)

    if st.button("Generate Test using Uploaded File"):
        result = generate_test_from_image(uploaded_file)
        st.write(result)

if picture:
    st.image(picture)

    if st.button("Generate Test using Photo"):
        result = generate_test_from_image(picture)
        st.write(result)
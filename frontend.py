import streamlit as st
from main import generate_test_from_image, generate_flashcards_from_image, generate_notes_from_image

if not st.session_state.get("user_id"):
    st.warning("Please log in to view this page.")
    st.page_link("app.py", label="Go to Login")
    st.stop()  # Instantly halts execution of the rest of the page code

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("app.py", label="Welcome", use_container_width=True)

with col2:
    st.page_link("frontend.py", label="Generator", use_container_width=True)

with col3:
    st.page_link("progresstracker.py", label="Progress Tracker", use_container_width=True)

st.divider()


st.markdown("""
<style>

.stApp {
    background-color: #000000;
    color: white;
}

.block-container {
    max-width: 1100px;
    padding-top: 5rem !important; /* Adjusted for navbar space */
    padding-bottom: 4rem;
}

header[data-testid="stHeader"] {
    z-index: 100 !important;
    background: transparent !important;
}

.acader-title {
    text-align: center;
    color: #b74b4b;
    font-size: 4.5rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
}

.acader-subtitle {
    text-align: center;
    color: #888888;
    font-size: 1.2rem;
    margin-bottom: 3rem;
}

.section-title {
    color: white;
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
}

.section-text {
    color: #888888;
    font-size: 1rem;
    margin-bottom: 1.2rem;
}

.stButton > button {
    background-color: #000000;
    color: #b74b4b;
    border: 2px solid #b74b4b;
    border-radius: 25px;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background-color: #b74b4b;
    color: #000000;
    border-color: #b74b4b;
    transform: translateY(-2px);
}

[data-testid="stFileUploader"] {
    background-color: #111111;
    border: 1px solid #333333;
    border-radius: 15px;
    padding: 15px;
    transition: 0.2s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: #b74b4b;
}

[data-testid="stCameraInput"] {
    background-color: #111111;
    border: 1px solid #333333;
    border-radius: 15px;
    padding: 15px;
}

[data-testid="stImage"] {
    border-radius: 15px;
    overflow: hidden;
}

hr {
    border-color: #222222 !important;
    margin: 2.5rem 0 !important;
}

[data-testid="stAlert"] {
    background-color: #111111;
    border: 1px solid #b74b4b;
    border-radius: 12px;
}

.navbar-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 70px;
    padding: 0 5%;
    background-color: #000000;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 999999;
    border-bottom: 1px solid #222222;
}

.navbar-container .logo {
    font-size: 2.2rem;
    color: #b74b4b;
    font-weight: 800;
    text-decoration: none;
    transition: 0.3s ease;
}

.navbar-container .logo:hover {
    transform: scale(1.05);
}

.navbar-container nav {
    display: flex;
    align-items: center;
    gap: 2rem;
}

.navbar-container nav a {
    font-size: 1.1rem;
    color: white;
    font-weight: 500;
    text-decoration: none;
    transition: 0.3s ease;
    border-bottom: 3px solid transparent;
    white-space: nowrap;
}

.navbar-container nav a:hover,
.navbar-container nav a.active {
    color: #b74b4b;
    border-bottom: 3px solid #b74b4b;
}

@media (max-width: 995px) {
    .navbar-container nav {
        display: none;
    }
}

[data-testid="stPageLink"] a {
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    color: #b74b4b !important;
    background-color: #111111 !important;
    border: 1px solid #333333 !important;
    border-radius: 10px !important;
    padding: 9px 16px !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    text-decoration: none !important;
    transition: all 0.2s ease !important;
}

[data-testid="stPageLink"] a:hover {
    background-color: #b74b4b !important;
    color: #000000 !important;
    border-color: #b74b4b !important;
    transform: translateY(-1px);
}
</style>
""", unsafe_allow_html=True)


st.markdown(
    """
    <div class="acader-title">
        Acader
    </div>

    <div class="acader-subtitle">
        Turn your notes into tests, flashcards, and review material.
    </div>
    """,
    unsafe_allow_html=True
)


if "camera_active" not in st.session_state:
    st.session_state.camera_active = False


left_pad, col_upload, spacer, col_btn, right_pad = st.columns(
    [1.5, 4, 0.7, 3, 1.5]
)


with col_upload:

    st.markdown(
        '<div class="section-title">Upload Your Notes</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-text">Upload an image of your notes.</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload your notes",
        type=["jpg", "jpeg", "png"]
    )


with col_btn:

    st.markdown(
        '<div class="section-title">Take a Photo</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-text">Capture your notes directly.</div>',
        unsafe_allow_html=True
    )

    if st.button("Open Camera"):
        st.session_state.camera_active = True


if st.session_state.camera_active:

    st.divider()

    st.markdown(
        '<div class="section-title">Camera</div>',
        unsafe_allow_html=True
    )

    picture = st.camera_input(
        "Take a picture"
    )

    if st.button("Close Camera"):
        st.session_state.camera_active = False

    if picture:

        st.image(
            picture,
            caption="Your notes"
        )

        st.divider()

        st.markdown(
            '<div class="section-title">Generate</div>',
            unsafe_allow_html=True
        )

        test_col, flashcard_col, notes_col = st.columns(3)

        with test_col:

            if st.button("Generate Test using Photo"):
                st.session_state.input_image = picture
                st.session_state.generation_type = "test"
                st.switch_page("loading.py")

        with flashcard_col:

            if st.button("Generate Flashcards using Photo"):
                st.session_state.input_image = picture
                st.session_state.generation_type = "flashcards"
                st.switch_page("loading.py")

        with notes_col:
            if st.button("Generate Review Notes using Photo"):
                st.session_state.input_image = picture
                st.session_state.generation_type = "notes"
                st.switch_page("loading.py")


if uploaded_file:

    st.divider()

    st.markdown(
        '<div class="section-title">Uploaded Notes</div>',
        unsafe_allow_html=True
    )

    st.image(
        uploaded_file,
        caption="Your notes"
    )

    st.divider()

    st.markdown(
        '<div class="section-title">Generate</div>',
        unsafe_allow_html=True
    )

    test_col, flashcard_col, notes_col = st.columns(3)

    with test_col:

        if st.button("Generate Test using Uploaded File"):
            st.session_state.input_image = uploaded_file
            st.session_state.generation_type = "test"
            st.switch_page("loading.py")


    with flashcard_col:

        if st.button("Generate Flashcards using Uploaded File"):
            st.session_state.input_image = uploaded_file
            st.session_state.generation_type = "flashcards"
            st.switch_page("loading.py")

    with notes_col:

        if st.button("Generate Review Notes using Uploaded File"):
            st.session_state.input_image = uploaded_file
            st.session_state.generation_type = "notes"
            st.switch_page("loading.py")




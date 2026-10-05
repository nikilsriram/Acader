import streamlit as st
from main import generate_flashcards_from_image, generate_test_from_image, generate_notes_from_image
import time

st.markdown(
    """
    <style>
    div[data-testid="stStatusWidget"],
    .stAppViewerFooter,
    div[class*="ViewerBadge"],
    div[class*="viewerBadge"],
    [data-testid="stActionButton"],
    footer {
        display: none !important;
        visibility: hidden !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
if not st.session_state.get("user_id"):
    st.warning("Please log in to view this page.")
    st.page_link("app.py", label="Go to Login")
    st.stop()  # Instantly halts execution of the rest of the page code

def call_load():
    placeholder = st.empty()
    placeholder.markdown("""
                <style>
                .loading-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    padding: 50px 20px;
                }
    
                .loading-spinner {
                    width: 55px;
                    height: 55px;
                    border: 5px solid rgba(255, 255, 255, 0.2);
                    border-top: 5px solid #ff3b3b;
                    border-radius: 50%;
                    animation: spin 0.9s linear infinite;
                    margin-bottom: 25px;
                }
    
                .loading-text {
                    color: white;
                    font-size: 24px;
                    font-weight: 600;
                }
    
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                </style>
    
                <div class="loading-container">
                    <div class="loading-spinner"></div>
                    <div class="loading-text">Getting your study materials ready...</div>
                    <div class="loading-text"> This may take a couple of minutes ... </div>
                </div>
                """, unsafe_allow_html=True)
    if st.session_state.generation_type == "flashcards":
        result = generate_flashcards_from_image(
            st.session_state.input_image
        )
        time.sleep(2)
        placeholder.empty()
        placeholder.markdown("""
                                <style>
                                .loading-container {
                                    display: flex;
                                    flex-direction: column;
                                    align-items: center;
                                    justify-content: center;
                                    padding: 50px 20px;
                                }
                    
                                .loading-text {
                                    color: white;
                                    font-size: 24px;
                                    font-weight: 600;
                                }
                                </style>
                    
                                <div class="loading-container">
                                    <div class="loading-text">Study Materials Complete.</div>
                                </div>
                                """, unsafe_allow_html=True)
        st.session_state.flashcards = result
        st.page_link("./flashcards.py", label="View Flashcards")
    if st.session_state.generation_type == "test":
        result = generate_test_from_image(
            st.session_state.input_image
        )
        time.sleep(2)
        placeholder.empty()
        placeholder.markdown("""
                        <style>
                        .loading-container {
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                            justify-content: center;
                            padding: 50px 20px;
                        }
            
                        .loading-text {
                            color: white;
                            font-size: 24px;
                            font-weight: 600;
                        }
                        </style>
            
                        <div class="loading-container">
                            <div class="loading-text">Study Materials Complete.</div>
                        </div>
                        """, unsafe_allow_html=True)
        st.session_state.test = result
        st.page_link("./test.py", label="View Test")
    if st.session_state.generation_type == "notes":
        result = generate_notes_from_image (
            st.session_state.input_image
        )
        time.sleep(2)
        placeholder.empty()
        placeholder.markdown("""
                                <style>
                                .loading-container {
                                    display: flex;
                                    flex-direction: column;
                                    align-items: center;
                                    justify-content: center;
                                    padding: 50px 20px;
                                }
                    
                                .loading-text {
                                    color: white;
                                    font-size: 24px;
                                    font-weight: 600;
                                }
                                </style>
                    
                                <div class="loading-container">
                                    <div class="loading-text">Study Materials Complete.</div>
                                </div>
                                """, unsafe_allow_html=True)
        st.session_state.notes = result
        st.page_link("./notes.py", label="View Notes")

call_load()



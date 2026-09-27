import streamlit as st
from main import generate_flashcards_from_image

def call_load():
    st.markdown("""
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
                </div>
                """, unsafe_allow_html=True)
    if st.session_state.generation_type == "flashcards":
        result = generate_flashcards_from_image(
            st.session_state.input_image
        )

        st.session_state.flashcards = result
        st.write("RESULT:", result)


        st.page_link("./flashcards.py", label="View Flashcards")

call_load()
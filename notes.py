import streamlit as st
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

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("app.py", label="🏠 Welcome", use_container_width=True)

with col2:
    st.page_link("frontend.py", label="⚡ Generator", use_container_width=True)

with col3:
    st.page_link("progresstracker.py", label="📈 Progress Tracker", use_container_width=True)

st.divider()

st.write(st.session_state.notes)
st.page_link("app.py", label='go to app')
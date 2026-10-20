
import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.page_link("app.py", label="Welcome", use_container_width=True)

with col2:
    st.page_link("frontend.py", label="Generator", use_container_width=True)

with col3:
    st.page_link("progresstracker.py", label="Progress Tracker", use_container_width=True)

with col4:
    st.page_link("deck.py", label="Decks", use_container_width=True)

st.set_page_config(page_title="Shared Study Deck", page_icon="🔑")

st.title("🔑 Open a Shared Study Deck")
st.write("Want to save some progress click here ↓ ")
st.page_link("app.py", label="Save Progress", use_container_width=True)

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    st.error("Supabase configuration is missing.")
    st.stop()

supabase = create_client(supabase_url, supabase_key)

if "guest_unlocked_content" not in st.session_state:
    st.session_state.guest_unlocked_content = None

if st.session_state.guest_unlocked_content is None:
    with st.form("receiver_form"):
        deckname = st.text_input(
            "Enter deckname",
            placeholder="BIOLOGYREVIEW"
        )
        passcode = st.text_input(
            "Enter passcode",
            placeholder="MYSECRET123"
        )
        submitted = st.form_submit_button("🔓 Load Deck")

    if submitted:
        if not passcode.strip() or not deckname.strip():
            st.error("Please enter a passcode or username.")
        else:
            try:
                response = supabase.rpc(
                    "get_shared_note",
                    {"p_passcode": passcode.strip().upper(), "d_deckname": deckname.strip().upper()}
                ).execute()
                

                if not response.data:
                    st.error("Passcode or username not found, or the linked note is unavailable.")
                else:
                    st.session_state.guest_unlocked_content = (
                        response.data[0].get("content") or ""
                    )
                    st.rerun()

            except Exception as e:
                st.error("Could not load the shared deck.")
                st.caption(str(e))

    st.stop()

st.success("🔓 Access granted!")
st.subheader("📝 Shared Study Notes")

content = st.session_state.guest_unlocked_content

if content:
    st.markdown(content)
else:
    st.info("This shared note is empty.")

if st.button("🚪 Close Shared Deck"):
    st.session_state.guest_unlocked_content = None
    st.rerun()
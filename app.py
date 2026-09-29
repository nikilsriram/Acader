import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Global Authentication States Tracker
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# Silent Token Session Recovery across browser refreshes
try:
    session = supabase.auth.get_session()
    if session and hasattr(session, 'user') and session.user:
        st.session_state.user_email = session.user.email
        st.session_state.user_id = session.user.id
except Exception:
    pass


def sign_up(email, password):
    try:
        return supabase.auth.sign_up({"email": email, "password": password})
    except Exception as e:
        st.error(f"Registration failed: {e}")

def sign_in(email, password):
    try:
        auth_data = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if auth_data and auth_data.user:
            st.session_state.user_email = auth_data.user.email
            st.session_state.user_id = auth_data.user.id
            st.success("Welcome back!")
            st.rerun()
    except Exception as e:
        st.error(f"Login failed: {e}")

def sign_out():
    try:
        supabase.auth.sign_out()
        st.session_state.user_email = None
        st.session_state.user_id = None
        st.session_state.pop("notes", None)
        st.session_state.pop("test", None)
        st.session_state.pop("flashcards", None)
        st.rerun()
    except Exception as e:
        st.error(f"Logout failed: {e}")


def main_app(user_email, user_id):
    st.title("Welcome Page")
    st.success(f"Welcome, {user_email}")
    st.write("You are logged in successfully!")
    
    # --- MASTER SAVE BUTTON ---
    if st.button("Save All Progress", type="primary"):
        saved_items = []
        has_errors = False

        # 1. Inspect Session State for background Notes
        if "notes" in st.session_state and st.session_state.notes:
            try:
                supabase.table("notes").insert({
                    "content": str(st.session_state.notes),
                    "user_id": user_id
                }).execute()
                saved_items.append("Notes")
            except Exception as e:
                st.error(f"Failed to save Notes from background session: {e}")
                has_errors = True

        # 2. Inspect Session State for background Test Results
        if "test" in st.session_state and st.session_state.test:
            try:
                supabase.table("test_results").insert({
                    "score": int(st.session_state.test.get("score", 0)),
                    "total": int(st.session_state.test.get("total_questions", 0)),
                    "user_id": user_id
                }).execute()
                saved_items.append("Test Results")
            except Exception as e:
                st.error(f"Failed to save Test Results from background session: {e}")
                has_errors = True

        # 3. Inspect Session State for background Flashcards
        if "flashcards" in st.session_state and st.session_state.flashcards:
            try:
                cards_payload = []
                for card in st.session_state.flashcards:
                    card_copy = card.copy()
                    card_copy["user_id"] = user_id
                    cards_payload.append(card_copy)
                    
                supabase.table("flashcards").insert(cards_payload).execute()
                saved_items.append("Flashcards")
            except Exception as e:
                st.error(f"Failed to save Flashcards from background session: {e}")
                has_errors = True

        if saved_items:
            st.success(f"🎉 Successfully captured and saved background data: {', '.join(saved_items)}")
        elif not has_errors:
            st.warning("Nothing to save! Background states for notes, tests, or flashcards are currently empty.")

    # --- MASTER LOAD BUTTON ---
    if st.button("Load Last Progress", type="secondary"):
        loaded_items = []
        
        try:
            # 1. Fetch ALL notes belonging to this user profile (No limits)
            res_notes = supabase.table("notes").select("content").eq("user_id", user_id).order("id", desc=True).execute()
            if res_notes.data and len(res_notes.data) > 0:
                # Save the full data collection array directly to session state
                st.session_state.notes = res_notes.data
                loaded_items.append("Notes")

            # 2. Load Test Results
            res_test = supabase.table("test_results").select("score, total").eq("user_id", user_id).order("id", desc=True).limit(5).execute()
            if res_test.data and len(res_test.data) > 0:
                st.session_state.test = {
                    "score": res_test.data[0]["score"],
                    "total_questions": res_test.data[0]["total"]
                }
                loaded_items.append("Test Results")

            # 3. Load Flashcards Array
            res_flash = supabase.table("flashcards").select("front, back").eq("user_id", user_id).order("id", desc=True).limit(20).execute()
            if res_flash.data and len(res_flash.data) > 0:
                st.session_state.flashcards = res_flash.data
                loaded_items.append("Flashcards")

            if loaded_items:
                st.success(f"📂 Session data pulled down: {', '.join(loaded_items)}")
                st.rerun()
            else:
                st.warning("No saved data rows found for your user account profile.")
                
        except Exception as e:
            st.error(f"Database error during load: {e}")

    # --- EXPORT INTERFACE LAYER ---
    # This renders outside the button scope so it never disappears on click
    if "notes" in st.session_state and isinstance(st.session_state.notes, list):
        st.write("---")
        st.subheader("📥 Export Complete Archive")
        
        # Aggregate all contents sequentially in plain text layout format
        all_notes_text = "=== ALL MY SAVED STUDY NOTES ===\n\n"
        for index, note_entry in enumerate(st.session_state.notes, 1):
            note_content = note_entry.get("content", "")
            all_notes_text += f"--- Note Entry #{index} ---\n{note_content}\n\n"
            
        st.download_button(
            label="Download Complete Notes History (.txt)",
            data=all_notes_text,
            file_name="all_my_study_notes.txt",
            mime="text/plain",
            use_container_width=True
        )

    # --- LIVE DATA MONITOR ---
    st.write("---")
    st.subheader("Current Live Session State Monitor")
    
    # Clean check if notes are formatted as raw text or history array lists
    if isinstance(st.session_state.get("notes"), list):
        st.write("📝 **Notes Record Count:**", len(st.session_state.notes))
    else:
        st.write("📝 **Notes:**", st.session_state.get("notes", "Empty"))
        
    st.write("📊 **Test:**", st.session_state.get("test", "Empty"))
    st.write("🗂️ **Flashcards Count:**", len(st.session_state.get("flashcards", [])))
    
    st.write("---")
    if st.button("Logout"):
        sign_out()


def auth_screen():
    st.title("Streamlit & Supabase Auth App")
    option = st.selectbox("Choose an action: ", ["Login", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if option == "Sign Up" and st.button("Register"):
        auth_data = sign_up(email, password)
        if auth_data and getattr(auth_data, 'user', None):
            st.success("Registration successful. Please log in.")

    if option == "Login" and st.button("Login"):
        sign_in(email, password)


# --- ROUTER ---
if st.session_state.user_email and st.session_state.user_id:
    main_app(st.session_state.user_email, st.session_state.user_id)
else:
    auth_screen()

st.write("---")
st.page_link('frontend.py', label='go to frontend')

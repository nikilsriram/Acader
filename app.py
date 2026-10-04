import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import ast
import json

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)


st.html(f"""
<html>

<head>
<style>
[data-testid="stHeader"], 
[data-testid="stStatusWidget"], 
#MainMenu {{
    display: none !important;
    height: 0 !important;
}}


header {{
            position: fixed;
            top: 20px;
            left: 0;
            width: 100%;
            height: 80px;
            padding: 0 5%;
            background-color: transparent;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 100;
        }}

        .logo {{
            font-size: 1.8rem; /* Scaled down further from 2.4rem */
            color: #b74b4b !important;
            font-weight: 800;
            cursor: pointer;
            transition: 0.5s ease;
            text-decoration: none;
        }}

        .logo:hover {{
            transform: scale(1.05);
        }}

        nav {{
            display: flex;
            align-items: center;
            gap: 1.8rem; /* Tightened gap spacing */
        }}

        nav a {{
            font-size: 1.1rem; /* Scaled down further from 1.3rem */
            color: white !important;
            font-weight: 500;
            transition: 0.3s ease;
            border-bottom: 2px solid transparent; /* Lightened border line scale */
            white-space: nowrap;
            text-decoration: none;
        }}

        nav a:hover,
        nav a.active {{
            color: #b74b4b !important;
            border-bottom: 2px solid #b74b4b;
        }}

        @media (max-width: 995px) {{
            nav {{
                position: absolute;
                display: none;
                top: 0;
                right: 0;
                width: 40%;
                border-left: 3px solid #b74b4b;
                border-bottom: 3px solid #b74b4b;
                border-bottom-left-radius: 2rem;
                padding: 1rem;
                background-color: #161616;
                border-top: 0.1rem solid rgba(0, 0, 0, 0.1);
            }}

            nav .active {{
                display: block;
            }}

            nav a {{
                display: block;
                font-size: 1.3rem; /* Scaled down mobile text */
                margin: 1.5rem 0;
            }}

            nav a:hover,
            nav a.active {{
                padding: 0.6rem;
                border-radius: 0.5rem;
                border-bottom: 0.4rem solid #b74b4b;
            }}
        }}

         [data-testid="stElementContainer"], .element-container {{
                    max-width: 100% !important;
                    width: 100vw !important;
                }}
        
                /* Make sure the iframe itself drops all borders and fills the space */
                iframe {{
                    display: block;
                    width: 100vw !important;
                    height: 100vh !important;
                    border: none !important;
                }}
</style>



</head>
<body>
<header>
        <a href="#" class="logo">Acader</a>

        <nav>
            <a href="/">Home</a>
            <a href="/aboutme">About Us</a>
            <a href="/">Education</a>
            <a href="/contact">Contact Us</a>
            <a href="/login" class="active">Login/Sign up</a>
        </nav>
    </header>
</body>
</html>
""")



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
    st.write("You are logged in successfully! Make sure to download saved files as only the last thing you generated will show up!")

    st.markdown(
        """
        <style>
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

    st.page_link(
        "frontend.py",
        label="Go to generator →",
    )

    st.page_link(
            "progresstracker.py",
            label="Go to progress tracker →",
        )
    
    # --- MASTER SAVE BUTTON ---
    if st.button("Save All Progress", type="primary"):
        saved_items = []
        has_errors = False

        # 1. Inspect Session State for background Notes
                # 1. Inspect Session State for background Notes
        if "notes" in st.session_state and st.session_state.notes:
            try:
                # Force it to be saved as a clean text string layout directly
                clean_note_text = str(st.session_state.notes)

                supabase.table("notes").insert({
                    "content": clean_note_text,
                    "user_id": user_id
                }).execute()
        
                saved_items.append("Notes")
            except Exception as e:
                st.error(f"Failed to save Notes from background session: {e}")
                has_errors = True


        # 2. Inspect Session State for background Test Results
        if "test" in st.session_state and st.session_state.test:
            try:
                import json
                
                # Force the data into a perfectly quoted JSON text block string
                if isinstance(st.session_state.test, (dict, list)):
                    serialized_test = json.dumps(st.session_state.test)
                else:
                    serialized_test = str(st.session_state.test)

                supabase.table("test_results").insert({
                    "questionsanswers": serialized_test,
                    "user_id": user_id
                }).execute()
                saved_items.append("Test Results")
            except Exception as e:
                st.error(f"Failed to save Test Results: {e}")
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
                # Extract the raw text content string from the newest entry immediately!
                raw_db_string = res_notes.data[0]["content"]
                st.session_state.notes = str(raw_db_string)
                loaded_items.append("Notes")

            # 2. Load Test Results
            res_test = supabase.table("test_results").select("questionsanswers").eq("user_id", user_id).order("id", desc=True).limit(5).execute()
            if res_test.data and len(res_test.data) > 0:
                db_string_payload = res_test.data[0]["questionsanswers"]
                
                # Assign it cleanly to session state so your application layer reads it instantly
                st.session_state.test = db_string_payload
                loaded_items.append("Test Results")

            # 3. Load Flashcards Array
            res_flash = supabase.table("flashcards").select("front, back").eq("user_id", user_id).order("id", desc=True).limit(20).execute()
            if res_flash.data and len(res_flash.data) > 0:
                st.session_state.flashcards = res_flash.data
                loaded_items.append("Flashcards")

            if loaded_items:
                st.success(f"📂 Session data pulled down: {', '.join(loaded_items)}")
            else:
                st.warning("No saved data rows found for your user account profile.")
                
        except Exception as e:
            st.error(f"Database error during load: {e}")



    if not st.session_state.get("user_id"):
        st.warning("Please log in to view this page.")
        st.page_link("app.py", label="Go to Login")
        st.stop()

        st.title("📝 Your Study Notes")

    if "notes" in st.session_state and st.session_state.notes:
        raw_text = str(st.session_state.notes)

        # A. Peel back any double-escaped database artifacts safely if they remain
        if raw_text.strip().startswith("[{'") or raw_text.strip().startswith('[{"'):
            try:
                import ast
                parsed_list = ast.literal_eval(raw_text.strip())
                if isinstance(parsed_list, list) and len(parsed_list) > 0:
                    inner_item = parsed_list[0]
                    if isinstance(inner_item, dict):
                        raw_text = inner_item.get("content", raw_text)
            except Exception:
                pass

        # B. Strip away backslashes and format code blocks into clean readable text lines
        clean_text = (
            raw_text.replace("\\n", "\n")
            .replace("\\'", "'")
            .replace('\\"', '"')
            .replace("\\\\", "\\")
        )

        st.write("---")
        st.subheader("📥 Export Complete Notes Archive")
        st.download_button(
            label="Download Clean Notes (.txt)",
            data=clean_text,
            file_name="my_study_notes.txt",
            mime="text/plain",
            use_container_width=True
        )

    # 🌟 FIXED TEST EXPORT BLOCK 🌟
    if "test" in st.session_state and st.session_state.test:
        st.write("---")
        st.subheader("📥 Export Complete Quiz Archive")
                
        raw_test_data = st.session_state.test
        test_dict = None

        # A. Safely convert data to a dictionary map without throwing errors
        if isinstance(raw_test_data, dict):
            test_dict = raw_test_data
        elif isinstance(raw_test_data, str):
            try:
                import json
                test_dict = json.loads(raw_test_data.strip())
            except Exception:
                try:
                    import ast
                    test_dict = ast.literal_eval(raw_test_data.strip())
                except Exception:
                    pass  # If it's a completely broken old string history row, catch it silently

        # B. Loop and print only if the dictionary loaded correctly
        if isinstance(test_dict, dict) and "multiple_choice" in test_dict:
            all_test_text = "=== ACADER SAVED MULTIPLE-CHOICE TEST SUITE ===\n\n"
            
            for index, item in enumerate(test_dict["multiple_choice"], 1):
                all_test_text += f"Question {index}: {item.get('question')}\n"
                for choice_index, choice in enumerate(item.get("choices", []), 1):
                    all_test_text += f"  [{choice_index}] {choice}\n"
                all_test_text += f"Correct Answer Key: {item.get('correct_answer')}\n"
                all_test_text += "--------------------------------------------------\n\n"
                        
            st.download_button(
                label="Download Complete Test History (.txt)",
                data=all_test_text,
                file_name="all_my_test_questions.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.warning("Active quiz session found, but structure format is incompatible. Run a fresh test to generate a clean history record!")

    st.write("---")
    if st.button("Logout"):
        sign_out()


def auth_screen():
    st.title("Registration & Login")
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

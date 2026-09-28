import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

def sign_up(email, password):
    try:
        return supabase.auth.sign_up({"email": email, "password": password})
    except Exception as e:
        st.error(f"Registration failed: {e}")

def sign_in(email, password):
    try:
        return supabase.auth.sign_in_with_password({"email": email, "password": password})
    except Exception as e:
        st.error(f"Login failed: {e}")

def sign_out():
    try:
        supabase.auth.sign_out()
        st.session_state.user_email = None
        st.session_state.user_id = None
        st.rerun()
    except Exception as e:
        st.error(f"Logout failed: {e}")

def main_app(user_email, user_id):
    st.title("Welcome Page")
    st.success(f"Welcome, {user_email}")
    
    st.subheader("Account Workspace")
    st.write("You are logged in successfully!")
    
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
        auth_data = sign_in(email, password)
        if auth_data and getattr(auth_data, 'user', None):
            st.session_state.user_email = auth_data.user.email
            st.session_state.user_id = auth_data.user.id
            st.success("Welcome back!")
            st.rerun()

# --- BACKEND RECOVERY AUTH FIX ---
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None

try:
    session = supabase.auth.get_session()
    if session and getattr(session, 'user', None):
        st.session_state.user_email = session.user.email
        st.session_state.user_id = session.user.id
except Exception:
    pass

# Routing logic
if st.session_state.user_email and st.session_state.user_id:
    main_app(st.session_state.user_email, st.session_state.user_id)
else:
    auth_screen()

st.page_link('frontend.py', label='go to frontend')
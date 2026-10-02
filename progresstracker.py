import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os

if not st.session_state.get("user_id") and not st.session_state.get("flashcards"):
    st.warning("Please log in to view this page.")
    st.page_link("app.py", label="Go to Login")
    st.stop()

user_id = st.session_state.user_id

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

def get_todos():
    response = supabase.table('todos').select('*').eq('user_id', user_id).execute()
    return response.data

# ✅ FIXED: Added user_id to the insert payload
def add_todo(task):
    supabase.table('todos').insert({
        'task': task,
        'user_id': user_id
    }).execute()

st.title("SUPABASE TODO APP")

task = st.text_input("Add a new task: ")

if st.button("Add Task"):
    if task:
        add_todo(task)
        st.success("Task added!")
        st.rerun()  # ✅ FIXED: Forces screen to update instantly with the new task
    else:
        st.error("Please enter a task.")

st.write("### Todo List: ")
todos = get_todos()

if todos:
    for todo in todos:
        st.write(f"- {todo['task']}")
else:
    st.write("No tasks available")

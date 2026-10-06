import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os
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

# -----------------------------
# LOGIN CHECK
# -----------------------------

access_token = st.session_state.get("access_token")
refresh_token = st.session_state.get("refresh_token")

if not st.session_state.get("user_id") or not access_token or not refresh_token:
    st.warning("Please log in to view this page.")
    st.page_link("app.py", label="Go to Login")
    st.stop()

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

try:
    auth_response = supabase.auth.set_session(access_token, refresh_token)

    if not auth_response or not auth_response.user or not auth_response.session:
        raise ValueError("Session could not be restored.")

    user_id = str(auth_response.user.id)
    st.session_state.user_id = user_id
    st.session_state.user_email = auth_response.user.email
    st.session_state.access_token = auth_response.session.access_token
    st.session_state.refresh_token = auth_response.session.refresh_token

except Exception:
    for key_name in ("user_id", "user_email", "access_token", "refresh_token"):
        st.session_state.pop(key_name, None)
    st.warning("Your session has expired. Please log in again.")
    st.page_link("app.py", label="Go to Login")
    st.stop()




col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("app.py", label="Welcome", use_container_width=True)

with col2:
    st.page_link("frontend.py", label="Generator", use_container_width=True)

with col3:
    st.page_link("progresstracker.py", label="Progress Tracker", use_container_width=True)

st.divider()

def get_todos():
    response = (
        supabase
        .table("todos")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    return response.data


def add_todo(task, test_score, notes_score, flashcard_score):
    supabase.table("todos").insert({
        "task": task,
        "task1": test_score,
        "task2": notes_score,
        "task3": flashcard_score,
        "user_id": user_id
    }).execute()


# -----------------------------
# HEADER
# -----------------------------

st.title("Progress Tracker")
st.caption("Track your performance across your study sessions.")

st.divider()


# -----------------------------
# ADD TOPIC
# -----------------------------

st.subheader(" Add Study Topic")

with st.container(border=True):

    topic = st.text_input(
        "Topic",
        placeholder="e.g. Newton's Laws"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        test_score = st.text_input(
            " Test Score",
            placeholder="e.g. 92%"
        )

    with col2:
        notes_score = st.text_input(
            " Time Spent",
            placeholder="e.g. 1 hr"
        )

    with col3:
        flashcard_score = st.text_input(
            " Flashcards Score",
            placeholder="e.g. 85%"
        )

    if st.button("Add Topic", type="primary", use_container_width=True):

        if topic:
            add_todo(
                topic,
                test_score,
                notes_score,
                flashcard_score
            )

            st.success("Topic added!")
            st.rerun()

        else:
            st.error("Please enter a topic.")


st.divider()


# -----------------------------
# GET TOPICS
# -----------------------------

todos = get_todos()


# -----------------------------
# OVERVIEW
# -----------------------------

st.subheader(" Your Progress")

if todos:

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Topics Tracked",
            len(todos)
        )

    with col2:
        completed = sum(
            1 for todo in todos
            if todo["task1"] and todo["task2"] and todo["task3"]
        )

        st.metric(
            "Completed",
            completed
        )


    st.write("")


    # -----------------------------
    # TOPIC CARDS
    # -----------------------------

    for todo in todos:

        with st.container(border=True):

            st.subheader(todo["task"])

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    " Test",
                    todo["task1"] or "—"
                )

            with col2:
                st.metric(
                    " Notes",
                    todo["task2"] or "—"
                )

            with col3:
                st.metric(
                    "Flashcards",
                    todo["task3"] or "—"
                )

            st.write("")

            with st.expander("View details"):
                st.write(f"**Topic:** {todo['task']}")
                st.write(f"**Test Score:** {todo['task1'] or 'Not completed'}")
                st.write(f"**Notes Score:** {todo['task2'] or 'Not completed'}")
                st.write(f"**Flashcards Score:** {todo['task3'] or 'Not completed'}")

else:

    st.info(
        "No topics tracked yet. Add your first study topic above!"
    )
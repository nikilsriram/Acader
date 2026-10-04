import json
import streamlit as st
import streamlit.components.v1 as components

if not st.session_state.get("user_id") and not st.session_state.get("flashcards"):
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

def format_ai_output_to_list(raw_data):
    """Convert AI flashcard output into a list."""

    formatted_list = []

    if isinstance(raw_data, list):
        formatted_list = raw_data

    elif isinstance(raw_data, dict):

        for i in range(1, 21):

            question = raw_data.get(f"Question {i}")
            answer = raw_data.get(f"Answer {i}")

            if question is not None and answer is not None:
                formatted_list.append({
                    "question": question,
                    "answer": answer
                })

    return formatted_list


def show_my_flashcards(data):

    clean_data = format_ai_output_to_list(data)

    if not clean_data:
        st.error("No flashcards were generated.")
        st.write("Raw data:", data)
        return

    json_string = json.dumps(clean_data)

    html = """
<!DOCTYPE html>

<html>

<head>

    <meta charset="UTF-8">

<style>

    body {
        font-family: 'Inter', sans-serif;

        display: flex;
        justify-content: center;
        align-items: center;

        min-height: 100vh;

        background-color: black;

        margin: 0;
        color: white;
    }


    .flashcard-container {

        text-align: center;

        background-color: #161616;

        padding: 30px;

        border-radius: 20px;

        box-shadow:
            0 0 25px rgba(183, 75, 75, 0.25);

        width: 320px;

        border: 1px solid #b74b4b;
    }


    .flashcard-container h1 {

        color: white;

        font-size: 2rem;

        margin-bottom: 10px;
    }


    .flashcard {

        width: 100%;
        height: 180px;

        position: relative;

        transform-style: preserve-3d;

        transition: transform 0.6s;

        margin: 20px auto;
    }


    .flashcard.is-flipped {

        transform: rotateY(180deg);
    }


    .flashcard div {

        position: absolute;

        width: 100%;
        height: 100%;

        backface-visibility: hidden;

        border-radius: 15px;

        background-color: #1f1f1f;

        border: 2px solid #b74b4b;

        display: flex;

        justify-content: center;
        align-items: center;

        padding: 20px;

        box-sizing: border-box;

        font-size: 1.1em;

        color: white;

        box-shadow:
            0 0 15px rgba(183, 75, 75, 0.15);
    }


    .front {

        color: white;
    }


    .back {

        transform: rotateY(180deg);

        background-color: #b74b4b !important;

        color: black !important;

        border-color: #b74b4b !important;
    }


    button {

        margin: 5px;

        padding: 10px 20px;

        border: 2px solid #b74b4b;

        border-radius: 25px;

        background-color: black;

        color: #b74b4b;

        font-size: 1rem;

        font-weight: 600;

        cursor: pointer;

        transition: 0.3s ease;
    }


    button:hover {

        background-color: #b74b4b;

        color: black;

        transform: scale(1.05);

        box-shadow:
            0 0 15px rgba(183, 75, 75, 0.5);
    }


</style>


</head>


<body>


<div class="flashcard-container">


    <h1>Flashcard Quiz</h1>


    <div
        id="flashcard"
        class="flashcard"
    >

        <div class="front">

            <p id="question">
                Loading...
            </p>

        </div>


        <div class="back">

            <p id="answer">
                Loading...
            </p>

        </div>

    </div>


    <button id="flip-card">
        Flip Card
    </button>


    <button id="next-card">
        Next
    </button>


</div>


<!-- Python JSON gets inserted here -->

<script id="flashcard-data" type="application/json">
FLASHCARDS_DATA
</script>


<script>

    // Get the JSON that Python inserted
    const dataElement =
        document.getElementById("flashcard-data");


    // Read it as text
    const jsonText =
        dataElement.textContent;


    // Convert JSON -> JavaScript array
    const flashcards =
        JSON.parse(jsonText);


    let currentCard = 0;


    const flashcardElement =
        document.getElementById("flashcard");


    const questionElement =
        document.getElementById("question");


    const answerElement =
        document.getElementById("answer");


    function displayCard() {

        if (flashcards.length === 0) {
            questionElement.textContent = "No flashcards available.";
            answerElement.textContent = "";
            return;
        }

        const card = flashcards[currentCard];

        questionElement.textContent = card.question;
        answerElement.textContent = card.answer;

        flashcardElement.classList.remove("is-flipped");
    }


    document
        .getElementById("flip-card")
        .addEventListener("click", function() {

            flashcardElement.classList.toggle(
                "is-flipped"
            );

        });


    document
        .getElementById("next-card")
        .addEventListener("click", function() {

            currentCard =
                (currentCard + 1)
                % flashcards.length;

            displayCard();

        });


    // Show first card
    displayCard();

</script>


</body>

</html>
"""

    # Insert the Python JSON
    html = html.replace(
        "FLASHCARDS_DATA",
        json_string
    )

    components.html(
        html,
        height=500
    )


if "flashcards" in st.session_state:

    show_my_flashcards(
        st.session_state.flashcards
    )
import json
import streamlit as st
import streamlit.components.v1 as components


def format_ai_output_to_list(raw_data):
    """Convert AI output into a list of {question, answer} dictionaries."""

    # Already in the correct format
    if isinstance(raw_data, list):
        return raw_data

    formatted_list = []

    if isinstance(raw_data, dict):

        for i in range(1, 100):

            question = (
                raw_data.get(f"Question {i}")
                or raw_data.get(f"tion {i}")
            )

            answer = raw_data.get(f"Answer {i}")

            if question and answer:
                formatted_list.append({
                    "question": question,
                    "answer": answer
                })

    return formatted_list


def show_my_flashcards(data):

    # Convert whatever the AI gave us into:
    # [
    #   {"question": "...", "answer": "..."},
    #   ...
    # ]

    clean_data = format_ai_output_to_list(data)

    # Convert Python list -> JSON
    json_string = json.dumps(clean_data)

    html = """
<!DOCTYPE html>

<html>

<head>

    <meta charset="UTF-8">

    <style>

        body {
            font-family: sans-serif;

            display: flex;
            justify-content: center;
            align-items: center;

            min-height: 100vh;

            background: linear-gradient(
                135deg,
                #f5a623,
                #f29d77
            );

            margin: 0;
        }


        .flashcard-container {

            text-align: center;

            background-color: white;

            padding: 30px;

            border-radius: 20px;

            box-shadow:
                0 0 15px rgba(0, 0, 0, 0.2);

            width: 320px;
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

            background: linear-gradient(
                135deg,
                #f5f7fa,
                #c3cfe2
            );

            display: flex;

            justify-content: center;
            align-items: center;

            padding: 20px;

            box-sizing: border-box;

            font-size: 1.1em;
        }


        .back {

            transform: rotateY(180deg);
        }


        button {

            margin: 5px;

            padding: 10px 20px;

            border: none;

            border-radius: 25px;

            background-color: #ff5722;

            color: white;

            font-size: 1rem;

            cursor: pointer;
        }


        button:hover {

            background-color: #e64a19;
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

        const card =
            flashcards[currentCard];


        questionElement.textContent =
            card.question;


        answerElement.textContent =
            card.answer;


        flashcardElement.classList.remove(
            "is-flipped"
        );

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
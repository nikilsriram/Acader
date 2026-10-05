import streamlit as st
import json

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

if "test" not in st.session_state:
    st.session_state.test = None


if st.session_state.test:

    test_data = st.session_state.test

    questions = []

    for q in test_data["multiple_choice"]:
        answers = []

        for choice in q["choices"]:
            answers.append({
                "text": choice,
                "correct": choice == q["correct_answer"]
            })

        questions.append({
            "question": q["question"],
            "answers": answers
        })

    test_json = json.dumps(questions)

    html = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Inter', sans-serif;
}

body {
    background: black;
    color: white;
}

.app {
    background: black;
    width: 90%;
    max-width: 600px;
    margin: 50px auto 0;
    border-radius: 10px;
    padding: 30px;
}

.app h1 {
    font-size: 25px;
    color: white;
    font-weight: 600;
    border-bottom: 1px solid #333;
    padding-bottom: 30px;
}

.quiz {
    padding: 20px 0;
}

.quiz h2 {
    font-size: 18px;
    color: white;
    font-weight: 600;
}

.btn {
    background: black;
    color: white;
    font-weight: 500;
    width: 100%;
    border: 1px solid #333;
    padding: 12px;
    margin: 10px 0;
    text-align: left;
    border-radius: 6px;
    cursor: pointer;
    transition: 0.3s ease;
}

.btn:hover:not([disabled]) {
    border-color: #b74b4b;
    color: #b74b4b;
}

.btn:disabled {
    cursor: no-drop;
}

#next-btn {
    background: black;
    color: #b74b4b;
    font-weight: 600;
    width: 150px;
    border: 2px solid #b74b4b;
    padding: 10px;
    margin: 20px auto 0;
    border-radius: 40px;
    cursor: pointer;
    transition: 0.3s ease;
}

#next-btn:hover {
    background: #b74b4b;
    color: black;
    transform: scale(1.03);
}

.correct {
    background: #1f5c3a !important;
    border-color: #4ade80 !important;
    color: white !important;
}

.incorrect {
    background: #5c1f1f !important;
    border-color: #b74b4b !important;
    color: white !important;
}

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
</head>
<body>
    <div class="app">
        <div class="quiz">
            <h2 id="question">Question goes here</h2>
            <div id="answer-buttons">
                <button class="btn">Answer 1</button>
                <button class="btn">Answer 2</button>
                <button class="btn">Answer 3</button>
                <button class="btn">Answer 4</button>
            </div>
            <button id="next-btn">Next</button>
        </div>

    </div>

    <script>
    const questions = TEST_DATA;

    const questionElement = document.getElementById("question");
    const answerButtons = document.getElementById("answer-buttons");
    const nextButton = document.getElementById("next-btn");

    let currentQuestionIndex = 0;
    let score = 0;

    function startQuiz() {
        currentQuestionIndex = 0;
        score = 0;
        nextButton.innerHTML = "Next";
        showQuestion();
    }

    function showQuestion() {
        resetState();

        let currentQuestion = questions[currentQuestionIndex];
        let questionNo = currentQuestionIndex + 1;

        questionElement.innerHTML =
            questionNo + ". " + currentQuestion.question;

        currentQuestion.answers.forEach(answer => {
            const button = document.createElement("button");

            button.innerHTML = answer.text;
            button.classList.add("btn");

            if (answer.correct) {
                button.dataset.correct = "true";
            }

            button.addEventListener("click", selectAnswer);
            answerButtons.appendChild(button);
        });
    }

    function resetState() {
        nextButton.style.display = "none";

        while (answerButtons.firstChild) {
            answerButtons.removeChild(answerButtons.firstChild);
        }
    }

    function selectAnswer(e) {
        const selectedBtn = e.target;
        const isCorrect = selectedBtn.dataset.correct === "true";

        if (isCorrect) {
            selectedBtn.classList.add("correct");
            score++;
        } else {
            selectedBtn.classList.add("incorrect");
        }

        Array.from(answerButtons.children).forEach(button => {
            if (button.dataset.correct === "true") {
                button.classList.add("correct");
            }

            button.disabled = true;
        });

        nextButton.style.display = "block";
    }

    function showScore() {
        resetState();

        questionElement.innerHTML =
            `You scored ${score} out of ${questions.length}!`;

        nextButton.innerHTML = "Play Again";
        nextButton.style.display = "block";
    }

    function handleNextButton() {
        currentQuestionIndex++;

        if (currentQuestionIndex < questions.length) {
            showQuestion();
        } else {
            showScore();
        }
    }

    nextButton.addEventListener("click", () => {
        if (currentQuestionIndex < questions.length) {
            handleNextButton();
        } else {
            startQuiz();
        }
    });

    startQuiz();
</script>
</body>
</html>
    """
    # Replace the placeholder with the actual Python data
    html = html.replace("TEST_DATA", test_json)

    st.components.v1.html(html, height=700)
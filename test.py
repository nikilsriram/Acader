import streamlit as st
import json

if "test" not in st.session_state:
    st.session_state.test = None


if st.session_state.test:

    test_data = st.session_state.test

    # Convert Python dictionary → JSON → JavaScript object
    test_json = json.dumps(test_data)

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>Test</title>

        <style>
            * {
                margin: 0;
                padding: 0;
                font-family: 'Poppins', sans-serif;
                box-sizing: border-box;
            }

            body {
                background: #001e4d;
            }

            .app {
                background: #fff;
                width: 90%;
                max-width: 600px;
                margin: 100px auto 0;
                border-radius: 10px;
                padding: 30px;
            }

            .app h1 {
                font-size: 25px;
                color: #001e4d;
                font-weight: 600;
                border-bottom: 1px solid #333;
                padding-bottom: 30px;
            }

            .quiz {
                padding: 20px 0;
            }

            .quiz h2 {
                font-size: 18px;
                color: #001e4d;
                font-weight: 600;
            }

            .btn {
                background: #fff;
                color: #222;
                font-weight: 500;
                width: 100%;
                border: 1px solid #222;
                padding: 10px;
                margin: 10px 0;
                text-align: left;
                border-radius: 4px;
                cursor: pointer;
            }

            .btn:hover {
                background: #222;
                color: #fff;
            }

            #next-btn {
                background: #001e4d;
                color: #fff;
                font-weight: 500;
                width: 150px;
                border: 0;
                padding: 10px;
                margin: 20px auto 0;
                border-radius: 4px;
                cursor: pointer;
            }
        </style>
    </head>

    <body>

        <div class="app">

            <h1>Test</h1>

            <div class="quiz">

                <h2 id="question">Question goes here</h2>

                <div id="answer-buttons">
                </div>

                <button id="next-btn">Next</button>

            </div>

        </div>


        <script>

            // Python test data gets inserted here
            const testData = TEST_DATA;

            // Get the multiple-choice questions
            const questions = testData.multiple_choice;

            console.log(questions);

            let currentQuestionIndex = 0;

            const questionElement = document.getElementById("question");
            const answerButtons = document.getElementById("answer-buttons");
            const nextButton = document.getElementById("next-btn");


            function showQuestion() {

                const currentQuestion = questions[currentQuestionIndex];

                questionElement.innerHTML =
                    (currentQuestionIndex + 1) + ". " +
                    currentQuestion.question;

                answerButtons.innerHTML = "";

                currentQuestion.choices.forEach(choice => {

                    const button = document.createElement("button");

                    button.innerHTML = choice;

                    button.classList.add("btn");

                    answerButtons.appendChild(button);

                });
            }


            showQuestion();

        </script>

    </body>
    </html>
    """

    # Replace the placeholder with the actual Python data
    html = html.replace("TEST_DATA", test_json)

    st.components.v1.html(html, height=700)
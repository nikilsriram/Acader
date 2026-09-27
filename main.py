from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv
import json

load_dotenv()


def load_image(theimage):
    import pytesseract
    from PIL import Image

    img = Image.open(theimage)
    extracted_text = pytesseract.image_to_string(img)

    return extracted_text


subagent = create_agent(
    model="openrouter:anthropic/claude-sonnet-4-6",
    tools=[]
)


@tool(
    "generate_test",
    description="""You are a test-generation specialist.

When given study notes, generate the actual test.
Do not describe or summarize the test.

Generate:
- 10 multiple-choice questions
- 5 true/false questions
- 5 short-answer questions

For each multiple-choice question:
- Provide exactly 4 answer choices.
- One choice must be correct.
- The other 3 choices must be incorrect but plausible distractors.
- Do not make the correct answer obviously longer, shorter, or more detailed than the distractors.
- Do not reveal which choice is correct.

For true/false questions:
- Provide only the statement.
- Do not reveal whether it is true or false.

For short-answer questions:
- Provide only the question.
- Do not provide the answer.

Return ONLY valid JSON in this exact structure:

{
    "multiple_choice": [
        {
            "question": "Question text",
            "choices": [
                "Choice A",
                "Choice B",
                "Choice C",
                "Choice D"
            ]
        }
    ],
    "true_false": [
        {
            "question": "Statement"
        }
    ],
    "short_answer": [
        {
            "question": "Question text"
        }
    ]
}

The JSON must contain exactly 10 multiple-choice questions, 5 true/false questions, and 5 short-answer questions.

Base all questions only on the provided study notes.
Do not add unsupported information.
Do not include markdown or any text outside the JSON.
"""
)
def generate_test(query: str):
    result = subagent.invoke({
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    })

    return result["messages"][-1].content


@tool(
    "generate_flashcards",
    description="""You are a flashcard-generation specialist.

When given study notes, generate exactly 20 flashcards.

Each flashcard MUST contain:
- One question
- One answer

Return ONLY valid JSON in this exact format:

{
    "Question 1": "What is the question?",
    "Answer 1": "This is the answer.",
    "Question 2": "What is the second question?",
    "Answer 2": "This is the second answer.",
    "Question 3": "What is the third question?",
    "Answer 3": "This is the third answer."
}

Continue this pattern through Question 20 and Answer 20.

Do not include markdown, explanations, or any text outside the JSON.
Base all questions and answers only on the provided study notes.
Do not add unsupported information.
"""
)
def generate_flashcards(query: str):
    result = subagent.invoke({
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    })

    content = result["messages"][-1].content

    return json.loads(content)


@tool(
    "generate_notes",
    description="""You are a study-notes specialist.

When given study notes, you MUST generate a clear and organized set of study notes.
Do not simply summarize the original notes.

Rewrite the material so it is easier for a student to understand and study from.

Include:
- Important concepts and definitions
- Key facts and details
- Clear headings and sections
- Important relationships between concepts
- Examples when helpful
- Remove unnecessary repetition or irrelevant information

Keep the information accurate and based only on the provided study material.
Do not add information that is not supported by the notes unless explicitly requested.
"""
)
def generate_notes(query: str):
    result = subagent.invoke({
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    })

    return result["messages"][-1].content


main_agent = create_agent(
    model="openrouter:openai/gpt-oss-20b",
    tools=[
        generate_test,
        generate_flashcards,
        generate_notes
    ],
    system_prompt=(
        "You coordinate specialized sub-agents. "
        "Choose the appropriate sub-agent based on the user's request.\n"
        "Available Agents:\n"
        "- test: generate a test for the user\n"
        "- flashcards: generate a flashcard set for the user\n"
        "- notes: generate well written notes for the user"
    )
)


def generate_test_from_image(uploaded_file):
    extracted_text = load_image(uploaded_file)

    result = main_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": "Generate a test from these notes:\n\n" + extracted_text
            }
        ]
    })

    return json.loads(result["messages"][-1].content)


def generate_flashcards_from_image(uploaded_file):
    extracted_text = load_image(uploaded_file)

    print("OCR COMPLETE")
    print("TEXT LENGTH:", len(extracted_text))

    result = subagent.invoke({
        "messages": [
            {
                "role": "user",
                "content": "Generate a flashcard set from these notes:\n\n" + extracted_text
            }
        ]
    })

    content = result["messages"][-1].content

    print("MODEL OUTPUT:")
    print(repr(content))

    return json.loads(content)


def generate_notes_from_image(uploaded_file):
    extracted_text = load_image(uploaded_file)

    result = main_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": "Generate a comprehensive note guide set from these notes:\n\n" + extracted_text
            }
        ]
    })

    return result["messages"][-1].content
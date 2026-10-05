from langchain.agents import create_tool_calling_agent as create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv
import os
import base64
import json
from langchain_openai import ChatOpenAI


load_dotenv()


def encode_image_to_base64(uploaded_file):
    image_bytes = uploaded_file.getvalue()
    mime_type = uploaded_file.type

    if mime_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise ValueError("Only JPG, PNG, and WEBP images are supported.")

    encoded_string = base64.b64encode(image_bytes).decode("utf-8")

    return encoded_string, mime_type


# Claude through OpenRouter
subagent_model = ChatOpenAI(
    model="anthropic/claude-sonnet-4-6",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

subagent = create_agent(
    model=subagent_model,
    tools=[]
)


@tool(
    "generate_test",
    description="""You are a test-generation specialist.

When given study notes, generate the actual test.

Generate:
- 10 multiple-choice questions
- 5 true/false questions
- 5 short-answer questions

For each multiple-choice question:
- Provide exactly 4 answer choices.
- One choice must be correct.
- The other 3 choices must be incorrect but plausible distractors.
- Do not make the correct answer obviously longer, shorter, or more detailed than the distractors.
- Include the correct answer in the "correct_answer" field.

For true/false questions:
- Provide only the statement.
- Include the correct answer in the "correct_answer" field as either true or false.

For short-answer questions:
- Provide only the question.
- Include the expected answer in the "correct_answer" field.

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
            ],
            "correct_answer": "Choice B"
        }
    ],
    "true_false": [
        {
            "question": "Statement",
            "correct_answer": true
        }
    ],
    "short_answer": [
        {
            "question": "Question text",
            "correct_answer": "Expected answer"
        }
    ]
}

The JSON must contain exactly 10 multiple-choice questions, 5 true/false questions, and 5 short-answer questions.

Base all questions and answers only on the provided study notes.
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
    content = content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "", 1)
        content = content.replace("```", "", 1)
        content = content.strip()

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


# GPT-OSS through OpenRouter
main_agent_model = ChatOpenAI(
    model="openai/gpt-oss-20b",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

main_agent = create_agent(
    model=main_agent_model,
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
    base64_image, mime_type = encode_image_to_base64(uploaded_file)

    result = subagent.invoke({
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Look carefully at this handwritten study-notes image.
Generate a test based ONLY on information visible in the image.

Generate exactly:
- 10 multiple-choice questions, each with 4 choices
- 5 true/false questions
- 5 short-answer questions

Each question must include its correct_answer.
For true/false, correct_answer must be a boolean.
Do not invent information.

Return ONLY valid JSON in this structure:
{
    "multiple_choice": [
        {
            "question": "Question",
            "choices": ["A", "B", "C", "D"],
            "correct_answer": "A"
        }
    ],
    "true_false": [
        {
            "question": "Statement",
            "correct_answer": true
        }
    ],
    "short_answer": [
        {
            "question": "Question",
            "correct_answer": "Answer"
        }
    ]
}

Include exactly 10, 5, and 5 questions respectively.
Do not include Markdown or explanations."""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    })

    content = result["messages"][-1].content

    if not isinstance(content, str):
        raise ValueError("The model returned a non-text response.")

    content = content.strip()

    # Remove Markdown code fences if present.
    if content.startswith("```"):
        lines = content.splitlines()
        if lines and lines[0].strip().lower() in ("```json", "```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        content = "\n".join(lines).strip()

    # Parse the JSON object.
    start = content.find("{")
    if start == -1:
        raise ValueError(
            f"The model returned no JSON object: {content[:200]!r}"
        )

    try:
        test_data, _ = json.JSONDecoder().raw_decode(content[start:])
    except json.JSONDecodeError as e:
        raise ValueError(f"The model returned invalid JSON: {e}") from e

    # Validate the expected sections and counts.
    expected_counts = {
        "multiple_choice": 10,
        "true_false": 5,
        "short_answer": 5,
    }

    if not isinstance(test_data, dict):
        raise ValueError("The generated test must be a JSON object.")

    for section, count in expected_counts.items():
        questions = test_data.get(section)
        if not isinstance(questions, list) or len(questions) != count:
            raise ValueError(
                f"Invalid test: {section} must contain exactly {count} questions."
            )

    # Validate multiple-choice question structure.
    for question in test_data["multiple_choice"]:
        if (
            not isinstance(question, dict)
            or not isinstance(question.get("question"), str)
            or not isinstance(question.get("choices"), list)
            or len(question["choices"]) != 4
            or not isinstance(question.get("correct_answer"), str)
            or question["correct_answer"] not in question["choices"]
        ):
            raise ValueError("A multiple-choice question has an invalid structure.")

    # Validate true/false answers.
    for question in test_data["true_false"]:
        if (
            not isinstance(question, dict)
            or not isinstance(question.get("question"), str)
            or type(question.get("correct_answer")) is not bool
        ):
            raise ValueError("A true/false question has an invalid structure.")

    # Validate short-answer questions.
    for question in test_data["short_answer"]:
        if (
            not isinstance(question, dict)
            or not isinstance(question.get("question"), str)
            or not isinstance(question.get("correct_answer"), str)
        ):
            raise ValueError("A short-answer question has an invalid structure.")

    return test_data


def generate_flashcards_from_image(uploaded_file):
    base64_image, mime_type = encode_image_to_base64(uploaded_file)

    result = subagent.invoke({
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Look carefully at this handwritten study-notes image.

Use ONLY the information contained in the image to generate exactly 20 flashcards.

The response MUST begin with { and end with }.

DO NOT use Markdown.
DO NOT use ```json.
DO NOT use headings.
DO NOT use bullet points.
DO NOT write "Flashcard Set".
DO NOT write "Card 1".
DO NOT write Q: or A:.
DO NOT include any explanation.

Each flashcard must contain one question and one answer.

Use this exact structure:

{
    "Question 1": "question",
    "Answer 1": "answer",
    "Question 2": "question",
    "Answer 2": "answer",
    "Question 3": "question",
    "Answer 3": "answer"
}

Continue through Question 20 and Answer 20.

IMPORTANT:
- Base every flashcard ONLY on the handwritten notes.
- Do NOT invent information.
- Do NOT use outside knowledge.
- Make the questions directly relevant to the notes."""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    })

    content = result["messages"][-1].content

    print("MODEL OUTPUT:")
    print(repr(content))

    content = content.strip()

    if content.startswith("```json"):
        content = content[7:]
    elif content.startswith("```"):
        content = content[3:]

    if content.endswith("```"):
        content = content[:-3]

    content = content.strip()

    if not content.startswith("{"):
        raise ValueError(
            "Model did not return JSON. Model output was:\n" + content
        )

    return json.loads(content)


def generate_notes_from_image(uploaded_file):
    base64_image, mime_type = encode_image_to_base64(uploaded_file)

    result = subagent.invoke({
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Look carefully at this handwritten study-notes image.

Generate a comprehensive review guide that will make sure the individual masters the concepts."""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    })

    return result["messages"][-1].content
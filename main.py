from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv
import os
import base64
import json

load_dotenv()


def encode_image_to_base64(uploaded_file):
    image_bytes = uploaded_file.getvalue()
    mime_type = uploaded_file.type

    if mime_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise ValueError("Only JPG, PNG, and WEBP images are supported.")

    encoded_string = base64.b64encode(image_bytes).decode("utf-8")

    return encoded_string, mime_type


subagent = create_agent(
    model="openrouter:anthropic/claude-sonnet-4-6",
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
    base64_image, mime_type = encode_image_to_base64(uploaded_file)

    result = subagent.invoke({
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Look carefully at this handwritten study-notes image.

First, understand and transcribe the handwritten content as accurately as possible.

Then generate a test based ONLY on the information actually present in the image.

Generate exactly:
- 10 multiple-choice questions
- 5 true/false questions
- 5 short-answer questions

For multiple-choice questions:
- Exactly 4 choices.
- Exactly 1 correct answer.
- The other 3 choices must be plausible but incorrect.
- Include the correct answer in "correct_answer".

For true/false questions:
- Include "correct_answer" as true or false.

For short-answer questions:
- Include the expected answer in "correct_answer".

IMPORTANT:
- Do NOT invent information that is not visible in the notes.
- Do NOT generate questions about unrelated topics.
- If handwriting is unclear, use the surrounding context to interpret it.
- Base every question directly on the handwritten notes.

Return ONLY valid JSON.
Do NOT use Markdown.
Do NOT use ```json.
Do NOT include explanations.

Use exactly this structure:

{
    "multiple_choice": [
        {
            "question": "Question",
            "choices": [
                "Choice A",
                "Choice B",
                "Choice C",
                "Choice D"
            ],
            "correct_answer": "Choice A"
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

You MUST generate exactly 10 multiple-choice, 5 true/false, and 5 short-answer questions."""
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
    and generate a comprehensive review guide that will make sure the individual masters the concepts."""
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
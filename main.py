from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()



def load_image(theimage):
    import pytesseract
    from PIL import Image

    img = Image.open(theimage)
    extracted_text = pytesseract.image_to_string(img)

    return extracted_text




subagent = create_agent(model="openrouter:anthropic/claude-sonnet-4-6", tools=[])

# Wrap it as a tool  
@tool("generate_test", description="""You are a test-generation specialist.

When given study notes, you MUST generate the actual test.
Do not describe or summarize the test.

Output the complete questions that the student will answer.
Include:
- 10 multiple-choice questions
- 5 true/false questions
- 5 short-answer questions

Do not provide the answers unless explicitly requested.
""")
def generate_test(query: str):
    result = subagent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content

# Wrap it as a tool  
@tool("generate_flashcards", description="""You are a flashcard-generation specialist.

When given study notes, you MUST generate the actual flashcards.
Do not describe or summarize the flashcards.

Output complete flashcards that the student can study from.
Include:

* 20 flashcards
* A clear question or term on the front
* A concise, accurate answer on the back
* Cover the most important concepts from the provided notes
* Avoid duplicate or overly similar flashcards

Do not provide additional explanations unless explicitly requested.
""")
def generate_flashcards(query: str):
    result = subagent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


# Wrap it as a tool  
@tool("generate_notes", description="""You are a study-notes specialist.

When given study notes, you MUST generate a clear and organized set of study notes.
Do not simply summarize the original notes.

Rewrite the material so it is easier for a student to understand and study from.
Include:

* Important concepts and definitions
* Key facts and details
* Clear headings and sections
* Important relationships between concepts
* Examples when helpful
* Remove unnecessary repetition or irrelevant information

Keep the information accurate and based only on the provided study material.
Do not add information that is not supported by the notes unless explicitly requested.
""")
def generate_notes(query: str):
    result = subagent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


# Main agent with subagent as a tool  
main_agent = create_agent(model="openrouter:openai/gpt-oss-20b", 
                          tools=[generate_test, generate_flashcards, generate_notes], 
                          system_prompt=(f"You coordinate specialized sub-agents. "
    "Choose the appropriate sub-agent based on the user's request.\n"
    "Available Agents:\n"
    "- test: generate a test for the user"
    "- flashcards: generate a flashcard set for the user"
    "- notes: generate well written notes for the user"))



def generate_test_from_image(uploaded_file):
    extracted_text = load_image(uploaded_file)
    print("hello")
    result = main_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": "Generate a test from these notes:\n\n" + extracted_text,
            }
        ]
    })
    return result["messages"][-1].content
from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv
import pytesseract
from PIL import Image

load_dotenv()

img = Image.open("./yeahyeha.jpg")
extracted_text = pytesseract.image_to_string(img)

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

# Main agent with subagent as a tool  
main_agent = create_agent(model="openrouter:anthropic/claude-sonnet-4-6", 
                          tools=[generate_test], 
                          system_prompt=(f"You coordinate specialized sub-agents. "
    "Choose the appropriate sub-agent based on the user's request.\n"
    "Available Agents:\n"
    "- test: generate a test for the user"))

result = main_agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "Generate a test from these notes:\n\n" + extracted_text
        }
    ]
})

print(result["messages"][-1].content)
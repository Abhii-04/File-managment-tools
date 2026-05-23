import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from groq import Groq
from call_function import AVAILABLE_FUNCTIONS, call_function,call_function

load_dotenv()

PROJECT_ROOT = os.path.abspath("./") 
DEFAULT_WORKING_DIR='.'
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
MAX_TURNS = 1000

SYSTEM_PROMPT = """
You are a file system assistant.

You have access to tools. You MUST use them.

Rules:
- DO NOT generate shell commands.
- DO NOT explain what to do.
- ALWAYS call the appropriate function.

Available tools:
- get_files_info → list files
- get_file_content → read file
- write_file → write file
- run_python_file → execute python

Examples:

User: list all files  
→ call get_files_info

User: read main.py  
→ call get_file_content

Only respond using function calls.
""".strip()


CONFIG = types.GenerateContentConfig(
    tools=[AVAILABLE_FUNCTIONS],
    system_instruction=SYSTEM_PROMPT,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt",type=str,help='user_prompt')
    parser.add_argument(
        "--working_dir",
        default = DEFAULT_WORKING_DIR,
        help="working directory for tool exeution"
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="groq model name",
    )
    return parser.parse_args()

def extract_function_calls(response):
    function_calls = []

    for candidate in getattr(response, "candidates", []) or []:
        content = getattr(candidate, "content", None)
        if not content:
            continue

        for part in content.parts or []:
            function_call = getattr(part, "function_call", None)
            if function_call:
                function_calls.append(function_call)

    return function_calls
def run_agent(client, model, user_prompt, working_dir):
    contents = [types.UserContent(parts=[types.Part(text=user_prompt)])]

    for _ in range(MAX_TURNS):
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=CONFIG,
        )

        function_calls = extract_function_calls(response)
        if not function_calls:
            return response.text

        if not response.candidates or not response.candidates[0].content:
            return "Model returned an empty response."

        contents.append(response.candidates[0].content)

        for function_call_part in function_calls:
            tool_content = call_function(function_call_part, working_dir)
            contents.append(tool_content)

    return "Agent stopped after reaching the maximum number of tool-calling turns."


def main():
    args = parse_args()
    client = genai.Client()
    print(run_agent(client, args.model, args.user_prompt, args.working_dir))


if __name__ == "__main__":
    main()

import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

parser = argparse.ArgumentParser()
parser.add_argument("prompt")
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()

system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    messages = [
        types.Content(role = "user", parts = [types.Part(text = args.prompt)])
    ]

    response = client.models.generate_content(
    model = 'gemini-2.0-flash-001', contents = messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt)
    )

    if args.verbose:
        print(f"User prompt: {args.prompt}")
        print(f"{response.text}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(response.text)


if __name__ == "__main__":
    try:
        prompt = sys.argv[1]
    except IndexError:
        print("Prompt not provided.")
        sys.exit(1)
    main()

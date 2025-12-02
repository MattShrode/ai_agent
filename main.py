import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function

parser = argparse.ArgumentParser()
parser.add_argument("prompt")
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

def main():
    messages = [
        types.Content(role = "user", parts = [types.Part(text = args.prompt)])
    ]

    max_calls = 0

    if args.verbose:
        print(f"User prompt: {args.prompt}")

    try:

        while(max_calls < 20):

            max_calls += 1

            response = client.models.generate_content(
            model = 'gemini-2.0-flash-001', contents = messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt)
            )

            for candidate in response.candidates:
                messages.append(candidate.content)

            has_calls = bool(response.function_calls)

            if args.verbose:
                if not has_calls and response.text:
                    print(response.text)
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            if has_calls:
                response_list = []
                for part in response.function_calls:
                    result = call_function(part, verbose = args.verbose)
                    if (not result.parts or
                        not result.parts[0].function_response):
                        raise Exception(f"An error occured calling {part.name}.")
                    response_list.append(result.parts[0])
                    if args.verbose:
                        print(f"-> {result.parts[0].function_response.response}")
                
                messages.append(
                    types.Content(role = "user", parts = response_list)
                )
            else:
                if response.text:
                    print(response.text)
                    break

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        prompt = sys.argv[1]
    except IndexError:
        print("Prompt not provided.")
        sys.exit(1)
    main()

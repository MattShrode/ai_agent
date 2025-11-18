import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    result_string = ""

    full_file_path = os.path.join(working_directory, file_path)
    abs_full_path = os.path.abspath(full_file_path)
    abs_working_dir = os.path.abspath(working_directory)

    if not abs_full_path.startswith(abs_working_dir):
        result_string = f'Error: Cannot read "{file_path}" as it is outside the permitted working directory.'
        return result_string
    
    if not os.path.isfile(abs_full_path):
        result_string = f'Error: File not found, or is not a regular file: "{file_path}"'
        return result_string
    
    try:
        with open(abs_full_path, "r") as f:
            result_string = f.read()
        if len(result_string) > MAX_CHARS:
            truncated_string = result_string[:10000] + f'[...File "{file_path}" truncated at 10000 characters]'
            return truncated_string
        else:
            return result_string

    except Exception as e:
        return f"Error reading file: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read and return the contents of the file indicated by the file path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
        },
    ),
)
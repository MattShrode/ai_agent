import os

import sys
sys.path.append('../ai_agent')
#from ai_agent.config import MAX_CHARS

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
        pass

    except Exception as e:
        return f"Error reading file: {e}"
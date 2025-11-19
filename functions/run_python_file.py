import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):

    if args is None:
        args = []
    
    full_file_path = os.path.join(working_directory, file_path)
    abs_full_path = os.path.abspath(full_file_path)
    abs_working_dir = os.path.abspath(working_directory)

    if not abs_full_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
    
    if not os.path.isfile(abs_full_path):
        return f'Error: File "{file_path}" not found.'
    
    root, ext = os.path.splitext(file_path)
    if not ext == ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(["python", file_path] + args, cwd=abs_working_dir, capture_output=True, timeout=30, text=True)
        
        if not result.stdout and not result.stderr and result.returncode == 0:
            return "No output produced."
        
        formatted_result = (
            f'STDOUT: {result.stdout}\n' +
            f'STDERR: {result.stderr}\n'
        )

        if not result.returncode == 0:
            formatted_result += f"Process exited with code {result.returncode}"
        
        return formatted_result
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute the Python file indicated by the file path, with optional arguments if provided.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional command-line arguments to pass to the script.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)
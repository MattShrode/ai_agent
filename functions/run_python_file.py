import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    
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
    except Exception as e:
        return f"Error: executing Python file: {e}"
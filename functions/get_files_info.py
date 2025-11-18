import os
from google.genai import types

def get_files_info(working_directory, directory="."):

    full_path = os.path.join(working_directory, directory)

    absolute_working_dir = os.path.abspath(working_directory)

    absolute_full_path = os.path.abspath(full_path)

    results = []

    if directory == ".":
        results.append(f"Results for current directory:")
    else:
        results.append(f"Results for {directory} directory:")

    if not absolute_full_path.startswith(absolute_working_dir):
        results.append(f'   Error: Cannot list "{directory}" as it is outside the permitted working directory.')
    elif not os.path.isdir(absolute_full_path):
        results.append(f'   Error: "{directory}" is not a directory.')
    else:
        dir_contents = os.listdir(absolute_full_path)
 
        for item in dir_contents:
            item_path = os.path.join(absolute_full_path, item)
            size = os.path.getsize(item_path)
            is_dir_flag = os.path.isdir(item_path)

            results.append(f"- {item}: file_size={size} bytes, is_dir={is_dir_flag}")

    output = "\n".join(results)
    return output

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
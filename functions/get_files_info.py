import os

def get_files_info(working_directory, directory="."):

    full_path = os.path.join(working_directory, directory)

    absolute_working_dir = os.path.abspath(working_directory)

    absolute_full_path = os.path.abspath(full_path)

    if not absolute_full_path.startswith(absolute_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory.'

    if not os.path.isdir(absolute_full_path):
        return f'Error: "{directory}" is not a directory.'
    
    return "Success."
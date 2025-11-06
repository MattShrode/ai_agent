import os

def get_files_info(working_directory, directory="."):

    full_path = os.path.join(working_directory, directory)
    print(full_path)

    if not full_path.startswith(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory.'

    absolute_full_path = os.path.abspath(full_path)
    print(absolute_full_path)

    isdir = os.path.isdir(absolute_full_path)
    print(isdir)

    if not os.path.isdir(absolute_full_path):
        return f'Error: "{directory}" is not a directory.'
    
    return "Success."
    

file_path = get_files_info("calculator", "pkg")
print(file_path)
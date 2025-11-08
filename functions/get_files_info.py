import os

def get_files_info(working_directory, directory="."):

    full_path = os.path.join(working_directory, directory)

    absolute_working_dir = os.path.abspath(working_directory)

    absolute_full_path = os.path.abspath(full_path)

    if not absolute_full_path.startswith(absolute_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory.'

    if not os.path.isdir(absolute_full_path):
        return f'Error: "{directory}" is not a directory.'

    dir_contents = os.listdir(absolute_full_path)

    results = []

    if directory == ".":
        results.append(f"Results for current directory:")
    else:
        results.append(f"Results for {directory} directory:")
    
    for item in dir_contents:
        item_path = os.path.join(absolute_full_path, item)
        size = os.path.getsize(item_path)
        is_dir_flag = os.path.isdir(item_path)

        results.append(f"- {item}: file_size={size} bytes, is_dir={is_dir_flag}")

    output = "\n".join(results)
    return output
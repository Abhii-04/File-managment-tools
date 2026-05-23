import os
from google.genai import types
PROJECT_ROOT = os.path.abspath("./") 
def get_files_info(directory:None,working_directory=PROJECT_ROOT):
    abs_working_dir = os.path.abspath(working_directory)

    if directory is None:
        abs_directory = abs_working_dir
    else:
        abs_directory = os.path.abspath(os.path.join(abs_working_dir,directory))

    if not abs_directory.startswith(abs_working_dir):
        raise ValueError("the directory must be within the working directory")
    
    if not os.path.isdir(abs_directory):
        return f"{directory or '.'} is not a valid directory"
    

    final_response=""
    content = os.listdir(abs_directory)

    for content in content:
        content_path = os.path.join(abs_directory,content)
        is_dir=os.path.isdir(content_path)
        size = os.path.getsize(content_path)

        final_response += f"{content} - {'Directory' if is_dir else 'File'} - Size: {size} bytes\n"
    
    return final_response

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

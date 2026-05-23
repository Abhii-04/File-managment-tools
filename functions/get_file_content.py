import os
from google.genai import types

MAX_CHARS=2000
def get_file_content(working_directory,filepath:None):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir,filepath))
    if filepath is None:
        abs_file_path = abs_working_dir
    else:
        abs_file_path = os.path.abspath(os.path.join(abs_working_dir,filepath))

    if not abs_file_path.startswith(abs_working_dir):
        raise ValueError("the file must be within the working directory")
    
    if not os.path.isfile(abs_file_path):
       return f"{filepath or '.'} is not a valid file"


    try: 
        with open(abs_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            if(len(content)>=MAX_CHARS):
                content += "\n...(truncated)"

            return content
    except Exception as e:
        return f"Error reading file: {str(e)}"
    

schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

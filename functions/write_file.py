import os 
from google.genai import types


def write_file(working_directory,filepath:None,content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir,filepath))


    if filepath is None:
        abs_directory = abs_working_dir
    else:
        abs_directory = os.path.abspath(os.path.join(abs_working_dir,filepath))

    if not abs_directory.startswith(abs_working_dir):
        raise ValueError("the directory must be within the working directory")
    
    try:
        with open(abs_file_path,"w") as f:
            f.write(content)
        return f"succesfully wrote to {filepath}."
    except Exception as e:
        parent_dir = os.path.dirname(abs_file_path)

    try:
        os.makedirs(parent_dir,exist_ok=True)
    except Exception as e:
        return f"could not create parent directory: {parent_dir}, error:{e}"
    

    try:
        with open(abs_file_path,"w") as f:
            f.write(content)
        return f"succesfully wrote to {filepath} after creating parent directory."
    except Exception as e:
        return f"error writing to file after creating parent directory.{e}"
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file relative to the working directory, creating parent directories if necessary",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)



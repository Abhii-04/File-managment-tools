import os
import subprocess
from google.genai import types


def run_python_file(working_directory,filepath:None,args:None):
    if args is None:
        args = []
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
        final_args = ["python3", abs_file_path]
        final_args.extend(args)

        output = subprocess.run(
            final_args,
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True,
        )

        stdout = output.stdout.decode()
        stderr = output.stderr.decode()

        final_string = f"""
STDOUT:
{stdout}

STDERR:
{stderr}
"""

        if output.returncode != 0:
            final_string += f"\nprocess exited with code {output.returncode}"

        if stdout == "" and stderr == "":
            return "no output produced"

        return final_string

    except Exception as e:
        return f"Error running python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified Python file relative to the working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Python file path to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional command-line arguments passed to the Python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)

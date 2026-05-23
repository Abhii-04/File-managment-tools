from google.genai import types

from functions.get_file_content import get_file_content, schema_get_files_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file


AVAILABLE_FUNCTIONS = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_files_content,
        schema_write_file,
        schema_run_python_file,
    ]
)


FUNCTIONS = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


def execute_function_call(function_call_part, working_directory):
    function_name = function_call_part.name
    function_args = dict(function_call_part.args or {})
    function = FUNCTIONS.get(function_name)

    if function is None:
        return {"error": f"Unknown function: {function_name}"}

    try:
        return {"result": function(working_directory, **function_args)}
    except Exception as exc:
        return {"error": str(exc)}


def call_function(function_call_part, working_directory):
    return types.Content(
        role="user",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response=execute_function_call(function_call_part, working_directory),
            )
        ],
    )

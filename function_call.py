import json
from collections.abc import Callable
from functions.list_files import schema_list_files, list_files
from functions.read_file import schema_read_file, read_file
from functions.write_file import schema_write_file, write_file
from functions.run_file import schema_run_file, run_file

available_functions = [
    schema_list_files,
    schema_read_file,
    schema_write_file,
    schema_run_file,
]

function_map: dict[str, Callable[..., str]] = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "run_file": run_file,
}

def call_function(tool_call, verbose: bool = False) -> dict:
    name = tool_call.function.name
    functionn = function_map.get(name)
    if functionn == None:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {name}",
        }
    args = json.loads(tool_call.function.arguments or "{}")
    if verbose:
        print(f" - Calling function: {name}({args})")
    else:
        print(f" - Calling function: {name}")

    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": functionn('.', **args)
    }


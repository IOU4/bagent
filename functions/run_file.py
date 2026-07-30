import os
import subprocess
def run_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        base_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(base_dir, file_path))
        if not os.path.commonpath([base_dir, target_file]) == base_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if not args == None:
            command.extend(args)

        result = ""
        run = subprocess.run(args=command, cwd=base_dir, capture_output=True, text=True, timeout=30)
        if not run.returncode == 0:
            result += f"Process exited with code {run.returncode}"
        if run.stdout == "" and run.stderr == "":
            result += "No output produced"
        if not run.stdout == "":
            result += f'STDOUT: {run.stdout}'
        if not run.stderr == "":
            result += f'STDERR: {run.stderr}'
        
        return result

    except Exception as e:
        return f'Error: Exception {e}'

schema_run_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "run/execute a python file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "the path to the file to run relative to the working directory"
                },
                "args": {
                    "type": "array",
                    "items": "string",
                    "description": "list of arguments to pass to the python script"
                }
            }
        }
    }
}

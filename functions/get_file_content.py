import os

def get_file_content(working_directory: str, file_path: str) -> str:
    MAX_CHARS = 10000
    try:
        abs_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_dir, file_path))
        if not os.path.commonpath([abs_dir, target_file]) == abs_dir:
            return f'Error: Cannot read "{target_file}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{target_file}"'

        file = open(target_file)
        content = file.read(MAX_CHARS)
        if file.read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return content

    except Exception as e:
        return f'Error: Exception {e}'

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "read the contents of a file, limited to the first 10000 characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "the path to the file to read the contents of relative to the working directory"
                }
            }
        }
    }
}

from os import path, makedirs

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try: 
        base_dir = path.abspath(working_directory)
        target_file = path.normpath(path.join(base_dir, file_path))
        if not path.commonpath([base_dir, target_file]) == base_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        makedirs(path.dirname(target_file), exist_ok=True)
        with open(target_file, mode='w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Exception {e}'

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "overrites or creates the file in the requested file path with the provided content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "the path to the file to overrite or create relative to the working directory"
                },
                "content": {
                    "type": "string",
                    "description": "the new contents of the file, old content if exists is deleted"
                }
            }
        }
    }
}

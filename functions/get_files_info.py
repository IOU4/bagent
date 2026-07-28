import os
def get_files_info(working_directory: str, directory: str = "."):
    try:
        abs_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_dir, directory))
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        is_valid_target_dir = os.path.commonpath([abs_dir, target_dir]) == abs_dir
        if not is_valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        contents = os.listdir(target_dir)
        result = ""
        for item in contents:
            path = os.path.join(target_dir, item)
            result += f"- {item}: file_size={os.path.getsize(path)}, is_dir={os.path.isdir(path)}\n"

        return result
    except Exception as e:
            return f'Error: Exception {str(e)}'

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "lists files of directory relative to the working directory, provides file size and if it's a directory",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory to list files from, relative to the working directory default is the working directory itself"
                }
            }
        }
    }
}

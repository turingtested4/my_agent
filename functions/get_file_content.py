import os

MAX_CHARS = 10000
schema_get_files_content= {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "get the content of the files",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list content from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}




def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        path_w = os.path.abspath(working_directory)
        path_s = os.path.abspath(os.path.join(working_directory, file_path))
        common = os.path.commonpath([path_w, path_s])

        if os.path.isfile(path_s):
            if common == path_w:
                with open(path_s, "r") as f:
                    content = f.read(MAX_CHARS)
                    if f.read(1):
                        content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                    return content
            else:
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        else:
            return f'Error: File not found or is not a regular file: "{file_path}"'
    except Exception as e:
        return f"Error: {e}"

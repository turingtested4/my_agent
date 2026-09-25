import os



schema_write_file= {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "write into a file",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Runs the python file",
                },
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        path_w = os.path.abspath(working_directory)
        path_file = os.path.abspath(os.path.join(working_directory, file_path))
        common = os.path.commonpath([path_w, path_file])

        # Guard 1: Is it outside the permitted directory?
        if common != path_w:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Guard 2: Is it pointing to an existing directory instead of a file?
        if os.path.isdir(path_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Action: Ensure parent directories exist
        os.makedirs(os.path.dirname(path_file), exist_ok=True)

        # Action: Write to the file and return success message
        with open(path_file,"w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"

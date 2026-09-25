import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_directory, directory="."):
    lista = []
    try:
        working_dir_abs = os.path.abspath(working_directory)
        clean_path = os.path.normpath(os.path.join(working_dir_abs, directory))
        if os.path.commonpath([working_dir_abs, clean_path]) == working_dir_abs:
            if os.path.isdir(clean_path) == False:
                return f'Error: "{directory}" is not a directory'
            else:
                for f in os.listdir(clean_path):
                    path = os.path.join(clean_path, f)
                    lista.append(
                        f"- {f}: file_size={os.path.getsize(os.path.abspath(path))} bytes, is_dir={os.path.isdir(path)}"
                    )
                return "\n".join(lista)
        else:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: {e}"

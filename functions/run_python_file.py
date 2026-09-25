import os
import subprocess



schema_run_python_file= {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "run a python file",
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



def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:

        path_w = os.path.abspath(working_directory)
        path_file = os.path.abspath(os.path.join(working_directory, file_path))
        common = os.path.commonpath([path_w, path_file])

        # Guard 1: Is it outside the permitted directory?
        if common != path_w:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Clean and idiomatic: Guard clause checks for failure early
        if not os.path.isfile(path_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", path_file]
        if args:
            command.extend(args)

        result = subprocess.run(command,cwd=path_w,capture_output=True,text=True,timeout=30)

        output = []

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"

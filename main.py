import argparse
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from functions import call_function
from functions.call_function import available_functions
from functions.get_files_info import get_files_info

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


def setupagent(api_key):
    print("Hello from agent!")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    return client


def pregunta(client, args):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions
    )



    return response

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("I can find the api key bro")
    else:
        client = setupagent(api_key)
        respond = pregunta(
            client,
            args,
        )
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            if respond.usage is not None:
                print(f"Prompt tokens: {respond.usage.prompt_tokens}")
                print(f"Response tokens: {respond.usage.completion_tokens}")

        message = respond.choices[0].message
        if( message.tool_calls):
            print(message.tool_calls)
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                print(f"Calling function: {tool_call.function.name}({function_args})")
        else:
            print(f"Response:\n{respond.choices[0].message.content}")





if __name__ == "__main__":
    main()

import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI 
from openai.types import Completion, CompletionChoice, CompletionUsage
from function_call import available_functions, call_function
from system import system_prompt


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key == None:
        raise RuntimeError("no api key found!")

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    parser = argparse.ArgumentParser(description={"bagent"})
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="vebooose af")
    args = parser.parse_args()
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt}
    ]

    for _ in range(20):
        response = client.chat.completions.create(
            model = "deepseek/deepseek-v4-flash",
            messages = messages,
            tools=available_functions
        )
        message = response.choices[0].message
        if message.tool_calls:
            messages.append(message.model_dump(exclude_none=True))
            for tool_call in message.tool_calls:
                messages.append(call_function(tool_call, args.verbose))
            continue

        if response.usage == None:
            raise RuntimeError("Api error!")

        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Model Used: {response.model}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
            print(f"Response: {response.choices[0].message.content}")
        else:
            print(response.choices[0].message.content)

        return 
    exit(1)

if __name__ == "__main__":
    main()

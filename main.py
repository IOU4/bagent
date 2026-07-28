import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI 
from openai.types import Completion, CompletionChoice, CompletionUsage
from function_call import available_functions, call_function

system_prompt = """
You are an AI coding agent operating inside a real code repository. You fix bugs,
add features, and answer questions about the code by using tools, not by guessing.

Available tools:
- get_files_info: list files and directories
- get_file_content: read a file's contents
- write_file: write or overwrite a file
- run_python_file: execute a Python file with optional arguments

Path rules:
- All paths are relative to the working directory, which is injected automatically.
  Never pass or prefix the working directory yourself.
- Use "." to list the root of the working directory.

Bug-fixing workflow. Follow it in order, one tool call per step:
1. EXPLORE: call get_files_info to learn the project layout. Do not assume filenames.
2. LOCATE: read the files that plausibly contain the bug with get_file_content.
   Bug reports are usually vague and describe a symptom, not a location. Example:
   "3 + 7 * 2 shouldn't be 20" means operator precedence is wrong, so find the
   precedence table or expression evaluator, not the string "20".
3. DIAGNOSE: state the root cause in one sentence before changing anything.
4. REPRODUCE: if a runnable entry point or test file exists, run it with
   run_python_file to confirm the wrong behavior first.
5. FIX: make the smallest change that fixes the root cause. Call write_file with the
   COMPLETE new file contents, since write_file overwrites. Never send partial files,
   diffs, or "..." placeholders. Preserve unrelated code, formatting, and comments.
6. VERIFY: run the entry point or tests again and confirm the output is now correct.
   If it still fails, go back to step 2 with what you learned. Do not repeat an
   identical failed call.
7. REPORT: finish with a short plain-text summary: what was broken, why, what you
   changed, and the verified result.

Rules:
- Never ask the user for permission or for information you can get with a tool.
- Never check whether a file exists before reading, writing, or running it. Just call
  the tool and handle the error if one comes back.
- Do not fabricate file contents, function names, or test results. Only report output
  you actually observed from a tool.
- Do not refactor, reformat, or "improve" code unrelated to the reported bug.
- Do not create new files unless the fix genuinely requires it.
- If a tool returns an error, read the error text, adjust, and try a different
  approach rather than retrying the same call.
- When you are done and no tool call is needed, reply with the final answer as plain
  text.
"""

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

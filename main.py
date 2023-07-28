import openai
import os
import sys
import argparse
from colorama import Fore, Style

MODEL="gpt-3.5-turbo"
#MODEL="gpt-4-0613"
MAX_TOKENS=256
TEMPERATURE=1

def concatenate_arguments(*args):
    return ' '.join(map(str, args))

def setup_openai():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environmental variable.")
    openai.api_key = api_key

def interact_with_gpt(messages):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )
    return response['choices'][0]['message']['content'].strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", action="store_true", help="Print 'Hello, World!' and exit")
    parser.add_argument("text", nargs="*", help="Text to send to ChatGPT")
    args = parser.parse_args()

    setup_openai()

    if args.c:
        print("Hello, World!")
        return

    prompt_args = concatenate_arguments(*args.text)

    if prompt_args:
        response = interact_with_gpt(messages=[{"role": "user", "content": prompt_args}])
        print(response)
        return

    print("Welcome to ChatGPT CLI. Type 'exit' to end the conversation. Using model: " + MODEL)
    
    conversation = []
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        conversation.append({"role": "user", "content": user_input})
        response = interact_with_gpt(messages=conversation)
        conversation.append({"role": "assistant", "content": response})
        print(Fore.GREEN + "ChatGPT: " + response + Style.RESET_ALL)

if __name__ == "__main__":
    main()

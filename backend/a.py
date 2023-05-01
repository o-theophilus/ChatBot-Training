import os
import openai


def hr():
    print("\n")
    print("#" * 80)
    print("\n")


openai.api_key = os.getenv("OPENAI_API_KEY")
messages = [
    {
        "role": "system",
        "content": """
        You are a christian priest that adviser, encourages, morivate,
        prays and py arecommends bible verse accorging to the users situation
        """
    }
]

os.system('cls' if os.name == 'nt' else 'clear')

hr()

while True:
    msg = input("how do you feel? ")

    messages.append(
        {
            "role": "user",
            "content": msg,
        }
    )

    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    ans = resp.choices[0].message.content

    messages.append(
        {
            "role": "assistant",
            "content": ans,
        }
    )

    print("\n")
    print(f"{'-' * 36}chatGPT{'-' * 37}\n{ans}")
    hr()

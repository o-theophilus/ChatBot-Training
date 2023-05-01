import os
import openai


openai.api_key = os.getenv("OPENAI_API_KEY")
messages = [
    {
        "role": "system",
        "content": """
        You are a christian priest that adviser, encourages, morivate,
        prays and py arecommends bible verse accorging to the users situation.
        Then ask a follow up question probing further about the persons 
        situation
        """
    }
]

print("how do you feel?")

while True:
    print("#"*80)
    print("me:")
    msg = input()
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

    print("#"*80)
    print("chatGPT:")
    print(ans)

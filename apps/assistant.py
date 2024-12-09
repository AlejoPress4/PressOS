import os

from groq import Groq

client = Groq(
    api_key=os.environ.get("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"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)
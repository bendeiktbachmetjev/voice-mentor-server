import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(transcript):
    messages = [
        {"role": "system", "content": "Ты коуч. Дай короткий, доброжелательный комментарий по речи пользователя."},
        {"role": "user", "content": transcript}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return response.choices[0].message["content"]

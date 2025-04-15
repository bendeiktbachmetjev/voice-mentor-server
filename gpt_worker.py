import os
import requests

def get_coaching_advice(transcript):
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError('OPENAI_API_KEY not set in environment')
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
    )
    return response.choices[0].message["content"].strip()

def get_coaching_advice(transcript):
    return generate_response(transcript)

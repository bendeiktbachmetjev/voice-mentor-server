import openai
from app.config import Config

def generate_response(text, system_prompt="You are a helpful assistant.", temperature=0.7, max_tokens=1000):
    """
    Generate response using GPT-3.5
    
    Args:
        text (str): Input text to generate response for
        system_prompt (str): System message to set the behavior of the assistant
        temperature (float): Controls randomness (0.0 to 1.0)
        max_tokens (int): Maximum number of tokens to generate
        
    Returns:
        str: Generated response from GPT-3.5
        
    Raises:
        ValueError: If API key is not set or input text is empty
        Exception: For other errors during response generation
    """
    # Input validation
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")
    
    if not Config.OPENAI_API_KEY:
        raise ValueError("OpenAI API key is not set in environment variables")
    
    if not 0 <= temperature <= 1:
        raise ValueError("Temperature must be between 0 and 1")
    
    if max_tokens <= 0:
        raise ValueError("Max tokens must be greater than 0")
    
    try:
        # Call GPT-3.5 API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=Config.OPENAI_API_KEY
        )
        
        # Extract and return the response
        return response.choices[0].message.content.strip()
        
    except openai.error.AuthenticationError:
        raise Exception("Invalid OpenAI API key")
    except openai.error.RateLimitError:
        raise Exception("Rate limit exceeded. Please try again later")
    except openai.error.InvalidRequestError as e:
        raise Exception(f"Invalid request to OpenAI API: {str(e)}")
    except openai.error.APIError as e:
        raise Exception(f"OpenAI API error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error in response generation: {str(e)}") 
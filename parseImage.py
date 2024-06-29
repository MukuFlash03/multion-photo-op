
import base64
from anthropic import Anthropic
import os
import httpx
from IPython.display import Image
from dotenv import load_dotenv

load_dotenv()

claude_api_key = os.getenv('CLAUDE_API_KEY')

client = Anthropic(
    api_key=claude_api_key,
)
MODEL_NAME = "claude-3-opus-20240229"

# Image as a file
def parseImageFile(imageFilepath):
    with open(imageFilepath, "rb") as image_file:
        binary_data = image_file.read()
        base_64_encoded_data = base64.b64encode(binary_data)
        base64_string = base_64_encoded_data.decode('utf-8')
    return base64_string

# Image as a URL
def parseImageURL(imageUrl):
    base_64_encoded_data = base64.b64encode(httpx.get(imageUrl).content)
    base64_string = base_64_encoded_data.decode('utf-8')
    return base64_string

def prepareMessagePrompt(prompt, base64_string):
# Message
    message_list = [
        {
            "role": 'user',
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64_string}},
                # {"type": "text", "text": "Describe this image in two sentences."}
                {
                    "type": "text", 
                    "text": prompt
                }
            ]
        }
    ]
    return message_list

def fetchLLMResponse(message_list):
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2048,
        messages=message_list
    )

    print(response.content[0].text)
    return response


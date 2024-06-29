
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
IMAGE_PATH="./assets/sunset.jpeg"

with open(IMAGE_PATH, "rb") as image_file:
    binary_data = image_file.read()
    base_64_encoded_data = base64.b64encode(binary_data)
    base64_string = base_64_encoded_data.decode('utf-8')



# Image as a URL
# IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Machu_Picchu%2C_Peru_%282018%29.jpg/2560px-Machu_Picchu%2C_Peru_%282018%29.jpg"
# # Image(url=IMAGE_URL)
# base_64_encoded_data = base64.b64encode(httpx.get(IMAGE_URL).content)
# base64_string = base_64_encoded_data.decode('utf-8')


# Message
message_list = [
    {
        "role": 'user',
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64_string}},
            {"type": "text", "text": "Describe this image in two sentences."}
        ]
    }
]

response = client.messages.create(
    model=MODEL_NAME,
    max_tokens=2048,
    messages=message_list
)
print(response.content[0].text)

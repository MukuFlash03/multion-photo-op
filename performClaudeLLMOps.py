
import base64
from anthropic import Anthropic
import os
import httpx
from IPython.display import Image
from dotenv import load_dotenv
import json
import re

load_dotenv()

claude_api_key = os.getenv('CLAUDE_API_KEY')

client = Anthropic(
    api_key=claude_api_key,
)
modelDict = {
    'opus': "claude-3-opus-20240229",
    'haiku': "claude-3-haiku-20240307",
}

promptDict = {
    'categorizing': '''
                        You are an AI assistant trained to analyze product images and extract key information for online shopping. 
                        You will mainly be helping with online shopping on Amazon. Y
                        our task is to formulate a natural language command to search for and add an item to a shopping cart based on the following information:
                        1. Identify the general product category that best matches categories on Amazon.com (e.g. Books, Toys, Beauty & Personal Care, Home & Kitchen, Electronics, Clothing, etc.)
                        2. Extract the most relevant details from the image to enable accurate searching and purchasing on Amazon. 
                        Focus on the key identifying features that would be most useful in an Amazon search such as:
                        - For books: title, author
                        - For electronics: brand, model, key features
                        - For clothing: type, brand, color
                        - For home items: type, material, color, size
                        - For any item: any distinctive features or markings
                        Provide only the most crucial details that would be used in a search query. 
                        Limit your response to 2-3 key details.
                        Provide your analysis in the following format only:
                        {
                        "Category": [identified product category],
                        "Details": [2-3 key details extracted from the image, formatted as a comma-separated list]
                        }
                        Do not include any other text in your response besides this JSON-like output.
                    ''',
    'bookOrder': '''
                    I will be uploading images of books that I would like to buy. 
                    Can you please give me the name of the book and the author of the book in this format: 
                    Name: <name of book> Author: <author name>.
                '''
}

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

def parseClaudeResponse(response):
    # Remove newlines and extra spaces at the beginning and end
    response = response.strip()
    
    # Use a more flexible regex to extract category and details
    match = re.search(r'\{\s*"Category":\s*(.+?),\s*"Details":\s*(.+?)\s*\}', response, re.DOTALL)
    
    if match:
        category = match.group(1).strip()
        details = match.group(2).strip()
        
        # Remove quotes from category and details if present
        category = category.strip('"')
        details = details.strip('"')
        
        return category, details
    else:
        raise ValueError("Unable to parse the response")

def prepareMessagePrompt(prompt, base64_string):
# Message
    message_list = [
        {
            "role": 'user',
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64_string}},
                {
                    "type": "text", 
                    "text": prompt
                }
            ]
        }
    ]
    return message_list
    
def fetchLLMResponse(message_list, model):
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        messages=message_list
    )

    print(response.content[0].text)
    return response

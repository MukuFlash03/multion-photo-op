
import os
from dotenv import load_dotenv
from multion.client import MultiOn

load_dotenv()

multion_api_key = os.getenv('MULTION_API_KEY')

client = MultiOn(
    api_key=multion_api_key,
)

def addBookToCart(bookName, authorName):
    cart_response = client.browse(
        cmd=f"Add the {bookName} book by {authorName} to my cart",
        url="https://amazon.com",
        local=True,
    )

    print(cart_response.message)
    return cart_response

def addItemToCart(category, details):
    cart_response = client.browse(
        cmd=f"Add the following {category} item to my cart: {details}",
        url="https://amazon.com",
        local=True,
    )

    print(cart_response.message)
    return cart_response
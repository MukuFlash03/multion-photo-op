import base64
import httpx
from IPython.display import Image
from parseImage import parseImageFile, parseImageURL, prepareMessagePrompt, fetchLLMResponse
from performAmazonOperations import addBookToCart

# imageFilepath="./assets/sunset.jpeg"
imageFilepath="./assets/jack_and_the_beanstalk.jpeg"
# imageFilepath="./assets/atomic_habits.jpeg"

base64_string = parseImageFile(imageFilepath)

# imageUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Machu_Picchu%2C_Peru_%282018%29.jpg/2560px-Machu_Picchu%2C_Peru_%282018%29.jpg"
# base64_string = parseImageURL(imageUrl)

prompt = '''
    I will be uploading images of books that I would like to buy. 
    Can you please give me the name of the book and the author of the book in this format: 
    Name: <name of book> Author: <author name>.
'''
message_list = prepareMessagePrompt(prompt, base64_string)
responseFromClaude = fetchLLMResponse(message_list).content[0].text

bookDetails = responseFromClaude.split("\n")
bookName = bookDetails[0].split(": ")[1]
authorName = bookDetails[1].split(": ")[1]

responseFromMultiOn = addBookToCart(bookName, authorName)
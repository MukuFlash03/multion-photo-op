import base64
import httpx
from IPython.display import Image
from performClaudeLLMOps import parseImageFile, parseImageURL, prepareMessagePrompt, fetchLLMResponse, parseClaudeResponse, promptDict, modelDict
from performAmazonOperations import addBookToCart, addItemToCart

# imageFilepath="./assets/sunset.jpeg"
# imageFilepath="./assets/jack_and_the_beanstalk.jpeg"
# imageFilepath="./assets/coffee_mug_1.jpeg"
imageFilepath="./assets/adidas_shoes_name_1.jpeg"
# imageFilepath="./assets/adidas_shoes_no_name_1.jpeg"
# imageFilepath="./assets/nike_shoes_1.jpeg"
# imageFilepath="./assets/white_sneakers_1.jpeg"
# imageFilepath="./assets/silver_blue_watch_1.jpeg"
# imageFilepath="./assets/atomic_habits.jpeg"

base64_string = parseImageFile(imageFilepath)

# imageUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Machu_Picchu%2C_Peru_%282018%29.jpg/2560px-Machu_Picchu%2C_Peru_%282018%29.jpg"
# base64_string = parseImageURL(imageUrl)

message_list = prepareMessagePrompt(promptDict['categorizing'], base64_string)
responseFromClaude = fetchLLMResponse(message_list, modelDict['haiku']).content[0].text

# bookDetails = responseFromClaude.split("\n")
# bookName = bookDetails[0].split(": ")[1]
# authorName = bookDetails[1].split(": ")[1]

print(responseFromClaude)

category, details = parseClaudeResponse(responseFromClaude)
if category and details:
    responseFromMultiOn = addItemToCart(category, details)
    # print(responseFromMultiOn.message)

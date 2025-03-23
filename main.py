import requests
import base64
from dotenv import load_dotenv
import os

load_dotenv()


headers = {"Authorization":  f'Bearer {os.getenv("token")}'}


# IMAGE TO TEXT

# API_URL = "https://router.huggingface.co/hf-inference/models/Salesforce/blip-image-captioning-base"

# def query(filename):
#     with open(filename, "rb") as f:
#         data = f.read()
#     response = requests.post(API_URL, headers={"Content-Type": "image/jpeg", **headers}, data=data)
#     print('**************** RESPONSE *******************', response.json())
#     return response.json()

# output = query("2.png")


# ANSWERING YOUR QUESTIONS BY THE IMAGE

# API_URL = "https://router.huggingface.co/hf-inference/models/google/gemma-3-27b-it/v1/chat/completions"

# def query(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.json()


# response = query({
#     "messages": [
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "Print the data start with $ symbol."
#                 },
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": "https://images.template.net/wp-content/uploads/2016/04/06054458/Free-Warehouse-Inventory-Template-Download.jpg"
#                     }

#                 }
#             ]
#         }
#     ],
#     "max_tokens": 500,
#     "model": "google/gemma-3-27b-it"
# })

# print(response["choices"][0]["message"])


# DOCUMENT TO TEXT


# API_URL = "https://router.huggingface.co/hf-inference/models/impira/layoutlm-document-qa"

# def query(payload):
#     # Handle base64 encoding of the image
#     with open(payload["image"], "rb") as f:
#         img = f.read()
#         payload["image"] = base64.b64encode(img).decode("utf-8")
    
#     # Ensure 'inputs' is sent in the payload if required by the API
#     response = requests.post(API_URL, headers=headers, json={"inputs": payload})
#     return response.json()

# # Call the function
# output = query({
#     "image": "2.png",  # Path to the local image
#     "question": "What is in this image?",  # Question to ask
# })

# print(output)



API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"

def query():
    payload = {
        "inputs": "Astronaut riding a horse",
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

print('************** RESULT **************', query())

# image_bytes = query({
#     "inputs": "Astronaut riding a horse",
# })

# # You can access the image with PIL.Image for example
# import io
# from PIL import Image
# image = Image.open(io.BytesIO(image_bytes))
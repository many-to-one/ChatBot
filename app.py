from fastapi import FastAPI, Form, Depends, Request, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from sqlalchemy.orm import Session

import requests
import re
import base64
import shutil

from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    data = {"title": "Chatbot"}
    return templates.TemplateResponse("index.html", {"request": request, **data})



@app.post("/")
async def handle_chat_input(request: Request, user_input: str = Form(...)):
    """
    Receives user input, processes it, and returns the response as JSON.
    """

    print('************* USER INPUT *****************', user_input)

    parameters = {
        "max_new_tokens": 5000,
        "temperature": 0.01,
        "top_k": 50,
        "top_p": 0.95,
        "return_full_text": False
    }

    prompt = f"""
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are a helpful assistant. Provide accurate answers to the user's query.<|eot_id|>
    <|start_header_id|>user<|end_header_id|>
    {user_input}<|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    """

    headers = {
        'Authorization': f'Bearer {os.getenv("token")}',
        'Content-Type': 'application/json'
    }

    payload = {
        "inputs": prompt,
        "parameters": parameters
    }

    response = requests.post(os.getenv("url"), headers=headers, json=payload)
    print('************* RESPONSE *****************', response)
    print('************* RESPONSE TEXT *****************', response.text)

    try:
        response_text = response.json()[0]['generated_text'].strip()
        formatted_text = response_text.replace("\n", "<br>")

        # Detect and format code blocks
        code_pattern = re.compile(r"```(.*?)```", re.DOTALL)

        def format_code_blocks(text):
            return code_pattern.sub(r'<pre><code>\1</code></pre>', text)

        # def format_code_blocks(text):
        #     def replace_code_block(match):
        #         language = match.group(1) if match.group(1) else "plaintext"  # Default to plaintext if no language is specified
        #         code_content = match.group(2)
        #         return f'<pre><code class="language-{language}">{code_content}</code></pre>'
            
        #     return code_pattern.sub(replace_code_block, text)

        response_text = format_code_blocks(formatted_text)

    except Exception:
        response_text = "Error: No valid response received."

    return JSONResponse({"answer": response_text})


import base64
from translate import Translator

@app.post("/image-generate")
async def handle_chat_input(request: Request, user_input: str = Form(...)):
    """
    Receives user input, processes it, and returns the response as JSON.
    """

    print('************* USER INPUT *****************', user_input)

    # Translate user input to English
    translator = Translator(to_lang="en")  # Specify target language
    translated_input = translator.translate(user_input)

    payload = {
        "inputs": translated_input,
    }

    API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
    headers = {
        'Authorization': f'Bearer {os.getenv("token")}',
        'Content-Type': 'application/json'
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    base64_image = base64.b64encode(response.content).decode("utf-8")

    # return response.content
    if response.status_code != 200:
        # Handle API errors gracefully
        return JSONResponse({"error": f"Request failed with status {response.status_code}: {response.text}"})

    return Response(content=base64_image, media_type="application/octet-stream")




API_URL = "https://router.huggingface.co/hf-inference/models/lllyasviel/sd-controlnet-depth" #"https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-refiner-1.0"
HEADERS = {'Authorization': f'Bearer {os.getenv("token")}',}  # Replace with your API key

@app.post("/image-to-image")
async def process_image(file: UploadFile, prompt: str = Form(...)):
    """
    Accepts an image and a prompt, processes it, and returns the result.
    """
    # Save the uploaded file temporarily
    temp_file = f"temp_{file.filename}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Open and encode the image to base64
    with open(temp_file, "rb") as img:
        encoded_image = base64.b64encode(img.read()).decode("utf-8")

    # Prepare payload for Hugging Face API
    payload = {
        "inputs": encoded_image,
        "parameters": {
            "prompt": prompt
        }
    }

    # Send the payload to Hugging Face API
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    base64_image = base64.b64encode(response.content).decode("utf-8")

    print('**************** IMAGE TO IMAGE ***************', response )

    if response.status_code != 200:
        return JSONResponse({"error": f"Failed to process the image: {response.text}"})

    # Return processed image (assuming the output is in bytes format)
    return Response(content=base64_image, media_type="application/octet-stream") # Base64 encoded image
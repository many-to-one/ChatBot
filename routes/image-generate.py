import os, re, requests

from fastapi import FastAPI, Form, Depends, Request, UploadFile, APIRouter
from fastapi.responses import JSONResponse, HTMLResponse, Response

import base64
from translate import Translator


router = APIRouter(tags=["ChatArea"], prefix="/")

router.post("/image-generate")
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
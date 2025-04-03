import os, re, requests
from fastapi import FastAPI, Form, Depends, Request, UploadFile, APIRouter, status
from fastapi.responses import JSONResponse, HTMLResponse, Response, RedirectResponse
from models.models import ChatHistory
from orm.orm import OrmService
from schemas.chats import ChatBase
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_db
from schemas.users import UserBase
from settings.security import get_current_user, get_current_user_with_cookies

import base64
from translate import Translator

# import cv2
import numpy as np

import base64
from fastapi import FastAPI, File, UploadFile
from io import BytesIO



router = APIRouter(tags=["AiChat"], prefix="/ai_chat")


@router.post("/chat", status_code=status.HTTP_201_CREATED, response_model=ChatBase)
async def handle_chat_input(
    request: Request, 
    user_input: str = Form(...),
    db: AsyncSession = Depends(get_db),
    current_user: UserBase = Depends(get_current_user_with_cookies),
    ):
    """
    Receives user input, processes it, and returns the response as JSON.
    """

    print('************* USER INPUT *****************', user_input)

    API_URL = "https://router.huggingface.co/together/v1/chat/completions"
    headers = {"Authorization": f'Bearer {os.getenv("token")}'}

    payload = {
        "messages": [
            {
                "role": "user",
                "content": user_input #"What is the capital of France?"
            }
        ],
        "max_tokens": 500,
        "model": "deepseek-ai/DeepSeek-R1"
    }

    __orm = OrmService(db)

    response_text='Test'
    chat_data = {
        "user_input": user_input,
        "response_text": user_input, #response_text,
        "chat_user": current_user,
    }

    save_chat = await __orm.create(ChatHistory, chat_data)
    print('save_chat *****************************', save_chat)

    # response = requests.post(API_URL, headers=headers, json=payload)

    # print('RESPONSE *****************************', response.text)
    # response_text = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    # prompt_tokens = response.json().get("usage", {}).get("prompt_tokens", 0)
    # completion_tokens = response.json().get("usage", {}).get("completion_tokens", 0)
    # total_tokens = response.json().get("usage", {}).get("total_tokens", 0)
    # print('response_text *****************************', response_text)
    # print('response_text *****************************', prompt_tokens)
    # print('completion_tokens *****************************', completion_tokens)
    # print('total_tokens *****************************', total_tokens)
    try:
        # response_text = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        # formatted_text = response_text.replace("\n", "<br>")

        # # Detect and format code blocks
        # code_pattern = re.compile(r"```(.*?)```", re.DOTALL)

        # def format_code_blocks(text):
        #     return code_pattern.sub(r'<pre><code>\1</code></pre>', text)

        # response_text = format_code_blocks(formatted_text)
        # prompt_tokens = response.json().get("usage", {}).get("prompt_tokens", 0)
        # completion_tokens = response.json().get("usage", {}).get("completion_tokens", 0)
        # total_tokens = response.json().get("usage", {}).get("total_tokens", 0)

        # print('response_text *****************************', response_text)
        # print('response_text *****************************', prompt_tokens)
        # print('completion_tokens *****************************', completion_tokens)
        # print('total_tokens *****************************', total_tokens)

        __orm = OrmService(db)

        response_text='Test'
        chat_data = {
            "user_input": user_input,
            "response_text": user_input, #response_text,
            "chat_user": current_user,
        }

        save_chat = await __orm.create(ChatHistory, "chat", chat_data)
        print('save_chat *****************************', save_chat)


    except Exception:
        response_text = "Error: No valid response received."
    

    return JSONResponse({"answer": response_text})



@router.post("/image-generate", status_code=status.HTTP_201_CREATED, response_model=ChatBase)
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




# print(response["choices"][0]["message"])

# async def handle_chat_input(
#     request: Request, 
#     user_input: str = Form(...),
#     db: AsyncSession = Depends(get_db),
#     current_user: UserBase = Depends(get_current_user_with_cookies),
#     ):
#     """
#     Receives user input, processes it, and returns the response as JSON.
#     """

#     print('************* USER INPUT *****************', user_input)

#     parameters = {
#         "max_new_tokens": 5000,
#         "temperature": 0.01,
#         "top_k": 50,
#         "top_p": 0.95,
#         "return_full_text": False
#     }

#     prompt = f"""
#     <|begin_of_text|><|start_header_id|>system<|end_header_id|>
#     You are a helpful assistant. Provide accurate answers to the user's query.<|eot_id|>
#     <|start_header_id|>user<|end_header_id|>
#     {user_input}<|eot_id|>
#     <|start_header_id|>assistant<|end_header_id|>
#     """

#     headers = {
#         'Authorization': f'Bearer {os.getenv("token")}',
#         'Content-Type': 'application/json'
#     }

#     payload = {
#         "inputs": prompt,
#         "parameters": parameters
#     }


#         # current_user = await get_current_user_with_cookies(access_token, refresh_token, db)
#         # print('MAIN PAGE------------------- user', current_user)

#     response = requests.post(os.getenv("url"), headers=headers, json=payload)
#     print('************* RESPONSE *****************', response)
#     print('************* RESPONSE TEXT *****************', response.text)

#     try:
#         response_text = response.json()[0]['generated_text'].strip()
#         formatted_text = response_text.replace("\n", "<br>")

#         # Detect and format code blocks
#         code_pattern = re.compile(r"```(.*?)```", re.DOTALL)

#         def format_code_blocks(text):
#             return code_pattern.sub(r'<pre><code>\1</code></pre>', text)

#         # def format_code_blocks(text):
#         #     def replace_code_block(match):
#         #         language = match.group(1) if match.group(1) else "plaintext"  # Default to plaintext if no language is specified
#         #         code_content = match.group(2)
#         #         return f'<pre><code class="language-{language}">{code_content}</code></pre>'
                
#         #     return code_pattern.sub(replace_code_block, text)

#         response_text = format_code_blocks(formatted_text)

#         __orm = OrmService(db)

#         chat_data = {
#             "user_input": user_input,
#             "response_text": response_text,
#             "chat_user": current_user,
#         }

#         save_chat = await __orm.create(ChatHistory, "chat", chat_data)


#     except Exception:
#         response_text = "Error: No valid response received."
    

#     return JSONResponse({"answer": response_text})
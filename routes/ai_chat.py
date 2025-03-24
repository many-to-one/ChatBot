import os, re, requests
from fastapi import FastAPI, Form, Depends, Request, UploadFile, APIRouter, status
from fastapi.responses import JSONResponse, HTMLResponse, Response
from models.models import ChatHistory
from orm.orm import OrmService
from schemas.chats import ChatBase
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_db
from schemas.users import UserBase
from settings.security import get_current_user


router = APIRouter(tags=["AiChat"], prefix="/ai_chat")

@router.post("/chat", status_code=status.HTTP_201_CREATED, response_model=ChatBase)
async def handle_chat_input(
    request: Request, 
    user_input: str = Form(...),
    db: AsyncSession = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
    ):
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

        __orm = OrmService(db)

        chat_data = {
            "user_input": user_input,
            "response_text": response_text,
            "chat_user": current_user,
        }

        save_chat = await __orm.create(ChatHistory, "chat", chat_data)


    except Exception:
        response_text = "Error: No valid response received."

    return JSONResponse({"answer": response_text})
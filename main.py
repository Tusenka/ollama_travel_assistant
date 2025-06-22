import argparse
import logging
import os
from datetime import datetime, timedelta

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, Request, HTTPException, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse

from services.booking.hotellook_client import HotelLookClient
from services.chat_service import ChatService
from services.llm.ollama_client import OllamaClient
from services.llm.deepseek_client import DeeSeekClient
from services.llm.openai_client import OpenAiClient

load_dotenv()

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument( '-log',
                     '--loglevel',
                     default='warning',
                     help='Provide logging level. Example --loglevel debug, default=info' )

args = parser.parse_args()
logging.basicConfig( level=args.loglevel.upper() )

app = FastAPI(title="GPT-Assist Travel Bot", debug=True)

# Подключаем статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


MAX_HISTORY_LENGTH = int(os.getenv("MAX_HISTORY_LENGTH", 20))


ollama_client = OllamaClient()
deepseek_client = DeeSeekClient()
openai_client = OpenAiClient()
hotellook_booking_client = HotelLookClient(api_key=os.getenv("TRAVELPAYOUT_KEY"))
chat_service = ChatService(
    llm_clients=[deepseek_client, ollama_client, openai_client],
    booking_clients=[hotellook_booking_client]
)

GPT_ASSIST_PORT = os.getenv("GPT_ASSIST_PORT", 80)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()

    history = data

    if len(history) > MAX_HISTORY_LENGTH:
        history = history[-MAX_HISTORY_LENGTH:]

    ai_response = await chat_service.handle_user_message(history)

    return {"reply": ai_response}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(GPT_ASSIST_PORT),
        proxy_headers=True,
        reload=True,
    )

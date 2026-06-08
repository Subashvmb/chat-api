from fastapi import FastAPI
from pydantic import BaseModel
import anthropic
import os

app = FastAPI()

from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)

class Message(BaseModel):
    text: str

@app.get("/debug")
def debug():
    key = os.environ.get("ANTHROPIC_API_KEY")
    return {"key_set": key is not None, "key_preview": key[:10] if key else "NOT SET"}

@app.post("/chat")
def chat(message: Message):
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": message.text}]
    )
    return {"reply": response.content[0].text}
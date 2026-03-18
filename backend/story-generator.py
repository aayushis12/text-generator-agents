from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
import base64

load_dotenv()

app = FastAPI()

# allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

class StoryRequest(BaseModel):
    prompt: str
    language: str
    voice: str
    api_key: str

@app.post("/generate-story")
def generate_story(req: StoryRequest):
    # 1. generate story
    client = OpenAI(api_key=req.api_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"You are a storyteller for kids. Write in {req.language} with simple, fun and short stories."
            },
            {
                "role": "user",
                "content": req.prompt
            }
        ]
    )

    story = completion.choices[0].message.content

    # 2. generate audio
    audio = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=req.voice,
        input=story
    )

    audio_base64 = base64.b64encode(audio.content).decode("utf-8")

    return {
        "story": story,
        "audio": audio_base64
    }

from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory=".", html=False), name="static")
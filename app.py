
import os
import base64

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from huggingface_hub import InferenceClient


app = FastAPI(title="AI Video Studio API")


# -----------------------------
# CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hesamehrsana-cmd.github.io"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Hugging Face API
# -----------------------------

HF_TOKEN = os.environ.get("HF_TOKEN")

if not HF_TOKEN:
    print("WARNING: HF_TOKEN is not configured.")


client = InferenceClient(
    provider="fal-ai",
    api_key=HF_TOKEN,
)


# -----------------------------
# Request Model
# -----------------------------

class VideoRequest(BaseModel):
    prompt: str


# -----------------------------
# Home
# -----------------------------

@app.get("/")
def home():

    return {
        "status": "online",
        "service": "AI Video Studio"
    }


# -----------------------------
# Generate Video
# -----------------------------

@app.post("/generate")
def generate_video(request: VideoRequest):

    if not HF_TOKEN:

        raise HTTPException(
            status_code=500,
            detail="HF_TOKEN is not configured."
        )


    prompt = request.prompt.strip()


    if not prompt:

        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty."
        )


    try:

        print(
            f"Generating video for: {prompt}"
        )


        # Generate video
        video_bytes = client.text_to_video(

            prompt,

            model=
            "Lightricks/LTX-Video-0.9.5",

        )


        # Convert video to Base64
        video_base64 = base64.b64encode(
            video_bytes
        ).decode("utf-8")


        return {

            "success": True,

            "video":
            video_base64

        }


    except Exception as e:

        print(
            "VIDEO GENERATION ERROR:",
            str(e)
        )


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )
@app.get("/test")
def test_connection():
    return {
        "success": True,
        "message": "Backend connection works!"
    }

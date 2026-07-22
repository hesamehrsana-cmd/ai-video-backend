```python
import os
import base64

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from huggingface_hub import InferenceClient


# ==========================================
# APP
# ==========================================

app = FastAPI(
    title="AI Video Studio API"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "https://hesamehrsana-cmd.github.io"
    ],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ==========================================
# HUGGING FACE
# ==========================================

HF_TOKEN = os.environ.get("HF_TOKEN")


if not HF_TOKEN:

    print(
        "WARNING: HF_TOKEN is not configured!"
    )


client = InferenceClient(
    provider="fal-ai",
    api_key=HF_TOKEN,
)


# ==========================================
# REQUEST MODEL
# ==========================================

class VideoRequest(BaseModel):

    prompt: str


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {

        "status": "online",

        "service":
        "AI Video Studio"

    }


# ==========================================
# CONNECTION TEST
# ==========================================

@app.get("/test")
def test_connection():

    return {

        "success": True,

        "message":
        "Backend connection works!"

    }


# ==========================================
# GENERATE VIDEO
# ==========================================

@app.post("/generate")
def generate_video(
    request: VideoRequest
):

    # Check API Key

    if not HF_TOKEN:

        raise HTTPException(

            status_code=500,

            detail=
            "HF_TOKEN is not configured."

        )


    # Check Prompt

    prompt = (
        request.prompt.strip()
    )


    if not prompt:

        raise HTTPException(

            status_code=400,

            detail=
            "Prompt cannot be empty."

        )


    try:

        print(
            "Starting video generation..."
        )

        print(
            f"Prompt: {prompt}"
        )


        # ==================================
        # GENERATE VIDEO
        # ==================================

        video_bytes = (
            client.text_to_video(

                prompt,

                model=
                "Lightricks/LTX-Video-0.9.5"

            )
        )


        print(
            "Video generated successfully!"
        )


        # ==================================
        # CONVERT TO BASE64
        # ==================================

        video_base64 = (

            base64.b64encode(

                video_bytes

            ).decode(
                "utf-8"
            )

        )


        print(
            "Video converted to Base64."
        )


        # ==================================
        # RETURN RESULT
        # ==================================

        return {

            "success": True,

            "video":
            video_base64

        }


    except Exception as e:

        print(
            "VIDEO GENERATION ERROR:"
        )

        print(
            str(e)
        )


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )
```

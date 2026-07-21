import os
import uuid
import tempfile

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from huggingface_hub import InferenceClient

app = FastAPI(title="AI Video Studio API")

# اجازه دسترسی سایت به Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hesamehrsana-cmd.github.io"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key باید در Environment Variable باشد
HF_TOKEN = os.environ.get("HF_TOKEN")

if not HF_TOKEN:
    print("WARNING: HF_TOKEN is not configured.")

client = InferenceClient(
    provider="fal-ai",
    api_key=HF_TOKEN,
)


class VideoRequest(BaseModel):
    prompt: str


@app.get("/")
def home():
    return {
        "status": "online",
        "service": "AI Video Studio"
    }


@app.post("/generate")
def generate_video(request: VideoRequest):

    if not HF_TOKEN:
        raise HTTPException(
            status_code=500,
            detail="HF_TOKEN is not configured."
        )

    if not request.prompt.strip():
        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty."
        )

    try:

        video_bytes = client.text_to_video(
            request.prompt,
            model="Lightricks/LTX-Video-0.9.5",
        )

        filename = f"{uuid.uuid4()}.mp4"

        output_dir = "generated_videos"

        os.makedirs(
            output_dir,
            exist_ok=True
        )

        output_path = os.path.join(
            output_dir,
            filename
        )

        with open(
            output_path,
            "wb"
        ) as f:

            f.write(video_bytes)

        return {
            "success": True,
            "video_url": f"/videos/{filename}"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

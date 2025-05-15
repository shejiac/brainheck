"""Runs the ASR server."""

# Unless you want to do something special with the server, you shouldn't need
# to change anything in this file.


import base64
from fastapi import FastAPI, Request
from .asr_manager import ASRManager
from pydantic import BaseModel
from typing import List, Optional

class Instance(BaseModel):
    key: int
    b64: str

class ASRRequest(BaseModel):
    instances: List[Instance]


app = FastAPI()
manager = ASRManager()


@app.post("/asr")
async def asr(request: ASRRequest) -> dict[str, list[str]]:
    """Performs ASR on audio files."""

    predictions = []

    for instance in request.instances:
        try:
            # Access Pydantic fields as attributes
            key = instance.key
            audio_bytes = base64.b64decode(instance.b64)
            transcription = manager.asr(audio_bytes)

        except Exception as e:
            print(f"❌ Error during transcription for key={key}: {e}")
            transcription = f"❌ Error: {str(e)}"

        predictions.append(transcription)

    return {"predictions": predictions}



@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint for the server."""
    return {"message": "health ok"}

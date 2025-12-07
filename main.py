from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import Response
import edge_tts

app = FastAPI()

class TTSRequest(BaseModel):
    text: str
    voice: str = "es-ES-ElviraNeural"
    rate: str = "+0%"

@app.post("/tts")
async def tts_endpoint(req: TTSRequest):
    communicate = edge_tts.Communicate(
        text=req.text,
        voice=req.voice,
        rate=req.rate,
    )

    audio_bytes = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes += chunk["data"]

    return Response(content=audio_bytes, media_type="audio/mpeg")

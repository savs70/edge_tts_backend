import io
import tempfile
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import edge_tts

# FastAPI con docs activadas explícitamente
app = FastAPI(
    title="Edge TTS Backend",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

class TTSRequest(BaseModel):
    text: str
    voice: str = "es-ES-ElviraNeural"
    rate: str = "+0%"
    volume: str = "+0%"

@app.get("/")
async def home():
    return {"status": "Edge TTS backend ready!"}

@app.post("/tts")
async def tts_endpoint(req: TTSRequest):
    """
    Endpoint que genera audio MP3 usando Edge TTS.
    Devuelve un stream de audio.
    """
    try:
        communicate = edge_tts.Communicate(
            text=req.text,
            voice=req.voice,
            rate=req.rate,
            volume=req.volume
        )

        audio_bytes = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_bytes += chunk["data"]

        if not audio_bytes:
            raise HTTPException(
                status_code=500,
                detail="No se recibió audio desde Edge TTS."
            )

        # Devolver el audio como streaming
        return StreamingResponse(
            io.BytesIO(audio_bytes),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": 'attachment; filename="tts_output.mp3"'
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno en Edge TTS: {e}"
        )

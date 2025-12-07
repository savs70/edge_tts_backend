from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import edge_tts
import asyncio
import tempfile

app = FastAPI()

class TTSRequest(BaseModel):
    text: str
    voice: str = "es-ES-ElviraNeural"
    rate: str = "+0%"
    volume: str = "+0%"

@app.post("/tts")
async def tts_endpoint(req: TTSRequest):

    communicate = edge_tts.Communicate(
        text=req.text,
        voice=req.voice,
        rate=req.rate,
        volume=req.volume
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        output_path = tmp.name

    await communicate.save(output_path)

    def iterfile():
        with open(output_path, "rb") as f:
            yield from f

    return StreamingResponse(
        iterfile(),
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": 'attachment; filename="tts_output.mp3"'
        }
    )

@app.get("/")
def home():
    return {"status": "Edge TTS backend ready!"}

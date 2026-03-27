from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn
from audio_agent import AudioAgent

app = FastAPI(
    title="PodCraft AI Audio Agent",
    version="3.0.0",
    description="Generate high-quality podcast audio using ElevenLabs TTS with intelligent voice selection"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

audio_agent = AudioAgent()

# ============= Models =============
class GenerateAudioRequest(BaseModel):
    text: str = Field(..., description="النص المراد تحويله إلى صوت", min_length=1)
    persona: str = Field("host", description="الشخصية: host / guest / narrator / teacher")
    name: str = Field("Speaker", description="اسم الملف")
    language: str = Field("en", description="اللغة: en / ar-eg")
    gender: str = Field("male", description="الجنس: male / female")
    age: str = Field("adult", description="العمر: adult / young / child / teen")
    style: str = Field("professional", description="الستايل: calm / energetic / professional / warm / expressive / deep / clear")
    speed: float = Field(1.0, description="سرعة الصوت (0.5 - 2.0)", ge=0.5, le=2.0)
    voice_id: Optional[str] = Field(None, description="معرف الصوت المحدد (اختياري)")


class GenerateAudioResponse(BaseModel):
    success: bool
    audio_url: Optional[str] = None
    audio_base64: Optional[str] = None
    voice: Optional[str] = None
    voice_id: Optional[str] = None
    persona: Optional[str] = None
    style: Optional[str] = None
    duration: Optional[float] = None
    language: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[str] = None
    speed: Optional[float] = None
    error: Optional[str] = None


# ============= Endpoints =============
@app.get("/")
async def root():
    return {
        "name": "PodCraft AI Audio Agent",
        "version": "3.0.0",
        "status": "running",
        "tts_provider": "ElevenLabs",
        "storage": "Cloudinary",
        "voices_available": len(audio_agent.get_available_voices())
    }


@app.get("/voices")
async def get_voices():
    return {"voices": audio_agent.get_available_voices(), "total": len(audio_agent.get_available_voices())}


@app.get("/styles")
async def get_styles():
    return {"styles": audio_agent.get_styles(), "total": len(audio_agent.get_styles())}


@app.get("/personas")
async def get_personas():
    return {"personas": audio_agent.get_personas(), "total": len(audio_agent.get_personas())}


@app.post("/generate-audio", response_model=GenerateAudioResponse)
async def generate_audio(request: GenerateAudioRequest):
    result = await audio_agent.generate_speech(
        text=request.text,
        persona=request.persona,
        name=request.name,
        language=request.language,
        gender=request.gender,
        age=request.age,
        style=request.style,
        speed=request.speed,
        voice_id=request.voice_id
    )
    return GenerateAudioResponse(**result)


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
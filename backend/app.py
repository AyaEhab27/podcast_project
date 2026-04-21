from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn
from audio_agent import AudioAgent


# أضيفي ده بعد from audio_agent import AudioAgent
STYLES = {
    "calm": "calm",
    "energetic": "energetic",
    "professional": "professional",
    "warm": "warm",
    "authoritative": "authoritative",
    "clear": "clear",
    "natural": "natural"
}
app = FastAPI(
    title="PodCraft AI Audio Agent",
    version="3.0.0",
    description="Generate high-quality podcast audio using ElevenLabs, Munsit, and gTTS"
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
    name: str = Field("Speaker", description="اسم المتحدث")
    language: str = Field("en", description="اللغة: en / ar")
    gender: str = Field("male", description="الجنس: male / female")
    dialect: str = Field("egyptian", description="اللهجة للعربي: egyptian / emirati / saudi / kuwaiti / qatari / omani / bahraini / hijazi / fusha / american / british / australian / indian")
    style: str = Field("professional", description="الستايل: calm / energetic / professional / warm / authoritative / clear / natural")
    speed: float = Field(1.0, description="سرعة الصوت (0.5 - 2.0)", ge=0.5, le=2.0)
    voice_id: Optional[str] = Field(None, description="معرف الصوت المحدد (اختياري)")

class GenerateAudioResponse(BaseModel):
    success: bool
    audio_url: Optional[str] = None
    audio_base64: Optional[str] = None
    voice: Optional[str] = None
    dialect: Optional[str] = None
    provider: Optional[str] = None
    persona: Optional[str] = None
    style: Optional[str] = None
    duration: Optional[float] = None
    language: Optional[str] = None
    gender: Optional[str] = None
    speed: Optional[float] = None
    error: Optional[str] = None

# ============= Endpoints =============
@app.get("/")
async def root():
    return {
        "name": "PodCraft AI Audio Agent",
        "version": "3.0.0",
        "status": "running",
        "tts_providers": ["ElevenLabs", "Munsit", "gTTS"],
        "storage": "Cloudinary"
    }

@app.get("/voices")
async def get_voices(language: Optional[str] = None, dialect: Optional[str] = None):
    voices = audio_agent.get_available_voices(language, dialect)
    return {"voices": voices, "total": len(voices)}

@app.get("/dialects")
async def get_dialects():
    dialects = [
        {"id": "egyptian", "name": "Egyptian (gTTS)", "styles": []},
        {"id": "emirati", "name": "Emirati", "styles": ["clear", "calm", "energetic", "professional", "authoritative", "warm", "natural"]},
        {"id": "saudi", "name": "Saudi / Najdi", "styles": ["professional", "energetic", "warm", "calm", "authoritative", "clear"]},
        {"id": "hijazi", "name": "Hijazi", "styles": ["warm", "natural", "calm"]},
        {"id": "kuwaiti", "name": "Kuwaiti", "styles": ["energetic", "natural"]},
        {"id": "qatari", "name": "Qatari", "styles": ["calm"]},
        {"id": "omani", "name": "Omani", "styles": ["warm"]},
        {"id": "bahraini", "name": "Bahraini", "styles": ["natural", "professional"]},
        {"id": "fusha", "name": "Fusha / MSA", "styles": ["clear", "energetic", "authoritative", "professional"]},
        {"id": "american", "name": "American English", "styles": ["authoritative", "professional"]},
        {"id": "british", "name": "British English", "styles": ["professional", "energetic", "calm"]},
        {"id": "australian", "name": "Australian English", "styles": ["warm"]},
        {"id": "indian", "name": "Indian English", "styles": ["professional", "clear"]}
    ]
    return {"dialects": dialects, "total": len(dialects)}

@app.get("/styles")
async def get_styles(dialect: Optional[str] = None):
    if dialect:
        styles = audio_agent.get_available_styles_for_dialect(dialect)
        return {"dialect": dialect, "styles": styles, "total": len(styles)}
    return {"styles": list(STYLES.keys()), "total": len(STYLES)}

@app.post("/generate-audio", response_model=GenerateAudioResponse)
async def generate_audio(request: GenerateAudioRequest):
    result = await audio_agent.generate_speech(
        text=request.text,
        persona=request.persona,
        name=request.name,
        language=request.language,
        gender=request.gender,
        dialect=request.dialect,
        style=request.style,
        speed=request.speed,
        voice_id=request.voice_id
    )
    return GenerateAudioResponse(**result)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

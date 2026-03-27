import os
import uuid
import io
import base64
import tempfile
import cloudinary
import cloudinary.uploader
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from gtts import gTTS
import time

load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Initialize ElevenLabs client (للإنجليزي)
elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# ========== الأصوات المتاحة ==========
# الأصوات الإنجليزية (مدعومة من ElevenLabs مجاناً)
ENGLISH_VOICES = {
    "adam": {
        "id": "pNInz6obpgDQGcFmaJgB",
        "name": "Adam",
        "gender": "male",
        "style": "professional",
        "language": "en",
        "description": "Dominant, Firm - Professional male voice"
    },
    "sarah": {
        "id": "EXAVITQu4vr4xnSDxMaL",
        "name": "Sarah",
        "gender": "female",
        "style": "professional",
        "language": "en",
        "description": "Mature, Reassuring, Confident - Professional female voice"
    },
    "george": {
        "id": "JBFqnCBsd6RMkjVDRZzb",
        "name": "George",
        "gender": "male",
        "style": "warm",
        "language": "en",
        "description": "Warm, Captivating Storyteller"
    },
    "alice": {
        "id": "Xb7hH8MSUJpSbSDYk0k2",
        "name": "Alice",
        "gender": "female",
        "style": "clear",
        "language": "en",
        "description": "Clear, Engaging Educator"
    },
    "charlie": {
        "id": "IKne3meq5aSn9XLyUdCD",
        "name": "Charlie",
        "gender": "male",
        "style": "energetic",
        "language": "en",
        "description": "Deep, Confident, Energetic"
    },
    "bella": {
        "id": "hpp4J3VqNfWAUOO0d1Us",
        "name": "Bella",
        "gender": "female",
        "style": "warm",
        "language": "en",
        "description": "Professional, Bright, Warm"
    }
}

# الأصوات العربية (ستستخدم gTTS مجاناً)
ARABIC_VOICES = {
    "arabic_male": {
        "name": "Arabic Male",
        "gender": "male",
        "style": "natural",
        "language": "ar",
        "description": "صوت عربي رجالي طبيعي (gTTS)"
    },
    "arabic_female": {
        "name": "Arabic Female",
        "gender": "female",
        "style": "natural",
        "language": "ar",
        "description": "صوت عربي ست طبيعي (gTTS)"
    },
    "child_male": {
        "name": "Child Male",
        "gender": "male",
        "style": "natural",
        "age": "child",
        "language": "ar",
        "description": "صوت طفل رجالي (gTTS)"
    },
    "child_female": {
        "name": "Child Female",
        "gender": "female",
        "style": "natural",
        "age": "child",
        "language": "ar",
        "description": "صوت طفلة ست (gTTS)"
    }
}

# دمج الأصوات
AVAILABLE_VOICES = {**ENGLISH_VOICES, **ARABIC_VOICES}

# خريطة الستايلات
STYLE_MAPPING = {
    "calm": ["george", "alice", "arabic_female"],
    "warm": ["george", "bella", "arabic_male"],
    "energetic": ["charlie", "bella", "arabic_male"],
    "professional": ["adam", "sarah", "arabic_male"],
    "expressive": ["charlie", "bella", "arabic_female"],
    "deep": ["adam", "charlie", "arabic_male"],
    "natural": ["alice", "bella", "arabic_female"],
    "clear": ["alice", "sarah", "arabic_female"]
}

# Persona settings
PERSONAS = {
    "host": {
        "name": "Host",
        "description": "مقدم البودكاست - واثق، احترافي",
        "preferred_style": "professional",
        "preferred_gender": "male"
    },
    "guest": {
        "name": "Guest",
        "description": "ضيف البودكاست - دافيء، طبيعي",
        "preferred_style": "warm",
        "preferred_gender": "female"
    },
    "narrator": {
        "name": "Narrator",
        "description": "راوي القصة - هادئ، معبر",
        "preferred_style": "calm",
        "preferred_gender": "male"
    },
    "teacher": {
        "name": "Teacher",
        "description": "صوت تعليمي - واضح، احترافي",
        "preferred_style": "clear",
        "preferred_gender": "female"
    },
    "child": {
        "name": "Child",
        "description": "صوت طفل - مناسب للقصص الأطفال",
        "preferred_style": "natural",
        "preferred_gender": "female",
        "preferred_age": "child"
    }
}

# Style settings for ElevenLabs (للإنجليزي فقط)
STYLES = {
    "calm": {"stability": 0.8, "similarity_boost": 0.5},
    "energetic": {"stability": 0.4, "similarity_boost": 0.8},
    "professional": {"stability": 0.7, "similarity_boost": 0.6},
    "warm": {"stability": 0.6, "similarity_boost": 0.7},
    "expressive": {"stability": 0.5, "similarity_boost": 0.8},
    "deep": {"stability": 0.7, "similarity_boost": 0.5},
    "natural": {"stability": 0.65, "similarity_boost": 0.65},
    "clear": {"stability": 0.75, "similarity_boost": 0.7}
}

MODEL_ID = "eleven_turbo_v2"


def detect_language(text: str) -> str:
    """كشف اللغة من النص"""
    arabic_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
    if arabic_chars > len(text) * 0.3:
        return 'ar'
    return 'en'


def find_best_voice(gender: str, style: str, age: str = "adult", language: str = None, preferred_voice_id: str = None) -> dict:
    """البحث عن أفضل صوت بناءً على الجنس والستايل والعمر واللغة"""
    if preferred_voice_id:
        for voice in AVAILABLE_VOICES.values():
            if voice.get("id") == preferred_voice_id:
                return voice
    
    if language == 'ar':
        if age == "child":
            return ARABIC_VOICES["child_male" if gender == "male" else "child_female"]
        return ARABIC_VOICES["arabic_male" if gender == "male" else "arabic_female"]
    
    if style in STYLE_MAPPING:
        for voice_key in STYLE_MAPPING[style]:
            if voice_key in ENGLISH_VOICES:
                voice = ENGLISH_VOICES[voice_key]
                if voice["gender"] == gender:
                    return voice
    
    for voice in ENGLISH_VOICES.values():
        if voice["gender"] == gender:
            return voice
    
    return ENGLISH_VOICES["adam"]


def generate_arabic_speech(text: str, gender: str, speed: float = 1.0) -> bytes:
    """توليد صوت عربي باستخدام gTTS - نسخة معدلة"""
    try:
        # استخدام tempfile مع تأخير بسيط
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
            tmp_path = tmp.name
        
        # توليد الصوت
        tts = gTTS(text=text, lang='ar', slow=False)
        tts.save(tmp_path)
        
        # قراءة الملف
        with open(tmp_path, 'rb') as f:
            audio_bytes = f.read()
        
        # حذف الملف بعد التأكد من إغلاقه
        try:
            os.unlink(tmp_path)
        except:
            time.sleep(0.1)
            os.unlink(tmp_path)
        
        return audio_bytes
        
    except Exception as e:
        print(f"❌ Arabic TTS error: {e}")
        raise


class AudioAgent:
    def __init__(self):
        self.client = elevenlabs_client
        print(f"✅ ElevenLabs API Key loaded")
        print(f"📢 Available voices: {len(AVAILABLE_VOICES)}")
        print(f"   English voices: {len(ENGLISH_VOICES)}")
        print(f"   Arabic voices: {len(ARABIC_VOICES)} (using gTTS - free)")
        print(f"🎙️ Model: {MODEL_ID}")
    
    async def generate_speech(
        self, 
        text: str, 
        persona: str = "host",
        name: str = "Speaker",
        language: str = "en",
        gender: str = "male",
        age: str = "adult",
        style: str = "professional",
        speed: float = 1.0,
        voice_id: str = None
    ) -> Dict[str, Any]:
        try:
            if not text or not text.strip():
                return {'success': False, 'error': 'Text cannot be empty'}
            
            # كشف اللغة إذا لم تكن محددة
            detected_lang = detect_language(text)
            final_language = language if language != "ar-eg" else "ar"
            if final_language == "en" and detected_lang == "ar":
                final_language = "ar"
            
            # اختيار الصوت
            voice_config = find_best_voice(gender, style, age, final_language, voice_id)
            
            print(f"\n{'='*50}")
            print(f"🎤 Generating speech")
            print(f"   Language: {final_language}")
            print(f"   Speed: {speed}x")
            print(f"   Requested: Gender={gender}, Style={style}, Age={age}")
            print(f"   Selected: {voice_config['name']}")
            print(f"   Persona: {persona}")
            print(f"   Text: {text[:100]}...")
            print(f"{'='*50}")
            
            # توليد الصوت حسب اللغة
            if final_language == 'ar':
                audio_bytes = generate_arabic_speech(text, gender, speed)
                voice_name = voice_config['name']
                voice_id = "gtts_arabic"
                duration = len(audio_bytes) / 16000  # تقدير المدة
            else:
                selected_voice_id = voice_config.get("id", "pNInz6obpgDQGcFmaJgB")
                style_settings = STYLES.get(style, STYLES["professional"])
                
                audio_generator = self.client.text_to_speech.convert(
                    text=text,
                    voice_id=selected_voice_id,
                    model_id=MODEL_ID,
                    output_format="mp3_44100_128",
                    voice_settings={
                        "stability": style_settings["stability"],
                        "similarity_boost": style_settings["similarity_boost"]
                    }
                )
                audio_bytes = b"".join(chunk for chunk in audio_generator)
                voice_name = voice_config['name']
                voice_id = selected_voice_id
                duration = 0  # سيتم تحديثه من Cloudinary
            
            # حفظ الملف مؤقتاً
            filename = f"audio_files/{uuid.uuid4()}.mp3"
            os.makedirs("audio_files", exist_ok=True)
            
            with open(filename, 'wb') as f:
                f.write(audio_bytes)
            
            # رفع على Cloudinary
            try:
                public_id = f"podcast_audio/{name}_{uuid.uuid4().hex[:8]}"
                upload_result = cloudinary.uploader.upload(
                    filename,
                    public_id=public_id,
                    resource_type="auto",
                    folder="podcast_audio"
                )
                
                audio_url = upload_result.get('secure_url')
                duration = upload_result.get('duration', duration)
                
                print(f"☁️ Uploaded to Cloudinary: {audio_url}")
                
                os.remove(filename)
                
                return {
                    'success': True,
                    'audio_url': audio_url,
                    'duration': duration,
                    'voice': voice_name,
                    'voice_id': voice_id,
                    'persona': persona,
                    'style': style,
                    'language': final_language,
                    'gender': gender,
                    'age': age,
                    'speed': speed
                }
                
            except Exception as e:
                print(f"⚠️ Cloudinary upload failed: {e}")
                audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
                os.remove(filename)
                return {
                    'success': True,
                    'audio_base64': audio_base64,
                    'voice': voice_name,
                    'voice_id': voice_id,
                    'persona': persona,
                    'style': style,
                    'language': final_language,
                    'speed': speed
                }
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_available_voices(self):
        return [{'id': vid, 'name': v['name'], 'gender': v['gender'], 
                 'style': v.get('style', 'natural'), 
                 'description': v.get('description', ''),
                 'language': v.get('language', 'en'),
                 'voice_id': v.get('id', vid)} 
                for vid, v in AVAILABLE_VOICES.items()]
    
    def get_styles(self):
        return [{'id': s, 'name': s} for s in STYLES.keys()]
    
    def get_personas(self):
        return [{'id': p, 'name': data['name'], 'description': data['description']} 
                for p, data in PERSONAS.items()]
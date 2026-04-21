# import os
# import uuid
# import io
# import base64
# import tempfile
# import cloudinary
# import cloudinary.uploader
# from typing import Optional, Dict, Any
# from dotenv import load_dotenv
# from elevenlabs.client import ElevenLabs
# from gtts import gTTS
# import time

# load_dotenv()

# # Configure Cloudinary
# cloudinary.config(
#     cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
#     api_key=os.getenv('CLOUDINARY_API_KEY'),
#     api_secret=os.getenv('CLOUDINARY_API_SECRET')
# )

# # Initialize ElevenLabs client (للإنجليزي)
# elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# # ========== الأصوات المتاحة ==========
# # الأصوات الإنجليزية (مدعومة من ElevenLabs مجاناً)
# ENGLISH_VOICES = {
#     "adam": {
#         "id": "pNInz6obpgDQGcFmaJgB",
#         "name": "Adam",
#         "gender": "male",
#         "style": "professional",
#         "language": "en",
#         "description": "Dominant, Firm - Professional male voice"
#     },
#     "sarah": {
#         "id": "EXAVITQu4vr4xnSDxMaL",
#         "name": "Sarah",
#         "gender": "female",
#         "style": "professional",
#         "language": "en",
#         "description": "Mature, Reassuring, Confident - Professional female voice"
#     },
#     "george": {
#         "id": "JBFqnCBsd6RMkjVDRZzb",
#         "name": "George",
#         "gender": "male",
#         "style": "warm",
#         "language": "en",
#         "description": "Warm, Captivating Storyteller"
#     },
#     "alice": {
#         "id": "Xb7hH8MSUJpSbSDYk0k2",
#         "name": "Alice",
#         "gender": "female",
#         "style": "clear",
#         "language": "en",
#         "description": "Clear, Engaging Educator"
#     },
#     "charlie": {
#         "id": "IKne3meq5aSn9XLyUdCD",
#         "name": "Charlie",
#         "gender": "male",
#         "style": "energetic",
#         "language": "en",
#         "description": "Deep, Confident, Energetic"
#     },
#     "bella": {
#         "id": "hpp4J3VqNfWAUOO0d1Us",
#         "name": "Bella",
#         "gender": "female",
#         "style": "warm",
#         "language": "en",
#         "description": "Professional, Bright, Warm"
#     }
# }

# # الأصوات العربية (ستستخدم gTTS مجاناً)
# ARABIC_VOICES = {
#     "arabic_male": {
#         "name": "Arabic Male",
#         "gender": "male",
#         "style": "natural",
#         "language": "ar",
#         "description": "صوت عربي رجالي طبيعي (gTTS)"
#     },
#     "arabic_female": {
#         "name": "Arabic Female",
#         "gender": "female",
#         "style": "natural",
#         "language": "ar",
#         "description": "صوت عربي ست طبيعي (gTTS)"
#     },
#     "child_male": {
#         "name": "Child Male",
#         "gender": "male",
#         "style": "natural",
#         "age": "child",
#         "language": "ar",
#         "description": "صوت طفل رجالي (gTTS)"
#     },
#     "child_female": {
#         "name": "Child Female",
#         "gender": "female",
#         "style": "natural",
#         "age": "child",
#         "language": "ar",
#         "description": "صوت طفلة ست (gTTS)"
#     }
# }

# # دمج الأصوات
# AVAILABLE_VOICES = {**ENGLISH_VOICES, **ARABIC_VOICES}

# # خريطة الستايلات
# STYLE_MAPPING = {
#     "calm": ["george", "alice", "arabic_female"],
#     "warm": ["george", "bella", "arabic_male"],
#     "energetic": ["charlie", "bella", "arabic_male"],
#     "professional": ["adam", "sarah", "arabic_male"],
#     "expressive": ["charlie", "bella", "arabic_female"],
#     "deep": ["adam", "charlie", "arabic_male"],
#     "natural": ["alice", "bella", "arabic_female"],
#     "clear": ["alice", "sarah", "arabic_female"]
# }

# # Persona settings
# PERSONAS = {
#     "host": {
#         "name": "Host",
#         "description": "مقدم البودكاست - واثق، احترافي",
#         "preferred_style": "professional",
#         "preferred_gender": "male"
#     },
#     "guest": {
#         "name": "Guest",
#         "description": "ضيف البودكاست - دافيء، طبيعي",
#         "preferred_style": "warm",
#         "preferred_gender": "female"
#     },
#     "narrator": {
#         "name": "Narrator",
#         "description": "راوي القصة - هادئ، معبر",
#         "preferred_style": "calm",
#         "preferred_gender": "male"
#     },
#     "teacher": {
#         "name": "Teacher",
#         "description": "صوت تعليمي - واضح، احترافي",
#         "preferred_style": "clear",
#         "preferred_gender": "female"
#     },
#     "child": {
#         "name": "Child",
#         "description": "صوت طفل - مناسب للقصص الأطفال",
#         "preferred_style": "natural",
#         "preferred_gender": "female",
#         "preferred_age": "child"
#     }
# }

# # Style settings for ElevenLabs (للإنجليزي فقط)
# STYLES = {
#     "calm": {"stability": 0.8, "similarity_boost": 0.5},
#     "energetic": {"stability": 0.4, "similarity_boost": 0.8},
#     "professional": {"stability": 0.7, "similarity_boost": 0.6},
#     "warm": {"stability": 0.6, "similarity_boost": 0.7},
#     "expressive": {"stability": 0.5, "similarity_boost": 0.8},
#     "deep": {"stability": 0.7, "similarity_boost": 0.5},
#     "natural": {"stability": 0.65, "similarity_boost": 0.65},
#     "clear": {"stability": 0.75, "similarity_boost": 0.7}
# }

# MODEL_ID = "eleven_turbo_v2"


# def detect_language(text: str) -> str:
#     """كشف اللغة من النص"""
#     arabic_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
#     if arabic_chars > len(text) * 0.3:
#         return 'ar'
#     return 'en'


# def find_best_voice(gender: str, style: str, age: str = "adult", language: str = None, preferred_voice_id: str = None) -> dict:
#     """البحث عن أفضل صوت بناءً على الجنس والستايل والعمر واللغة"""
#     if preferred_voice_id:
#         for voice in AVAILABLE_VOICES.values():
#             if voice.get("id") == preferred_voice_id:
#                 return voice
    
#     if language == 'ar':
#         if age == "child":
#             return ARABIC_VOICES["child_male" if gender == "male" else "child_female"]
#         return ARABIC_VOICES["arabic_male" if gender == "male" else "arabic_female"]
    
#     if style in STYLE_MAPPING:
#         for voice_key in STYLE_MAPPING[style]:
#             if voice_key in ENGLISH_VOICES:
#                 voice = ENGLISH_VOICES[voice_key]
#                 if voice["gender"] == gender:
#                     return voice
    
#     for voice in ENGLISH_VOICES.values():
#         if voice["gender"] == gender:
#             return voice
    
#     return ENGLISH_VOICES["adam"]


# def generate_arabic_speech(text: str, gender: str, speed: float = 1.0) -> bytes:
#     """توليد صوت عربي باستخدام gTTS - نسخة معدلة"""
#     try:
#         # استخدام tempfile مع تأخير بسيط
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
#             tmp_path = tmp.name
        
#         # توليد الصوت
#         tts = gTTS(text=text, lang='ar', slow=False)
#         tts.save(tmp_path)
        
#         # قراءة الملف
#         with open(tmp_path, 'rb') as f:
#             audio_bytes = f.read()
        
#         # حذف الملف بعد التأكد من إغلاقه
#         try:
#             os.unlink(tmp_path)
#         except:
#             time.sleep(0.1)
#             os.unlink(tmp_path)
        
#         return audio_bytes
        
#     except Exception as e:
#         print(f"❌ Arabic TTS error: {e}")
#         raise


# class AudioAgent:
#     def __init__(self):
#         self.client = elevenlabs_client
#         print(f"✅ ElevenLabs API Key loaded")
#         print(f"📢 Available voices: {len(AVAILABLE_VOICES)}")
#         print(f"   English voices: {len(ENGLISH_VOICES)}")
#         print(f"   Arabic voices: {len(ARABIC_VOICES)} (using gTTS - free)")
#         print(f"🎙️ Model: {MODEL_ID}")
    
#     async def generate_speech(
#         self, 
#         text: str, 
#         persona: str = "host",
#         name: str = "Speaker",
#         language: str = "en",
#         gender: str = "male",
#         age: str = "adult",
#         style: str = "professional",
#         speed: float = 1.0,
#         voice_id: str = None
#     ) -> Dict[str, Any]:
#         try:
#             if not text or not text.strip():
#                 return {'success': False, 'error': 'Text cannot be empty'}
            
#             # كشف اللغة إذا لم تكن محددة
#             detected_lang = detect_language(text)
#             final_language = language if language != "ar-eg" else "ar"
#             if final_language == "en" and detected_lang == "ar":
#                 final_language = "ar"
            
#             # اختيار الصوت
#             voice_config = find_best_voice(gender, style, age, final_language, voice_id)
            
#             print(f"\n{'='*50}")
#             print(f"🎤 Generating speech")
#             print(f"   Language: {final_language}")
#             print(f"   Speed: {speed}x")
#             print(f"   Requested: Gender={gender}, Style={style}, Age={age}")
#             print(f"   Selected: {voice_config['name']}")
#             print(f"   Persona: {persona}")
#             print(f"   Text: {text[:100]}...")
#             print(f"{'='*50}")
            
#             # توليد الصوت حسب اللغة
#             if final_language == 'ar':
#                 audio_bytes = generate_arabic_speech(text, gender, speed)
#                 voice_name = voice_config['name']
#                 voice_id = "gtts_arabic"
#                 duration = len(audio_bytes) / 16000  # تقدير المدة
#             else:
#                 selected_voice_id = voice_config.get("id", "pNInz6obpgDQGcFmaJgB")
#                 style_settings = STYLES.get(style, STYLES["professional"])
                
#                 audio_generator = self.client.text_to_speech.convert(
#                     text=text,
#                     voice_id=selected_voice_id,
#                     model_id=MODEL_ID,
#                     output_format="mp3_44100_128",
#                     voice_settings={
#                         "stability": style_settings["stability"],
#                         "similarity_boost": style_settings["similarity_boost"]
#                     }
#                 )
#                 audio_bytes = b"".join(chunk for chunk in audio_generator)
#                 voice_name = voice_config['name']
#                 voice_id = selected_voice_id
#                 duration = 0  # سيتم تحديثه من Cloudinary
            
#             # حفظ الملف مؤقتاً
#             filename = f"audio_files/{uuid.uuid4()}.mp3"
#             os.makedirs("audio_files", exist_ok=True)
            
#             with open(filename, 'wb') as f:
#                 f.write(audio_bytes)
            
#             # رفع على Cloudinary
#             try:
#                 public_id = f"podcast_audio/{name}_{uuid.uuid4().hex[:8]}"
#                 upload_result = cloudinary.uploader.upload(
#                     filename,
#                     public_id=public_id,
#                     resource_type="auto",
#                     folder="podcast_audio"
#                 )
                
#                 audio_url = upload_result.get('secure_url')
#                 duration = upload_result.get('duration', duration)
                
#                 print(f"☁️ Uploaded to Cloudinary: {audio_url}")
                
#                 os.remove(filename)
                
#                 return {
#                     'success': True,
#                     'audio_url': audio_url,
#                     'duration': duration,
#                     'voice': voice_name,
#                     'voice_id': voice_id,
#                     'persona': persona,
#                     'style': style,
#                     'language': final_language,
#                     'gender': gender,
#                     'age': age,
#                     'speed': speed
#                 }
                
#             except Exception as e:
#                 print(f"⚠️ Cloudinary upload failed: {e}")
#                 audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
#                 os.remove(filename)
#                 return {
#                     'success': True,
#                     'audio_base64': audio_base64,
#                     'voice': voice_name,
#                     'voice_id': voice_id,
#                     'persona': persona,
#                     'style': style,
#                     'language': final_language,
#                     'speed': speed
#                 }
                
#         except Exception as e:
#             print(f"❌ Error: {e}")
#             return {'success': False, 'error': str(e)}
    
#     def get_available_voices(self):
#         return [{'id': vid, 'name': v['name'], 'gender': v['gender'], 
#                  'style': v.get('style', 'natural'), 
#                  'description': v.get('description', ''),
#                  'language': v.get('language', 'en'),
#                  'voice_id': v.get('id', vid)} 
#                 for vid, v in AVAILABLE_VOICES.items()]
    
#     def get_styles(self):
#         return [{'id': s, 'name': s} for s in STYLES.keys()]
    
#     def get_personas(self):
#         return [{'id': p, 'name': data['name'], 'description': data['description']} 
#                 for p, data in PERSONAS.items()]
import os
import uuid
import base64
import tempfile
import time
import httpx
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from gtts import gTTS
import cloudinary.uploader
import numpy as np
from scipy.io import wavfile

load_dotenv()

# تكوين Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

def convert_pcm_to_wav(pcm_data: bytes, sample_rate: int = 24000) -> bytes:
    """تحويل PCM إلى WAV (من غير FFmpeg)"""
    try:
        audio_array = np.frombuffer(pcm_data, dtype=np.int16)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
            wav_path = tmp.name
        
        wavfile.write(wav_path, sample_rate, audio_array)
        
        with open(wav_path, 'rb') as f:
            wav_bytes = f.read()
        
        os.unlink(wav_path)
        return wav_bytes
        
    except Exception as e:
        print(f"⚠️ PCM to WAV error: {e}")
        return pcm_data

# ========== الأصوات الإنجليزية (ElevenLabs) ==========
ENGLISH_VOICES = {
    "adam": {"id": "pNInz6obpgDQGcFmaJgB", "name": "Adam", "gender": "male", "style": "professional"},
    "sarah": {"id": "EXAVITQu4vr4xnSDxMaL", "name": "Sarah", "gender": "female", "style": "professional"},
    "george": {"id": "JBFqnCBsd6RMkjVDRZzb", "name": "George", "gender": "male", "style": "warm"},
    "alice": {"id": "Xb7hH8MSUJpSbSDYk0k2", "name": "Alice", "gender": "female", "style": "calm"},
    "charlie": {"id": "IKne3meq5aSn9XLyUdCD", "name": "Charlie", "gender": "male", "style": "energetic"},
    "bella": {"id": "hpp4J3VqNfWAUOO0d1Us", "name": "Bella", "gender": "female", "style": "warm"},
    "jessica": {"id": "cgSgspJ2msm6clMCkdW9", "name": "Jessica", "gender": "female", "style": "energetic"}
}

# ========== الأصوات العربية من Munsit (اللي شغالة بس) ==========
MUNSIT_VOICES = {
    # Najdi (سعودي) - شغالة
    "fahad": {"id": "ar-najdi-male-2", "name": "Fahad", "gender": "male", "dialect": "saudi", "style": "professional"},
    "maha": {"id": "ar-najdi-female-1", "name": "Maha", "gender": "female", "dialect": "saudi", "style": "calm"},
    "reem": {"id": "ar-najdi-female-2", "name": "Reem", "gender": "female", "dialect": "saudi", "style": "calm"},
    
    # Hijazi (حجازي) - شغالة
    "lama": {"id": "ar-hijazi-female-1", "name": "Lama", "gender": "female", "dialect": "hijazi", "style": "warm"},
}

# ========== إعدادات الستايلات ==========
STYLES = {
    "calm": {"stability": 0.8, "similarity_boost": 0.5},
    "energetic": {"stability": 0.4, "similarity_boost": 0.8},
    "professional": {"stability": 0.7, "similarity_boost": 0.6},
    "warm": {"stability": 0.6, "similarity_boost": 0.7},
    "authoritative": {"stability": 0.75, "similarity_boost": 0.55},
    "clear": {"stability": 0.75, "similarity_boost": 0.7},
    "natural": {"stability": 0.65, "similarity_boost": 0.65}
}

# ========== الستايلات المتاحة لكل لهجة ==========
DIALECT_STYLES = {
    "saudi": ["professional", "calm"],
    "hijazi": ["warm"],
    "egyptian": []  # gTTS
}

# ========== الـ voice_id لكل لهجة وجنس ==========
DIALECT_VOICE_IDS = {
    "saudi": {
        "male": "ar-najdi-male-2",
        "female": "ar-najdi-female-1"
    },
    "hijazi": {
        "male": None,
        "female": "ar-hijazi-female-1"
    },
    "egyptian": {
        "male": None,
        "female": None
    }
}

MODEL_ID = "eleven_turbo_v2"

def detect_language(text: str) -> str:
    arabic_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
    return 'ar' if arabic_chars > len(text) * 0.3 else 'en'

def generate_arabic_gtts(text: str, speed: float = 1.0) -> bytes:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
        tmp_path = tmp.name
    
    tts = gTTS(text=text, lang='ar', slow=(speed < 0.8))
    tts.save(tmp_path)
    
    with open(tmp_path, 'rb') as f:
        audio_bytes = f.read()
    
    try:
        os.unlink(tmp_path)
    except:
        time.sleep(0.1)
        os.unlink(tmp_path)
    
    return audio_bytes

class AudioAgent:
    def __init__(self):
        # ElevenLabs keys
        self.elevenlabs_keys = []
        for i in range(1, 10):
            key = os.getenv(f"ELEVENLABS_API_KEY{i}")
            if key:
                self.elevenlabs_keys.append(key)
        
        self.current_key_index = 0
        
        # Munsit keys
        self.munsit_keys = []
        for i in range(1, 10):
            key = os.getenv(f"MUNSIT_API_KEY{i}")
            if key:
                self.munsit_keys.append(key)
        
        self.current_munsit_index = 0
        
        print(f"✅ ElevenLabs: {len(self.elevenlabs_keys)} keys loaded")
        print(f"✅ Munsit: {len(self.munsit_keys)} keys loaded")
        print(f"✅ Munsit Voices: {len(MUNSIT_VOICES)} voices available")
        print(f"✅ Cloudinary: Configured")
    
    def get_elevenlabs_key(self):
        if not self.elevenlabs_keys:
            return None
        return self.elevenlabs_keys[self.current_key_index]
    
    def rotate_elevenlabs_key(self):
        if not self.elevenlabs_keys:
            return None
        self.current_key_index = (self.current_key_index + 1) % len(self.elevenlabs_keys)
        return self.get_elevenlabs_key()
    
    def get_munsit_key(self):
        if not self.munsit_keys:
            return None
        return self.munsit_keys[self.current_munsit_index]
    
    def rotate_munsit_key(self):
        if not self.munsit_keys:
            return None
        self.current_munsit_index = (self.current_munsit_index + 1) % len(self.munsit_keys)
        return self.get_munsit_key()
    
    def get_available_styles_for_dialect(self, dialect: str) -> list:
        return DIALECT_STYLES.get(dialect, ["professional"])
    
    async def generate_speech(
        self, 
        text: str, 
        persona: str = "host",
        name: str = "Speaker",
        language: str = "en",
        gender: str = "male",
        dialect: str = "egyptian",
        style: str = "professional",
        speed: float = 1.0,
        voice_id: str = None
    ) -> Dict[str, Any]:
        
        try:
            if not text or not text.strip():
                return {'success': False, 'error': 'Text cannot be empty'}
            
            detected_lang = detect_language(text)
            final_language = language if language != "ar-eg" else "ar"
            if final_language == "en" and detected_lang == "ar":
                final_language = "ar"
            
            print(f"\n{'='*50}")
            print(f"🎤 Generating speech for {persona}: {name}")
            print(f"   Language: {final_language}, Dialect: {dialect}")
            print(f"   Gender: {gender}, Style: {style}")
            print(f"   Speed: {speed}x (user selected)")
            print(f"   Text: {text[:80]}...")
            print(f"{'='*50}")
            
            # ========== العربية ==========
            if final_language == 'ar':
                # مصري => gTTS
                if dialect == 'egyptian':
                    print("🎙️ Using gTTS (Egyptian Arabic)")
                    audio_bytes = generate_arabic_gtts(text, speed)
                    
                    filename = f"audio_files/{uuid.uuid4()}.mp3"
                    os.makedirs("audio_files", exist_ok=True)
                    with open(filename, 'wb') as f:
                        f.write(audio_bytes)
                    
                    upload_result = cloudinary.uploader.upload(
                        filename, 
                        folder="podcast_audio",
                        resource_type="auto"
                    )
                    os.remove(filename)
                    
                    return {
                        'success': True,
                        'audio_url': upload_result.get('secure_url'),
                        'duration': upload_result.get('duration', len(audio_bytes) / 16000),
                        'voice': 'Egyptian Arabic (gTTS)',
                        'dialect': 'egyptian',
                        'provider': 'gtts',
                        'persona': persona,
                        'style': style,
                        'language': final_language,
                        'gender': gender,
                        'speed': speed
                    }
                
                # للهجات التانية (سعودي، حجازي) => Munsit
                # تحديد voice_id المناسب
                voice_id_to_use = None
                if dialect in DIALECT_VOICE_IDS:
                    voice_id_to_use = DIALECT_VOICE_IDS[dialect].get(gender)
                
                if not voice_id_to_use:
                    print(f"⚠️ No voice_id for {dialect}/{gender}, falling back to gTTS")
                    audio_bytes = generate_arabic_gtts(text, speed)
                    filename = f"audio_files/{uuid.uuid4()}.mp3"
                    os.makedirs("audio_files", exist_ok=True)
                    with open(filename, 'wb') as f:
                        f.write(audio_bytes)
                    upload_result = cloudinary.uploader.upload(filename, folder="podcast_audio", resource_type="auto")
                    os.remove(filename)
                    return {
                        'success': True,
                        'audio_url': upload_result.get('secure_url'),
                        'duration': upload_result.get('duration', len(audio_bytes) / 16000),
                        'voice': f'{dialect.capitalize()} (gTTS Fallback)',
                        'dialect': dialect,
                        'provider': 'gtts',
                        'persona': persona,
                        'style': style,
                        'language': final_language,
                        'gender': gender,
                        'speed': speed
                    }
                
                # تجربة Munsit
                for attempt in range(len(self.munsit_keys)):
                    try:
                        api_key = self.get_munsit_key()
                        if not api_key:
                            break
                        
                        print(f"🎙️ Trying Munsit: {name} ({dialect}) - Style: {style} with voice_id: {voice_id_to_use}")
                        
                        async with httpx.AsyncClient(timeout=30.0) as client:
                            response = await client.post(
                                "https://api.munsit.com/api/v1/text-to-speech/faseeh-v1-preview",
                                headers={
                                    "x-api-key": api_key,
                                    "Content-Type": "application/json"
                                },
                                json={
                                    "text": text,
                                    "voice_id": voice_id_to_use,
                                    "speed": speed,
                                    "streaming": True
                                }
                            )
                            
                            if response.status_code == 200:
                                audio_bytes = response.content
                                
                                # تحويل PCM إلى WAV إذا لزم الأمر
                                content_type = response.headers.get('content-type', '')
                                if 'pcm' in content_type or 'x-pcm' in content_type:
                                    print("🔄 Converting PCM to WAV...")
                                    try:
                                        audio_bytes = convert_pcm_to_wav(audio_bytes)
                                        file_ext = '.wav'
                                    except Exception as e:
                                        print(f"⚠️ Conversion failed: {e}")
                                        file_ext = '.pcm'
                                else:
                                    file_ext = '.mp3'
                                
                                filename = f"audio_files/{uuid.uuid4()}{file_ext}"
                                os.makedirs("audio_files", exist_ok=True)
                                with open(filename, 'wb') as f:
                                    f.write(audio_bytes)
                                
                                upload_result = cloudinary.uploader.upload(
                                    filename, 
                                    folder="podcast_audio",
                                    resource_type="auto"
                                )
                                os.remove(filename)
                                
                                print(f"✅ Munsit success: {upload_result.get('secure_url')}")
                                
                                return {
                                    'success': True,
                                    'audio_url': upload_result.get('secure_url'),
                                    'duration': upload_result.get('duration', 0),
                                    'voice': name,
                                    'dialect': dialect,
                                    'provider': 'munsit',
                                    'persona': persona,
                                    'style': style,
                                    'language': final_language,
                                    'gender': gender,
                                    'speed': speed
                                }
                            else:
                                print(f"⚠️ Munsit attempt {attempt+1} failed: {response.status_code}")
                                try:
                                    error_text = response.text
                                    print(f"   Error details: {error_text[:200]}")
                                except:
                                    pass
                                self.rotate_munsit_key()
                                
                    except Exception as e:
                        print(f"⚠️ Munsit error: {e}")
                        self.rotate_munsit_key()
                        continue
                
                # Fallback: gTTS لو فشل Munsit
                print(f"⚠️ Munsit failed for dialect: {dialect}, falling back to gTTS")
                audio_bytes = generate_arabic_gtts(text, speed)
                filename = f"audio_files/{uuid.uuid4()}.mp3"
                os.makedirs("audio_files", exist_ok=True)
                with open(filename, 'wb') as f:
                    f.write(audio_bytes)
                upload_result = cloudinary.uploader.upload(filename, folder="podcast_audio", resource_type="auto")
                os.remove(filename)
                return {
                    'success': True,
                    'audio_url': upload_result.get('secure_url'),
                    'duration': upload_result.get('duration', len(audio_bytes) / 16000),
                    'voice': f'{dialect.capitalize()} (gTTS Fallback)',
                    'dialect': dialect,
                    'provider': 'gtts',
                    'persona': persona,
                    'style': style,
                    'language': final_language,
                    'gender': gender,
                    'speed': speed
                }
            
            # ========== الإنجليزية (ElevenLabs) ==========
            else:
                selected_voice = None
                for v in ENGLISH_VOICES.values():
                    if v['gender'] == gender and v['style'] == style:
                        selected_voice = v
                        break
                if not selected_voice:
                    for v in ENGLISH_VOICES.values():
                        if v['gender'] == gender:
                            selected_voice = v
                            break
                if not selected_voice:
                    selected_voice = ENGLISH_VOICES['adam']
                
                style_settings = STYLES.get(style, STYLES["professional"])
                
                for attempt in range(len(self.elevenlabs_keys)):
                    try:
                        api_key = self.get_elevenlabs_key()
                        if not api_key:
                            raise Exception("No ElevenLabs API keys available")
                        
                        print(f"🎙️ Trying ElevenLabs account {attempt+1}: {selected_voice['name']}")
                        
                        client = ElevenLabs(api_key=api_key)
                        
                        audio_generator = client.text_to_speech.convert(
                            text=text,
                            voice_id=selected_voice['id'],
                            model_id=MODEL_ID,
                            output_format="mp3_44100_128",
                            voice_settings={
                                "stability": style_settings["stability"],
                                "similarity_boost": style_settings["similarity_boost"]
                            }
                        )
                        
                        audio_bytes = b"".join(chunk for chunk in audio_generator)
                        
                        filename = f"audio_files/{uuid.uuid4()}.mp3"
                        os.makedirs("audio_files", exist_ok=True)
                        with open(filename, 'wb') as f:
                            f.write(audio_bytes)
                        
                        upload_result = cloudinary.uploader.upload(
                            filename, 
                            folder="podcast_audio",
                            resource_type="auto"
                        )
                        os.remove(filename)
                        
                        print(f"✅ ElevenLabs success: {upload_result.get('secure_url')}")
                        
                        return {
                            'success': True,
                            'audio_url': upload_result.get('secure_url'),
                            'duration': upload_result.get('duration', 0),
                            'voice': selected_voice['name'],
                            'provider': 'elevenlabs',
                            'persona': persona,
                            'style': style,
                            'language': final_language,
                            'gender': gender,
                            'speed': speed
                        }
                        
                    except Exception as e:
                        print(f"⚠️ ElevenLabs account {attempt+1} failed: {e}")
                        self.rotate_elevenlabs_key()
                        continue
                
                return {'success': False, 'error': 'All ElevenLabs accounts failed'}
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_available_voices(self, language=None, dialect=None):
        voices = []
        
        if language != 'ar':
            for v in ENGLISH_VOICES.values():
                voices.append({**v, 'provider': 'elevenlabs', 'language': 'en'})
        
        if language != 'en':
            for v_id, v in MUNSIT_VOICES.items():
                if dialect and v['dialect'] != dialect:
                    continue
                voices.append({
                    'id': v_id, 
                    'name': v['name'], 
                    'gender': v['gender'],
                    'dialect': v['dialect'],
                    'style': v['style'],
                    'provider': 'munsit', 
                    'language': 'ar'
                })
            
            voices.append({
                'id': 'gtts', 
                'name': 'Egyptian Arabic (gTTS - Free)',
                'gender': 'neutral', 
                'dialect': 'egyptian',
                'provider': 'gtts', 
                'language': 'ar'
            })
        
        return voices

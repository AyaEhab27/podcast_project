# import os
# from dotenv import load_dotenv

# load_dotenv()

# # ElevenLabs Configuration
# ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
# ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

# # ========== قاعدة الأصوات المتاحة (النسخة النهائية) ==========
# AVAILABLE_VOICES = {
#     # ========== أصوات رجالية عربية ==========
#     "elareef_warm": {
#         "id": "VqHyN6PYNu3uNKGdbxKs",
#         "name": "Elareef",
#         "gender": "male",
#         "style": "warm",
#         "age": "adult",
#         "language": "ar",
#         "description": "دافيء، ودود - مناسب للضيوف والمحتوى العاطفي"
#     },
#     "mamdoh_deep": {
#         "id": "68MRVrnQAt8vLbu0FCzw",
#         "name": "Mamdoh",
#         "gender": "male",
#         "style": "deep",
#         "age": "adult",
#         "language": "ar",
#         "description": "عميق، قوي - مناسب للمقدمين والمحتوى الجاد"
#     },
#     "abdullah_professional": {
#         "id": "ocqVw6LVSdCxCra4XhMH",
#         "name": "Abdullah",
#         "gender": "male",
#         "style": "professional",
#         "age": "adult",
#         "language": "ar",
#         "description": "احترافي، واضح - مناسب للبودكاست التقني"
#     },
#     "ahmed_expressive": {
#         "id": "ihycSANIrpHfhWoaq1g3",
#         "name": "Ahmed",
#         "gender": "male",
#         "style": "expressive",
#         "age": "adult",
#         "language": "ar",
#         "description": "معبر، حيوي - مناسب للقصص والمحتوى التحفيزي"
#     },
#     "adham_narrator": {
#         "id": "OFHP1Qg30FPoNfkUFFlA",
#         "name": "Adham",
#         "gender": "male",
#         "style": "calm",
#         "age": "adult",
#         "language": "ar",
#         "description": "راوي، هادئ - مناسب للسرد والقصص"
#     },
#     "hanafi_energetic": {
#         "id": "DWMVT5WflKt0P8OPpIrY",
#         "name": "Hanafi",
#         "gender": "male",
#         "style": "energetic",
#         "age": "adult",
#         "language": "ar",
#         "description": "واثق، قوي - مناسب للافتتاحيات"
#     },
    
#     # ========== أصوات نسائية عربية ==========
#     "yasmine_natural": {
#         "id": "L10lEremDiJfPicq5CPh",
#         "name": "Yasmine",
#         "gender": "female",
#         "style": "natural",
#         "age": "adult",
#         "language": "ar",
#         "description": "طبيعي، سلس - مناسب للمحادثات العامة"
#     },
#     "hoda_expressive": {
#         "id": "meAbY2VpJkt1q46qk56T",
#         "name": "Hoda",
#         "gender": "female",
#         "style": "expressive",
#         "age": "adult",
#         "language": "ar",
#         "description": "معبر، حيوي - مناسب للمحتوى العاطفي"
#     },
#     "salma_clear": {
#         "id": "B5xxC4eQoOFJnY4R5XkI",
#         "name": "Salma",
#         "gender": "female",
#         "style": "clear",
#         "age": "adult",
#         "language": "ar",
#         "description": "صوت واضح، نقي - مناسب للشرح والتعليم"
#     },
#     "sama_professional": {
#         "id": "a1KZUXKFVFDOb33I1uqr",
#         "name": "Sama",
#         "gender": "female",
#         "style": "professional",
#         "age": "adult",
#         "language": "ar",
#         "description": "احترافي، راقي - مناسب للمحتوى الرسمي"
#     },
#     "ghaida_young": {
#         "id": "Wim44P0dU9HtjyzNnFsv",
#         "name": "Ghaida",
#         "gender": "female",
#         "style": "natural",
#         "age": "young",
#         "language": "ar",
#         "description": "شابة، طبيعي - مناسبة للمحتوى الشبابي"
#     },
#     "adina_young": {
#         "id": "FvmvwvObRqIHojkEGh5N",
#         "name": "Adina",
#         "gender": "female",
#         "style": "warm",
#         "age": "young",
#         "language": "ar",
#         "description": "شابة، دافيء - مناسبة للقصص والمحتوى العاطفي"
#     },
    
#     # ========== أصوات أطفال ==========
#     "little_girl_ana": {
#         "id": "rCmVtv8cYU60uhlsOo1M",
#         "name": "Little Girl (Ana)",
#         "gender": "female",
#         "style": "natural",
#         "age": "child",
#         "language": "en",
#         "description": "طفلة صغيرة - مناسبة لقصص الأطفال"
#     },
    
#     # ========== أصوات إنجليزية ==========
#     "edward_british_deep": {
#         "id": "goT3UYdM9bhm0n2lmKQx",
#         "name": "Edward",
#         "gender": "male",
#         "style": "deep",
#         "age": "adult",
#         "language": "en",
#         "description": "British, deep, seductive - مناسب للروايات"
#     },
#     "dallin_storyteller": {
#         "id": "alFofuDn3cOwyoz1i44T",
#         "name": "Dallin",
#         "gender": "male",
#         "style": "calm",
#         "age": "adult",
#         "language": "en",
#         "description": "American, calming, warm - مناسب للقصص"
#     },
#     "victoria_warm": {
#         "id": "qSeXEcewz7tA0Q0qk9fH",
#         "name": "Victoria",
#         "gender": "female",
#         "style": "warm",
#         "age": "adult",
#         "language": "en",
#         "description": "Warm, trustworthy - مناسب للتعليم والشرح"
#     },
#     "drew_flirty": {
#         "id": "65dhNaIr3Y4ovumVtdy0",
#         "name": "Drew",
#         "gender": "male",
#         "style": "expressive",
#         "age": "adult",
#         "language": "en",
#         "description": "American, flirty - مناسب للروايات الرومانسية"
#     },
#     "ivy_sophisticated": {
#         "id": "MClEFoImJXBTgLwdLI5n",
#         "name": "Ivy",
#         "gender": "female",
#         "style": "professional",
#         "age": "adult",
#         "language": "en",
#         "description": "Sophisticated, sassy - مناسب للمحتوى الاحترافي"
#     },
#     "joseph_professional": {
#         "id": "8fcyCHOzlKDlxh1InJSf",
#         "name": "Joseph",
#         "gender": "male",
#         "style": "professional",
#         "age": "adult",
#         "language": "en",
#         "description": "Professional, calm - مناسب للدعم والمحتوى الرسمي"
#     }
# }

# # خريطة لتحويل طلب المستخدم إلى أقرب صوت
# STYLE_MAPPING = {
#     "calm": ["adham_narrator", "dallin_storyteller", "joseph_professional"],
#     "warm": ["elareef_warm", "adina_young", "victoria_warm"],
#     "energetic": ["hanafi_energetic", "hoda_expressive", "drew_flirty"],
#     "professional": ["abdullah_professional", "sama_professional", "ivy_sophisticated"],
#     "expressive": ["ahmed_expressive", "hoda_expressive", "drew_flirty"],
#     "deep": ["mamdoh_deep", "edward_british_deep"],
#     "natural": ["yasmine_natural", "ghaida_young", "little_girl_ana"],
#     "clear": ["salma_clear", "ivy_sophisticated"]
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
#     "child": {
#         "name": "Child",
#         "description": "صوت طفل - مناسب للقصص الأطفال",
#         "preferred_style": "natural",
#         "preferred_gender": "female",
#         "preferred_age": "child"
#     },
#     "teacher": {
#         "name": "Teacher",
#         "description": "صوت تعليمي - واضح، احترافي",
#         "preferred_style": "clear",
#         "preferred_gender": "female"
#     }
# }

# # Style settings for ElevenLabs
# STYLES = {
#     "calm": {
#         "stability": 0.8,
#         "similarity_boost": 0.5,
#         "description": "هادئ ومتوازن"
#     },
#     "energetic": {
#         "stability": 0.4,
#         "similarity_boost": 0.8,
#         "description": "نشيط ومعبر"
#     },
#     "professional": {
#         "stability": 0.7,
#         "similarity_boost": 0.6,
#         "description": "احترافي وواضح"
#     },
#     "warm": {
#         "stability": 0.6,
#         "similarity_boost": 0.7,
#         "description": "دافيء وودود"
#     },
#     "expressive": {
#         "stability": 0.5,
#         "similarity_boost": 0.8,
#         "description": "معبر وحيوي"
#     },
#     "deep": {
#         "stability": 0.7,
#         "similarity_boost": 0.5,
#         "description": "عميق وقوي"
#     },
#     "natural": {
#         "stability": 0.65,
#         "similarity_boost": 0.65,
#         "description": "طبيعي وسلس"
#     },
#     "clear": {
#         "stability": 0.75,
#         "similarity_boost": 0.7,
#         "description": "واضح ونقي"
#     }
# }

# # Model ID
# MODEL_ID = "eleven_monolingual_v1"


# def find_best_voice(gender: str, style: str, age: str = "adult") -> dict:
#     """
#     البحث عن أفضل صوت بناءً على الجنس والستايل والعمر المطلوب
#     """
#     # محاولة العثور على صوت بنفس الجنس والستايل والعمر
#     for voice_id, voice in AVAILABLE_VOICES.items():
#         if (voice["gender"] == gender and 
#             voice.get("style") == style and 
#             voice.get("age") == age):
#             return voice
    
#     # إذا لم يوجد، حاول بدون العمر
#     for voice_id, voice in AVAILABLE_VOICES.items():
#         if voice["gender"] == gender and voice.get("style") == style:
#             return voice
    
#     # إذا لم يوجد، استخدم الخريطة
#     if style in STYLE_MAPPING:
#         for voice_key in STYLE_MAPPING[style]:
#             if voice_key in AVAILABLE_VOICES:
#                 voice = AVAILABLE_VOICES[voice_key]
#                 if voice["gender"] == gender:
#                     return voice
    
#     # آخر حل: أول صوت بنفس الجنس
#     for voice in AVAILABLE_VOICES.values():
#         if voice["gender"] == gender:
#             return voice
    
#     # حل أخير
#     return AVAILABLE_VOICES["abdullah_professional"]
import os
from dotenv import load_dotenv

load_dotenv()

# ElevenLabs Configuration
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

# ========== الأصوات من حسابك الفعلي (من القائمة اللي طلعت) ==========
AVAILABLE_VOICES = {
    # أصوات رجالية
    "adam": {
        "id": "pNInz6obpgDQGcFmaJgB",
        "name": "Adam",
        "gender": "male",
        "style": "professional",
        "age": "adult",
        "language": "en",
        "description": "Dominant, Firm"
    },
    "abdullah": {
        "id": "ocqVw6LVSdCxCra4XhMH",
        "name": "Abdullah",
        "gender": "male",
        "style": "professional",
        "age": "adult",
        "language": "ar",
        "description": "Egyptian Arabic Voice"
    },
    "charlie": {
        "id": "IKne3meq5aSn9XLyUdCD",
        "name": "Charlie",
        "gender": "male",
        "style": "energetic",
        "age": "adult",
        "language": "en",
        "description": "Deep, Confident, Energetic"
    },
    "george": {
        "id": "JBFqnCBsd6RMkjVDRZzb",
        "name": "George",
        "gender": "male",
        "style": "warm",
        "age": "adult",
        "language": "en",
        "description": "Warm, Captivating Storyteller"
    },
    
    # أصوات نسائية
    "sarah": {
        "id": "EXAVITQu4vr4xnSDxMaL",
        "name": "Sarah",
        "gender": "female",
        "style": "professional",
        "age": "adult",
        "language": "en",
        "description": "Mature, Reassuring, Confident"
    },
    "alice": {
        "id": "Xb7hH8MSUJpSbSDYk0k2",
        "name": "Alice",
        "gender": "female",
        "style": "clear",
        "age": "adult",
        "language": "en",
        "description": "Clear, Engaging Educator"
    },
    "bella": {
        "id": "hpp4J3VqNfWAUOO0d1Us",
        "name": "Bella",
        "gender": "female",
        "style": "warm",
        "age": "adult",
        "language": "en",
        "description": "Professional, Bright, Warm"
    },
    "jessica": {
        "id": "cgSgspJ2msm6clMCkdW9",
        "name": "Jessica",
        "gender": "female",
        "style": "expressive",
        "age": "adult",
        "language": "en",
        "description": "Playful, Bright, Warm"
    }
}

# خريطة الستايلات
STYLE_MAPPING = {
    "calm": ["george", "sarah"],
    "warm": ["george", "bella", "jessica"],
    "energetic": ["charlie", "jessica"],
    "professional": ["adam", "sarah", "abdullah"],
    "expressive": ["jessica", "charlie"],
    "deep": ["adam", "charlie"],
    "natural": ["alice", "bella"],
    "clear": ["alice", "sarah"]
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
    "child": {
        "name": "Child",
        "description": "صوت طفل - مناسب للقصص الأطفال",
        "preferred_style": "natural",
        "preferred_gender": "female"
    },
    "teacher": {
        "name": "Teacher",
        "description": "صوت تعليمي - واضح، احترافي",
        "preferred_style": "clear",
        "preferred_gender": "female"
    }
}

# Style settings for ElevenLabs
STYLES = {
    "calm": {"stability": 0.8, "similarity_boost": 0.5, "description": "هادئ ومتوازن"},
    "energetic": {"stability": 0.4, "similarity_boost": 0.8, "description": "نشيط ومعبر"},
    "professional": {"stability": 0.7, "similarity_boost": 0.6, "description": "احترافي وواضح"},
    "warm": {"stability": 0.6, "similarity_boost": 0.7, "description": "دافيء وودود"},
    "expressive": {"stability": 0.5, "similarity_boost": 0.8, "description": "معبر وحيوي"},
    "deep": {"stability": 0.7, "similarity_boost": 0.5, "description": "عميق وقوي"},
    "natural": {"stability": 0.65, "similarity_boost": 0.65, "description": "طبيعي وسلس"},
    "clear": {"stability": 0.75, "similarity_boost": 0.7, "description": "واضح ونقي"}
}

MODEL_ID = "eleven_turbo_v2"


def find_best_voice(gender: str, style: str, age: str = "adult") -> dict:
    """البحث عن أفضل صوت بناءً على الجنس والستايل"""
    if style in STYLE_MAPPING:
        for voice_key in STYLE_MAPPING[style]:
            if voice_key in AVAILABLE_VOICES:
                voice = AVAILABLE_VOICES[voice_key]
                if voice["gender"] == gender:
                    return voice
    
    # إذا لم يوجد، أرجع أول صوت بنفس الجنس
    for voice in AVAILABLE_VOICES.values():
        if voice["gender"] == gender:
            return voice
    
    # حل أخير
    return AVAILABLE_VOICES["adam"]
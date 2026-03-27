import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import requests

load_dotenv()

# الحصول على API Key
api_key = os.getenv("ELEVENLABS_API_KEY")
print(f"🔑 API Key: {api_key[:15]}...")

# تهيئة العميل
client = ElevenLabs(api_key=api_key)

# قائمة الأصوات المتاحة
print("\n📢 جلب الأصوات المتاحة...")
try:
    response = requests.get(
        "https://api.elevenlabs.io/v1/voices",
        headers={"xi-api-key": api_key}
    )
    if response.status_code == 200:
        voices = response.json()["voices"]
        print(f"✅ تم جلب {len(voices)} صوت")
        for i, voice in enumerate(voices[:10]):
            print(f"   {i+1}. {voice['name']} - ID: {voice['voice_id']}")
    else:
        print(f"❌ فشل: {response.status_code}")
except Exception as e:
    print(f"❌ خطأ: {e}")

# اختبار توليد صوت
print("\n🎤 توليد صوت تجريبي...")
try:
    # استخدام صوت George (ID معروف)
    audio = client.text_to_speech.convert(
        text="Hello",
        voice_id="JBFqnCBsd6RMkjVDRZzb",  # George voice
        model_id="eleven_monolingual_v1",
        output_format="mp3_44100_128"
    )
    
    # حفظ الصوت
    with open("test_output.mp3", "wb") as f:
        for chunk in audio:
            f.write(chunk)
    print("✅ تم حفظ الصوت في test_output.mp3")
    
    # تشغيل الصوت (اختياري)
    # play(audio)
    print("🎧 يمكنك فتح test_output.mp3 لتشغيل الصوت")
    
except Exception as e:
    print(f"❌ فشل التوليد: {e}")
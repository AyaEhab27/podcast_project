import asyncio
import httpx
import json
from typing import Any, Dict, Optional

API_BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 30.0

async def make_request(client: httpx.AsyncClient, method: str, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]:
    """Make HTTP request with error handling"""
    response = None
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method.upper() == "GET":
            response = await client.get(url, timeout=TIMEOUT, **kwargs)
        elif method.upper() == "POST":
            response = await client.post(url, timeout=TIMEOUT, **kwargs)
        else:
            print(f"❌ Unsupported method: {method}")
            return None
        
        response.raise_for_status()
        return response.json()
    except httpx.TimeoutException:
        print(f"❌ Timeout error: Request took longer than {TIMEOUT}s")
        return None
    except httpx.ConnectError:
        print(f"❌ Connection error: Cannot connect to {API_BASE_URL}")
        return None
    except httpx.HTTPStatusError as e:
        status = response.status_code if response else "Unknown"
        print(f"❌ HTTP error {status}: {e}")
        return None
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON response")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

async def test_api():
    async with httpx.AsyncClient() as client:
        tests_passed = 0
        tests_failed = 0
        
        print("="*50)
        print("1. Testing GET /")
        print("="*50)
        data = await make_request(client, "GET", "/")
        if data:
            print(json.dumps(data, indent=2, ensure_ascii=False))
            tests_passed += 1
        else:
            tests_failed += 1
        
        print("\n" + "="*50)
        print("2. Testing GET /voices")
        print("="*50)
        data = await make_request(client, "GET", "/voices")
        if data and 'total' in data and 'voices' in data:
            print(f"Total voices: {data['total']}")
            for voice in data['voices'][:5]:  # أول 5 أصوات
                print(f"  - {voice['name']} ({voice['language']})")
            tests_passed += 1
        else:
            tests_failed += 1
        
        print("\n" + "="*50)
        print("3. Testing GET /styles")
        print("="*50)
        data = await make_request(client, "GET", "/styles")
        if data and 'styles' in data:
            for style in data['styles']:
                print(f"  - {style['name']}: pitch={style['pitch']}, speed={style['speed']}")
            tests_passed += 1
        else:
            tests_failed += 1
        
        print("\n" + "="*50)
        print("4. Testing POST /text-to-speech (Arabic Egyptian)")
        print("="*50)
        result = await make_request(client, "POST", "/text-to-speech",
            json={
                "text": "أهلاً بيكم في بودكاست PodCraft AI! النهاردة هنتكلم عن الذكاء الاصطناعي في مصر",
                "voice_id": "egyptian_male_adult",
                "style": "energetic",
                "speed": 1.0
            }
        )
        if result:
            if result.get('success'):
                print(f"✅ Success!")
                print(f"   Audio URL: {result.get('audio_url')}")
                print(f"   Voice: {result.get('voice')}")
                print(f"   Duration: {result.get('duration')} seconds")
                tests_passed += 1
            else:
                print(f"❌ Failed: {result.get('error')}")
                tests_failed += 1
        else:
            tests_failed += 1
        
        print("\n" + "="*50)
        print("5. Testing POST /text-to-speech (English)")
        print("="*50)
        result = await make_request(client, "POST", "/text-to-speech",
            json={
                "text": "Welcome to PodCraft AI podcast! Today we're talking about artificial intelligence",
                "voice_id": "english_female_adult",
                "style": "professional",
                "speed": 1.0
            }
        )
        if result:
            if result.get('success'):
                print(f"✅ Success!")
                print(f"   Audio URL: {result.get('audio_url')}")
                print(f"   Voice: {result.get('voice')}")
                tests_passed += 1
            else:
                print(f"❌ Failed: {result.get('error')}")
                tests_failed += 1
        else:
            tests_failed += 1
        
        print("\n" + "="*50)
        print("6. Testing auto-detect (without voice_id)")
        print("="*50)
        result = await make_request(client, "POST", "/text-to-speech",
            json={
                "text": "السلام عليكم، كيف حالكم؟",
                "gender": "female",
                "age": "adult",
                "style": "calm"
            }
        )
        if result:
            if result.get('success'):
                print(f"✅ Success! Auto-detected voice: {result.get('voice')}")
                print(f"   Audio URL: {result.get('audio_url')}")
                tests_passed += 1
            else:
                print(f"❌ Failed: {result.get('error')}")
                tests_failed += 1
        else:
            tests_failed += 1
        
        return tests_passed, tests_failed

if __name__ == "__main__":
    print(f"\n🚀 Starting API tests...")
    print(f"Target: {API_BASE_URL}\n")
    try:
        results = asyncio.run(test_api())
        if results:
            passed, failed = results
            print(f"\n{'='*50}")
            print(f"📊 Test Summary:")
            print(f"   ✅ Passed: {passed}")
            print(f"   ❌ Failed: {failed}")
            print(f"   Total: {passed + failed}")
            print(f"{'='*50}")
            if failed == 0:
                print("🎉 All tests passed!")
            else:
                print(f"⚠️ {failed} test(s) failed")
        else:
            print("\n✅ All tests completed!")
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
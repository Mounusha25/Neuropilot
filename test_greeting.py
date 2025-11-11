import requests
import base64

API_URL = "http://localhost:8000/api/audio/start"

print("\n" + "="*60)
print("TEST: AI Greeting (Before User Speaks)")
print("="*60)

# Test 1: Start with default name
print("\n1. Testing with default name:")
response = requests.post(API_URL, data={})

if response.status_code == 200:
    result = response.json()
    print(f"✅ Session ID: {result['session_id']}")
    print(f"✅ AI Greeting: {result['ai_text_response']}")
    print(f"✅ Conversation Count: {result['conversation_count']}")
    
    # Save audio
    audio_data = base64.b64decode(result['audio_response'])
    with open('/tmp/greeting_default.mp3', 'wb') as f:
        f.write(audio_data)
    print("✅ Audio saved: /tmp/greeting_default.mp3")
else:
    print(f"❌ Error: {response.text}")

# Test 2: Start with custom name
print("\n2. Testing with custom name 'Alex':")
response = requests.post(API_URL, data={'user_name': 'Alex'})

if response.status_code == 200:
    result = response.json()
    print(f"✅ Session ID: {result['session_id']}")
    print(f"✅ AI Greeting: {result['ai_text_response']}")
    print(f"✅ Conversation Count: {result['conversation_count']}")
    
    # Save audio
    audio_data = base64.b64decode(result['audio_response'])
    with open('/tmp/greeting_alex.mp3', 'wb') as f:
        f.write(audio_data)
    print("✅ Audio saved: /tmp/greeting_alex.mp3")
else:
    print(f"❌ Error: {response.text}")

print("\n" + "="*60)
print("Play greetings:")
print("  afplay /tmp/greeting_default.mp3")
print("  afplay /tmp/greeting_alex.mp3")
print("="*60)


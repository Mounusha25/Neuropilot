import requests
import base64
import json
from pathlib import Path

# Test the conversational flow
API_URL = "http://localhost:8000/api/audio/converse"

# Create a simple test audio file (you can replace this with actual audio)
# For now, let's just test with a minimal mp3 file
test_audio_path = "/tmp/test_audio.mp3"

# If you have an actual audio file, use it. Otherwise, we'll create a minimal one
# Let's try to use the one we created earlier if it exists
if Path("/tmp/neuropilot_test.mp3").exists():
    test_audio_path = "/tmp/neuropilot_test.mp3"
    print(f"Using existing test audio: {test_audio_path}")
else:
    print("No test audio found. Please record a short audio message.")
    print("You can use: arecord -d 3 -f cd /tmp/test_audio.wav")
    print("Then convert: ffmpeg -i /tmp/test_audio.wav /tmp/test_audio.mp3")
    exit(1)

# Test 1: First conversation (should get greeting)
print("\n" + "="*60)
print("TEST 1: First message (empty history)")
print("="*60)

with open(test_audio_path, 'rb') as audio_file:
    files = {'audio': ('test.mp3', audio_file, 'audio/mpeg')}
    data = {
        'session_id': None,  # Will generate new UUID
        'include_feedback': False
    }
    
    response = requests.post(API_URL, files=files, data=data)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nSession ID: {result['session_id']}")
        print(f"Avatar: {result['avatar']}")
        print(f"User said: {result['user_text']}")
        print(f"AI responded: {result['ai_text_response']}")
        print(f"Conversation count: {result['conversation_count']}")
        
        # Save audio response
        if result.get('audio_response'):
            audio_data = base64.b64decode(result['audio_response'])
            with open('/tmp/test_response.mp3', 'wb') as f:
                f.write(audio_data)
            print("\nAudio response saved to: /tmp/test_response.mp3")
            print("Play with: afplay /tmp/test_response.mp3")
        
        # Save session ID for next test
        session_id = result['session_id']
    else:
        print(f"Error: {response.text}")

print("\n" + "="*60)
print("Test completed!")
print("="*60)


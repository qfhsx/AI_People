import os
import sys
import requests
import json
import time

# Add current directory to path so we can import app
sys.path.append(os.getcwd())

try:
    from app.config import VOLC_ACCESS_KEY, VOLC_SECRET_KEY, RESOURCE_ID
    print("✅ Config loaded.")
    print(f"   Access Key: {VOLC_ACCESS_KEY[:4]}...{VOLC_ACCESS_KEY[-4:]}")
except ImportError:
    print("❌ Could not import config.")
    sys.exit(1)

try:
    from volcengine.visual.VisualService import VisualService
    print("✅ Volcengine SDK installed.")
except ImportError:
    print("❌ Volcengine SDK NOT installed.")
    sys.exit(1)

try:
    from app.service.volc_service import upload_audio_to_public
    print("✅ Service module loaded.")
except ImportError:
    print("❌ Could not import service module.")
    sys.exit(1)

def test_file_upload():
    print("\nTesting File Upload (file.io / transfer.sh)...")
    try:
        dummy_file = "test_audio.txt"
        with open(dummy_file, "w") as f:
            f.write("This is a test audio file content.")
            
        # Use the actual function from service
        link = upload_audio_to_public(os.path.abspath(dummy_file))
        print(f"✅ Upload successful. Link: {link}")
        return link
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None
    finally:
        if os.path.exists("test_audio.txt"):
            os.remove("test_audio.txt")

def test_volc_api(audio_url):
    print("\nTesting Volcengine API...")
    visual_service = VisualService()
    visual_service.set_ak(VOLC_ACCESS_KEY)
    visual_service.set_sk(VOLC_SECRET_KEY)
    
    body = {
        "req_key": "realman_avatar_creation_task",
        "resource_id": RESOURCE_ID,
        "audio_url": audio_url
    }
    
    print(f"   Sending request with Resource ID: {RESOURCE_ID}")
    
    try:
        # Using generic json method
        resp = visual_service.json("CVSubmitTask", {}, json.dumps(body))
        print(f"   Response: {resp}")
        
        if 'data' in resp and 'task_id' in resp['data']:
            print(f"✅ Task submitted successfully. Task ID: {resp['data']['task_id']}")
            return resp['data']['task_id']
        else:
            print("❌ Task submission failed (No task_id in response).")
            return None
    except Exception as e:
        print(f"❌ API Call Exception: {e}")
        return None

if __name__ == "__main__":
    link = test_file_upload()
    if link:
        test_volc_api(link)

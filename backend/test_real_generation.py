import os
import sys
import time
import requests
from app.config import VOLC_ACCESS_KEY, VOLC_SECRET_KEY, RESOURCE_ID
from app.service.volc_service import submit_task, get_result, upload_audio_to_public
from app.service.tts_service import text_to_speech

# Add current directory to path
sys.path.append(os.getcwd())
# Ensure temp dir exists
TEMP_DIR = os.path.join(os.getcwd(), 'temp')
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

def test_full_generation():
    print("🚀 Starting Real Video Generation Test...")
    
    # 1. Generate TTS
    text = "大家好，我是林云志。这是一个数字人生成测试。"
    print(f"1. Generating TTS for text: '{text}'...")
    try:
        audio_path = text_to_speech(text, TEMP_DIR)
        print(f"✅ TTS Success: {audio_path}")
    except Exception as e:
        print(f"❌ TTS Failed: {e}")
        return

    # 2. Upload Audio
    print("2. Uploading Audio to Public URL...")
    try:
        audio_url = upload_audio_to_public(audio_path)
        print(f"✅ Upload Success: {audio_url}")
    except Exception as e:
        print(f"❌ Upload Failed: {e}")
        return

    # 3. Submit Task
    print("3. Submitting Task to Volcengine...")
    try:
        task_id = submit_task(audio_url)
        print(f"✅ Task Submitted. Task ID: {task_id}")
    except Exception as e:
        print(f"❌ Submission Failed: {e}")
        return

    # 4. Poll Result
    print("4. Polling for result (timeout 120s)...")
    start_time = time.time()
    while time.time() - start_time < 120:
        try:
            video_url = get_result(task_id)
            if video_url:
                print(f"\n🎉 SUCCESS! Video Generated!")
                print(f"📺 Video URL: {video_url}")
                return
            else:
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(2)
        except Exception as e:
            print(f"\n❌ Polling Error: {e}")
            break
            
    print("\n❌ Timeout waiting for video generation.")

if __name__ == "__main__":
    test_full_generation()

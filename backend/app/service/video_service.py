import os
import time
import threading
import uuid
import requests
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import shutil
from ..config import VOLC_ACCESS_KEY, LLM_MAX_RESPONSE_LENGTH, DEMO_MODE, DEMO_VIDEO_PATH, DEMO_AUDIO_PATH, DEMO_DELAY_SECONDS, DEMO_TEXT
from .tts_service import text_to_speech
from .volc_service import submit_task, get_result, upload_audio_to_public
from .llm_service import optimize_script
from moviepy.editor import ImageClip, CompositeVideoClip, VideoFileClip, AudioFileClip

tasks = {}

# Get absolute path to temp directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMP_DIR = os.path.join(BASE_DIR, 'temp')
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

def generate_video(text, voice="zh-CN-XiaoxiaoNeural", layout="raw", max_length=LLM_MAX_RESPONSE_LENGTH):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "taskId": task_id,
        "progress": 0,
        "videoUrl": "",
        "status": "pending",
        "text": text,
        "voice": voice,
        "layout": layout
    }
    
    thread = threading.Thread(target=process_video_task, args=(task_id, text, voice, layout, max_length))
    thread.start()
    
    return task_id

def get_task_status(task_id):
    task = tasks.get(task_id)
    if not task:
        raise Exception("Task not found")
    return task

def update_progress(task_id, progress):
    if task_id in tasks:
        tasks[task_id]["progress"] = progress

def process_video_task(task_id, text, voice="zh-CN-XiaoxiaoNeural", layout="raw", max_length=LLM_MAX_RESPONSE_LENGTH):
    try:
        if DEMO_MODE:
            print(f"Running in DEMO MODE for task {task_id}")
            update_progress(task_id, 10)
            
            # Use fixed demo text for demo
            tasks[task_id]["optimized_text"] = DEMO_TEXT
            update_progress(task_id, 30)
            
            time.sleep(DEMO_DELAY_SECONDS / 2) # Simulate processing
            update_progress(task_id, 60)
            
            # Copy demo video to temp dir with new task id
            filename = f"{task_id}_demo.mp4"
            dest_path = os.path.join(TEMP_DIR, filename)
            
            if os.path.exists(DEMO_VIDEO_PATH):
                 shutil.copy(DEMO_VIDEO_PATH, dest_path)
            else:
                 raise Exception(f"Demo video not found at {DEMO_VIDEO_PATH}")
                 
            time.sleep(DEMO_DELAY_SECONDS / 2) # Simulate processing
            update_progress(task_id, 90)
            
            final_video_path = dest_path
        else:
            # 0. LLM Optimization
            update_progress(task_id, 5)
            # Call LLM to optimize text
            optimized_text = optimize_script(text, max_length=max_length)
            # Update task info with optimized text
            tasks[task_id]["optimized_text"] = optimized_text
            # Use optimized text for TTS
            text_for_tts = optimized_text
            
            # 1. Text Processing
            update_progress(task_id, 10)
            
            # 2. TTS
            update_progress(task_id, 20)
            audio_path = text_to_speech(text_for_tts, TEMP_DIR, voice)
            update_progress(task_id, 40)
            
            # 3. Upload Audio & Call Volcengine
            # Check if keys are placeholders
            if "YOUR_ACCESS_KEY" in VOLC_ACCESS_KEY:
                # Mock mode
                print("Using Mock Mode (Keys not set)")
                time.sleep(2)
                # Create a dummy video (no avatar)
                final_video_path = create_mock_video(text, audio_path, task_id)
            else:
                try:
                    audio_url = upload_audio_to_public(audio_path)
                    volc_task_id = submit_task(audio_url)
                    update_progress(task_id, 50)
                    
                    # Poll for result
                    avatar_video_url = None
                    for _ in range(60): # Timeout 2 mins (2s * 60)
                        try:
                            avatar_video_url = get_result(volc_task_id)
                            if avatar_video_url:
                                break
                        except Exception as poll_e:
                            print(f"Polling warning: {poll_e}. Retrying...")
                        time.sleep(2)
                    
                    if not avatar_video_url:
                        raise Exception("Volcengine timeout")
                    
                    update_progress(task_id, 70)
                    
                    # Download avatar video
                    avatar_video_path = os.path.join(TEMP_DIR, f"{task_id}_avatar.mp4")
                    download_file(avatar_video_url, avatar_video_path)
                    
                    update_progress(task_id, 90)
                    
                    if layout == "merge":
                        final_video_path = compose_video(text_for_tts, audio_path, avatar_video_path, task_id)
                    else:
                        final_video_path = avatar_video_path
                    
                except Exception as e:
                    # Do NOT fallback to mock, let it fail so we can see the error
                    print(f"API failed. Error details: {e}")
                    import traceback
                    traceback.print_exc()
                    raise e
                    # final_video_path = create_mock_video(text, audio_path, task_id)

        # Finish
        filename = os.path.basename(final_video_path)
        # Assuming app serves static/temp
        video_url = f"http://localhost:5000/static/temp/{filename}"
        
        # Log the final video URL for debugging
        print(f"Task {task_id} completed. Final video URL: {video_url}")
        
        tasks[task_id]["videoUrl"] = video_url
        update_progress(task_id, 100)
        
    except Exception as e:
        print(f"Error: {e}")
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["msg"] = str(e)

def download_file(url, path):
    r = requests.get(url)
    with open(path, 'wb') as f:
        f.write(r.content)

def create_text_image(text, width=1280, height=720):
    img = Image.new('RGB', (width, height), color=(50, 50, 50))
    d = ImageDraw.Draw(img)
    
    # Try to find a font that supports Chinese
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc", # macOS
        "/System/Library/Fonts/STHeiti Light.ttc", # macOS
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf", # Linux
        "C:\\Windows\\Fonts\\msyh.ttc", # Windows (Microsoft YaHei)
        "C:\\Windows\\Fonts\\simhei.ttf", # Windows (SimHei)
        "Arial.ttf" # Fallback
    ]
    
    font = None
    for path in font_paths:
        try:
            if os.path.exists(path) or (os.name == 'nt' and not path.startswith("/")):
                 # On windows checking existence might differ or just try loading
                 font = ImageFont.truetype(path, 40)
                 break
        except:
            continue
            
    if not font:
        try:
            font = ImageFont.load_default()
            print("Warning: No suitable font found, using default (Chinese may not render)")
        except:
            pass

    # Better text wrapping for Chinese
    margin = 50
    offset = 100
    line_height = 60
    max_width = width - 2 * margin
    
    lines = []
    current_line = ""
    
    for char in text:
        # Check width of current line + char
        test_line = current_line + char
        # getSize is deprecated in newer Pillow, using getbbox or getlength
        try:
            # Pillow >= 9.2.0
            line_width = font.getlength(test_line)
        except:
            try:
                # Older Pillow
                line_width = font.getsize(test_line)[0]
            except:
                # Very old or default font
                line_width = len(test_line) * 20 # Approximation
        
        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = char
            
    if current_line:
        lines.append(current_line)
    
    for line in lines:
        if offset > height - 50: break
        d.text((margin, offset), line, font=font, fill=(255, 255, 255))
        offset += line_height
        
    return np.array(img)

def compose_video(text, audio_path, avatar_video_path, task_id):
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    
    # Create Blackboard with text using Pillow
    img_array = create_text_image(text)
    bg = ImageClip(img_array).set_duration(duration)
    
    # Avatar
    # Resize to be smaller and in corner
    avatar = VideoFileClip(avatar_video_path).resize(height=360).set_position(("right", "bottom"))
    
    # Loop avatar if shorter than audio, or cut if longer
    if avatar.duration < duration:
        avatar = avatar.loop(duration=duration)
    else:
        avatar = avatar.subclip(0, duration)
        
    final = CompositeVideoClip([bg, avatar])
    final = final.set_audio(audio)
    
    output_path = os.path.join(TEMP_DIR, f"{task_id}_final.mp4")
    final.write_videofile(output_path, fps=24)
    
    return output_path

def create_mock_video(text, audio_path, task_id):
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    
    img_array = create_text_image(text)
    bg = ImageClip(img_array).set_duration(duration)
    
    final = bg.set_audio(audio)
    output_path = os.path.join(TEMP_DIR, f"{task_id}_final.mp4")
    final.write_videofile(output_path, fps=24)
    return output_path

import uuid
import os
import asyncio
import edge_tts

def text_to_speech(text, output_dir, voice="zh-CN-XiaoxiaoNeural"):
    try:
        filename = f"{uuid.uuid4()}.mp3" # edge-tts outputs mp3 by default
        filepath = os.path.join(output_dir, filename)
        
        # Use provided voice or default to XiaoxiaoNeural
        VOICE = voice
        
        async def _generate():
            communicate = edge_tts.Communicate(text, VOICE)
            await communicate.save(filepath)

        # Run async function in synchronous context
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        loop.run_until_complete(_generate())
        
        if os.path.exists(filepath):
            return filepath
        else:
            raise Exception("TTS file not created")
            
    except Exception as e:
        print(f"Edge-TTS Error: {e}")
        # Fallback to pyttsx3 if Edge-TTS fails (e.g. no internet)
        print("Falling back to pyttsx3...")
        try:
            import pyttsx3
            engine = pyttsx3.init()
            # Try to set a Chinese voice if available, otherwise default
            engine.setProperty('rate', 150)
            
            fallback_filename = f"{uuid.uuid4()}_fallback.wav"
            fallback_filepath = os.path.join(output_dir, fallback_filename)
            
            engine.save_to_file(text, fallback_filepath)
            engine.runAndWait()
            return fallback_filepath
        except Exception as fallback_e:
            raise Exception(f"TTS Failed (Edge-TTS: {e}, Fallback: {fallback_e})")

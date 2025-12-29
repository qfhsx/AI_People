import requests
import json
import os
from ..config import VOLC_ACCESS_KEY, VOLC_SECRET_KEY, RESOURCE_ID
# Attempt to import Volcengine SDK, if fails we will handle it in logic
try:
    from volcengine.visual.VisualService import VisualService
except ImportError:
    VisualService = None

def submit_task(audio_url):
    if not VisualService:
        raise Exception("Volcengine SDK not installed")

    # Temporarily unset proxy for Volcengine (Domestic Service)
    # to avoid timeout caused by local proxies (e.g. 127.0.0.1:7890)
    original_http = os.environ.get('http_proxy')
    original_https = os.environ.get('https_proxy')
    
    try:
        if 'http_proxy' in os.environ: del os.environ['http_proxy']
        if 'https_proxy' in os.environ: del os.environ['https_proxy']
        
        visual_service = VisualService()
        visual_service.set_ak(VOLC_ACCESS_KEY)
        visual_service.set_sk(VOLC_SECRET_KEY)
        
        body = {
            "req_key": "realman_avatar_creation_task",
            "resource_id": RESOURCE_ID,
            "audio_url": audio_url
        }
        
        # Using generic json method if available
        # SDK might return string or dict depending on version
        resp = visual_service.json("CVSubmitTask", {}, json.dumps(body))
        
        if isinstance(resp, str):
            resp = json.loads(resp)
            
        if 'data' in resp and 'task_id' in resp['data']:
            return resp['data']['task_id']
        else:
            raise Exception(f"Volcengine Error: {resp}")

    except Exception as e:
        raise Exception(f"Volcengine Call Failed: {e}")
    finally:
        # Restore proxy settings (in case other services need it)
        if original_http: os.environ['http_proxy'] = original_http
        if original_https: os.environ['https_proxy'] = original_https


def get_result(task_id):
    if not VisualService:
        raise Exception("Volcengine SDK not installed")

    visual_service = VisualService()
    visual_service.set_ak(VOLC_ACCESS_KEY)
    visual_service.set_sk(VOLC_SECRET_KEY)
    
    body = {
        "req_key": "realman_avatar_creation_task",
        "task_id": task_id
    }
    
    try:
        resp = visual_service.json("CVGetResult", {}, json.dumps(body))
        
        if isinstance(resp, str):
            resp = json.loads(resp)
        
        if 'data' in resp:
            data = resp['data']
            if data.get('status') == 'done':
                 if 'resp_data' in data:
                     # resp_data is a JSON string
                     resp_data = json.loads(data['resp_data'])
                     if 'vid' in resp_data and 'url' in resp_data['vid']:
                         return resp_data['vid']['url']
            elif data.get('status') == 'fail':
                 raise Exception("Task failed at Volcengine side")
            return None # Still processing
        else:
             raise Exception(f"Volcengine Error: {resp}")
             
    except Exception as e:
        raise Exception(f"Volcengine Check Failed: {e}")

def upload_audio_to_public(filepath):
    # 1. Try Catbox.moe (Generally most reliable for temporary hosting)
    try:
        with open(filepath, 'rb') as f:
            resp = requests.post('https://catbox.moe/user/api.php', 
                               data={'reqtype': 'fileupload', 'userhash': ''},
                               files={'fileToUpload': f})
        
        if resp.status_code == 200:
            return resp.text.strip()
        else:
            print(f"catbox.moe upload failed: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"catbox.moe upload error: {e}")

    # 2. Try tmpfiles.org
    try:
        with open(filepath, 'rb') as f:
            resp = requests.post('https://tmpfiles.org/api/v1/upload', files={'file': f})
            
        if resp.status_code == 200:
            data = resp.json()
            if data['status'] == 'success':
                url = data['data']['url']
                # Convert to direct download link
                direct_url = url.replace('tmpfiles.org/', 'tmpfiles.org/dl/')
                return direct_url
        print(f"tmpfiles.org upload failed: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"tmpfiles.org upload error: {e}")

    # 3. Try file.io (One-time download often causes issues if API checks head)
    try:
        with open(filepath, 'rb') as f:
            resp = requests.post('https://file.io', files={'file': f}, data={'expires': '1d'})
        
        if resp.status_code == 200:
            return resp.json()['link']
        else:
            print(f"file.io upload failed: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"file.io upload error: {e}")

    # 4. Fallback to transfer.sh
    try:
        filename = os.path.basename(filepath)
        with open(filepath, 'rb') as f:
            # transfer.sh uses PUT
            resp = requests.put(f'https://transfer.sh/{filename}', data=f)
            
        if resp.status_code == 200:
            return resp.text.strip()
        else:
            print(f"transfer.sh upload failed: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"transfer.sh upload error: {e}")

    raise Exception("Failed to upload audio to public storage (all providers failed)")

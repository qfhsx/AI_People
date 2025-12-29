from flask import Blueprint, request, jsonify
from ..service.video_service import generate_video, get_task_status
from ..config import LLM_MAX_RESPONSE_LENGTH

api_bp = Blueprint('api', __name__)

@api_bp.route('/generate', methods=['POST'])
def generate():
    data = request.json
    text = data.get('text')
    voice = data.get('voice', 'zh-CN-XiaoxiaoNeural') # Default to female teacher
    layout = data.get('layout', 'raw') # Default to raw avatar
    max_length = data.get('max_length', LLM_MAX_RESPONSE_LENGTH)
    
    if not text:
        return jsonify({"code": 400, "msg": "Text is required", "data": None}), 400
    
    try:
        task_id = generate_video(text, voice, layout, max_length)
        return jsonify({"code": 200, "msg": "Success", "data": {"taskId": task_id, "progress": 0, "videoUrl": ""}})
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e), "data": None}), 500

@api_bp.route('/status', methods=['GET'])
def status():
    task_id = request.args.get('taskId')
    if not task_id:
        return jsonify({"code": 400, "msg": "Task ID is required", "data": None}), 400
    
    try:
        data = get_task_status(task_id)
        return jsonify({"code": 200, "msg": "Success", "data": data})
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e), "data": None}), 500

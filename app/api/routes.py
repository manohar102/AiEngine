from flask import Blueprint, request, jsonify
from app.services.log_service import LogService
api_bp = Blueprint('api', __name__)
@api_bp.route('/generate-log', methods=['POST'])
def generate_log():
    data = request.json
    code = data.get('code')
    language = data.get('language')
    prefix = data.get('prefix', '')
    suffix = data.get('suffix', '')
    api_provider = data.get('apiProvider', 'gemini')
    log_service = LogService()
    log_message = log_service.generate_log(code, language, prefix, suffix, api_provider)
    if log_message is None:
        return jsonify({'error': 'Failed to generate log'}), 500
    return jsonify({'logMessage': log_message})
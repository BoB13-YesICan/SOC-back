from flask import Blueprint, Response, jsonify, request
from app.services.logging import fetch_logs, get_filter_logs


logs_bp = Blueprint('logs', __name__)

@logs_bp.route('/all_logs')
def stream_logs():
    return Response(fetch_logs(), content_type='text/event-stream')

@logs_bp.route('/filter_logs', methods=['GET'])
def filter_logs():
    attack_type = request.args.get('attack')
    can_id = request.args.get('can_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    return jsonify(get_filter_logs(attack_type, can_id, start_date, end_date))

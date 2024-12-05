from flask import Blueprint, jsonify, Response
from app.services.bigquery import get_daily_attack_count, update_attack_count
import json
import time

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/daily_count', methods=['GET'])
def daily_attack_count():
    return jsonify(get_daily_attack_count())

@stats_bp.route('/hours_count', methods=['GET'])
def attack_count():
    def generate():
        while True:
            yield f"data: {json.dumps(update_attack_count())}\n\n"
            time.sleep(1)

    return Response(generate(), content_type='text/event-stream')

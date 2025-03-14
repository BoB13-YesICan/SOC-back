from flask import Blueprint, jsonify, Response
from app.services.bigquery import get_daily_attack_count, update_attack_count, get_overall_risk
import json
import time

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/daily_count', methods=['GET'])
def daily_count():
    def generate():
        while True:
            yield f"data: {json.dumps(get_daily_attack_count())}\n\n"
            time.sleep(60)  # 60초 간격으로 데이터 전송

    return Response(generate(), content_type='text/event-stream')

@stats_bp.route('/hours_count', methods=['GET'])
def hours_attack_count():
    def generate():
        while True:
            yield f"data: {json.dumps(update_attack_count())}\n\n"
            time.sleep(60)  # 60초 간격으로 데이터 전송

    return Response(generate(), content_type='text/event-stream')

@stats_bp.route('/overall_risk', methods=['GET'])
def overall_risk():
    def generate():
        while True:
            yield f"data: {json.dumps(get_overall_risk())}\n\n"
            time.sleep(60)  # 60초 간격으로 데이터 전송

    return Response(generate(), content_type='text/event-stream')

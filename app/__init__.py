from flask import Flask, jsonify, Response, request
from flask_cors import CORS
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Config 클래스에서 설정 로드
    CORS(app)

    # 블루프린트 등록
    from app.routes.logs import logs_bp
    from app.routes.stats import stats_bp
    
    app.register_blueprint(logs_bp, url_prefix='/api/logs')
    app.register_blueprint(stats_bp, url_prefix='/api/stats')

    return app

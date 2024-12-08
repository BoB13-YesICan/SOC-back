from flask import Blueprint, jsonify, request, send_file
from app.services.reporting import get_report_logs, process_can_info, summarize_logs, attack_detection_status, generate_detailed_report
from ..report.report_generator import generate_report, html2pdf
from config import Config


report_bp = Blueprint('report', __name__)

@report_bp.route('/generate_report', methods=['GET'])
def generate_report_endpoint():
    try:
        # 요청에서 시간 범위 가져오기
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        # 로그 필터링 및 데이터 처리
        df = get_report_logs(start_date, end_date)
        df["periodic"] = df["periodic"].astype(str).str.strip()
        df["periodic"] = df["periodic"].replace(["0.0", 0.0], "미측정").replace(["-1.0", -1], "비주기")

        # 데이터 처리
        static_df = process_can_info(df)
        summary_df = summarize_logs(df)
        attack_status_df = attack_detection_status(df)

        detailed_report = generate_detailed_report(df)

        # 리포트 생성
        html_file_path = Config.REPORT_HTML_FILTEPATH
        pdf_file_path = Config.REPORT_PDF_FILEPATH
        sections = ["2. CAN 기본 정보", "3. SUMMARY", "4. 공격 감지 상태"]
        generate_report(html_file_path, [static_df, summary_df, attack_status_df], sections, detailed_report)
        html2pdf(html_file_path, pdf_file_path)
        
        return send_file(pdf_file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

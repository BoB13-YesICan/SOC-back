import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    # Google Cloud Credentials
    GOOGLE_APPLICATION_CREDENTIALS_LOG = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_LOG")
    GOOGLE_APPLICATION_CREDENTIALS_BQ = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_BQ")
    GOOGLE_PROJECT = os.getenv("GOOGLE_PROJECT")
    ATTACK_BIGQUERY = os.getenv("ATTACK_BIGQUERY")
    NOMRAL_BIGQUERY = os.getenv("NORMAL_BIGQUERY")

    REPORT_HTML_FILTEPATH = os.getenv("REPORT_HTML_FILTEPATH")
    REPORT_PDF_FILEPATH = os.getenv("REPORT_PDF_FILEPATH")

    # Flask 환경 설정
    FLASK_ENV = os.getenv("FLASK_ENV", "production")



from google.cloud import logging_v2
from google.oauth2 import service_account
from config import Config
from datetime import datetime
import time
import json

log_credentials = service_account.Credentials.from_service_account_file(Config.GOOGLE_APPLICATION_CREDENTIALS_LOG)
log_client = logging_v2.Client(credentials=log_credentials, project=Config.GOOGLE_PROJECT)

last_timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

# Your existing fetch_logs function here
def fetch_logs():
    global last_timestamp
    last_sent_log = None  # 마지막으로 보낸 로그 저장 변수

    while True:
        filter_str = 'resource.type="global" AND timestamp > "{}"'.format(last_timestamp)
        try:
            entries = list(log_client.list_entries(filter_=filter_str))  # Fetch logs based on filter
            for entry in entries:
                try:
                    payload = entry.payload
                    log_entry = {
                        'timestamp': payload['timestamp'],
                        'can_id': payload['can_id'],
                        'payload': payload['payload'],
                        'label': payload['label']
                    }

                    # 중복된 로그인지 확인
                    if log_entry == last_sent_log:
                        continue

                    # 중복이 아니면 로그 스트리밍
                    log_entry_json = json.dumps(log_entry)
                    yield f"data: {log_entry_json}\n\n"

                    # 마지막으로 보낸 로그 업데이트
                    last_sent_log = log_entry

                except Exception as e:
                    print(f"Error processing entry: {e}")

            if entries:
                last_timestamp = entries[-1].timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")

        except Exception as e:
            print(f"Error fetching logs: {e}")

        # Increase the sleep time to avoid quota limit errors
        time.sleep(10)

def get_filter_logs(attack_type, can_id, start_date, end_date):
    
    # print(start_date, end_date)

    start_date = datetime.strptime(start_date.split('.')[0], "%Y-%m-%dT%H:%M:%S")
    end_date = datetime.strptime(end_date.split('.')[0], "%Y-%m-%dT%H:%M:%S")

    start_date = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")


    # print(attack_type, can_id, start_date, end_date)

    filter_str = 'resource.type="global"'
    if attack_type:
        filter_str += f' AND jsonPayload.label="{attack_type}"'
    if can_id:
        filter_str += f' AND jsonPayload.can_id="{can_id}"'
    if start_date and end_date:
        filter_str += f' AND timestamp>="{start_date}" AND timestamp<="{end_date}"'

    entries = list(log_client.list_entries(filter_=filter_str))  # list()로 모든 로그를 가져와야 함
    filtered_logs = {
        'can_id': 'N/A',
        'periodic': 'N/A',
        'clock_skew_min': 'N/A',
        'clock_skew_max': 'N/A',
        'logs': []
    }

    if entries:
        try:
            payload = entries[0].payload
            filtered_logs = {
                'can_id': payload.get('can_id', 'N/A'),
                'periodic': payload.get('periodic', 'N/A'),
                'clock_skew_min': payload.get('clock_skew_min', 'N/A'),
                'clock_skew_max': payload.get('clock_skew_max', 'N/A'),
                'logs': []
            }
            for entry in entries:
                try:
                    payload = entry.payload
                    log_entry = {
                        'timestamp': payload.get('timestamp', 'N/A'),
                        'payload': payload.get('payload', 'N/A'),
                        'timediff': payload.get('time_diff', 'N/A'),
                        'similarity': payload.get('similarity', 'N/A'),
                        'clock_skew': payload.get('clock_skew', 'N/A'),
                    }
                    filtered_logs['logs'].append(log_entry)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
        
        # Increase the sleep time to avoid quota limit errors
        time.sleep(10)

    return filtered_logs
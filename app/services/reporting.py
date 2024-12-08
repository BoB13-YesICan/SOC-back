from google.cloud import logging_v2
from google.oauth2 import service_account
from config import Config
import pandas as pd
from ..report.log_parse_info import ids  # 공격 유형 정보 가져오기

log_credentials = service_account.Credentials.from_service_account_file(Config.GOOGLE_APPLICATION_CREDENTIALS_LOG)
log_client = logging_v2.Client(credentials=log_credentials, project=Config.GOOGLE_PROJECT)

# 로그 필터링 함수
def get_report_logs(start_time, end_time):
    filter_str = f'resource.type="global" AND timestamp>="{start_time}" AND timestamp<="{end_time}"'
    entries = list(log_client.list_entries(filter_=filter_str))
    filtered_logs = []

    if entries:
        for entry in entries:
            try:
                payload = entry.payload
                if payload.get('timestamp', 'N/A') == "N/A":
                    continue

                log_entry = {
                    'timestamp': payload.get('timestamp', 'N/A'),
                    'can_id': payload.get('can_id', 'N/A'),
                    'label': payload.get('label', 'N/A'),
                    'payload': payload.get('payload', 'N/A'),
                    'actual_DLC': int(len(payload.get('payload', 'N/A')) / 2),
                    'time_diff': payload.get('time_diff', 'N/A'),
                    'similarity': payload.get('similarity', 'N/A'),
                    'clock_skew': payload.get('clock_skew', 'N/A'),
                    'periodic': payload.get('periodic', 'N/A'),
                    'clock_skew_min': payload.get('clock_skew_min', 'N/A'),
                    'clock_skew_max': payload.get('clock_skew_max', 'N/A'),
                }
                filtered_logs.append(log_entry)
            except Exception as e:
                print(f"Error processing entry: {e}")

    return pd.DataFrame(filtered_logs)

# CAN 기본 정보 처리
def process_can_info(df):
    static_data = []
    filtered = df[~df['periodic'].isin(['미측정', 'N/A', '비주기'])]

    for _, row in filtered.iterrows():
        static_data.append({
            'ID': row['can_id'],
            'type': '주기',
            'period': row['periodic']
        })
    if (df['periodic'] == '미측정').any():
        static_data.append({
            'ID': ', '.join(df[df['periodic'] == '미측정']['can_id']),
            'type': '미측정',
            'period': 'X'
        })
    if (df['periodic'] == '비주기').any():
        static_data.append({
            'ID': ', '.join(df[df['periodic'] == '비주기']['can_id']),
            'type': '비주기',
            'period': 'X'
        })
    if (df['periodic'] == 'N/A').any():
        static_data.append({
            'ID': ', '.join(df[df['periodic'] == 'N/A']['can_id']),
            'type': '오류',
            'period': 'X'
        })

    return pd.DataFrame(static_data)

# 로그 요약
def summarize_logs(df):
    label_counts = df['label'].value_counts()
    summary = {
        "DoS": sum(label_counts.get(label, 0) for label in [1, 2, 3]),
        "Fuzzing": sum(label_counts.get(label, 0) for label in [4, 5]),
        "Replay": label_counts.get(6, 0),
        "Suspension": sum(label_counts.get(label, 0) for label in [7, 8]),
        "Masquerade": label_counts.get(9, 0),
    }
    total_count = sum(summary.values())

    criteria_mapping = {
        "Fuzzing": "DBC, Payload",
        "Masquerade": "clock skew",
        "DoS": "Timediff",
        "Suspension": "Timediff",
        "Replay": "Timediff, Payload",
    }

    percentage_data = {
        "TYPE": [],
        "탐지 비율": [],
        "탐지 갯수": [],
        "기준": [],
    }

    for attack_type, count in summary.items():
        percentage_data["TYPE"].append(attack_type)
        percentage_data["탐지 갯수"].append(str(count))

        percentage = (count / total_count * 100) if total_count > 0 else 0
        percentage_data["탐지 비율"].append(f"{percentage:.1f}%")

        percentage_data["기준"].append(criteria_mapping.get(attack_type, "N/A"))

    return pd.DataFrame(percentage_data)

# 공격 감지 상태 처리
def attack_detection_status(df):
    grouped = df[df['label'] != 0.0].groupby(['label', 'periodic']).size().reset_index(name='count')
    status_data = []

    for _, row in grouped.iterrows():
        filtered = df[(df['label'] == row['label']) & (df['periodic'] == row['periodic'])]
        can_id_string = ', '.join(filtered['can_id'])
        status_data.append({
            'label': row['label'],
            'id': can_id_string,
            'periodic': row['periodic'],
            'count': row['count'],
            'time_diff_info': f"{filtered['time_diff'].min()}~{filtered['time_diff'].max()}-{filtered['time_diff'].mean()}",
        })

    return pd.DataFrame(status_data)


# 각 공격 유형별 데이터 처리
def generate_detailed_report(df):
    label_grouped = df.groupby(['label'])
    detailed_report = {
        "title": [],
        "subtitle": [],
        "describes": [],
        "img": [],
        "dataframe": []
    }

    for label in df['label'].unique():
        if label == 0:  # 정상 패킷은 건너뜀
            continue
        if label in ids:
            label_info = ids[label]
            detailed_report["title"].append(label_info["type"])
            detailed_report["subtitle"].append(label_info["desc"])
            detailed_report["describes"].append(label_info["detailed"])
            detailed_report["img"].append(label_info["img"])

            # 데이터프레임에서 해당 공격 유형 관련 데이터 추출
            selected_columns = label_info["c"]
            if label in label_grouped.groups:
                filtered_df = label_grouped.get_group((label,))[selected_columns]
                detailed_report["dataframe"].append(filtered_df)

    return detailed_report
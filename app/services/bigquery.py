from flask import jsonify
from google.oauth2 import service_account
from google.cloud import bigquery
from config import Config
from datetime import datetime, timedelta 
import time
from collections import defaultdict

bigquery_credentials = service_account.Credentials.from_service_account_file(Config.GOOGLE_APPLICATION_CREDENTIALS_BQ)
bigquery_client = bigquery.Client(credentials=bigquery_credentials, project=Config.GOOGLE_PROJECT)

attack_count_data = {
    "DoS": 0,
    "Fuzzing": 0,
    "Replay": 0,
    "Suspension": 0,
    "Masquerade": 0
}

# Background thread for periodically fetching the attack count from BigQuery
def update_attack_count():
    global attack_count_data
    while True:
        # 하나의 쿼리로 모든 label 값을 집계
        query = """
        SELECT jsonPayload.label, COUNT(*) AS log_count
        FROM `yesican-443010.attack_log.can_ids`
        WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
        GROUP BY jsonPayload.label
        """

        query_job = bigquery_client.query(query)

        # 쿼리 결과를 읽어와서 attack_count_data 업데이트
        for row in query_job.result():
            label = row.label
            log_count = row.log_count
            
            if label == 1:
                attack_count_data["DoS"] = log_count
            elif label == 2:
                attack_count_data["Fuzzing"] = log_count
            elif label == 3:
                attack_count_data["Replay"] = log_count
            elif label == 4:
                attack_count_data["Suspension"] = log_count
            elif label == 5:
                attack_count_data["Masquerade"] = log_count

        time.sleep(60)  # Update every 60 seconds



def get_daily_attack_count():

    current_time = datetime.today() - timedelta(days=1)
    current_time = current_time.strftime("%Y-%m-%dT15:00:00Z")

    print(current_time)

    # Define the BigQuery SQL query
    attack_query = f"""
    SELECT
        EXTRACT(HOUR FROM timestamp) AS hour,
        COUNT(*) AS attack_count
    FROM
        `yesican-443010.attack_log.can_ids`
    WHERE
        timestamp >= '{current_time}'
        AND timestamp <= TIMESTAMP_ADD('{current_time}', INTERVAL 24 HOUR)
    GROUP BY
        hour
    ORDER BY
        hour
    """

    normal_query = f"""
    SELECT
        EXTRACT(HOUR FROM timestamp) AS hour,
        COUNT(*) AS attack_count
    FROM
        `yesican-443010.normal_log.can_ids`
    WHERE
        timestamp >= '{current_time}'
        AND timestamp <= TIMESTAMP_ADD('{current_time}', INTERVAL 24 HOUR)
    GROUP BY
        hour
    ORDER BY
        hour
    """

    # Execute the BigQuery query
    attack_query_job = bigquery_client.query(attack_query)
    normal_query_job = bigquery_client.query(normal_query)

    # Prepare the result in a dictionary
    hourly_attack_counts = defaultdict(int)
    hourly_normal_counts = defaultdict(int)

    # Process the query results
    for row in attack_query_job.result():
        hour = (row['hour'] + 9) % 24
        attack_count = row['attack_count']
        hourly_attack_counts[hour] = attack_count

    for row in normal_query_job.result():
        hour = (row['hour'] + 9) % 24
        normal_count = row['attack_count']
        hourly_normal_counts[hour] = normal_count

    # Ensure all 24 hours are included in the result, even if no attacks occurred in some hours
    attack_counts_by_hour = {hour: hourly_attack_counts.get(hour, 0) for hour in range(24)}
    normal_counts_by_hour = {hour: hourly_normal_counts.get(hour, 0) for hour in range(24)}

    return {'daily_attack_count': attack_counts_by_hour, 'daily_normal_count': normal_counts_by_hour}

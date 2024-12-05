import json
import time

def stream_data(data):
    while True:
        yield f"data: {json.dumps(data)}\n\n"
        time.sleep(1)

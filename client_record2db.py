import json
import requests
def insert_into_db(channel: int, record_type: str, id_record: str, record_path: str, datetime_start: str, datetime_stop: str,
                record_length: float, record_extension: str, snapshot_path: str):
    api_url = 'http://192.168.35.57:1234/api_db_record'
    create_row_data = {
        "jsonrpc": "2.0",
        "method": "insert_record",
        "params": {
            "channel": channel,
            "record_type": f'{record_type}',
            "id_record": f'{id_record}',
            "record_path": f'{record_path}',
            "datetime_start": f'{datetime_start}',
            "datetime_stop": f'{datetime_stop}',
            "record_length": record_length,
            "record_extension": f'{record_extension}',
            "snapshot_path": f'{snapshot_path}'
        },
        "id": 1
    }
    print(create_row_data)
    r = requests.post(url=api_url, json=create_row_data)
    print(r.status_code, r.reason, r.text)
#insert_into_db(13,'sgd',12,'/sgaf','2022-07-06 14:07:14.300513','2022-07-06 14:07:14.300513',12,'avi','/ssfh')
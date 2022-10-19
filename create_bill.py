from notion_api_client import NotionApiClient
from datetime import datetime, timedelta, timezone
import parameter_store

KOKI_ID, SHUYA_ID =  parameter_store.get_params('KOKI_ID', 'SHUYA_ID')

def build_payload():
    JST = timezone(timedelta(hours=+9), 'JST')
    last_day_of_month = (datetime.now(JST) - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=999999)
    first_day_of_month = last_day_of_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    payload = {
        "filter": {
            "and": [
                {
                    "timestamp": "created_time",
                    "created_time": {
                        "on_or_after": datetime.strftime(first_day_of_month, '%Y-%m-%dT%H:%M:%S%z')
                    }
                }, 
                {
                    "timestamp": "created_time",
                    "created_time": {
                        "on_or_before": datetime.strftime(last_day_of_month, '%Y-%m-%dT%H:%M:%S%z')
                    }
                }
            ]
        }
    }
    return payload

def calculate_payments():
    data = NotionApiClient.post_database_query(build_payload())
    each_payment = {KOKI_ID: 0, SHUYA_ID: 0}
    for result in data['results']:
        each_payment[result['created_by']['id']] += result['properties']['金額']['number']
    return each_payment

def build_message():
    each_payment = calculate_payments()
    koki_payment = each_payment[KOKI_ID]
    shuya_payment = each_payment[SHUYA_ID]
    message = f"先月の支払いは\n- こーき: {koki_payment}円\n- しゅーや: {shuya_payment}円\nでした。\n\n"
    if koki_payment < shuya_payment:
        message += f"こーきがしゅーやに\n({shuya_payment} - {koki_payment}) / 2 = {(shuya_payment - koki_payment) / 2}円\n払ってください。"
    elif koki_payment > shuya_payment:
        message += f"しゅーやがこーきに\n({koki_payment} - {shuya_payment}) / 2 = {(koki_payment - shuya_payment) / 2}円\n払ってください。"
    else:
        message += '今回、支払いはありません。'
    return message

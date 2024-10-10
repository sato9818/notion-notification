import requests
import os
import parameter_store

class LineNotifier:
    LINE_NOTIFY_API_URL = os.getenv('LINE_NOTIFY_API_URL')
    LINE_SIMULATION_NOTIFIER_TOKEN = parameter_store.get_params('LINE_SIMULATION_NOTIFIER_TOKEN')
    
    def send(message):
        payload = {'message': f"\n{message}"}
        headers = {'Authorization': 'Bearer ' + LineNotifier.LINE_SIMULATION_NOTIFIER_TOKEN}

        print(f"Post Line Notify API : {LineNotifier.LINE_NOTIFY_API_URL}")
        print(f"payload: {payload}")
        res = requests.post(LineNotifier.LINE_NOTIFY_API_URL, data=payload, headers=headers)
        res.raise_for_status()

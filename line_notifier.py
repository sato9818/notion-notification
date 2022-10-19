import requests
import parameter_store

class LineNotifier:
    LINE_NOTIFY_API_URL, LINE_SIMULATION_NOTIFIER_TOKEN = parameter_store.get_params('LINE_NOTIFY_API_URL', 'LINE_SIMULATION_NOTIFIER_TOKEN')
    
    def send(message):
        payload = {'message': f"\n{message}"}
        headers = {'Authorization': 'Bearer ' + LineNotifier.LINE_SIMULATION_NOTIFIER_TOKEN} 
        requests.post(LineNotifier.LINE_NOTIFY_API_URL, data=payload, headers=headers)

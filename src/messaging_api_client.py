import requests
import parameter_store

class MessagingApiClient:
    GROUP_ID, MESSAGING_API_ACCESS_TOKEN = parameter_store.get_params('GROUP_ID', 'MESSAGING_API_ACCESS_TOKEN')
    LINE_PUSH_MESSAGE_URL = 'https://api.line.me/v2/bot/message/push'
    
    def send(message):
        payload = {'messages': [{'type': 'text', 'text': f"{message}"}], 'to': f"{MessagingApiClient.GROUP_ID}"}
        headers = {'Authorization': f"Bearer {MessagingApiClient.MESSAGING_API_ACCESS_TOKEN}", 'Content-Type': 'application/json'}
        print(f"payload: {payload}")
        res = requests.post(MessagingApiClient.LINE_PUSH_MESSAGE_URL, json=payload, headers=headers)
        res.raise_for_status()

import create_bill
from messaging_api_client import MessagingApiClient

def handler(event, context):
    message = create_bill.build_message()
    MessagingApiClient.send(message)

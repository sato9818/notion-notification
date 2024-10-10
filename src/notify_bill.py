import create_bill
from line_notifier import LineNotifier

def handler(event, context):
    message = create_bill.build_message()
    LineNotifier.send(message)

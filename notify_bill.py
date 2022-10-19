import create_bill
from line_notifier import LineNotifier

def notify_bill(event, context):
    message = create_bill.build_message()
    LineNotifier.send(message)

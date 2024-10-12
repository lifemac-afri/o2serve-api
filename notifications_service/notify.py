import pusher
# from orders.serializers import OrderSerializer

pusher_client = pusher.Pusher(
    app_id='1877114',
    key='54af578ab052ea82910e',
    secret='f538657c7c829c6773df',
    cluster='mt1',
    # ssl=True
)

def notify_event(event_type, message):
    
    if event_type not in ['new_order', 'order_assigned', 'order_updated', 'order_accepted']:
        raise ValueError("Invalid event type provided.")
    
    pusher_client.trigger('02-broker-development', event_type, {'message': message})


def notify_new_order(order_details):
    print(f"notify an order created: {order_details}")
    notify_event('new_order', order_details)

def notify_order_assigned(order_id, assignee):
    notify_event('order_assigned', {'order_id': order_id, 'assignee': assignee})

def notify_order_updated(order_id, updates):
    notify_event('order_updated', {'order_id': order_id, 'updates': updates})

def notify_order_accepted(order_id):
    notify_event('order_accepted', {'order_id': order_id})

import pusher
# from orders.serializers import OrderSerializer

pusher_client = pusher.Pusher(
  app_id='1877114',
  key='54af578ab052ea82910e',
  secret='f538657c7c829c6773df',
  cluster='mt1',
#   ssl=True
)

def notify_event(event_type, message):
    print(f"notify an event: {event_type} {message}")
    # pusher_client.trigger('02-broker-development', event_type, {'message': message})
    pusher_client.trigger('02-broker-development', event_type, {'message': message})
    print(f"pusher client triggered")

def notify_new_order(order_details):
    print(f"notify an order created: {order_details}")
    notify_event('new_order', order_details)

def notify_order_assigned(order_id, assignee):
    dynamic_event_type = f'order_assigned_{assignee}'
    notify_event(dynamic_event_type, {'order_number': order_id})

def notify_order_updated(order_id, updates):
    dynamic_event_type = f'order_updated_{order_id}'
    notify_event(dynamic_event_type, {'order_id': order_id, 'updates': updates})


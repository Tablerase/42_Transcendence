from channels.exceptions import DenyConnection

def authenticate_and_initialize(consumer):
    if not consumer.scope['user'].is_authenticated:
        raise DenyConnection("User is not authenticated")
    
    consumer.user = consumer.scope['user']
    consumer.tournament_id = consumer.scope['url_route']['kwargs']['tournament_id']
    consumer.group_name = f'tournament_{consumer.tournament_id}'


async def add_channel_to_group_and_accept(consumer):
  await consumer.channel_layer.group_add(
    consumer.group_name,
    consumer.channel_name
  )
  await consumer.accept()
  print("Conection established.")

async def send_message_to_group(consumer, message_type, **kwargs):
  message = {
      'type': message_type,
      'message': kwargs.get('message', '')
  }
  message.update(kwargs)
  await consumer.channel_layer.group_send(
      consumer.group_name,
      message
  )

async def discard_channel_from_group(consumer):
  await consumer.channel_layer.group_discard(
    consumer.group_name,
    consumer.channel_name
  )

async def send_message_to_group(consumer, message_type, **kwargs):
  message = {
      'type': message_type,
      'message': kwargs.get('message', '')
  }
  message.update(kwargs)
  await consumer.channel_layer.group_send(
      consumer.group_name,
      message
  )



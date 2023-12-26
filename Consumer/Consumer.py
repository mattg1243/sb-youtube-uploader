import pika
import json

class Consumer():
  
  queue_name = 'to_upload'

  def __init__(self, conn: pika.BlockingConnection):
    self.conn = conn
    self.channel = conn.channel()
    self.channel.queue_declare(queue=self.queue_name)


  # def __del__(self):
  #   self.conn.close()
  #   print('q connection close, Consumer destroyed')


  def get_msg_from_queue(self):
    """Attemps to retreive a msg from the queue if one exists. Returns the msg
    as json."""
    print('waiting for messages...')
    (method, properties, msg) = self.channel.basic_get(self.queue_name, auto_ack=False )
    # msg = {
    #     "title": 'datboi',
    #     "artist": 'bontanamrown',
    #     "img_link": 'https://d3fulr0i8qqtgb.cloudfront.net/images/2944ab59-60ad-4eb0-86a9-04abc938a394',
    #     'audio_link': 'https://d3fulr0i8qqtgb.cloudfront.net/beats/8ab8a5ac-2fa0-4199-ae34-ed3c6c529127'
    #   }
    print(method)
    print(properties)
    print(msg)
    if msg == None:
      print('no videos are queued for upload, Ill try again tmr')
      return None
    else:
      return (json.loads(msg.decode('utf-8')), method.delivery_tag)
    

  def send_ack(self, delivery_tag: str):
    try:
      self.channel.basic_ack(delivery_tag=delivery_tag)
    except Exception as e:
      print(e)
import pika

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
    print('waiting for messages...')
    # msg = self.channel.basic_get(self.queue_name, auto_ack=True )
    msg = {
        "title": 'datboi',
        "artist": 'bontanamrown',
        "img_link": 'https://d3fulr0i8qqtgb.cloudfront.net/images/2944ab59-60ad-4eb0-86a9-04abc938a394',
        'audio_link': 'https://d3fulr0i8qqtgb.cloudfront.net/beats/8ab8a5ac-2fa0-4199-ae34-ed3c6c529127'
      }
    if msg == (None, None, None):
      print('no videos are queued for upload, Ill try again tmr')
    else:
      # return fake msg for testing
      
      print(f"msg received\nf{msg}")
      return msg
import os
import sys
import urllib.request
from dotenv import load_dotenv
import pika

from Consumer.Consumer import Consumer
from Generator.Generator import Generator

load_dotenv()
MQ_URL = os.getenv('MQ_URL')
MQ_PW = os.getenv('MQ_PW')

def main():

  # connect to queue
  conn = pika.BlockingConnection(pika.URLParameters(MQ_URL))

  c = Consumer(conn)
  g = Generator()

  # check queue for beats to upload
  beat = c.get_msg_from_queue()
  if beat == None:
    print('no beats in the queue for today, Ill check again tomorrow')
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)

  # if theres a beat in the queue, fetch the audio and artwork 
  try:
    urllib.request.urlretrieve(beat['img_link'], os.path.abspath('artwork.png'))
    urllib.request.urlretrieve(beat['audio_link'], os.path.abspath('audio.mp3'))
  except Exception as e:
    print(e)
  # generate the html and save a screenshot
  g.write_html(beat['title'], beat['artist'])
  g.get_screenshot()

  # clean up files
  g.clean_up()


if __name__ == '__main__':
  try :
    main()
  except KeyboardInterrupt:
    print('closing')
  except Exception as e:
    print(e)
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)
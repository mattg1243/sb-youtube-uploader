import os
import subprocess
from playwright.sync_api import sync_playwright

class Generator():

  template_path = os.path.abspath("page.html")
  screenshot_path = os.path.abspath("screenshot.png")
  audio_path = os.path.abspath("audio.mp3")

  def __init__(self):
    print('   ✅   generator created')


  def write_html(self, title, artist):
    html = f"""
      <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <link rel="stylesheet" href="./template.css">
          <title>YouTube Template</title>
        </head>
        <body>
          <h1 class="title">{title} - {artist}</h1>
          <img src="artwork.png" class="artwork">
          <h1 class="site-url">sweatshopbeats.com</h1>
        </body>
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Kalam:wght@300;400&family=Pacifico&display=swap');

        body {{
          height: 100vh;
          width: 100vw;
          background-color: #ffbd59;
          position: relative;
        }}

        .title {{
          position: absolute;
          top: 5%;
          left: 10%;
          font-family: 'Kalam', cursive;
        }}

        .artwork {{
          width: 400px;
          height: 400px;
          box-shadow: 12px 12px black;
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
        }}

        .site-url {{
          position: absolute;
          top: 84%;
          right: 12%;
          font-family: 'Kalam', cursive;
        }}
        </style>
        </html>
      """

    with open('page.html', 'w') as file:
      file.write(html)


  def get_screenshot(self):
    with sync_playwright() as p:
      try:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1600, "height": 900})
        
        page.goto('file://' + self.template_path)
        page.screenshot(path=self.screenshot_path, full_page=True)
        print('   ✅   screenshot saved')
      except Exception as e:
        print(e)


  def make_video(self):
    try:
      os.system(f"ffmpeg -loop 1 -i {self.screenshot_path} -i {self.audio_path} -r 1 -c:v libx264 -preset slow -tune stillimage -crf 18 -c:a copy -shortest -s 1280x720 out.mp4")
      print('   ✅   video generated')
    except Exception as e:
      print('   ❌   video generation failed :(')
      print(e)


  def clean_up(self):
    try:
      os.remove('artwork.png')
      os.remove('audio.mp3')
      os.remove('page.html')
      print('   ✅ cleanup done')
    except Exception as e:
      print('   ❌ cleanup failed')
      print(e)
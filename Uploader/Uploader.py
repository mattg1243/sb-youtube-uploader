import os
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload


class Uploader():
    scopes = ["https://www.googleapis.com/auth/youtube"]
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secrets.json"
    api_key = os.getenv('YT_API_KEY')

    def __init__(self):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        try:
            creds = service_account.Credentials.from_service_account_file(
                'service-account.json', scopes=Uploader.scopes)
            self.youtube = googleapiclient.discovery.build(
                Uploader.api_service_name, Uploader.api_version, credentials=creds)

            print('   ✅   Uploader connected to YouTube')
        except Exception as e:
            print('   ❌   error creating Uploader:')
            print(e)

    def upload_video(self, title, artist, artist_id, beat_id, path="out.mp4"):
        try:
            body = {
                "snippet": {
                    "title": f"{title} (prod. {artist})",
                    "description": f"""{title} (Produced by {artist})
                    Get this beat: https://www.sweatshopbeats.com/app/beat?id={beat_id}\n{artist}: https://www.sweatshopbeats.com/app/user?id={artist_id}\n"""
                },
            }
            req = self.youtube.videos().insert(part='snippet', body=body,
                                               media_body=MediaFileUpload(path))
            res = req.execute()
            print(res)
        except Exception as e:
            print('   ❌   error uploading video:')
            print(e)
        print('   ⏳   uploading video...')

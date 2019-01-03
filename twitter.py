# twitter shit
print "importing twython"
from twython import Twython
print "done importing twython"
import keys
import subprocess

TWITTER_APP_KEY = keys.API_KEY 
TWITTER_APP_KEY_SECRET = keys.API_SECRET_KEY
TWITTER_ACCESS_TOKEN = keys.ACCESS_TOKEN
TWITTER_ACCESS_TOKEN_SECRET = keys.ACCESS_TOKEN_SECRET

client_args = {
    'timeout': 1300
}

t = Twython(app_key=TWITTER_APP_KEY,
            app_secret=TWITTER_APP_KEY_SECRET,
            oauth_token=TWITTER_ACCESS_TOKEN,
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
            client_args=client_args)


def tweet(a,b):
    msg = a
    movName = b
    video = open(movName, 'rb')
    response = t.upload_video(media=video, media_type='video/mp4')
    t.update_status(status=msg, media_ids=[response['media_id']])


if __name__ == '__main__':


    t.update_status(status="hello")
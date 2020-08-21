import os
import sys
import tweepy
import urllib.parse


API_KEY = os.environ['API_KEY']
API_KEY_SECRET = os.environ['API_KEY_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


class UserListener(tweepy.StreamListener):
    def __init__(self, user):
        super(UserListener, self).__init__()
        self.user = user

    def on_status(self, status):
        if status.user.screen_name != self.user:
            return

        print('\n', status.text)
    
        if status.text.startswith('RT @') or is_url(status.text):
            print('Skipping')
            return

        toddler = toddlerify(status.text)
        print('Tweeting:', toddler)
        api.update_status(toddler)
    
    def on_error(self, status_code):
        print('\n***ERROR: Status Code', status_code)
        return True


def is_url(string):
    try:
        result = urllib.parse.urlparse(string.strip())
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


def toddlerify(string):
    words = string.split()

    if words[0].isupper():
        toddler = 'MOMMY, ' + string
    else:
        toddler = 'Mommy, ' + string[0].lower() + string[1:]
    
    if words[-1].isupper() and len(toddler) <= 271:
        toddler += ' WAAAHHH!'

    return toddler[:280]


if __name__ == '__main__':
    handle = sys.argv[1] if len(sys.argv) >= 2 else 'realDonaldTrump'
    print('Handle:', handle)
    user_id = api.lookup_users(screen_names=[handle])[0].id_str
    print('Starting stream for user_id', user_id)

    tweepy \
        .Stream(auth=api.auth, listener=UserListener(handle)) \
        .filter(follow=[user_id])
import json
import os
import requests
import sys
import time
import tweepy

API_KEY = os.environ['API_KEY']
API_KEY_SECRET = os.environ['API_KEY_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
# BEARER_TOKEN = os.environ['BEARER_TOKEN']

# headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}

auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# URL = "https://api.twitter.com/2/tweets/search/stream"


class UserListener(tweepy.StreamListener):
    def __init__(self, user):
        super(UserListener, self).__init__()
        self.user = user

    def on_status(self, status):
        if status.user.screen_name != self.user:
            return

        print(status.text)
        print('Retweeted:', status.retweeted, status.text.startswith('RT @'))
        status = status.text
    
        if status.startswith('RT @'):
            return  # skip retweets

        if status.isupper():
            toddler = 'MOMMY, ' + status

            if len(toddler) <= 271:
                toddler += ' WAAAHHH!'

        else:
            toddler = 'Mommy, ' + status[0].lower() + status[1:]

        if len(toddler) <= 280:
            print('Tweeting:', toddler)
            api.update_status(toddler)
        else:
            print("Couldn't tweet - length", len(toddler))
            print(toddler)
    
    def on_error(self, status_code):
        print('***ERROR: Status Code', status_code)
        return True


# def reset_rules(from_='realDonaldTrump'):
#     rules = requests.get(f"{URL}/rules", headers=headers).json()

#     if rules is None or "data" not in rules:
#         return

#     payload = {"delete": {"ids": [rule["id"] for rule in rules["data"]]}}
#     requests.post(f"{URL}/rules", headers=headers, json=payload)

#     payload = {"add": [{"value": f"from:{from_}"}]}
#     requests.post(f"{URL}/rules", headers=headers, json=payload)


# def stream_tweets():
    # response = requests.get(URL, headers=headers, stream=True)
    # print('Starting stream')

    # for line in response.iter_lines():
    #     if not line:
    #         continue

    #     try:
    #         json_response = json.loads(line)

    #         if json_response.get('title') == 'ConnectionException':
    #             print(json_response)
    #             return True

    #         print('\nTrump tweet:', line)
    #         trump = json_response['data']['text']

    #         if trump.startswith('RT @'):
    #             continue  # skip retweets

    #         if trump.isupper():
    #             toddler = 'MOMMY, ' + trump

    #             if len(toddler) <= 271:
    #                 toddler += ' WAAAHHH!'

    #         else:
    #             toddler = 'Mommy, ' + trump[0].lower() + trump[1:]

    #         if len(toddler) <= 280:
    #             print('Tweeting:', toddler)
    #             api.update_status(toddler)
    #         else:
    #             print("Couldn't tweet - length", len(toddler))
    #             print(toddler)

    #     except Exception as e:
    #         print('\n***Exception')
    #         print(e)


if __name__ == '__main__':
    handle = sys.argv[1] if len(sys.argv) >= 2 else 'realDonaldTrump'
    print('Handle:', handle)
    # reset_rules(handle)

    # while stream_tweets():
    #     print('SLEEPING 30 SECONDS')
    #     time.sleep(30)
    user_id = api.lookup_users(screen_names=[handle])[0].id_str

    tweepy \
        .Stream(auth=api.auth, listener=UserListener(handle)) \
        .filter(follow=[user_id])

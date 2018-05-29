import tweepy
from tweepy import *
import json
from helpers import *

consumer_key = 'bDx9MfNMi6V5MxZdEXyPJar8Y'
consumer_secret = '0zLaESfKn4DtQQtJeLe0yQZPoETKMkLhjgcLkRwgr228V3JUIv'
access_token = '2862334799-lBSCIDYEiWmaiscroDW3BfAgKNH7pgdF8x9iimg'
access_secret = 'GtUjaYvPjoQ7gN74V2EAwy7Gy5Fh84tOnnGmjPPiEJyhY'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)



# consumer_key1 = 'jfXr8ooDAqN66mriYaKOY2UqT'
# consumer_secret1 = 'sbdmGS4NyaEJYcK5nIgC0vpPeHPYGuiiPkKcmeKtbVAwVCuYbk'
# access_token1 = '2862334799-e7HIB5oCvPDCK3P9oTm92KLs645dFgRjfCz5WSX'
# access_secret1 = '0LbahXs05GpcrkRnmULSbQIY1gNA3jN3qzBmbMp8uiAGu'
#
# auth1 = OAuthHandler(consumer_key1, consumer_secret1)
# auth1.set_access_token(access_token1, access_secret1)

# support for multiple authentication handlers
# retry 10 times with 5 seconds delay when getting these error codes
# For more details see
# https://dev.twitter.com/docs/error-codes-responses
# monitor remaining calls and block until replenished
# we dont need bcs i have one application ---->  monitor_rate_limit=True,
#
# auth0.append(auth1)

api = tweepy.API(auth, retry_count=10, retry_delay=5, retry_errors=set([401, 404, 500, 503]), wait_on_rate_limit=True)

consumer_key_ad = 'SmZ9XGLnKLoTKqEJX1YcfoQzP'
consumer_secret_ad = 'RyP1lofhYJeOOgYc2pkz3tsp8UY5PWSrxRt9CLIjnGZwzLTZYy'
access_token_ad = '2862334799-ph5XqfiD0CPYhzaAEQl4rXkQpxpD6nZiy7dgt3h'
access_secret_ad = '7wBIqxhKMKuKOtg6UlMq3b6HoxKMG2ALUBBX9OLpCgE5I'

auth_ad = OAuthHandler(consumer_key, consumer_secret)
auth_ad.set_access_token(access_token, access_secret)

# support for multiple authentication handlers
# retry 10 times with 5 seconds delay when getting these error codes
# For more details see
# https://dev.twitter.com/docs/error-codes-responses
# monitor remaining calls and block until replenished
# we dont need bcs i have one application ---->  monitor_rate_limit=True,


api_ad = tweepy.API(auth_ad, retry_count=10, retry_delay=5, retry_errors=set([401, 404, 500, 503]),
                    wait_on_rate_limit=True)


query = '#britainsgottalent'

file_count = 0

tweet_count = 0

namefile = str(file_count) + '.json'

all = []

for page in tweepy.Cursor(api.search, q=query, include_entities=True).pages():

    for tweet in page:

        print(tweet.text)

        with open(namefile, 'w') as file_tosave:

            d = {}
            d["creation_date"] = str(tweet.created_at)

            d["tweet_id_str"] = tweet.id_str

            d["user_id"] = tweet.user.id_str

            d["text"] = tweet.text.encode('utf8')

            d["nb_likes"] = tweet.favorite_count

            d["nb_retweet"] = tweet.retweet_count

            d["nb_reply"] = 0
            try:
                d["nb_reply"] = get_replies_nb(api_ad,tweet)
            except:
                pass

            d["repling_to_tweet_id"] = tweet.in_reply_to_status_id_str

            try:
                d["quoted_tweet_id"] = tweet.quoted_status_id_str
            except:
                d["quoted_tweet_id"] = None
            try:
                d["retweeted_tweet_id"] = tweet.retweeted_status.id_str
            except:
                d["retweeted_tweet_id"] = None

            text = tweet.text.encode('utf8')
            # document = types.Document(
            #     content=text,
            #     type=enums.Document.Type.PLAIN_TEXT)
            # try:
            #     sentiment = client.analyze_sentiment(document=document).document_sentiment
            #     d["opinion_score"] = sentiment.score
            #     d["magnitude_score"] = sentiment.magnitude
            # except:
            # on ne peut pas calculer a cause du facturation de google cloud

            d["opinion_score"] = -2

            d["magnitude_score"] = 0


            hashtags = ""

            for h in tweet.entities["hashtags"]:
                hashtags = hashtags + " " + h["text"]

            d['hashtages'] = hashtags

            d["geo"] = tweet.geo

            all.append(d)

            replies = get_replies(api_ad, tweet)

            all.append(replies)

            if all.__len__() > 5000:
                json.dump(all, file_tosave)

                all = []

                file_count += 1

                tweet_count = 0
                namefile = str(file_count) + '.json'

            else:
                tweet_count += 1
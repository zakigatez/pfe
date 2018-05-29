import tweepy
from tweepy import *
import json
import math


def get_replies(api,entry):
    tweet = get_root_tweet(entry)
    name = entry.user.screen_name
    id_str = tweet.id_str
    replies = []
    for page in tweepy.Cursor(api.search, q='to:' + name, result_type='recent', since_id=id_str,timeout=999999).pages():
        for tweet in page:
            if hasattr(tweet, 'in_reply_to_status_id_str'):
                if (tweet.in_reply_to_status_id_str == id_str):
                    d = {}
                    d["creation_date"] = str(tweet.created_at)
                    d["tweet_id_str"] = tweet.id_str
                    d["user_id"] = tweet.user.id_str
                    d["text"] = tweet.text.encode('utf8')
                    d["nb_likes"] = tweet.favorite_count
                    d["nb_retweet"] = tweet.retweet_count
                    try:
                        d["nb_reply"] = tweet.reply_count
                    except:
                        d["nb_reply"] = 0
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

                    hashtags = ''
                    for h in tweet.entities["hashtags"]:
                        hashtags = hashtags + ' ' + h["text"]

                    d['hashtages'] = hashtags
                    d["geo"] = tweet.geo
                    replies.append(d)
    return replies

def get_replies_nb(api,entry):
    tweet = get_root_tweet(entry)
    name = entry.user.screen_name
    id_str = tweet.id_str
    replies = 0
    for page in tweepy.Cursor(api.search, q='to:' + name, result_type='recent', since_id=id_str,timeout=999999).pages():
        for tweet in page:
            if hasattr(tweet, 'in_reply_to_status_id_str'):
                if (tweet.in_reply_to_status_id_str == id_str):
                    replies+=1
    return replies



def check_retweeted(status):
    if hasattr(status, 'retweeted_status'):
        retweet = status.retweeted_status
        retweet_screen_name = status.user.screen_name
        if hasattr(retweet, 'user'):
            if retweet.user is not None:
                if hasattr(retweet.user, "screen_name"):
                    if retweet.user.screen_name is not None:
                        tweet_screen_name = retweet.user.screen_name
                        return True
    return False



def check_quoted_tweet(status):
    if hasattr(status, 'quoted_status'):
        quote_tweet = status.quoted_status
        quoted_user = status.user.screen_name
        if hasattr(quote_tweet, 'user'):
            if quote_tweet.user is not None:
                user = quote_tweet.user
                if hasattr(user, 'screen_name'):
                    if user.screen_name is not None:
                        return quote_tweet
    return False


def get_root_tweet(status):
    if check_retweeted(status):
        if hasattr(status, 'retweeted_status'):
            retweet = status.retweeted_status
            return retweet
    if check_quoted_tweet(status):
        if hasattr(status, 'quoted_status'):
            quote_tweet = status.quoted_status
            return quote_tweet
    return status




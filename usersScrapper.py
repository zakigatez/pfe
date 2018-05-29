import json
import os
from  helpers import *
from tweepy import *

# consumer_key = 'E7VC3n5zbHMTXUu880IUlcFEg'
# consumer_secret = '1g30GaJfrMPBZhF55C79e9DehBhCIurvnR7z1PHuw0MpMo9vUs'
# access_token = '2862334799-chUkvDgRnfV0n34V26jYO1YaBF9jIuDE2BkSBEk'
# access_secret = 'Hj9XbC66f46fSUUVS1tdh8aoeG49K9CQY2JrSisDgKg3k'
#
# auth = OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_secret)


consumer_key = 'jfXr8ooDAqN66mriYaKOY2UqT'
consumer_secret = 'sbdmGS4NyaEJYcK5nIgC0vpPeHPYGuiiPkKcmeKtbVAwVCuYbk'
access_token = '2862334799-e7HIB5oCvPDCK3P9oTm92KLs645dFgRjfCz5WSX'
access_secret = '0LbahXs05GpcrkRnmULSbQIY1gNA3jN3qzBmbMp8uiAGu'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)


# support for multiple authentication handlers
# retry 10 times with 5 seconds delay when getting these error codes
# For more details see
# https://dev.twitter.com/docs/error-codes-responses
# monitor remaining calls and block until replenished
#we dont need bcs i have one application ---->  monitor_rate_limit=True,

api = tweepy.API(auth,retry_errors=set([401, 404, 500, 503]), wait_on_rate_limit=True)

users_file = 'users_file.json'
users_full_file = "users_full_file.json"

path = 'C:\Users\GZH\Desktop\PFE\\tweet'
os.chdir(path)

with open(users_full_file, "a+") as full_ref_w:
    print "file openned"

with open(users_file,"r") as f_ref:
    data = json.load(f_ref)
    for user in data:
        print(user)

        try:
            tweets = api.user_timeline(user_id=user["user_id"], count=10, exclude_replies=True)
        except:
            print("user undifined")
            tweets = None

        if tweets != None:
            nb_followers = tweets[0].user.followers_count
            if (nb_followers < 3):
                nb_followers = 3

            nb_following = tweets[0].user.friends_count
            if (nb_following < 3):
                nb_following = 3

            follow_rank = (5) * (math.log(nb_followers / math.log(nb_following)))

            nb_mentions = 0
            nb_likes = 0
            nb_replies = 0

            for t in tweets :
                nb_likes += t.favorite_count
                nb_mentions += t.retweet_count
                nb_replies +=  get_replies_nb(api,t)

            interaction_Rank = (1/10) *  nb_mentions * (100 / (nb_followers * 9))

            likes_rank =  (1/10) * nb_likes * (100 / (nb_followers * 1))

            individuelInfluence = (follow_rank * 70 / 100) + (likes_rank * 15 * 100 / 100) + (interaction_Rank * 15 * 100 / 100)

            print(individuelInfluence)

            u_d = {}
            u_d["user_id"] = user["user_id"]
            u_d["influence"] = individuelInfluence
            u_d["nb_followers"] = nb_followers
            u_d["nb_following"] = nb_following
            u_d["follow_rank"] = follow_rank
            u_d["interaction_rank"] = interaction_Rank

            users = []

            try :
                with open(users_full_file, "r") as full_ref_r:
                    users = json.load(full_ref_r)
                    users.append(u_d)
            except:
                print("file empty ")

            with open(users_full_file, "w") as full_ref_w:
                json.dump(users, full_ref_w)



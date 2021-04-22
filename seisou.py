import tweepy, datetime, json, pytz
from datetime import datetime

# Authenticate to Twitter
auth = tweepy.OAuthHandler("CONSUMERKEY_REDACTED", "CONSUMERSECRET_REDACTED")
auth.set_access_token("ACCESSKEY_REDACTED", "ACCESSSECRET_REDACTED")
api = tweepy.API(auth)
'''
# To test access to Twitter
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
'''

unaware_cutoff_date = datetime(2014, 01, 01)
aware_cutoff = unaware_cutoff_date.replace(tzinfo=pytz.UTC)
# print('aware is ', aware_cutoff)

file = open("tweet.js","r")
myjson = json.load(file)

for tweet in myjson:
	d = datetime.strptime(tweet['tweet']['created_at'], "%a %b %d %H:%M:%S %z %Y")
	if d < aware_cutoff:
		print(tweet['tweet']['created_at'] + " " + tweet['tweet']['id_str'] + ' will be deleted')
		api.destroy_status(tweet['tweet']['id_str'])
		print(tweet['tweet']["created_at"] + " " + tweet['tweet'] ['id_str'] + ' successfully deleted')

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
    print('Authentication OK')
except:
    print('Error during authentication')
'''

unaware_cutoff_date = datetime(2014, 01, 01)
aware_cutoff = unaware_cutoff_date.replace(tzinfo=pytz.UTC)
# print('aware is ', aware_cutoff)

file = open("tweet.js","r")
myjson = json.load(file)

# Counters
deleted_tweets = 0
failed_deletion = 0
unaffected_tweets = 0

for tweet in myjson:
	d = datetime.strptime(tweet['tweet']['created_at'], "%a %b %d %H:%M:%S %z %Y")
	if d < aware_cutoff:
		try:
			print(tweet["tweet"]["created_at"] + ' ' + tweet["tweet"]["id_str"] + ' will be deleted')
			api.destroy_status(tweet['tweet']['id_str'])
			print(tweet["tweet"]["created_at"] + ' ' + tweet["tweet"]["id_str"] + ' successfully deleted')
			if api.destroy_status(tweet["tweet"]["id_str"]):
				deleted_tweets +=1
		except (tweepy.error.TweepError):
			failed_deletion +=1
	else:
		unaffected_tweets +=1

print('Total deleted tweets = ', deleted_tweets)
print('Total failed deletion = ', failed_deletion)
print('Total unaffected tweets = ', unaffected_tweets)

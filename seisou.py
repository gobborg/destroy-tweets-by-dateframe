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

unaware_cutoff_date_1 = datetime(2014, 1, 1) #(cannot use leading zeroes)
aware_cutoff_1 = unaware_cutoff_date_1.replace(tzinfo=pytz.UTC)
# print('aware 1 is ', aware_cutoff_1)

# If you do not want to delete within a range of existing tweets, remove date_2 from here and line 36.
unaware_cutoff_date_2 = datetime(2015, 1, 1) #(cannot use leading zeroes)
aware_cutoff_2 = unaware_cutoff_date_2.replace(tzinfo=pytz.UTC)
# print('aware 2 is ', aware_cutoff_2)

file = open("tweet.js","r")
myjson = json.load(file)

# Counters for fun and data
deleted_tweets = 0
failed_deletion = 0
unaffected_tweets = 0

for tweet in myjson:
	d = datetime.strptime(tweet['tweet']['created_at'], "%a %b %d %H:%M:%S %z %Y")
	if aware_cutoff_1 < d < aware_cutoff_2:
		print(tweet["tweet"]["created_at"] + ' ' + tweet["tweet"]["id_str"] + ' will be deleted')
		try:
			api.destroy_status(tweet['tweet']['id_str'])
		except (tweepy.error.TweepError):
			print('Error destroying due to ', tweepy.error.TweepError)
			failed_deletion +=1
		try:
			api.get_status(tweet["tweet"]["id_str"])
		except (tweepy.error.TweepError):
			print(tweet["tweet"]["created_at"] + ' ' + tweet["tweet"]["id_str"] + ' successfully deleted')
			deleted_tweets +=1
		else:
			failed_deletion +=1
	else:
		unaffected_tweets +=1

print('Total deleted tweets = ', deleted_tweets)
print('Total failed deletion = ', failed_deletion)
print('Total unaffected tweets = ', unaffected_tweets)

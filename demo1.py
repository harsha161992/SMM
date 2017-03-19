from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import csv
import jsonpickle
#import nltk

#consumer key, consumer secret, access token, access secret.
ckey="USJhGR4oIjUx4dNyPenvps9Ra"
csecret="tZGOWRDWeClEMpkk8mD6LGhmPVqdLnLauCM1cSERYEq96USwvQ"
atoken="706371280996425728-GPXnQBSEjmlffaZXvMxSoJzv7l2JXN6"
asecret="Mf2mHPa6j6IjElovvm00Cnq0UEcAHGM4NcvYiL4gN7yIX"



auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)


api=tweepy.API(auth)

# This for loop is to avaoid getting duplicate sttaus requests
#Taken from  http://stackoverflow.com/questions/29635085/tweepy-error-python-2-7
for status in tweepy.Cursor(api.user_timeline).items():
    try:
        api.destroy_status(status.id)
    except:
        pass

#api.update_status('tweepy + oauth!')

user = api.get_user('digirajput')
print (user.screen_name)
#Code taken from https://gist.github.com/yanofsky/5436496
alltweets = []
	   
new_tweets = api.user_timeline(id = 'digirajput',count=200)

alltweets.extend(new_tweets)

oldest = alltweets[-1].id - 1

while len(new_tweets) > 0:
		print ("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(id = 'digirajput',count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print ("...%s tweets downloaded so far" % (len(alltweets)))


fid = open("niharikasa.json","w")
for tweet in alltweets:
	fid.write(jsonpickle.encode(tweet._json,unpicklable=False) + '\n')
fid.close()








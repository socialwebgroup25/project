# Import packages
import twitter, csv
from math import *

# token
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

# Search query
q='#ikstem since:2017-03-15 until:2017-03-16'

# Describing the query hashtag for the filename
query_hashtag = '#ikstem'


# The amount of tweets getting parsed per step
count = 100

#bound the number of tweets
counter=0
maximum=14000


# Function to write the data as a .csv file
def writeCsv(filename,length):
    with open(filename,'wb') as out:
        csv_out=csv.writer(out,delimiter=';')
        csv_out.writerow(['username','date','retweets','favorites','text','mentions','hashtags','id'])
        for i in range(length):
            row = [usernames_main[i].encode('utf-8'),dates_main[i].encode('utf-8'),str(retweets_main[i]),str(favorites_main[i]),status_texts_main[i].encode('utf-8'),mentions[i].encode('utf-8'),hashtags[i].encode('utf-8'),str(ids_main[i])]
            csv_out.writerow(row)

# Function to write .csv with only the username and mentions
def writeCsvMentions(filename,length):
    with open(filename,'wb') as out:
        csv_out=csv.writer(out,delimiter=';')
        for i in range(length):
            row = [usernames_main[i].encode('utf-8'),mentions[i].encode('utf-8')]
            csv_out.writerow(row)


# Set the ID from which you want to start looking for tweets
X=841891427856600999

# Empty lists to append later on
idlist = []
hashtags = []
mentions = []
ids_main = []
geos_main = []
usernames_main = []
dates_main = []
retweets_main = []
favorites_main = []
status_texts_main = []

while counter<maximum:
    search = twitter_api.search.tweets(q=q,
                                       count=count, lan='nl',
                        max_id=X
                      )
    statuses = search['statuses']

    # Get the text from the tweet
    status_texts = [ status['text']
    for status in statuses ]
    status_texts_main = status_texts_main + status_texts 

    # IDlist om de laagste uit te halen
    for status in statuses:
        idlist.append(int(status['id_str']))

    # Get the mentioned users from the tweet
    for status in statuses:
        print counter
        counter=counter+1
        mentioned_users_list = []
        if (status['entities']['user_mentions'] == []):
            mentions.append(u'')
        else:
            for user_mention in status['entities']['user_mentions']:
                mentioned_users_list.append(user_mention['screen_name'])
            mentioned_users = ','.join(mentioned_users_list)
            mentions.append(mentioned_users)
            
    # Get the hashtags used in the tweet
    for status in statuses:
        hashtag_list = []
        for hashtag in status['entities']['hashtags']:
            hashtag_list.append(hashtag['text'])
            hashtags_user = ','.join(hashtag_list)
        hashtags.append(hashtags_user)

    # Get the tweet ID
    ids = [ status['id']
        for status in statuses]
    ids_main = ids_main + ids

    # Get the location from the tweet (almost never used, thus not used in the end product)
    geos = [ status['geo']
        for status in statuses]
    geos_main = geos_main + geos

    # Get the username of the user sending the tweet
    usernames = [ status['user']['screen_name']
        for status in statuses]
    usernames_main = usernames_main + usernames

    # Get the time of the tweet posted
    dates = [ status['created_at']
        for status in statuses]
    dates_main = dates_main + dates

    # Get the amount of retweets
    retweets = [ status['retweet_count']
        for status in statuses]
    retweets_main = retweets_main + retweets

    # Get the amount of favorites
    favorites = [ status['favorite_count']
        for status in statuses]
    favorites_main = favorites_main + favorites


    # Set the smallest id as the first ID to go look for new tweets
    X = min(idlist) - 1

# Remove duplicates
def removeDuplicates():
    i = 0
    while (i < len(status_texts_main)):
        if status_texts_main[i] == status_texts_main[i+1]:
            del status_texts_main[i+1]
            del usernames_main [i+1]
            del dates_main [i+1]
            del favorites_main [i+1]
            del geos_main [i+1]
            del ids_main [i+1]
            del hashtags [i+1]
            del mentions [i+1]
        else:
            i += 1


# Write the .csv file from the data
writeCsv('twitterdata_' + query_hashtag + '.csv',len(dates_main))

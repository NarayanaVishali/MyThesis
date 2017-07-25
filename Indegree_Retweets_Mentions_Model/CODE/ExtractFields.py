#!/usr/bin/env python
import json,sys,re,os
sys.path.append('./')
#import TweetsLib as tlib


for line in sys.stdin:
    try:
        # Load Tweets
        parsed_json_tweets = json.loads(line)
        # Extract user handle
        this_user_handle = parsed_json_tweets['user']['screen_name'].lstrip().strip()
        # Extract date created
        this_tweet_timestamp = parsed_json_tweets['created_at'].lstrip().strip()
        # Extract tweet text
        tweet_text = parsed_json_tweets['text'].lstrip().strip()
        # Extract follower count
        follower_count = parsed_json_tweets['user']['followers_count']
        if 'retweeted_status' in parsed_json_tweets:
            retw_count = parsed_json_tweets['retweeted_status']['retweet_count']
        # Extract user_mentions
            user_mention = parsed_json_tweets['entities']['user_mentions']
            if len(user_mention)!=0:
                if user_mention != "":
                    names = user_mention[0]['screen_name']

                print "%s,%s,%s,%s,%s" % (this_user_handle, follower_count, retw_count, names, this_tweet_timestamp)
    except ValueError:
        continue
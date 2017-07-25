#!/usr/bin/env python
import json,sys,re,os
sys.path.append('./')
import TweetsLib as tlib

topicsArray = tlib.readFileandReturnAnArray("politicstopic3", "r", True)
currentTopics = ",".join(topicsArray).strip().lstrip()

for line in sys.stdin:
    try:
        parsed_json_tweets = json.loads(line)
        this_tweet_timestamp = parsed_json_tweets['created_at'].lstrip().strip()
        this_user_handle = parsed_json_tweets['user']['screen_name'].lstrip().strip()
        tweet_text = parsed_json_tweets['text'].lstrip().strip()
        if tweet_text != "":
            tweet_text = tlib.stripNewLineAndReturnCarriage(tweet_text)
            tweet_text = tlib.removeUserMentions(tweet_text)
            tweet_text = tlib.replaceRepeatedCharacters(tweet_text)
            tweet_text = tlib.convertMultipleWhiteSpacesToSingleWhiteSpace(tweet_text)
            tweet_text = tlib.replaceHashTagsWithWords(tweet_text)
            tweet_text = re.sub(r'([^\s\w:./]|_)', '', tweet_text)
            tweet_text = tweet_text.strip().lstrip().lower()
            if tlib.isArrayOfFilterWordsInTweet(tweet_text, currentTopics, ' ', ','):
                ownerName = "N/A"
                ownerTimeStamp = "N/A"
                if 'retweeted_status' in parsed_json_tweets:
                    tweet_text = tlib.removeItemsInTweetContainedInAList(tweet_text, ['rt'], ' ')
                    ownerName = parsed_json_tweets['retweeted_status']['user'][
                        'screen_name'].lstrip().strip()
                    ownerTimeStamp = parsed_json_tweets['retweeted_status']['user'][
                        'created_at'].lstrip().strip()
                print "%s\t%s,%s\t%s,%s" % (
                    tweet_text, this_tweet_timestamp, this_user_handle, ownerName, ownerTimeStamp)
    except ValueError:
        continue

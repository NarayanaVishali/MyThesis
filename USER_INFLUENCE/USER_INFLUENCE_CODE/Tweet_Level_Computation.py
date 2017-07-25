import json
from datetime import timedelta, date
import time, datetime


class Tweet:
    ''' Input for expected in the order of <TEXT>\t<TIMESTAMP>\t
    <USER HANDLE>\t<OWNER Handle>\t<ORIGINAL TIMESTAMP>'''

    def __init__(self, *args):
        self.timestamp = args[1]
        self.text = args[0]
        self.user = args[2]
        self.owner = args[3]
        self.own_timestamp = args[4]
        self.children = []
        if self.owner != "N/A":
            self.level = 1
        else:
            self.level = 0

    def is_retweet(self):
        if self.owner == "N/A":
            return False;
        return True

    def print_tweet(self):
        print self.text, self.user, self.timestamp, self.owner, self.own_timestamp

    def __str__(self):
        return self.text + "\t" + self.user + "\t" + str(self.level) + "\t" + str(
            self.timestamp) + "\t" + self.owner + "\t" + str(self.own_timestamp) +"\n"

    def addChild(self, tweet):
        self.children.append(tweet)

def toTimeStamp(timeStr):
    # print timeStr
    timeStr = timeStr.split("+")
    timeStr = timeStr[0] + timeStr[1][5:]
    return time.mktime(datetime.datetime.strptime(timeStr, "%a %b %d %H:%M:%S %Y").timetuple())


def tweet_propagation():
    tweet_list.sort(key=lambda Tweet: Tweet.timestamp, reverse=False)
    length = len(tweet_list)
    for i in range(0, length):
        temp_list = [tweet_list[i]]
        for j in range(i, length):
            if tweet_list[j].is_retweet() and (tweet_list[i].text == tweet_list[j].text) and (
                tweet_list[i].user == tweet_list[j].owner):
                for tweet in temp_list:
                    if tweet.user == tweet_list[j].owner:
                        tweet_list[j].level = tweet.level + 1
                        break
                temp_list.append(tweet_list[j])

output_file="output"
out = open(output_file, "w");
lst_twt = None
tweet_list = []
with open("part-00000.txt", "r") as input1:
    for tem in input1:
        tem = tem.split("\t")
        #print tem[0]
        temp = tem[1].split(",")
        temp1=tem[2].split(",")
        line = [tem[0], temp[0], temp[1], temp1[0], temp1[1]]
        line[1] = toTimeStamp(line[1])
        if line[3] != "N/A":
            line[4] = toTimeStamp(line[4][:-1])
        else:
            line[4] = line[4][:-1]
        tweet = Tweet(*line)
        if tweet.text != lst_twt and lst_twt != None :
                tweet_propagation()
                for tweet1 in tweet_list:
                    out.write(str(tweet1))
                    print tweet
                tweet_list=[tweet]
        else:
            tweet_list.append(tweet)
        lst_twt = tweet.text
    tweet_propagation()
    for tweet1 in tweet_list:
        out.write(str(tweet1))
        print tweet1
out.close()
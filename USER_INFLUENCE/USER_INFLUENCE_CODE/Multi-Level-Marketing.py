import json
from datetime import timedelta as td
from datetime import date
from dateutil import parser
import time, datetime
from datetime import datetime
import collections

class Tweet:
    ''' Input for expected in the order of <TEXT>\t<TIMESTAMP>\t
    <USER HANDLE>\t<OWNER Handle>\t<ORIGINAL TIMESTAMP>'''

    def __init__(self, *args):
        self.timestamp = args[3]
        self.text = args[0]
        self.user = args[1]
        self.owner = args[4]
        self.own_timestamp = args[5]
        self.potential = args[6]
        self.level = int(args[2])

    def is_retweet(self):
        if self.owner == "N/A":
            return False;
        return True

    def print_tweet(self):
        print self.text, self.user, self.timestamp, self.owner, self.own_timestamp

    def __str__(self):
        return self.text + "\t" + self.user + "\t" + str(self.level) + "\t" + str(
            self.timestamp) + "\t" + self.owner + "\t" + str(self.own_timestamp) +"\n"

def toTimeStamp(timeStr):
    # print timeStr
    timeStr = timeStr.split("+")
    timeStr = timeStr[0] + timeStr[1][5:]
    return time.mktime(datetime.datetime.strptime(timeStr, "%a %b %d %H:%M:%S %Y").timetuple())


output_file="output2"
input_file="output1"
out = open(output_file, "w");
lst_twt = None
rhi =2
tweet_list = []
start_date=parser.parse("09/01/2015")
end_date=parser.parse("09/30/2015")
#startDate = parser.parse(os.environ["START_DATE"])
#endDate = parser.parse(os.environ["END_DATE"])
date_list = [str((start_date + td(days=x)).date()) for x in range(0, (end_date-start_date).days)]
influence_dict = {}
user_list = []


for date in date_list:
    influence_dict[date] = {}

def get_owner(tweet_list, curr_tweet):
    owner = None
    for tweet in tweet_list:
            if curr_tweet.owner == tweet.user :

                owner = tweet
                break
    else:
        if curr_tweet.is_retweet():
            return curr_tweet.owner
    return owner

def calc_potential():
    twl = len(tweet_list)
    for i in range(0, twl):
        par_influence =0
        rev_lev = 1
        count = 0
        curr_tweet = tweet_list[i]
        while True:
            owner = get_owner(tweet_list, curr_tweet)
            if owner == None:
                #print curr_tweet
                break
            else:
                if isinstance(owner, str):
                    par_influence = int(tweet_list[i].potential) * pow(rhi, rev_lev)
                    dat = datetime.fromtimestamp(int(tweet_list[i].timestamp[:-2])).strftime('%Y-%m-%d')
                    if dat in influence_dict:
                        if owner in influence_dict[dat]:
                            influence_dict[dat][owner] += par_influence
                        else:
                            influence_dict[dat][owner] = par_influence
                    break
                else:
                    #count += 1
                    par_influence =  int(tweet_list[i].potential)* pow(rhi, rev_lev)
                    rev_lev += 1
                    dat = datetime.fromtimestamp(int(tweet_list[i].timestamp[:-2])).strftime('%Y-%m-%d')
                    if dat  in influence_dict:
                        if curr_tweet.user == owner.owner:
                            break
                        if owner.user in influence_dict[dat]:
                            influence_dict[dat][owner.user] += par_influence
                        else:
                            influence_dict[dat][owner.user] = par_influence


                    curr_tweet = owner
        #print curr_tweet.user
        user_list.append(curr_tweet.user)
        #print user_list
    #print count

with open(input_file, "r") as input1:
    for line in input1:
        line = line.split("\t")
        line[6] = int(line[6][:-1])
        if line[1] == line[4]:
            continue
        tweet = Tweet(*line)
        if tweet.text != lst_twt and lst_twt != None :
            calc_potential()
            tweet_list=[]
            tweet_list.append(tweet)
        else:
            tweet_list.append(tweet)
        lst_twt = tweet.text
    calc_potential()
    od = collections.OrderedDict(sorted(influence_dict.items()))
    #print od
    for key in od.keys():
        #print key
        for A in od[key].keys():
            #if A in user_list:
                print "\t"+key+"\t"+A+"\t"+str(od[key][A])

        print "------------------------------------------------------------------------"

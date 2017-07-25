#!/usr/bin/env python
import sys, os
from dateutil import parser
from datetime import timedelta as td
from itertools import chain, imap
from pprint import pprint
sys.path.append('./')
import TweetsLib as tlib

class User:
    # A utility function to create a new node
    def __init__(self, value):
        self.value = value
        self.children = []
        self.left = None
        self.right = None

    def __iter__(self):
        for v in chain(*imap(iter, self.children)):
            yield v
        yield self.value

    def addChild(self, value):
        self.children.append(value)

tweetLevels = {}
owner = User("root,root")
startDate = parser.parse(os.environ["START_DATE"])
endDate = parser.parse(os.environ["END_DATE"])
date_list = [str((parser.parse(startDate) + td(days=x)).date()) for x in range(0, (parser.parse(endDate) - parser.parse(startDate)).days)]
Previous_tweet = None
#output_file="treeoutput3.txt"
#out = open(output_file, "w");
global root_count
root_count = 0
global user_count
user_count = 0
global node_count
node_count = 0

def countNodes(rootNode):
   count = 1
   for child in rootNode.children:
      count +=  countNodes(child)
   return count


def ifParent_AddChildNode(rootNode, value, childToAdd):
    if rootNode.value.strip().lstrip() == value.strip().lstrip():
        rootNode.addChild(User(childToAdd))
    elif len(
            rootNode.children) == 0 and rootNode.value != value:
        return
    else:
        for child in rootNode.children:
            ifParent_AddChildNode(child, value, childToAdd)

def nodeExistence(rootNode, value):
    if rootNode.value.strip().lstrip() == value.strip().lstrip():
        return True
    elif len(rootNode.children) == 0 and rootNode.value != value:
        return None
    else:
        for child in rootNode.children:
            nodeExistence(child, value)

def extractLevelsFromATree(rootNode, level_count):
        if len(rootNode.children) >= 0:
            (ts, node_user) = rootNode.value.strip().lstrip().split(",")
            if ts != "root":
                thisDate = tlib.extractDateFromTimestamp(ts)
                if not tweetLevels.has_key(str(thisDate)):
                    tweetLevels.update({str(thisDate): str(level_count)})
                else:
                    dict_val = tweetLevels[str(thisDate)]
                    dict_val += "," + str(level_count)
                    tweetLevels.update({str(thisDate): dict_val})
            global root_count
            root_count += 1
            for child in rootNode.children:
                global root_count
                global user_count
                global node_count
                node_count = countNodes(owner)
                #print user_count
                #print root_count
                if root_count < user_count:
                    extractLevelsFromATree(child, level_count + 1)
                else:
                    break
        else:
            return



for line in sys.stdin:
        lineArray = tem.strip().lstrip().split("\t")
        this_tweet = lineArray[0]
        user_infos = lineArray[1]
        user_infoss = user_infos.split(",")
        this_user = (user_infoss[0]+","+user_infoss[1])
        owner_infos = lineArray[2]
        owner_infoss = owner_infos.split(",")
        prev_owner = (owner_infoss[1]+","+owner_infoss[0])
        if Previous_tweet != this_tweet:
            global user_count
            if Previous_tweet is not None:
                global node_count
                countNodes(owner)
                extractLevelsFromATree(owner, 0)
                owner = User("root,root")
                this_propagation = ['0'] * (parser.parse(endDate) - parser.parse(startDate)).days
                for key in tweetLevels.keys():
                    if key in date_list:
                        this_propagation[date_list.index(key)] = tweetLevels[key]
                tweetLevels = {}
                print Previous_tweet + "\t" + "\t".join(this_propagation)
                print "\n"
                this_propagation = []
            Previous_tweet = this_tweet
        if prev_owner == "N/A,N/A":
            owner.addChild(User(this_user))
            global user_count
            user_count += 1

        else:
            if nodeExistence(owner, prev_owner) is not True:
                owner.addChild(User(prev_owner))
                global user_count
                user_count += 1
            ifParent_AddChildNode(owner, prev_owner, this_user)
            global user_count
            user_count += 1

if Previous_tweet == this_tweet:
    countNodes(owner)
    extractLevelsFromATree(owner, 0)
    owner = User("root,root")
    this_propagation = ['0'] * (parser.parse(endDate) - parser.parse(startDate)).days
    for key in tweetLevels.keys():
        if key in date_list:
            this_propagation[date_list.index(key)] = tweetLevels[key]
    tweetLevels = {}
    print this_tweet + "\t" + "\t".join(this_propagation)
    this_propagation = []
    Previous_tweet = this_tweet

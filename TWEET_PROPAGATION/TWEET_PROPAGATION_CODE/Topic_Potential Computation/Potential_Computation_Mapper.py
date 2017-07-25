#!/usr/bin/env python
import sys,os
from dateutil import parser
from datetime import timedelta as td
import decimal
sys.path.append('./')
import TweetsLib as tlib

startDate = parser.parse(os.environ["START_DATE"])
endDate = parser.parse(os.environ["END_DATE"])
rho = float(os.environ["RHO"])
date_list = [str((startDate + td(days=x)).date()) for x in range(0, (endDate-startDate).days)]
topiclist = tlib.readFileandReturnAnArray("politicstopic2", "r", True)

def computePotential (current_level, rho):
    if "," not in current_level:
        return 0
    else:
        this_potential=0
        level_arr = current_level.strip().lstrip().split(",")
        for level in level_arr:
            if isInt(level) is True:

                if int(level) >= 0:
                    this_potential += pow(decimal.Decimal(rho), decimal.Decimal(int(level) - 1))
            return this_potential

def isInt(x):
    try:
        int(x)
        return True
    except ValueError:
        return False
for line in sys.stdin:
    myarr = line.strip().lstrip().split("\t")
    for topic in topiclist:
        if tlib.isWordInTweet(myarr[0],topic," "):
            for x in xrange(1,len(myarr),1):
				print topic+","+date_list[x-1]+"\t"+str(computePotential(myarr[x], rho))
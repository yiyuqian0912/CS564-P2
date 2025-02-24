
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"
bidID = 0
items_set = set()
users_dict = {}

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    global bidID, users_dict, items_set
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        item_attributes = ["ItemID", "Name", "Currently", "Buy_Price", "First_Bid", "Number_of_Bids", "Started", "Ends", "Description"]
        for item in items:
            if item["ItemID"] in items_set:
                pass
            items_set.add(item["ItemID"])
            with open("items.dat", "a") as item_file, open("bids.dat", "a") as bid_file, open("ItemCategory.dat", "a") as item_category_file:
                for category in item["Category"]:
                    item_category_file.write(item["ItemID"] + columnSeparator + category + '\n')
                for attribute in item_attributes:
                    if attribute not in item.keys():
                        item[attribute] = "NULL"

                item["Buy_Price"] = transformDollar(item["Buy_Price"]) if item["Buy_Price"] != "NULL" else "NULL"
                item["First_Bid"] = transformDollar(item["First_Bid"]) if item["First_Bid"] != "NULL" else "NULL"
                item["Currently"] = transformDollar(item["Currently"]) if item["Currently"] != "NULL" else "NULL"
                item["Started"] = transformDttm(item["Started"]) if item["First_Bid"] != "NULL" else "NULL"
                item["Ends"] = transformDttm(item["Ends"]) if item["First_Bid"] != "NULL" else "NULL"

                for attribute in item_attributes:
                    item_file.write(str(item[attribute]) + columnSeparator)
                item_file.write(item["Seller"]["UserID"] + '\n')
                
                userID = item["Seller"]["UserID"]
                if userID not in users_dict:
                    users_dict[userID] = {}
                if "IsSeller" not in users_dict[userID] or users_dict[userID]["IsSeller"] == "False":
                    users_dict[userID]["UserID"] = userID
                    users_dict[userID]["Rating"] = item["Seller"]["Rating"]
                    users_dict[userID]["Location"] = item["Location"]
                    users_dict[userID]["Country"] = item["Country"]
                    users_dict[userID]["IsSeller"] = "True"
                    if "IsBidder" not in users_dict[userID]:
                        users_dict[userID]["IsBidder"] = "False"


                if item["Bids"] is not None:
                    for bid in item["Bids"]:
                        bid_file.write(str(bidID) + columnSeparator)
                        bidID += 1
                        bid_file.write(transformDttm(bid["Bid"]["Time"]) + columnSeparator)
                        bid_file.write(transformDollar(bid["Bid"]["Amount"]) + columnSeparator)
                        bid_file.write(item["ItemID"] + columnSeparator)

                        bidder = bid["Bid"]["Bidder"]
                        bid_file.write(bidder["UserID"] + "\n")
                        if bidder["UserID"] not in users_dict:
                            users_dict[bidder["UserID"]] = {}
                            users_dict[bidder["UserID"]]["UserID"] = bidder["UserID"]
                            users_dict[bidder["UserID"]]["Rating"] = bidder["Rating"] 
                            users_dict[bidder["UserID"]]["Location"] = bidder["Location"] if "Location" in bidder else "NULL"
                            users_dict[bidder["UserID"]]["Country"] = bidder["Country"] if "Country" in bidder else "NULL"
                        users_dict[bidder["UserID"]]["IsBidder"] = "True"
                        if "IsSeller" not in users_dict[bidder["UserID"]]:
                            users_dict[bidder["UserID"]]["IsSeller"] = "False"
                    




"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print ("Success parsing " + f)
    with open("users.dat", "a") as users_file:
        for user in users_dict:
            user_info = str(users_dict[user]["UserID"]) + columnSeparator + str(users_dict[user]["Rating"]) + columnSeparator + str(users_dict[user]["Location"])+ columnSeparator + str(users_dict[user]["Country"]) + columnSeparator + users_dict[user]["IsSeller"] + columnSeparator + users_dict[user]["IsBidder"] + "\n"
            print(user_info)
            users_file.write(user_info)

if __name__ == '__main__':
    main(sys.argv)

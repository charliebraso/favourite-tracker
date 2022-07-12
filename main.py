import requests
import json
import time

GROUP_ID = input("Enter Group Id: ")
WEBHOOK_URL = input("Enter Webhook URL: ")

def favouriteChecker(groupId):
    timeout = 2
    favouriteCount = []
    r = requests.get(f"https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorType=2&IncludeNotForSale=false&Limit=30&CreatorTargetId={groupId}").json()
    cursor = r["nextPageCursor"]

    for i in r["data"]:
        favouriteCount.append({"assetId": i["id"], "favoriteCount": i["favoriteCount"], "name": i["name"]})
        
    while cursor != None:
        try:
            r = requests.get(f"https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorType=2&IncludeNotForSale=false&Limit=30&CreatorTargetId={groupId}&cursor={cursor}").json()
            cursor = r["nextPageCursor"]
            for i in r["data"]:
                favouriteCount.append({"assetId": i["id"], "favoriteCount": i["favoriteCount"], "name": i["name"]})
        except:
            print("ratelimit")
            timeout *= 1.2
        time.sleep(timeout)
    
    return favouriteCount

def main(groupId):
    firstFavouriteList = favouriteChecker(groupId)
    
    while True:
        favouriteList = favouriteChecker(groupId)
        
        if favouriteList != firstFavouriteList:
            for i in favouriteList:
                for x in firstFavouriteList:
                    if i["assetId"] == x["assetId"]:
                        if x['favoriteCount'] != i['favoriteCount']:
                            print(f"{x['favoriteCount']} --> {i['favoriteCount']}")

                            embed = {
                                "description": f"Favourite Count: {i['favoriteCount']}\nFavourites Gained: {i['favoriteCount']-x['favoriteCount']}\nCreated By phish#9999",
                                "title": f"New Favourite: {i['name']}"
                                }

                            data = {
                                "username": f"Favourite Tracker",
                                "embeds": [
                                    embed
                                    ],
                            }
                            print("Found new favourite")
                            headers = {"Content-Type": "application/json"}

                            result = requests.post(WEBHOOK_URL, json=data, headers=headers)
                            if 200 <= result.status_code < 300:
                                print(f"Webhook sent {result.status_code}")
                            else:
                                print(f"Not sent with {result.status_code}, response:\n{result.json()}")
                            
        firstFavouriteList = favouriteList         
        time.sleep(100)
                
main(GROUP_ID)

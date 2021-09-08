import os
from typing import Optional, List
import pymongo
import json
from bson import json_util

connection_url = 'mongodb+srv://bluemoon:224KdzDZ78ZkljZM@darklord.rwcoi.mongodb.net'
client = pymongo.MongoClient(connection_url)
db = client.get_database('sample_restaurants')

def get_all():
    restaurants = db["restaurants"].find()
    return restaurants

def get_restaurant_by_id(id: str):
    if (restaurant := db["restaurants"].find_one({"restaurant_id": id})) is not None:
        return restaurant 
    return None

def update_restaurant_by_id(id: str, restauant: UpdateRestaurantModel):
    #restauant = {k, v for k, v in restauant.dict().items() if v is not None}

    if len(restauant >=1):
        update_result =  db["students"].update_one({"restaurant_id": id}, {"$set": restauant})

        if update_result.modified_count == 1:
            if (
                updated_restaurant := db["restaurant"].find_one({"restaurant_id": id})
            ) is not None:
                return json.loads(json_util.dumps((updated_restaurant)))

    if (existing_restaurant := db["restaurant"].find_one({"restaurant_id": id})) is not None:

        return json.loads(json_util.dumps((updated_restaurant)))

    return None

def import_csv():
    """Takes a csv file, converts each row into json, and inserts the rows into mongo """

    try:
        
        #print("server_info"+ str(client.server_info()))
        #print(client.list_database_names())
        id = "40356018"
        #resultAll = get_all()
        result = get_restaurant_by_id(id)
        print("Result:")
        print("======================================")
        print(result)
        #print(str(resultAll))
        
    except pymongo.errors.ServerSelectionTimeoutError as err:
        # do whatever you need
        print("Error:")
        print("-----------------------------------------------------------------------")
        print(err)


if __name__ == '__main__':
    import sys, os
    sys.path.append(os.getcwd())
    import_csv()


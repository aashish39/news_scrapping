import pymongo

if __name__ == "__main__":
    print("Welcome to pyMongo")
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    print(client)
    db = client['DataLinks']
    collection = db['mysampleCollectionFactory']
    dictionary = {'link':'www.google.com','data':'live score'}
    collection.insert_one(dictionary)

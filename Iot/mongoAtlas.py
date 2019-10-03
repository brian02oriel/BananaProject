from pymongo import MongoClient
from datetime import datetime
import gridfs

client = MongoClient("mongodb+srv://brian02oriel:UTP-cat5@ripeness-8yi3b.mongodb.net/admin?retryWrites=true&w=majority")
db = client.get_database('Ripeness')
collection_names = db.collection_names()


#Server connected
print("Collection names: ", collection_names)

fs = gridfs.GridFS(db)



#Insert images
col = db.RipenessInfo
col.insert_one({
    "temperature": "20°C",
    "huminidty": "90%",
    "datetime":  datetime.now()
})





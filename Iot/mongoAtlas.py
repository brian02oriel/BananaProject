from pymongo import MongoClient
from datetime import datetime
import gridfs

def MongoConnection():
    client = MongoClient("mongodb+srv://brian02oriel:UTP-cat5@ripeness-8yi3b.mongodb.net/admin?retryWrites=true&w=majority")
    db = client.get_database('Ripeness')
    collection_names = db.collection_names()
    
    #Server connected
    print("Collection names: ", collection_names)
    MongoWrite(db)




def MongoWrite(db):
    fs = gridfs.GridFS(db)
    fileID = fs.put(open(r'../images/banano_m.jpg', 'rb'))
    out = fs.get(fileID)
    print("Image ID", fileID)
    print("Image length", out.length)

    #Insert images
    col = db.RipenessInfo
    col.insert_one({
        "fileID": fileID,
        "temperature": "20°C",
        "huminidty": "90%",
        "datetime":  datetime.now()
    })

MongoConnection()



# -*- coding: utf-8 -*-
from pymongo import MongoClient
from datetime import datetime
import gridfs

def MongoConnection(url):
    #Connecting server
    client = MongoClient("mongodb+srv://brian02oriel:UTP-cat5@ripeness-8yi3b.mongodb.net/admin?retryWrites=true&w=majority")
    db = client.get_database('Ripeness')
    collection_names = db.list_collection_names()
    
    MongoWrite(db, url)




def MongoWrite(db, url):
    #Setting gridfs for mongo file save
    fs = gridfs.GridFS(db)
    fileID = fs.put(open(url, 'rb'))
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
    
    print(url + ' insertada correctamente ' + str(datetime.now()))





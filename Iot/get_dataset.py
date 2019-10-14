# -*- coding: utf-8 -*-
from pymongo import MongoClient
from datetime import datetime
import gridfs

def MongoGetImage():
    #Connecting server
    client = MongoClient("mongodb+srv://brian02oriel:UTP-cat5@ripeness-8yi3b.mongodb.net/admin?retryWrites=true&w=majority")
    db = client.get_database('Ripeness')
    collection_names = db.list_collection_names()
    
    #Initialize gridfs
    fs = gridfs.GridFS(db)

    #Setting my db column
    col = db.RipenessInfo
    getfiles = col.find({})

    fileIDColumns = [ getfileID for getfileID in getfiles]
    fileIDs = list()
    for i in range(len(fileIDColumns)):
        fileIDs.append(fileIDColumns[i]['fileID'])
        print(fileIDColumns[i])
    

    print(fileIDs[0])
    #files = fs.get({"_id": fileIDs[0]})

    #print(files.read())
        

    

MongoGetImage()
    

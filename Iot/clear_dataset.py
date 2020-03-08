# -*- coding: utf-8 -*-
import io
from pymongo import MongoClient
from datetime import datetime
import gridfs

def MongoClearCollections():
    #Connecting server
    client = MongoClient("mongodb+srv://brian02oriel:UTP-cat5@ripeness-8yi3b.mongodb.net/admin?retryWrites=true&w=majority")
    db = client.get_database('Ripeness')
    collection_names = db.list_collection_names()
    
    #Initialize gridfs
    fs = gridfs.GridFSBucket(db)
    files = db.fs.files.find({})
    file_rows = [ value for value in files]
    files_id = list({value['_id'] for value in file_rows}) #Applying dictionary comprehension and convert it to list

    print(files_id)

    print('\n')

    for i in range(len(files_id)):
        fs.delete(files_id[i])
    
    print("Files deleted successfully")

    res = db.RipenessInfo.delete_many({})
    print("Ripeness info deleted successfully")

MongoClearCollections()




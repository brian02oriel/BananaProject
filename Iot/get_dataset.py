# -*- coding: utf-8 -*-
import io
from pymongo import MongoClient
from datetime import datetime
import gridfs
from PIL import Image

def MongoGetImage():
    #Connecting server
    client = MongoClient("mongodb+srv://brian02oriel:UTP-cat5@ripeness-8yi3b.mongodb.net/admin?retryWrites=true&w=majority")
    db = client.get_database('Ripeness')
    collection_names = db.list_collection_names()
    
    #Initialize gridfs
    fs = gridfs.GridFSBucket(db)

    #Setting my db column
    col = db.RipenessInfo

    #Getting columns
    getfiles = col.find({})

    #Getting file_IDs
    fileIDColumns = [ getfileID for getfileID in getfiles]
    fileIDs = list()
    for i in range(len(fileIDColumns)):
        fileIDs.append(fileIDColumns[i]['fileID'])

    #Getting image files
    for j in range(len(fileIDs)):
        grid_out = fs.open_download_stream(fileIDs[j])
        contents = grid_out.read()
        SaveFile(contents, j)

#Saving image into dataset folder
def SaveFile(data, j):
    img = Image.open(io.BytesIO(data))
    img.save("./dataset/pic" + str(j) +".jpg", "JPEG")


        

    

MongoGetImage()
    

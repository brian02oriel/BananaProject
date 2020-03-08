# -*- coding: utf-8 -*-
import io
from pymongo import MongoClient
from datetime import datetime
import gridfs
import pandas as pd
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
    file_id_columns = [ getfileID for getfileID in getfiles]
    file_ids = list()
    temperature = list()
    humidity = list()
    datetime = list()
    for i in range(len(file_id_columns)):
        file_ids.append(file_id_columns[i]['fileID'])
        temperature.append(file_id_columns[i]['temperature'])
        humidity.append(file_id_columns[i]['humidity'])
        datetime.append(file_id_columns[i]['datetime'])

    #Getting image files
    for j in range(len(file_ids)):
        grid_out = fs.open_download_stream(file_ids[j])
        contents = grid_out.read()
        SaveFile(contents, j)
    
    #Getting humidity and temperature
    enviromental_information = {
        'temperature': temperature,
        'humidity': humidity,
        'datetime': datetime
    }
    df = pd.DataFrame(data=enviromental_information)
    print(df)
    df.to_csv('dataset/enviromental_information', sep='\t', encoding='utf-8')

#Saving image into dataset folder
def SaveFile(data, j):
    img = Image.open(io.BytesIO(data))
    img.save("./dataset/pic" + str(j) +".jpg", "JPEG")

MongoGetImage()
    

# -*- coding: utf-8 -*-
from pymongo import MongoClient
from datetime import datetime
from raspduino import SerialConnection
import gridfs

def MongoConnection(url):
    #Connecting server
    client = MongoClient("mongodb+srv://brian02oriel:UTP-cat5@ripeness-8yi3b.mongodb.net/admin?retryWrites=true&w=majority")
    db = client.get_database('Ripeness')
    collection_names = db.list_collection_names()
    
    MongoWrite(db, url)




def MongoWrite(db, url):
    #Getting JSON from Arduino Sensors
    #sensor_data = SerialConnection()
    temperature = 0 #sensor_data["temperature"]
    humidity = 0#sensor_data["humidity"]
    
    #Setting gridfs for mongo file save
    fs = gridfs.GridFS(db)
    fileID = fs.put(open(url, 'rb'))
    out = fs.get(fileID)
    

    #Insert images
    col = db.RipenessInfo
    col.insert_one({
        "fileID": fileID,
        "temperature": temperature,
        "huminidty": humidity,
        "datetime":  datetime.now()
    })

    print(url + ' insertada correctamente ' + str(datetime.now()))





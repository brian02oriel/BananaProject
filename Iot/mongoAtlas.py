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
    try:
        sensor_data = SerialConnection()
    except ValueError:
        print("Error found: ", ValueError)
        sensor_data = {'temperature': 0, 'humidity': 0}
        
    print("Serial Connection: ", sensor_data)
    temperature = sensor_data["temperature"]
    humidity = sensor_data["humidity"]
    
    #Setting gridfs for mongo file save
    fs = gridfs.GridFS(db)
    fileID = fs.put(open(url, 'rb'))
    out = fs.get(fileID)
    

    #Insert images
    col = db.RipenessInfo
    col.insert_one({
        "fileID": fileID,
        "temperature": temperature,
        "humidity": humidity,
        "datetime":  datetime.now()
    })

    print(url + ' insertada correctamente ' + str(datetime.now()))





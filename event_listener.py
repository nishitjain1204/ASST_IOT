import pyrebase
import datetime
from config import config,firebase,authe,storage,database
import json 
import os 
from  image_download import  image_downloader
from face_encode import  face_encoder

def stream_handler(message):
    for key in message['data']:
        adhar=message['data'][key]['adhar']
        adhar = ''.join(e for e in adhar if e.isalnum())
        sname = database.child('Secretary_mapping').get()
        for key in sname.each():
            if (key.val()['email'] == existing_email):
                society_name= key.val()['sname']
        try:
            os.mkdir(society_name +'/'+adhar)
        except FileExistsError:

            print(society_name +'/'+adhar)
        image_downloader(society_name)
        face_encoder(society_name +'/'+adhar)


my_stream = database.child(society_name).child('users').stream(stream_handler)

    
       
        

    # print(message["event"]) # put
    # print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    # print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}

# os.mkdir('Sahajeevan Residency')
# my_stream = database.child("Sahajeevan Residency").child('users').stream(stream_handler)

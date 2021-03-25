import pyrebase
import datetime
from config import config,firebase,authe,database,storage 
import json 
import os 
from face_encode import  face_encoder
import pickle
# from pickle_loader import  pickle_loader
import shutil
import re
import json
from PIL import Image
import requests
from io import BytesIO
from datetime import datetime
# from smbus2 import SMBus
# from mlx90614 import MLX90614

# def get_temperature():
#     bus = SMBus(1)
#     sensor = MLX90614(bus, address=0x5A)

#     print ("Ambient Temperature :", sensor.get_ambient())
#     print(type(sensor.get_ambient()))
#     print ("Object Temperature :", sensor.get_object_1())
#     obj_temp=sensor.get_object_1()

#     bus.close()
#     return obj_temp
    

       

def image_downloader(society_name):

    users=database.child(society_name).child('users').get()
    for user in users.each():
        image_list=user.val()['image']
        i=0
        print(str(type(image_list)))
        if str(type(image_list))=="<class 'list'>":
            for image in image_list:
                try:
                    print(image)
                    response = requests.get(image)
                    img = Image.open(BytesIO(response.content))
                    img.convert('RGB').save(society_name+'/'+''.join(e for e in user.val()['adhar'] if e.isalnum())+'/'+str(datetime.now())+'.jpg')
                except Exception as e:
                    print(e)
        else:
            try:
                response = requests.get(image_list)
                img = Image.open(BytesIO(response.content))
                img.convert('RGB').save(society_name+'/'+''.join(e for e in user.val()['adhar'] if e.isalnum())+'/'+str(datetime.now())+'.jpg')
            except  Exception as e :
                print(e)



        


def secretary_signin(email, password):
    #authentication of secretary 
    try:
        user = authe.sign_in_with_email_and_password(email, password)
        if user:
            sname = database.child('Secretary_mapping').get()
            for key in sname.each():
                if (key.val()['email'] == email):
                    if 'isSecretary' in key.val():
                        print(key.val()['isSecretary'])
                        if key.val()['isSecretary'] == True:
                            return user
                    
           
    except:
        return False
    
    

def  get_society(user):
        existing_email=user['email']
        # getting society associated to the secretary 
        sname = database.child('Secretary_mapping').get()
        for key in sname.each():
            if (key.val()['email'] == existing_email):
                society_name= key.val()['sname']
        try:
            os.mkdir(society_name )
            return society_name
        except FileExistsError:
            return society_name

def json_dump(user,society_name):
        #dumping the secretary data as a json file for future purposes
        json_dict =user
        json_dict['society'] = society_name
        with open("sample.json", "w") as outfile:  
            json.dump(json_dict, outfile)
    

def face_encode_data_get(society_name):
#making local folders for photos for face recog dataset
    adhars=[]
    users = database.child(society_name).child('users').get()
    user_dict=users.val()
    for user in user_dict:
        adhars.append(''.join(e for e in user_dict[user]['adhar'] if e.isalnum()))
    for adhar in adhars:
        try:
            os.mkdir(society_name+'/'+adhar)
        except FileExistsError:
            pass
    image_downloader(society_name)
    data=face_encoder(society_name )
    with open('face_enc','wb') as fp:
        fp.write(pickle.dumps(data))
    for adhar in adhars:
        shutil.rmtree(society_name+'/'+adhar, ignore_errors=True)
        
       
   


def stream_handler(message):
    
    if os.path.isfile('sample.json'):
        with open('sample.json') as file:
            data=json.load(file)
        society_name=data['society']
    else:
        return 
    # print(message)
    for key in message['data']:
        # print(key)
        if key=='adhar':
            adhar=message['data'][key]
            adhar = ''.join(e for e in adhar if e.isalnum())
            if not os.path.isdir(society_name +'/'+adhar):
                os.mkdir(society_name +'/'+adhar)
            image_downloader(society_name)
            pickle_dict = pickle_loader()
            encodings=pickle_dict['encodings']
            names=pickle_dict['names']
            data =face_encoder(society_name +'/'+adhar)
            encodings.append(data['encodings'])
            names.append(data['names'])
            new_data = {'encodings':encodings,'names':names }
            with open('face_enc','wb') as fp:
                # print(pickle.dumps(data))
                fp.write(pickle.dumps(new_data))
            shutil.rmtree(society_name+'/'+adhar, ignore_errors=True)

if __name__ == '__main__':

	image_downloader('Sahajeevan Residency')

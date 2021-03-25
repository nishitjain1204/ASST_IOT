import time 
from face_recog import face_recognizer
import os
from helper_functions import secretary_signin,get_society,json_dump,face_encode_data_get,stream_handler
import time
from config import database,storage
import getpass
import cv2
from datetime import datetime,date
from notificationpush import notificationsend


def image_uploader(society_name, foldername, name):
    print(society_name+'/' + foldername+'/'+name)
    storage.child(society_name+'/' + foldername+'/'+name).put(name)
    return storage.child(society_name+'/' + foldername+'/'+name).get_url('None')


if __name__ ==  "__main__":
    email=input('enter email : ')
    password=getpass.getpass('Enter password : ')
    new_user=secretary_signin(email,password)
    if new_user != False:
        society_name=get_society(new_user)
        print('got society name.........')
        json_dump(new_user,society_name)
        print('json dumped to file.......')
        face_encode_data_get(society_name)
        print('face encodings created......')
        my_stream = database.child(society_name).child('users').stream(stream_handler)
        print('stream initialized')
        while True:
            recognized_person,frame=face_recognizer()
            now_time=str(datetime.now())
            print('recog person',recognized_person)
            cv2.imwrite('rec_person'+now_time+'.jpeg',frame)
            image_file_name='rec_person'+now_time+'.jpeg'
            if recognized_person != 'unknown':
                print(recognized_person)
                
                
                user_dict = database.child(society_name).child('users').get().val()
                for user in user_dict:
                    if user_dict[user]['adhar']==recognized_person:
                        print('person recognized')
                        required_dict=user_dict[user]
                        if 'isresident' in required_dict:
                            if required_dict['isresident']==False:
                                reason=required_dict['occupation']
                                print(reason)
                        else:
                            reason='resident at roomnum '+ str(required_dict['roomnum'])

                        dict_to_push={
                            'name':required_dict['fname'],
                            'image':image_uploader(society_name,'resident_entry',image_file_name),
                            'time':datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                            'reason':reason
                            # 'temperature':get_temperature()
                        }

                       
                       
                        database.child(society_name).child('Entry_Logs').child(str(date.today())).push(dict_to_push)
                        print(dict_to_push)
                        print('entry logged') 
                        time.sleep(60)
                        
            else:
                name = input('Enter name : ')
                myadmins=database.child(society_name).child('Admins').get().val()
                print(list(myadmins.keys()))
                roomnum=input('Enter interested roomnum from the above keys : \n')
                reason=input('Enter reason : \n')
                data ={
                    'name' : name,
                    'roomnum':roomnum,
                    'reason':reason,
                    'image':image_uploader(society_name,'pending_visitors','rec_person'+now_time+'.jpeg'),
                    'time':datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    # 'temperature':get_temperature()
                }
                
                if roomnum in list(myadmins.keys()):
                    key=database.child(society_name).child('visitors').child('Non_validated').child('pending').child(roomnum).push(data)
                    print(key)
                    reg_ids=database.child(society_name).child('Admins').child(roomnum).child('signedinDevices').get().val()
                    print(reg_ids)
                    body={
                        'reason':reason,
                        'key':key,
                        
                        
                    }
                    click_action='/pending_visitors'
                    notificationsend(reg_ids,'You have a new visitor',body,click_action)
                else:
                    print('Invalid room number')
            try:       
                os.remove('rec_person'+time+'.jpeg')
            except Exception as E :
                print(E)
                pass

                       
                
            
           

                  
            
        
                    
                    

         

                

    else:
        print('USER INVALID')
        exit
        



    

                    # face_encoder(society_name)
        
   
   
   
   
   
 # my_stream = database.child(society_name).child('users').stream(stream_handler)
        



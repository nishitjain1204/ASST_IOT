import pickle
from config import storage
import re
import urllib.request

def pickle_loader():
    data = []
    with open('face_enc', 'rb') as fr:
        try:
            while True:
                data.append(pickle.load(fr))
        except EOFError:
            pass
    return data[0]

def image_downloader_from_link(link):
    if link:
        r = urllib.request.urlopen(link)
    else:
        return False
    with open("wind_turbine.jpg", "wb") as f:
        f.write(r.read())


def image_downloader(society_name):


    all_files = storage.list_files()
    
    for file in all_files:
        search=re.search(r"^[^/]*",file.name)
        print(search[0])

image_downloader_from_link("https://firebasestorage.googleapis.com/v0/b/regi-a7a96.appspot.com/o/Sahajeevan%20Residency%2F289094618333%2F289094618333202102252342599952570.jpg?alt=media&token=None")

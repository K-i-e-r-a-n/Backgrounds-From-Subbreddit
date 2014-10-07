from pprint import pprint
#Networking imports
import requests
import json
import datetime
import time
import os
from PIL import Image

import ctypes

#Constants for script
DL_LIMIT = 10
SUBREDDIT = 'spaceporn'



#get json object from imgur gallery
r = requests.get(r'http://imgur.com/r/{sr}/top.json'.format(sr=SUBREDDIT))
#create python dict from JSON object
j = json.loads(r.text)

#pprint(j)

#get the list of images from j['gallery']
image_list = j['data']
#print number of images found
print (len(image_list), 'images found in the gallery')

#pprint(image_list[0])

#get the time object for today and create a folder with the time
folder = datetime.datetime.today()

folder_name = str(folder)
folder_name = folder_name.replace(':', '.')

os.mkdir(str(folder_name))

image_pairs = []

#extract image and file extension from dict
for image in image_list:
    img_name = image['hash'] #name
    img_ext = image['ext'] #extension
    image_pairs.append((img_name, img_ext))

current = 0

#Download images until DL_LIMIT is reached
for name, ext in image_pairs:
    if current < DL_LIMIT:
        url = r'http://imgur.com/{name}{ext}'.format(name=name, ext=ext) #get image urls from json data
        print ('Current image being dled: ', url)
        response = requests.get(url)
        path = r'./{fldr}/{name}{ext}'.format(fldr=folder_name,
                                              name=name,
                                              ext=ext)
        fp = open(path, 'wb')
        fp.write(response.content)
        fp.close()
        Image.open(path).save(r'./{fldr}/{name}.bmp'.format(fldr=folder_name, name=name)) #convert 
        current += 1
print ('Finished downloading {cnt} images to {fldr}.'.format(cnt=current, fldr=folder_name))

print(os.getcwd())

#Sets the desktop wallpaper to a rotating cycle of the images downloaded.
for name, ext in image_pairs:
    SPI_SETDESKWALLPAPER = 0x0014
    code = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, r"{dir}\\{fldr}\\{name}{ext}".format(dir=os.getcwd(), fldr=folder_name, name=name, ext=ext), 2) #set desktop wallpaper to current image
    print ('Wallpaper set to {name}, code: {code}'.format(name=name, code=code))
    for i in range(0,60):
        time.sleep(1)
    


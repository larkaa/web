#!/usr/bin/env python
import os
from PIL import Image
import sys


def verify_images(Localpath):
    
    res = []

    for root, dirs, files in os.walk(Localpath): 
        #print(root)
        for filename in files:
            if filename.endswith(('.png','.jpg','.gif','.jpeg')):
                try:
                    img = Image.open(os.path.join(root,filename)) # open the image file
                    img.verify() # verify that it is, in fact an image
                except (IOError, SyntaxError) as e:
                    print('Bad file:', os.path.join(root,filename)) # print out the names of corrupt files
                    res.append(os.path.join(root,filename))
                    #os.remove(os.path.join(root, filename))
    print(res)
    return
    
if sys.argv[1:]:
    verify_images(sys.argv[1])
else:
    print("Please pass the paths to check as parameters to the script")

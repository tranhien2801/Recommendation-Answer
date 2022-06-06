
import cv2 # cv2.imread(), cv2.imshow() , cv2.imwrite()
import numpy as np #create a NumPy array, use broadcasting, access values, manipulate arrays, and much more
import matplotlib.pyplot as plt  #Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python.


# Generic Libraries
from PIL import Image
import os
import pandas as pd
import numpy as np
import re,string,unicodedata

#Tesseract Library
import pytesseract


#Garbage Collection
import gc

import numpy as np
import matplotlib.pyplot as plt
import os
import urllib.request

def getQuestions(text):
    questions = []
    for i in text.lower().splitlines():
        if 'câu' in i: 
            print(i)
            questions.append(i)
    return questions

def convertImgtoText(url):
    print("Start convert")
    # Let's start with a simple image
    req = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1) # 'Load it as it is'
    # img = cv2.imread("Screenshot 2022-04-15 155237.png") # image in BGR format
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # fig = plt.figure(figsize = [10,10])
    # height,width,channel = img.shape

    pytesseract.pytesseract.tesseract_cmd = r"C:\Users\tranh\AppData\Local\Tesseract-OCR\tesseract.exe"

    # as the image is simple enough, image_to_string method reads all characters almost perfectly!
    text = pytesseract.image_to_string(img,lang='vie')
    print(text)
    print('-------------------------------------------------------------------------------------')
            
    return getQuestions(text)


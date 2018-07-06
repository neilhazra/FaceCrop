#@author Neil Hazra
import numpy as np
import cv2 as cv
import os, re
from os.path import realpath, normpath
from math import atan

delta = -7; #Constant used to shift the region of interest to cover the entire face
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml') #location of the haar classifier XML file
directory = 'RawImages' #location of the raw imges

processed = 0 #keep track of how many images processed and skipped
skipped = 0
#helper function to make sure the region of interest does not extend past the original image
def constrain(val, min_val, max_val):
    if val < min_val:
        val = min_val
    elif val > max_val:
        val = max_val
    return val

for filename in os.listdir(directory): #for even file in the raw images folder
    firstnum = re.search("\d", filename)
    try:
        fullName = filename[:firstnum.start()] #get the name of the person
    except Exception as e:
        print(filename + "ERRRORORORORORORROROR")
    #Make sure the image hasn't already been processed before
    if os.path.exists("CroppedImages//" + fullName + "//" + filename[:-5] + '_cropped' + '.jpg'):
        print("SkippingCroppedFile")
        continue
    img = cv.imread(os.path.join(directory, filename)) #read the raw file into memory
    faces = face_cascade.detectMultiScale(img, 1.3, 5) #detect faces
    if len(faces) < 1:
        skipped = skipped + 1
        continue    #if it doesn't detect any face skip the file
    (x,y,w,h) = faces[0] #x,y represents top left file and w,h are the width and height of the image
    rows,cols,channels = img.shape
    x = constrain(x-int(0.2*w),0,cols)  #Create ROI based on the x,y coordinate of top left corner of face and the width and height
                                        #extend the ROI (region of interest) a further 20 to 50 percent to make sure the entire face is covered
    y = constrain(y-int(0.5*h),0,rows)
    w = int(1.45*w)
    h = int(1.25*w) #Force the image to a 5:4 aspect ratio

    img = img[y:y+h, x:x+w] #set the region of interest as the cropped image
    faces = face_cascade.detectMultiScale(img, 1.3, 5) #check for faces again to make sure cropping was successful
    if not len(faces) == 1:
        skipped = skipped + 1;
        continue
    rows,cols,channels = img.shape

    #print(filename[:-5]+ " " + str(float(h/w)))
    if abs(float(float(rows)/float(cols))-1.25) >0.03:    #if the image doesn't fit the specified aspect ratio throw it out
        skipped = skipped + 1
        print("Bad Aspect Ratio")
        continue
    if w*h < 72000:
        img = cv.resize(img, (240,300),interpolation=cv.INTER_CUBIC)    #resize the image with cubic interpolation if its soo small
    if w*h > 72000:
        img = cv.resize(img, (240,300),interpolation=cv.INTER_AREA)     #resize the image with integration if it is too large
    if not os.path.exists("CroppedImages//" + fullName):
        os.mkdir("CroppedImages//" + fullName)
    cv.imwrite("CroppedImages//" + fullName + "//" + filename[:-5] + '_cropped' + '.jpg', img)    #save the image
    processed = processed + 1
    print("Processing Image")
print("Processed " + str(processed) + " Images")
print("Skipped " + str(skipped) + " Images")
print("%Success" + str(100*processed/(processed+skipped)))
cv.waitKey(0)
cv.destroyAllWindows()

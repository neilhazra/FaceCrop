import numpy as np
import cv2 as cv
import os, re
from os.path import realpath, normpath
from math import atan
delta = -7;
face_cascade = cv.CascadeClassifier('C:/Python27/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
directory = 'D:\Crop\RawImages'

processed = 0
skipped = 0
def constrain(val, min_val, max_val):
    if val < min_val:
        val = min_val
    elif val > max_val:
        val = max_val
    return val

for filename in os.listdir(directory):
    firstnum = re.search("\d", filename)
    firstName = filename[:firstnum.start()]
    if os.path.exists("CroppedImages//" + firstName + "//" + filename[:-5] + '_cropped' + '.jpg'):
        print("SkippingCroppedFile")
        continue
    img = cv.imread(os.path.join(directory, filename))
    faces = face_cascade.detectMultiScale(img, 1.3, 5)
    if len(faces) < 1:
        continue
    (x,y,w,h) = faces[0]
    #print(img.shape)
    rows,cols,channels = img.shape
    x = constrain(x-int(0.2*w),0,cols)
    y = constrain(y-int(0.5*h),0,rows)
    w = int(1.45*w)
    h = int(1.25*w)
    #topLeft = (constrain(x-int(0.2*w),0,cols),constrain(y-int(0.45*h),0,rows))
    #bottomRight = (constrain(x+w+int(0.25*w),0,cols),constrain(y+h+int(0.4*h),0,rows))

    #x = topLeft[0]
    #y = topLeft[1]
    #w = bottomRight[0] - topLeft[0]
    #h = bottomRight[1] - topLeft[1]

    img = img[y:y+h, x:x+w]
    faces = face_cascade.detectMultiScale(img, 1.3, 5)
    if not len(faces) == 1:
        skipped = skipped + 1;
        continue
    rows,cols,channels = img.shape
    print(rows)
    print(cols)
    print(rows/cols)
    #print(filename[:-5]+ " " + str(float(h/w)))
    if abs(float(rows/cols)-1.25) >0.03:
        skipped = skipped + 1
        print(rows/cols)
        continue
    if w*h < 72000:
        img = cv.resize(img, (240,300),interpolation=cv.INTER_CUBIC)
    if w*h > 72000:
        img = cv.resize(img, (240,300),interpolation=cv.INTER_AREA)

    cv.imwrite("CroppedImages//" + filename[:-5] + '_cropped' + '.jpg', img)
    processed = processed + 1
    #print("Processing Image")
print("Processed " + str(processed) + " Images")
print("Skipped " + str(skipped) + " Images")
print("%Success" + str(100*processed/(processed+skipped)))
cv.waitKey(0)
cv.destroyAllWindows()

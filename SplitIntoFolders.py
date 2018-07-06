import os, shutil, re

directory = '/home/youbuntu/Documents/Crop/CroppedImages'

for filename in os.listdir(directory):
    firstnum = re.search("\d", filename)
    #print(firstnum.start())
    newdir = filename[:firstnum.start()]
    #print(newdir)
    if not os.path.exists(newdir):
        #print("Making new directory")
        os.mkdir(newdir)
    if not os.path.exists(newdir + "/" + filename):
        shutil.move('/home/youbuntu/Documents/Crop/CroppedImages/' + filename, newdir)
    #else:
        #print("already done")

#@author Neil Hazra
import re
import urllib2
import multiprocessing
import os

f = open("facescrub_actors.txt", "r")

def save_content((url,name)):
    print name
    try:
        img = urllib2.urlopen(url)
        with open("RawImages//" + name,"wb") as code:
            code.write(img.read())
    except Exception as e:
        pass

urls_names = []

for line in f:
    s = re.split('\t',line) #separate the words in each line of the facescrub text file to isolate the URL from the names of the actors
    url = s[3]
    name = s[0] + s[2] + ".jpeg"
    if os.path.exists("RawImages//" + name):#make sure the file hasn't already been downloaded
        continue
    urls_names.append((url,name)) #add url and name to a list of all items to be downloaded

if __name__=="__main__":
    print(len(urls_names))
    pool = multiprocessing.Pool(processes=8)   #Start 8 processes to expediate the download
    pool.map(save_content, urls_names) #divide the items to be downloaded among the 8 "cores"
f.close()

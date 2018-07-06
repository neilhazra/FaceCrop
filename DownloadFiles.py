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
    s = re.split('\t',line)
    url = s[3]
    name = s[0] + s[2] + ".jpeg"
    if os.path.exists("RawImages//" + name):
        continue
    urls_names.append((url,name))

if __name__=="__main__":
    print(len(urls_names))
    pool = multiprocessing.Pool(processes=16)
    pool.map(save_content, urls_names)
f.close()

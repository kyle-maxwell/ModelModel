import urllib
import requests
import socket
import os
import random

def main():
    # This promotes a more diverse set of photos
    with open('fall11_urls.txt', errors='ignore') as links:
        raw_links = links.read().split()[0::2]
    print(raw_links[0:10])
    i = 0
    dir_name = 'data/val/empty_images/'
    socket.setdefaulttimeout(3)
    print(len(raw_links))
    
    while(True):
        link = raw_links[random.randint(0,len(raw_links)-1)]
        if '.gif' in link:
            continue
        if(i == 500):
            for root, _, files in os.walk(dir_name):
                for f in files:
                    fullpath = os.path.join(root, f)
                    if(os.path.getsize(fullpath) < 10 * 1024):
                        os.remove(fullpath)
                        print('removed ' + fullpath)
            print("~~~~~~~~~~~~~~~~~~CHANGED DIRECTORY~~~~~~~~~~~~~~~~~~~~~")
            dir_name = 'data/train/empty_images/'
        if(i == 2000):
            for root, _, files in os.walk(dir_name):
                for f in files:
                    fullpath = os.path.join(root, f)
                    if(os.path.getsize(fullpath) < 10 * 1024):
                        os.remove(fullpath)
                        print('removed ' + fullpath)
            exit()
        try:
            urllib.request.urlretrieve(link, dir_name+str(i)+".jpg")
            print("Downloading Image " + str(i))
            i += 1
        except Exception:
            print("Download Issue")
            
if __name__ == "__main__":
    main()

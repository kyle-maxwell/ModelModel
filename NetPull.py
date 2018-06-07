import urllib
import requests
import socket
import os
def main():
    # Uses links from ImageNet's links compilation file to download images.
    # Set dir_name accordingly. Chooses one image to download from every other 50 images.
    # This promotes a more diverse set of photos
    with open('fall11_urls.txt', errors='ignore') as links:
        raw_links = links.read().split()[1::2]
    i = 0
    dir_name = '../../shared/data/train/nobottle/ImageNet'
    socket.setdefaulttimeout(3)
    print(len(raw_links))
    
    for link in raw_links[::50]:
        if(i == 400):
            dir_name = '../../shared/data/ImageNetPool/ImageNet'
            for root, _, files in os.walk('../../shared/data/train/nobottle/'):
                for f in files:
                    fullpath = os.path.join(root, f)
                    if(os.path.getsize(fullpath) < 10 * 1024):
                        os.remove(fullpath)
                        print('removed ' + fullpath)
            print("~~~~~~~~~~~~~~~~~~CHANGED DIRECTORY~~~~~~~~~~~~~~~~~~~~~")
        if(i == 3400):
            for root, _, files in os.walk('../../shared/data/ImageNetPool/'):
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

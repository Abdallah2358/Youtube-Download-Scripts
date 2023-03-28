#!/usr/bin/env python3

# Usage -
# 1. open cmd
# 2. cd to the folder where these files are present
# 3. type - python ytdown.py
# the script will start working
# Credit to https://github.com/mohit23x/youtube-playlist-downloader

import os
from pytube import YouTube
import requests
import re
import string
from pytube.helpers import safe_filename

#imp functions


def foldertitle(url):

    try:
        res = requests.get(url)
    except:
        print('no internet')
        return False
    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]
    else:
        print('Incorrect attempt.')
        return False
    return cPL



def link_snatcher(url):
    our_links = []
    try:
        res = requests.get(url)
    except:
        print('no internet')
        return False

    plain_text = res.text

    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]
    else:
        print('Incorrect Playlist.')
        return False

    tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
    mat = re.findall(tmp_mat, plain_text)

    for m in mat:
        new_m = m.replace('&amp;', '&')
        work_m = 'https://youtube.com/' + new_m
        # print(work_m)
        if work_m not in our_links:
            our_links.append(work_m)

    return our_links


BASE_DIR = os.getcwd()

print('WELCOME TO PLAYLIST DOWNLOADER DEVELOPED BY - https://github.com/Abdallah2358/')
url = str(input("Please Enter PlayList URL\n"))
def choose_res() ->str:
    res_list = ['360p','720p']
    print('\nCHOOSE The Resolution of the Videos\n')
    for i in range(len(res_list)):
        print(str(i+1)+".",res_list[i])
    res_choice = int(input("Enter Resolution Number : "))-1
    return res_list[res_choice]
user_res = choose_res()

print('...You choosed ' + user_res + ' resolution\n.')

links = link_snatcher(url)

# print(our_links)

os.chdir(BASE_DIR)

new_folder_name = foldertitle(url)
print(new_folder_name[:7])

try:
    os.mkdir(new_folder_name[:7])
except:
    print('folder already exists')

os.chdir(new_folder_name[:7])
SAVEPATH = os.getcwd()
print(f'\n files will be saved to {SAVEPATH}')

x=[]
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        pathh = os.path.join(root, name)
        if os.path.getsize(pathh) < 1:
            os.remove(pathh)
        else:
            x.append(str(name))


print('\nconnecting . . .\n')


print()
# print("X= \n")
# print(x)
count = 1
while len(links)>0:
    prefix = '' 
    try:
        yt = YouTube(links[0])
        if not string[:1].isdigit():
            prefix = str(count)+"."
        main_title =prefix+ safe_filename(yt.title)
        main_title = main_title + '.mp4'

        
        print("Main Title "+main_title)
    except:
        print('connection problem..unable to fetch video info')
        print('Will try again')


    if main_title not in x:  
        if user_res == '360p' or user_res == '720p':
            vid = yt.streams.filter(progressive=True, file_extension='mp4', res=user_res).first()
            print('Downloading. . . ' + vid.default_filename + ' and its file size -> ' + str(round(vid.filesize / (1024 * 1024), 2)) + ' MB.')
            vid.download(SAVEPATH,vid.default_filename,prefix)
            print('Video Downloaded')
            count+=1
            links.pop(0)
        else:
            print('something is wrong..')
            print("Will try again")
    else:
        count+=1
        links.pop(0)
        print(f'\n skipping "{main_title}" video \n')    


print(' downloading finished')
print(f'\n all your videos are saved at --> {SAVEPATH}')
#!/usr/bin/env python3

from pytube import YouTube
from pytube.helpers import safe_filename
from winreg import OpenKey
from winreg import HKEY_CURRENT_USER
from winreg import QueryValueEx
def get_Downloads_path()->str:
    with OpenKey(HKEY_CURRENT_USER, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
        return QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]

def choose_res() ->str:
    res_list = ['360p','480p','720p']
    print('\nCHOOSE The Resolution of the Videos\n')
    for i in range(3):
        print(str(i+1)+".",res_list[i])
    res_choice = int(input("Enter Resolution Number : "))-1
    return res_list[res_choice]
    
chosenRes = choose_res()
link = input("Enter Video Link\n")
UserDwDefultDir =  get_Downloads_path()
dwDir = input(f"Choose Download Path Defaults to\"{UserDwDefultDir}\"\n")
if len(dwDir) == 0:
    dwDir =UserDwDefultDir
fName = input(f"Choose Vide Name optional\n")

try:
    yt = YouTube(link)
    vid = yt.streams.filter(progressive=True, file_extension='mp4', res=chosenRes).first()
    if len(fName) ==0:
        fName = vid.default_filename
    else:
        fName =safe_filename(fName)
    print('Downloading. . . ' + fName + ' and its file size -> ' + str(round(vid.filesize / (1024 * 1024), 2)) + ' MB.')
    vid.download(dwDir, fName  ,max_retries=10)
    print('Video Downloaded')
except :
    print('connection problem..unable to fetch video info')
    print('Will try again')

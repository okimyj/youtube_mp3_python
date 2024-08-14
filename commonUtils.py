import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
os.environ['PATH'] = os.environ['PATH'] + ";"+resource_path("ffmpeg")

import cv2
import ffmpeg
import subprocess

FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
def explore(path):
    # explorer would choke on forward slashes
    path = os.path.normpath(path)

    if os.path.isdir(path):
        subprocess.run([FILEBROWSER_PATH, path])
    elif os.path.isfile(path):
        subprocess.run([FILEBROWSER_PATH, '/select,', path])

def DownloadYoutubeFile(url, isOnlyAudio, saveDirectory):
    from pytube import YouTube
    print("DownloadYoutubeFile - " + str(url) + " isOnlyAudio : " + str(isOnlyAudio))
    
    yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
    downloadFolder = saveDirectory + "/" + yt.title
    savePath = ""
    try :
        if isOnlyAudio == True :
            savePath = yt.streams.filter(only_audio=isOnlyAudio, file_extension='mp4').first().download(downloadFolder)
            originPath = savePath
            savePath = savePath.replace('mp4', 'mp3')
            print("originPath : " + originPath + "\nsavePath : "+ savePath)
            #mp4에서 mp3로 변환
            ffmpeg.input(originPath).output(savePath).run(overwrite_output=True)
            #변환되기 전 mp4파일 삭제
            os.remove(originPath)
        else :
            savePath = yt.streams.filter(only_audio=isOnlyAudio, file_extension='mp4').get_highest_resolution().download(downloadFolder)
        print("DownloadYoutubeFile - success. " + savePath)
    except Exception as e:
        print(e)
    #stream = yt.streams.get_highest_resolution()
    #savePath = stream.download(downloadFolder)
    print("DownloadYoutubeFile - savePath : " + savePath)
    return savePath

def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
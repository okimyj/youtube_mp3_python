import sys
import os
import commonUtils
from pydub import AudioSegment
AudioSegment.ffmpeg = commonUtils.resource_path("ffmpeg\\ffmpeg.exe")

def capture():
    DOWNLOAD_FOLDER_BASE = "./AudioTest"
    print("start capture")
    url = "https://www.youtube.com/watch?v=3iM_06QeZi8"
    savePath = commonUtils.DownloadYoutubeFile(url, True, DOWNLOAD_FOLDER_BASE)
    
    audioFile = AudioSegment.from_mp3(savePath)
    duration_in_milliseconds = len(audioFile)

    splitMs = 20000
    splitDurationMs = 5000
    passedMs = 0
    count=0
    extract = audioFile[passedMs:passedMs+splitDurationMs]
    capturePath = "./AudioTest/Capture/"
    try:
        if not os.path.exists(capturePath):
            os.makedirs(capturePath)
    except OSError:
        print ('Error: Creating directory. ' +  capturePath, True)

    extract.export(capturePath + "split_%d.mp3"% count, format="mp3")
    while passedMs < duration_in_milliseconds :
        count+=1
        passedMs += splitMs
        if passedMs + splitDurationMs > duration_in_milliseconds :
            break
        extract = audioFile[passedMs:passedMs+splitDurationMs]
        extract.export(capturePath + "split_%d.mp3"% count, format="mp3")
    input("종료하려면 아무키")
    
    
capture()

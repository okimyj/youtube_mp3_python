# -*- coding: utf-8 -*-
#https://www.youtube.com/watch?v=3iM_06QeZi8
import os
import sys
import commonUtils
from pydub import AudioSegment
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton,QLineEdit, QTextBrowser, QCheckBox

AudioSegment.ffmpeg = commonUtils.resource_path("ffmpeg\\ffmpeg.exe")

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Youtube Audio Downloader")
        self.resize(700, 500)
        
        # setting layout
        settingLayout = QHBoxLayout()
        self.autoCapture = QCheckBox("Auto Capture", self)
        settingLayout.addWidget(self.autoCapture)

        # url layout
        urlLayout = QHBoxLayout()
        label_url = QLabel("Youtube URL or Local File Path : ", self)
        label_url.adjustSize()
        self.input_url = QLineEdit(self)
        self.input_url.setText("")
        self.input_url.resize(300, 30)
        btn_select = QPushButton("Select File", self)
        btn_select.clicked.connect(self.openAudioFile)
        btn_load = QPushButton("Down Load", self)
        btn_load.clicked.connect(self.loadAudio)
        
        urlLayout.addWidget(label_url)
        urlLayout.addWidget(self.input_url)
        urlLayout.addWidget(btn_load)
        urlLayout.addWidget(btn_select)

        saveLayout = QHBoxLayout()
        label_savePath = QLabel("Save Directory :")
        self.input_saveDir = QLineEdit(self)
        self.input_saveDir.setText("")
        self.input_saveDir.resize(300, 30)
        btn_saveDir = QPushButton("Select", self)
        btn_saveDir.clicked.connect(self.selectSaveDirectory)
        btn_openDir = QPushButton("Open", self)
        btn_openDir.clicked.connect(self.openSaveDirectory)
        saveLayout.addWidget(label_savePath)
        saveLayout.addWidget(self.input_saveDir)
        saveLayout.addWidget(btn_saveDir)
        saveLayout.addWidget(btn_openDir)
        
        
        # captureLayout
        captureWidget = QWidget(self)
        captureLayout = QHBoxLayout()
        captureWidget.setLayout(captureLayout)

        captureLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        label_capture = QLabel("추출 설정 : ", self)
        label_capture.adjustSize()
        label_capture.setFixedSize(label_capture.width(), label_capture.height())
        # 추출 간격
        self.input_sec = QLineEdit(self)
        self.input_sec.setText("5")
        self.input_sec.setFixedSize(30, 30)
        label_sec = QLabel("초 마다", self)
        label_sec.adjustSize()
        label_sec.setFixedSize(label_sec.width(), label_sec.height())
        #추출 길이
        self.input_captureDuration = QLineEdit(self)
        self.input_captureDuration.setText("5")
        self.input_captureDuration.setFixedSize(30, 30)
        label_sec2 = QLabel("초 추출합니다.", self)
        label_sec2.adjustSize()
        label_sec2.setFixedSize(label_sec2.width(), label_sec2.height())

        label_prefix = QLabel(" 파일 접두사 : ", self)
        label_prefix.adjustSize()
        label_prefix.setFixedSize(label_prefix.width(), label_prefix.height())
        self.input_prefix = QLineEdit(self)
        self.input_prefix.setText("capture_")

        btn_capture = QPushButton("Capture", self)
        btn_capture.clicked.connect(self.captureAudio)

        captureLayout.addWidget(label_capture)
        captureLayout.addWidget(self.input_sec)
        captureLayout.addWidget(label_sec)
        captureLayout.addWidget(self.input_captureDuration)
        captureLayout.addWidget(label_sec2)
        captureLayout.addWidget(label_prefix)
        captureLayout.addWidget(self.input_prefix)
        captureLayout.addWidget(btn_capture)
        
        # log print area
        self.logBrowser = QTextBrowser()
        self.logBrowser.setAcceptRichText(True)
        self.logBrowser.setOpenExternalLinks(True)
        btn_clearLog = QPushButton("Clear Log", self)
        btn_clearLog.clicked.connect(self.clearLog)

        label_okimyj = QLabel("by okimyj :D", self)
        label_okimyj.setAlignment(Qt.AlignmentFlag.AlignRight)

        wid = QWidget(self)
        self.setCentralWidget(wid)
        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignTop)
        mainLayout.addLayout(settingLayout)
        mainLayout.addLayout(urlLayout)
        mainLayout.addLayout(saveLayout)
        mainLayout.addWidget(captureWidget)
        mainLayout.addWidget(self.logBrowser)
        mainLayout.addWidget(btn_clearLog)
        mainLayout.addWidget(label_okimyj)
        
        wid.setLayout(mainLayout)
        
        #captureWidget.setHidden(True)

        self.show()
    
        
    def printLog(self, log, isError = False) :
        print(log)
        if isError == True :
            log = "<b style=\"color:red\">" + log + "</b>"
        self.logBrowser.append(log)

    def clearLog(self):
        self.logBrowser.clear()
    
    def openAudioFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Audio", QDir.currentPath())
        self.input_url.setText(fileName)
        if self.autoCapture.isChecked() :
                self.captureAudio()

    def loadAudio(self):
        url = self.input_url.text()
        if url is None or url == "" :
            self.printLog("error> is not youtube url", True)
        else:
            self.printLog("Start Youtube Audio DownLoad. Please wait...")
            saveDirectory = self.checkSaveDirectory()
            
            savePath = commonUtils.DownloadYoutubeFile(url, True, saveDirectory)
            self.input_url.setText(savePath)
            self.printLog("<b style = 'color:blue'>[download complete.]</b>")
            self.printLog("savePath : " + savePath)

            if self.autoCapture.isChecked() :
                self.captureAudio()
        

    def selectSaveDirectory(self):
        saveDirectory = QFileDialog.getExistingDirectory(self, "Select Directory", QDir.currentPath())
        self.setSaveDirectory(saveDirectory)
        return saveDirectory
    
    def openSaveDirectory(self):
        saveDirectory = self.input_saveDir.text()
        commonUtils.explore(saveDirectory)
    
    def checkSaveDirectory(self):
        saveDirectory = self.input_saveDir.text()
        if saveDirectory is None or saveDirectory == "" :
            saveDirectory = self.selectSaveDirectory()
        return saveDirectory
    
    def setSaveDirectory(self, path):
        self.input_saveDir.setText(path)

    def captureAudio(self) :
        self.printLog("captureAudio start - ")

        path = self.input_url.text()
        if path is None or path == "" :
            self.printLog("파일 경로가 없습니다.", True)
            return
        
        splitMs = int(self.input_sec.text()) * 1000
        splitDurationMs = int(self.input_captureDuration.text()) * 1000
        passedMs = 0
        count = 0
        
        print("splitMs : %d"% splitMs)
        print("splitDurationMs : %d"% splitDurationMs)
        
        capturePath = os.path.dirname(path) + "/capture"        
        
        try:
            if not os.path.exists(capturePath):
                os.makedirs(capturePath)
        except OSError:
            print ('Error: Creating directory. ' +  capturePath, True)
        
        audioFile = AudioSegment.from_mp3(path)
        duration_in_milliseconds = len(audioFile)
        fileNamePrefix = self.input_prefix.text()
        while passedMs < duration_in_milliseconds :
            count+=1
            if passedMs + splitDurationMs > duration_in_milliseconds :
                break
            extract = audioFile[passedMs:passedMs+splitDurationMs]
            extract.export(capturePath + "/" + fileNamePrefix + "%d.mp3"% count, format="mp3")
            self.printLog("capture audio : " + capturePath + "/" + fileNamePrefix + "%d.mp3"% count)

            passedMs += splitMs
        self.printLog("<b style = 'color:blue'>Audio Capture Finished</b>")
        

if __name__ == "__main__": 
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())





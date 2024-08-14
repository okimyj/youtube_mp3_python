# -*- coding: utf-8 -*-
#https://www.youtube.com/watch?v=3iM_06QeZi8
import os
import sys
import cv2
import commonUtils
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton,QLineEdit, QTextBrowser, QCheckBox


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Youtube Video Downloader")
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
        btn_select.clicked.connect(self.openVideoFile)
        btn_load = QPushButton("Down Load", self)
        btn_load.clicked.connect(self.loadVideo)
        
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
        label_capture = QLabel("초 단위로 캡쳐하기 : ", self)
        label_capture.adjustSize()
        label_capture.setFixedSize(label_capture.width(), label_capture.height())
        # 캡쳐 간격
        self.input_sec = QLineEdit(self)
        self.input_sec.setText("5")
        self.input_sec.setFixedSize(30, 30)
        label_sec = QLabel("초", self)
        label_sec.adjustSize()
        label_sec.setFixedSize(label_sec.width(), label_sec.height())

        label_prefix = QLabel(" 파일 접두사 : ", self)
        label_prefix.adjustSize()
        label_prefix.setFixedSize(label_prefix.width(), label_prefix.height())
        self.input_prefix = QLineEdit(self)
        self.input_prefix.setText("capture_")

        btn_capture = QPushButton("Capture", self)
        btn_capture.clicked.connect(self.captureVideo)
        captureLayout.addWidget(label_capture)
        captureLayout.addWidget(self.input_sec)
        captureLayout.addWidget(label_sec)
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
    
    def openVideoFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Video", QDir.currentPath())
        self.input_url.setText(fileName)
        if self.autoCapture.isChecked() :
                self.captureVideo()

    def loadVideo(self):
        url = self.input_url.text()
        if url is None or url == "" :
            self.printLog("error> is not youtube url", True)
        else:
            self.printLog("Start Youtube Video DownLoad. Please wait...")
            saveDirectory = self.checkSaveDirectory()
            
            savePath = commonUtils.DownloadYoutubeFile(url, False, saveDirectory)
            self.input_url.setText(savePath)
            self.printLog("<b style = 'color:blue'>[download complete.]</b>")
            self.printLog("savePath : " + savePath)

            if self.autoCapture.isChecked() :
                self.captureVideo()
        

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

    def captureVideo(self) :
        path = self.input_url.text()
        splitSecond = int(self.input_sec.text())
        if path is None or path == "" :
            self.printLog("파일 경로가 없습니다.", True)
            return
        videoCapture = cv2.VideoCapture(path)
        if not videoCapture.isOpened() : 
            self.printLog("error> 파일을 열 수 없습니다." + str(path) , True)
            return
        # 불러온 비디오 파일의 정보 출력
        length = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = videoCapture.get(cv2.CAP_PROP_FPS)
        duration = length/fps
        self.printLog("[[-- video Info --]]")
        self.printLog("length : %f"% length)
        self.printLog("width : %f"% width)
        self.printLog("height :%f"% height)
        self.printLog("fps : %f"% fps)
        self.printLog("duration : %f"% duration)
        self.printLog("---------------------")
        passedSecond = 0   # 지나간 초. 
        count = 0               # 캡쳐 횟수 
        
        capturePath = os.path.dirname(path) + "/capture"

        #프레임을 저장할 디렉토리를 생성
        try:
            if not os.path.exists(capturePath):
                os.makedirs(capturePath)
        except OSError:
            self.printLog ('Error: Creating directory. ' +  capturePath, True)

        videoCapture.set(cv2.CAP_PROP_POS_MSEC, passedSecond * 1000)
        success, image = videoCapture.read()
        fileNamePrefix = self.input_prefix.text()
        while success and passedSecond < duration :
            count += 1
            passedSecond += splitSecond
            #print("이번 캡쳐할 시간대는", passedSecond, "초")
            videoCapture.set(cv2.CAP_PROP_POS_MSEC, passedSecond * 1000)
            success, image = videoCapture.read()
            if(passedSecond > duration) :
                break
            saveSuccess = commonUtils.imwrite(capturePath + "/"+fileNamePrefix+"%d.jpg" % count, image)
            if(saveSuccess) :
                self.printLog("saveImage " + capturePath + "/"+fileNamePrefix+"%d.jpg" % count)
            else :
                self.printLog("save failed.", True)

        videoCapture.release()
        self.printLog("<b style = 'color:blue'>video Capture Finished</b>")


if __name__ == "__main__": 
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())





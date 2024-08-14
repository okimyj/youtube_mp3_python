import os
from PIL import Image

# -*- coding: utf-8 -*-
#https://www.youtube.com/watch?v=3iM_06QeZi8
import os
import sys
import cv2
import commonUtils
from pydub import AudioSegment
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton,QLineEdit, QTextBrowser, QCheckBox

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
        label_url = QLabel("Target Image Path : ", self)
        label_url.adjustSize()
        self.input_targetImage = QLineEdit(self)
        self.input_targetImage.setText("")
        self.input_targetImage.resize(300, 30)
        btn_select = QPushButton("Select", self)
        btn_select.clicked.connect(self.selectTargetImage)
                
        urlLayout.addWidget(label_url)
        urlLayout.addWidget(self.input_targetImage)
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

        label_desc = QLabel("가로 crop 개수 : ", self)
        label_desc.adjustSize()
        label_desc.setFixedSize(label_desc.width(), label_desc.height())

        self.input_cropNumX = QLineEdit(self)
        self.input_cropNumX.setText("2")
        self.input_cropNumX.setFixedSize(30, 30)
        
        label_desc2 = QLabel("세로 crop 개수 : ", self)
        label_desc2.adjustSize()
        label_desc2.setFixedSize(label_desc2.width(), label_desc2.height())

        self.input_cropNumY = QLineEdit(self)
        self.input_cropNumY.setText("2")
        self.input_cropNumY.setFixedSize(30, 30)
        
        label_prefix = QLabel(" 파일 접두사 : ", self)
        label_prefix.adjustSize()
        label_prefix.setFixedSize(label_prefix.width(), label_prefix.height())
        self.input_prefix = QLineEdit(self)
        self.input_prefix.setText("crop_")
        
        btn_crop = QPushButton("Crop", self)
        btn_crop.clicked.connect(self.cropImage)
        captureLayout.addWidget(label_capture)
        captureLayout.addWidget(label_desc)
        captureLayout.addWidget(self.input_cropNumX)
        captureLayout.addWidget(label_desc2)
        captureLayout.addWidget(self.input_cropNumY)
        
        captureLayout.addWidget(label_prefix)
        captureLayout.addWidget(self.input_prefix)
        captureLayout.addWidget(btn_crop)
        
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
    
    def selectTargetImage(self):
        fname = QFileDialog.getOpenFileName(self, "Select Target Image", QDir.currentPath())
        self.input_targetImage.setText(fname[0])

    def selectSaveDirectory(self):
        saveDirectory = QFileDialog.getExistingDirectory(self, "Select Save Directory", QDir.currentPath())
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

    def cropImage(self):
        targetFilePath = self.input_targetImage.text()
        saveDir = self.checkSaveDirectory()
        cropNumX = int(self.input_cropNumX.text())
        cropNumY = int(self.input_cropNumY.text())
        
        try:
            if not os.path.exists(saveDir):
                os.makedirs(saveDir)
        except OSError:
            print ('Error: Creating directory. ' +  saveDir, True)
        
        img = Image.open(targetFilePath)
        (img_h, img_w) = img.size
        print(img.size)
    
        # crop 할 사이즈 : grid_w, grid_h
        grid_w = img_w/cropNumX # crop width
        grid_h = img_h/cropNumY # crop height
        range_w = (int)(img_w/grid_w)
        range_h = (int)(img_h/grid_h)
        print(range_w, range_h)
    
        count = 0
        fileNamePrefix = self.input_prefix.text()
        for w in range(range_w):
            for h in range(range_h):
                count += 1
                bbox = (h*grid_h, w*grid_w, (h+1)*(grid_h), (w+1)*(grid_w))
                print(h*grid_h, w*grid_w, (h+1)*(grid_h), (w+1)*(grid_w))
                # 가로 세로 시작, 가로 세로 끝
                crop_img = img.crop(bbox)
                
                #fname = fileNamePrefix + "{}.jpg".format("{0:05d}".format(i))
                fname = fileNamePrefix+"%d.jpg" % count
                savename = saveDir + "/" + fname
                if os.path.isfile(savename) :
                    os.remove(savename)
                crop_img.save(savename)
                self.printLog('save file ' + savename + '....')
                
        self.printLog("<b style = 'color:blue'>Image Crop Finished.</b>")


if __name__ == "__main__": 
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())



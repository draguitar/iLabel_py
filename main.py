import argparse
import sys, os, subprocess
from PySide6.QtCore import QSize,QPoint
from PySide6.QtWidgets import ( QApplication, QWidget, 
             QVBoxLayout, QHBoxLayout, QPushButton,QFrame,QMessageBox,QDialog
)
from ui import ClassifyImgLabel, InfoPanel, ClassifyActivityBtns
from models import WorkFolder
from models import winH, winW, imgH, imgW, strbtnstylesys

def get_parser():
    parser = argparse.ArgumentParser(description="輸入標記圖片路徑")
    parser.add_argument('-d','--dir', required=True, type=str, help='Image folder path')
    return parser.parse_args()


class MainWindow(QWidget):
    def __init__(self, workFolder: WorkFolder, width, height):
        super().__init__()
        self.setMaximumSize(QSize(width, height))
        self.workFolder=workFolder
        layout=QHBoxLayout()
        panelsLayout=QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle(str(workFolder))
        if imgH>height*0.9 or imgW>width*0.8:
            wgtW=int(width*0.8)
            wgtH=int(height*0.9)
        else:
            wgtW, wgtH= imgW, imgH
        self.imgLabel=ClassifyImgLabel(workFolder, wgtW, wgtH, self)
        self.imgLabel.setFixedSize(QSize(wgtW, wgtH))
        self.activityPanel=ClassifyActivityBtns(workFolder,self)
        self.infoPanel=InfoPanel(workFolder,self)
        layout.addWidget(self.imgLabel)
        layout.addLayout(panelsLayout)
        panelsLayout.addWidget(self.infoPanel)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        
        panelsLayout.addWidget(line)
        panelsLayout.addWidget(self.activityPanel)
        openBtn = QPushButton('Open Work Folder')
        panelsLayout.addWidget(openBtn)
        openBtn.setStyleSheet(strbtnstylesys)
        openBtn.clicked.connect(self.openDir)
        
        exitBtn=QPushButton('Exit')
        panelsLayout.addWidget(exitBtn)
        exitBtn.setStyleSheet(strbtnstylesys)
        exitBtn.clicked.connect(app.exit)
    
    def openDir(self):
        if sys.platform.startswith('win'):
            os.startfile(str(self.workFolder))
        elif sys.platform.startswith('darwin'):
            subprocess.call(["open", str(self.workFolder)])
        elif sys.platform.startswith('linux'):
            subprocess.call(["xdg-open", str(self.workFolder)])
        
if __name__ == "__main__":
    app = QApplication([])
    args = get_parser()
    wf=WorkFolder(args.dir)
    if wf:
        screenRect = QApplication.instance().screens()[0].availableSize()
        screenW, screenH= screenRect.width(), screenRect.height()
        
        print('screenW, screenH= ', screenW, screenH)
        #當 config.ini 視窗設定winW,winH大小大於螢幕可用尺寸時, 降低為螢幕可用尺寸
        if winH < screenH and winW < screenW:
            screenW, screenH=winW, winH

        win=MainWindow(wf, screenW, screenH)
        win.show()
        win.move(QPoint(0,0))
        

        
        msg = QMessageBox()
        msg.styleSheet()
        msg.setText("""
        power by Longer_lung
        # 64639
        """)
        msg.setStyleSheet("")
        # msg.windowTitle("Title")
        msg.show()
        
        
        app.exec()
    else:
        print("""Please select a Directory containing at least one image to be labled!""")
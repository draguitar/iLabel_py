from PySide6.QtWidgets import (QWidget, QButtonGroup,
            QLabel, QVBoxLayout, QPushButton, QLineEdit,QFrame)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
from models import WorkFolder
from models import classes,strlblstyle,infostyle

FONT_STYLE_1 = QFont('Microsoft JhengHei', 8)

class ClassifyImgLabel(QLabel):
    def __init__(self, workFolder: WorkFolder, width, height, parent=None):
        super().__init__(parent)
        self.width, self.height = width, height
        self.setStyleSheet("border: 1px inset grey;")
        self.setAlignment(Qt.AlignCenter)
        self.workFolder=workFolder
        self.refreshImg()

    def refreshImg(self):
        imgPath=self.workFolder.getCurrentImg()
        if imgPath:
            pix=QPixmap()
            pix.load(imgPath)
            if pix.width()>self.width or pix.height()>self.height:
                pix=pix.scaled(self.width, self.height, Qt.KeepAspectRatio)
            self.setPixmap(pix)
        else:
            self.setFont(QFont('Microsoft JhengHei', 14))
            self.setText(f"""
            資料夾【{str(self.workFolder)}】
            圖片已標記完成
            '點擊Exit離開' 
    """)

class ClassifyActivityBtns(QFrame):
    def __init__(self, workFolder: WorkFolder, parent=None):
        super().__init__(parent)
        layout=QVBoxLayout()
        self.setLayout(layout)
        self.parent=parent
        self.workFolder=workFolder
        self.buttonRoll = QPushButton('返回前一張(back')
        self.buttonRoll.setShortcut('b')
        self.buttonRoll.clicked.connect(self.rollback)
        self.buttonRoll.setDisabled(True)
        layout.addWidget(self.buttonRoll)
        
        self.cls_group = QButtonGroup()
        self.keys=[]
        id=0
        for key,cl in classes.items():
            self.keys.append(key)
            classifiedBtn = QPushButton(cl+" ("+key)
            classifiedBtn.setShortcut(key)
            layout.addWidget(classifiedBtn)
            self.cls_group.addButton(classifiedBtn, id)
            id +=1            
        self.cls_group.buttonClicked.connect(self.classifiedTo)
        self.checkCurrentImg()
    
    def classifiedTo(self, object):
        clsId=self.cls_group.id(object)
        self.workFolder.labelCurrentImg(self.keys[clsId])
        self.parent.imgLabel.refreshImg()
        self.parent.infoPanel.refreshPanel()
        self.buttonRoll.setDisabled(False)
        self.checkCurrentImg()

    def checkCurrentImg(self):
        if self.workFolder.getCurrentImg():
            self._enableClassify()
        else:
            self._disableClassify()

    def _disableClassify(self):
        for b in self.cls_group.buttons():
            b.setDisabled(True)

    def _enableClassify(self):
        for b in self.cls_group.buttons():
            b.setDisabled(False)

    def rollback(self):
        try:
            self.workFolder.rollback()
            self.parent.imgLabel.refreshImg()
            self.parent.infoPanel.refreshPanel()
        except:
            print('No Classification History to rollback')

        if len(self.workFolder.history)==0:    
            self.buttonRoll.setDisabled(True)
        self._enableClassify()

class InfoPanel(QWidget):
    def __init__(self, workFolder: WorkFolder, parent=None):
        super().__init__()
        layout=QVBoxLayout()
        self.setLayout(layout)
        self.parent=parent
        self.workFolder=workFolder
        self.setFont(QFont('Microsoft JhengHei', 12))
        
        infoLabel=QLabel("▉▉▉ Longer_Lung#64639 ▉▉▉")
        infoLabel.setStyleSheet(infostyle)
        layout.addWidget(infoLabel)
    
        currentLabel=QLabel('Current Img:')
        self.current=QLineEdit('-')
        self.current.setReadOnly(True)
        self.imgSize=QLabel('-')
        historyLabel=QLabel('Label History:')
        self.history=QLabel('-')
        remainsLabel=QLabel('Remain Imgs:')
        self.remains=QLabel('-')
        labeledLabel=QLabel('Total Labeled Imgs:')
        self.labeled=QLabel('-')
        remainsLabel.setStyleSheet(strlblstyle)
        labeledLabel.setStyleSheet(strlblstyle)
        currentLabel.setStyleSheet(strlblstyle)
        historyLabel.setStyleSheet(strlblstyle)
        layout.addWidget(currentLabel)
        layout.addWidget(self.current)
        layout.addWidget(self.imgSize)
        layout.addWidget(historyLabel)
        layout.addWidget(self.history)
        layout.addWidget(remainsLabel)
        layout.addWidget(self.remains)
        layout.addWidget(labeledLabel)
        layout.addWidget(self.labeled)
        self.refreshPanel()
    
    def refreshPanel(self):
        self.current.setText(self.workFolder.getCurrentName())
        self.current.setFont(FONT_STYLE_1)
        self.imgSize.setText(self.workFolder.getCurrentSize())
        self.imgSize.setFont(FONT_STYLE_1)
        self.history.setText(str(len(self.workFolder.history)))
        self.history.setFont(FONT_STYLE_1)
        self.remains.setText(str(len(self.workFolder.remains)))
        self.remains.setFont(FONT_STYLE_1)
        self.labeled.setText(self.workFolder.getLabeledCountStr())
        self.labeled.setFont(FONT_STYLE_1)
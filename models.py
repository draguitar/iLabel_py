from PIL import Image
from pathlib import Path, _windows_flavour, _posix_flavour
import os
from configparser import ConfigParser

"""
configuration
----------------------------------------------------------------
讀取config.ini 

"""
config = ConfigParser()
config.read('config.ini',encoding='utf-8')
classes = dict(config.items('class'))
strlblstyle=config['main']['strlblstyle']
strbtnstylesys=config['main']['strbtnstylesys']
infostyle=config['main']['infostyle']
imgH=int(config['main']['imgh'])
imgW=int(config['main']['imgw'])
winW=int(config['main']['winw'])
winH=int(config['main']['winh'])

class WorkFolder(Path):
    """
    擴展 Path 藉由搬移圖片檔到對應的子目錄來進行分類, 分類類別必須記錄在執行目錄下 config.ini 的 [class] 下
    範例:
    [class]
    1 = 迪麗熱巴	
    2 = Angelababy
    
    Attributes
    ----------
    fullPath : str
        包含圖片的路徑目錄
    self.history : []
        已經標完的圖片歷史紀錄, 主要給rollback 用

    Methods
    -------
    getCurrentImg()
        現在正要標示的圖片檔案全路徑字串
    labelCurrentImg(classId)
        將 current Img 標示為 代號為classId的類別 (亦即移動到 classId 子目錄)
    rollback()
        將上一個誤分類圖片回復 (移回上一層目錄). 歷史紀錄亦移除此紀錄後 設為_current.

    """
    _flavour = _windows_flavour if os.name == 'nt' else _posix_flavour

    def __new__(cls, fullPath: str):
        tmp=super(WorkFolder, cls).__new__(cls, fullPath)
        return tmp if tmp.is_dir() else None
        
    def __init__(self, fullPath: str):
        self.classIds = list(classes.keys())
        self.remains = [child for child in self.iterdir() if \
                    (child.is_file() and child.suffix.lower() in ['.png','.jpeg','.jpg'])]
        
        if len(self.remains) > 0:
            for c in self.classIds:
                os.makedirs(self.joinpath(c), exist_ok=True)
            self.history = []
            self._current = self.remains.pop()
        else:
            self.history = []
            self._current = None
    
    def getCurrentImg(self) -> str:
        return str(self._current) if self._current else None
    
    def getCurrentSize(self):
        try:
            return str(Image.open(self._current).size)
        except:
            return '-'

    def labelCurrentImg(self, classId: str):
        targetDir = self._current.parent.joinpath(classId, self._current.name)
        self._current.rename(targetDir)
        self.history.append(targetDir)
        if len(self.remains) > 0:
            self._current = self.remains.pop()
        else:
            self._current = None

    def getCurrentName(self) -> str:
        return self._current.name if self._current else None

    def getLabeledCountStr(self) -> str:
        result=''
        subDirs=[path for path, _, _ in os.walk(self)][1:]
        for p in subDirs:
            cnt=len([name for name in os.listdir(p) if os.path.isfile(os.path.join(p,name))])
            result=result+  f"● 數量:[{str(cnt)}] {classes[Path(p).name]} ({Path(p).name}\n"
        return result
            
    def rollback(self):
        if len(self.history) > 0:
            self.remains.append(self._current)
            tmp = self.history.pop()
            targetDir = tmp.parents[1].joinpath(tmp.name)
            tmp.rename(targetDir)
            self._current = targetDir
        else:
            raise IndexError("Can not rollback empty labeling history!")

if __name__ == "__main__":
    wf=WorkFolder(r'.\dataset')

    if wf:
        print(len(wf.remains),wf._current)
        print(wf.getLabeledCountStr())

    else:
        print('None work')
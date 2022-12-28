一個協助用戶快速進行圖像分類標示的小工具.

第一次嘗試使用 github, 非典型使用方式.
相關說明暫時放置於 https://www.zoominonline.com/dev
未來補加程式文件, 單元測試後會持續更新.
```
git clone https://github.com/draguitar/iLabel_py.git
cd iLabel_py
```

使用前必須先修訂 config.ini 檔案 [class] 段落裡的關於快速鍵與類別的名稱對應關係.

簡易使用: 於 Python 3.9
```
pip install pyside6 Pillow
```
假設要做標示的所有圖像檔都放置於 C:\YOUR IMAGES 目錄下
```
python main.py -d [dataset_path]
```

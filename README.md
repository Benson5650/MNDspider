# 全民國防有獎徵答系統自動化動態爬蟲

## 免責聲明
本專案僅供學術研究練習使用，請勿用於任何商業用途。

使用者需合理設置間格時間，以免造成破壞。

## 專案簡介
本專案旨在開發一個自動化動態爬蟲系統，用於自動回答全民國防有將徵答系統的題目。該系統將自動從提庫中抓取題目並提交答案，從而提高答題效率。

## 功能特點
- 自動抓取全民國防有將徵答系統的題目
- 自動提交答案
- 支援動態網頁爬取
- 自動填入驗證碼

## 使用說明
1. 每個身分證需要自行完成一次答題爾後才能使用自動程式
2. 題庫會存於q.json
3. 使用者需將自己的身分證填入user_id.json
```json
{
	"your id": "已回答次數(預設為0)",
	"more id": "已回答次數(預設為0)"
}
```
4. 於程式開始時設定每次答題間格時間
(建議為 30/"n of id")
 
## 安裝與使用
需要google chrome瀏覽器
### (i)使用python環境
1. 需要Python 3.x (建議使用3.10/3.11)
pip 第三方庫:
selenium
matplotlib
ddddocr
2. 將身分證填入user_id.json
3. 確保.py與user_id.json q.json chromedriver.exe在同一目錄下
4. 編譯.py檔案
5. 如果需要使用pyinstaller打包成exe請直接選擇Pythonapplication4.spec
```
pyinstaller Pythonapplication4.spec
```
6. 見下文


### (ii)直接使用.exe
1. 僅支援windows 64位元
2. 將身分證填入user_id.json
3. 確保.py與user_id.json q.json chromedriver.exe在同一目錄下
    
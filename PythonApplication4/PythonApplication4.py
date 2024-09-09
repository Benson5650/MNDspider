from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import ddddocr
import time
import base64
import json
import io
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
ocr = ddddocr.DdddOcr()

def write_in_jason(qu_ls,j):
    q_dict[qu_ls[1]]=qu_ls[j+1][3:]
    with open("q.json",'w') as file:
        json.dump(q_dict,file)
    
def answer_a_question_with_answer(ls):
    print("開始回答有答案的題目")
    ans=q_dict[ls[1]]
    print("應選",ans)
    for k in range(2,8):
        print("迴圈檢測")
        if(ans==ls[k][3:]):
            num=k-1
            print("選擇第",k-1,"'個選項[]",ls[k],"[]")
            driver.find_element(By.ID,"Ans"+str(num)).click()
            break
    try:
        driver.find_element(By.ID,"imgBack2").click()
        return 1
    except:
        try:
            driver.find_element(By.ID,"PID")
            print("這裡難道是世界的近頭")
            return 1
        except:
            print("\033[31m回答有答案之問題是出錯\033[0m")
            time.sleep(1000)
            return 0
        
def answer_a_question_without_answer(ls):
    print("開始回答無答案的題目")
    for i in range(1,7):
        try:
            print("開始顯式等待")
            WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID,'Ans'+str(i))))
            driver.find_element(By.ID,'Ans'+str(i)).click()
            print("按下第",i,"個答案")
        except:
          print("\033[31m按不下去 告辭\033[0m")
          return 0  
        try:#try except
            driver.find_element(By.ID,'imgBack').click()        
            print("\033[31m答錯了 回到上一部\033[0m")
        except:
            try:     
                driver.find_element(By.ID,'imgBack2').click()
                print("下一題")
                write_in_jason(ls,i)
                return 1;
            except:
                try:
                    driver.find_element(By.ID,"PID")
                    print("這裡難道是世界的近頭")
                    return 1
                except:
                    print("\033[31m回答無答案問題時無法返回\033[0m")
                    return 0
        
def start_answering(user_id):
    print("進入網頁")
    driver.get("https://game.mnd.gov.tw/")
    print("載入完成")
    try:
        print("開始顯式等待")
        WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME,'pulse')))
        driver.find_element(By.CLASS_NAME,'pulse').click()
        print("開始答題")#按按鈕1
    except:
        print("\033[31m無法開始答題\033[0m")
        return 0
    try:
        print("開始顯式等待")
        WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME,'pulse')))
        driver.find_element(By.CLASS_NAME,'pulse').click()
        print("開始答題2")#按按鈕2
    except:
        print("\033[31m無法開始答題2\033[0m")
        return 0
    
    print("回答",user_id,"號的")
    for i in range(9):
        print("開始答第",i+1,"題")
        try:
            print("開始顯式等待")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME,'card-body')))
            q_for_this_q=driver.find_element(By.CLASS_NAME,'card-body').text
            print("題目是\033[32m",q_for_this_q,"\033[0m")
        except:
           print("\033[31m無法獲取題目\033[0m")
           return 0
        q_list_in_q=q_for_this_q.split("\n")
        print("輸出分割字串\n\033[32m",q_list_in_q,"\033[0m")
        if q_list_in_q[1] in q_dict:#有答案
            if(answer_a_question_with_answer(q_list_in_q)==0):
                print("\033[31m無法回答有答案之問題\033[0m")
                return 0
            else:
                print("回答成功")
        else:
            print("無答案")
            if(answer_a_question_without_answer(q_list_in_q)==0):
                print("\033[31m無法回答無答案之問題\033[0m")
                return 0
            else:
                print("回答成功")
    print("\033[33m成功回答",user_id,"的問題\033[0m")
    
    #加入輸入驗證碼
    
    captcha_status = 0
    while(captcha_status == 0):
        get_image()
        time.sleep(1)
        enter_data(user_id)
        time.sleep(0.5)
        
        try:
            alert = driver.switch_to.alert
            print("你媽媽跟你說:",alert.text)
            alert.accept()
            captcha_status = 0
        except:
            captcha_status = 1
            print("captcha send")
    return 1

def get_image():
    captchaBase64 = driver.execute_async_script("""
        var canvas = document.createElement('canvas');
        var context = canvas.getContext('2d');
        var img = document.querySelector('#CAPTCHAImage');; 
        canvas.height = img.naturalHeight;
        canvas.width = img.naturalWidth;
        context.drawImage(img, 0, 0);

        callback = arguments[arguments.length - 1];
        callback(canvas.toDataURL());
        """)

    i = base64.b64decode(captchaBase64.split(',')[1])
    i = io.BytesIO(i)

    i = mpimg.imread(i,format='PNG')
    
    print("test")
    
    plt.imsave('test.png', i)
   
def enter_data(idd):
    with open('test.png', 'rb') as f:
        captcha = f.read()
    result = ocr.classification(captcha)
    print("result:",result)
    driver.find_element(By.XPATH,'//*[@id="txtValidateCode"]').clear()
    driver.find_element(By.XPATH,'//*[@id="txtValidateCode"]').send_keys(result)
    driver.find_element(By.XPATH,'//*[@id="PID"]').send_keys(idd)
    driver.find_element(By.ID,"ImgBtn").click()
    



t = input("輸入等待時間")
driver = webdriver.Chrome()
print("開啟瀏覽器")
with open('q.json', 'r') as file:
    q_dict= json.load(file)
with open('user_id.json', 'r') as file:
    id_list= json.load(file)
print(q_dict)
print(id_list)

while(1):
    for ID in id_list:
        time.sleep(int(t))
        if(start_answering(ID)==1):
            id_list[ID]=id_list[ID]+1
            time.sleep(1000)
            with open("user_id.json",'w') as file:
                json.dump(id_list,file)


from selenium.webdriver.chrome.options import Options
import requests
import random
import pandas as pd
import json
import mysql.connector
from fake_useragent import UserAgent


# 阻擋通知
options = Options()
# options.add_argument("-disable-notifications") 

# pref 禁用瀏覽器彈出視窗
prefs = {"profile.default_content_setting_values.notifications":2}
options.add_experimental_option("prefs",prefs)

#pandas read csv
proxyIP = pd.read_csv("../py-proxy/proxyIP.csv")
proxyIPs = proxyIP['proxyIP']


# 透過隨機代理IP，反爬蟲，並且使用隨機使用者代理(User-Agent)反爬蟲
# 用try...except去防止異常值
# 使用ajax非同步爬蟲
# 計算總共有幾個頁面、計算每個頁面的二手車數量
# 將抓到的json資料轉乘python
# 分析要抓哪些資料，並存到csv

try:
    
    proxy_ip0 = random.choice(proxyIPs)
    print(proxy_ip0)
    user_agent = UserAgent()
    valid_data = []
    
    for page in range(1,17):
        #頁碼使用GET的方式，變換page參數的值時，就可以前往對應的頁碼網頁。
        url = "https://auto.8891.com.tw/usedauto-newSearch.html?b=27&series=A&page={}&device_id=a012337c-06e9-419a-9f67-b99c60056ea1".format(page)


        headers = {
            "Content-Type" : "application/json",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "user-agent":user_agent.random # 隨機user-agent
        }

        response = requests.get(url,headers=headers,timeout=5)
        # print(response.text)
            
        data = json.loads(response.text)
        Total = data['data']['total']
        carlist = data['data']['data']
        # print(page)
        N = len(carlist) # 每頁的二手車的數量
        print(N)
        # i = 0 
        for i in range(0,N-1):
            
            id0 = carlist[i]['id']
            title = carlist[i]['title']
            brand = carlist[i]['auto_brand_en']
            address = carlist[i]['auto_address']
            price = carlist[i]['auto_price']
            renew = carlist[i]['item_renew_date'] #更新頻率
            show = carlist[i]['item_show_num'] # 瀏覽次數
            # print(address,price,renew,show)
            # 使用append將將需要的資料透過List方式收集到valid_data
            valid_data.append([page,i,title,brand,address,price,renew,show])
    #確認是否將每一筆資料都疊加        
    # print(valid_data) 
    second_car_df = pd.DataFrame(valid_data,columns=["頁數","序號",'標題','品牌','地址','價格(萬)','更新頻率','瀏覽次數'])
    second_car_df.to_csv("secondhand_car.csv",encoding='utf-8-sig')
    s = pd.read_csv("secondhand_car.csv")
    print(s)
except:
    print("scrapy wrong",response.status_code)




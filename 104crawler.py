import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import csv

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword=%E6%95%B8%E6%93%9A%E5%B7%A5%E7%A8%8B%E5%B8%AB&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc'
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
jobs = soup.find_all('article',class_='js-job-item') 

fn='104人力銀行職缺內容.csv'                                             
columns_name=['職位名稱','公司名稱','網址','所需技能']                     
with open(fn,'w',newline='',) as csvFile:                                   
    dictWriter = csv.DictWriter(csvFile,fieldnames=columns_name)            
    dictWriter.writeheader()

    for job in jobs:
        jobtitle = job.find('a',class_="js-job-link").text              #職位名稱
        company = job.get('data-cust-name')                             #公司名稱
        link = 'https:' + job.find('a').get('href')                     #網址
        print(job.find('a',class_="js-job-link").text)                  #職缺內容
        print(job.get('data-cust-name'))                                #公司名稱
        print(link)                                                     #網址
 
        link = 'https:' + job.find('a').get('href')
        link1 = link.split('?')[0]
        link2 = link1.split('/')[-1]
    
        url1='https://www.104.com.tw/job/ajax/content/' + link2
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'referer' : link}
    
        res = requests.get(url = url1, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        json_data = json.loads(res.text)
        datalist = json_data['data']['condition']['specialty']
        tempList = json_data['data']['condition']['specialty']
        len_list = len(json_data['data']['condition']['specialty'])
    
        for x in range(len_list):
            tools = datalist[x]['description']                  #所需技能
            print(tools)
        
        dictWriter.writerow({'職位名稱':jobtitle,'公司名稱':company,
                            '網址':link,'所需技能':tools})

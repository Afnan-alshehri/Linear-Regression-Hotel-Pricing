from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import os 
from selenium.webdriver.chrome.service import Service
import time
import csv

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = Service(os.path.join(PROJECT_ROOT, "chromedriver"))


driver = webdriver.Chrome(service=DRIVER_BIN)
driver.get("https://www.agoda.com/search?city=14524&locale=en-us&ckuid=27aa9619-e018-45c4-bf84-4fe339663aab&prid=0&currency=USD&correlationId=3dbb0f8f-339a-4dc1-a5cb-0c8dd2692b03&pageTypeId=103&realLanguageId=1&languageId=1&origin=EG&cid=1887945&userId=27aa9619-e018-45c4-bf84-4fe339663aab&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=7&currencyCode=USD&htmlLanguage=en-us&cultureInfoName=en-us&machineName=am-crweb-4008&trafficGroupId=2&sessionId=fqg5xsex5tbsd30iwcpfkyuf&trafficSubGroupId=111&aid=271356&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&checkIn=2021-12-09&checkOut=2022-01-31&rooms=1&adults=1&children=0&priceCur=USD&los=53&textToSearch=Kuala%20Lumpur&travellerType=0&familyMode=off")

with open('rooms.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['name','price','type','bedroom_count','bed_count','review_count'])
    count = 1

    for i in range(26):
        print('Scrolling')
        for i in range(1,7):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)

        time.sleep(4)

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        rooms = soup.find_all('li', attrs={'class':'PropertyCardItem'})
        for room in rooms:
            try:
                room_name = room.find_all('h3')[0].text 
            except:
                room_name = None
                

            try:
                price = room.find_all('span','PropertyCardPrice__Value')[0].text
            except:
                price = None

            try:
                room_type = room.find_all('span','Spanstyled__SpanStyled-sc-16tp9kb-0')[0].text
            except:
                room_type = None

            try:
                bedroom_count = (room.find_all('span','Spanstyled__SpanStyled-sc-16tp9kb-0')[2].text).replace('x ','')
            except:
                bedroom_count = None

            try:
                bed_count = (room.find_all('span','Spanstyled__SpanStyled-sc-16tp9kb-0')[3].text).replace('x ','')
            except:
                bed_count = None


            try:
                reviews_count = (room.find_all('span','Spanstyled__SpanStyled-sc-16tp9kb-0')[5].text).replace('reviews','')
            except:
                reviews_count = None
            
            if  room_name :
                writer.writerow([room_name,price,room_type,bedroom_count,bed_count,reviews_count ])
                count += 1


        print(count)
            # if count == 6 :
            #     break

        time.sleep(2)
        driver.find_element_by_id('paginationNext').click()
        time.sleep(5)



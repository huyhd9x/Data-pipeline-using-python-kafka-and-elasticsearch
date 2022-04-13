from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
from time import time
import random
from kafka import KafkaProducer
import json, time
#Log into web
#Open chrome browser and login chotot site
driver = webdriver.Chrome()
url = "https://www.chotot.com/"
driver.get(url)

#click login to enter your infomation
login_field = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div/div[2]/div/a/span/b')
login_field.click()
sleep(2)

# Import username and password
credential = open('acct_chotot.txt')
line = credential.readlines()
username = line[0]
password = line[1]

# Key in username
phone_field = driver.find_element_by_xpath('//*[@id="__next"]/div[3]/main/div/form/div[2]/div/input')
phone_field.send_keys(username)
sleep(3)

# Key in password
password_field = driver.find_element_by_xpath('//*[@id="__next"]/div[3]/main/div/form/div[3]/div/input')
password_field.send_keys(password)
sleep(5)

# Click login button
login2_field = driver.find_element_by_xpath('//*[@id="__next"]/div[3]/main/div/form/button')
login2_field.click()
sleep(2)

# Search for the items we want to buy
# Locate the search bar element
search_field = driver.find_element_by_xpath('//*[@id="__inputItemProps"]')

# Input the search query to search bar
search_query = input("What items do you want to scrape? ")
# search_query = giá đất
search_field.send_keys(search_query)
sleep(5)

#Search
search_field.send_keys(Keys.RETURN)

# Step 3: Scrape the URLs of the item
def GetURL():    
    page_source = BeautifulSoup(driver.page_source)
    items = page_source.find_all('a', class_ = 'AdItem_adItem__2O28x')
    all_item_URL = []
    for item in items:
        item_URL = item.get('href')
        if item_URL not in all_item_URL:
            all_item_URL.append(item_URL)
    return all_item_URL

input_page = int(input('How many pages you want to scrape: '))
URLs_all_page = []
for page in range(input_page):
    URLs_one_page = GetURL()
    sleep(3)
    driver.execute_script('window.scrollTo(0, 3100)') #document.body.scrollHeight
    sleep(2)
    #if next_button is dynamic element instead of next_button = driver.find_element_by_class_name()
    next_button = driver.find_element_by_xpath('//*[@id="__next"]/div/div[3]/div[1]/div[2]/main/div[1]/div[3]/div/div/div[10]/a/i')
    next_button.click()
    URLs_all_page = URLs_all_page + URLs_one_page
    sleep(2)
    print(URLs_all_page)

#Kafka Producer
producer = KafkaProducer(bootstrap_servers = ['localhost:9092'],
	value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8'))

# Task 4: Scrape the data of 1 item, and write the data to a .CSV file
i = 0
for chotot_URL in URLs_all_page:
    try:
        driver.get(chotot_URL)
        i = i + 1
        print(i)
        print("Link URL: ",chotot_URL)
        page_source = BeautifulSoup(driver.page_source, "html.parser")
            #Location
        info_span1=page_source.find('span', class_ = "fz13")
        location = info_span1.get_text().strip()
        if 'Xem bản đồ' in location:
            location = location.strip("Xem bản đồ")
#         print(location)
        # Area
        info_span2 = page_source.find('span',itemprop ='size',class_ = "AdParam_adParamValue__1ayWO")
        area = info_span2.get_text().strip()
#         print(area)
            # price_m2
        info_span3 = page_source.find('span',itemprop ='price_m2', class_ = "AdParam_adParamValue__1ayWO")
        price_m2 = info_span3.get_text().strip()
#         print(price_m2)
        
        temp = {
            'link': chotot_URL,
            'location': location,
            'area': area,
            'price_m2': price_m2
        }
        print(temp)
        producer.send(topic='haiau', value = temp)
        time.sleep(1)
    except:
        pass
print("Successfully!!!")
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 11:50:53 2017

@author: kyunghoon
"""
import time, csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

def get_info(start_url):
    driver = webdriver.Chrome('C:/Users/kyunghoon/Downloads/chromedriver_win32/chromedriver')
    driver.implicitly_wait(15)
    driver.get(start_url)
    elm = driver.find_element_by_tag_name('html')
   # i = 1
    for i in range(1, 6): # scroll down (1 ~ 300)
        elm.send_keys(Keys.END)
        time.sleep(10)
        driver.implicitly_wait(30)
    driver.find_element_by_xpath('//*[@id="show-more-button"]').click()
    for i in range(1, 5): # scroll down (300 ~ 540)
        elm.send_keys(Keys.END)
        time.sleep(10)
        driver.implicitly_wait(30)
    
    driver.implicitly_wait(10)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.implicitly_wait(15) #
    main_content = soup.find('div', class_='body-content')
    apps = main_content.find_all('div', class_='card-content id-track-click id-track-impression')
    rank = 1    
    for app in apps:
        driver.implicitly_wait(10)
        code = app.find('a', class_='card-click-target').get('href')
        target_url = base_url + code
        driver.get(target_url)
        driver.implicitly_wait(5)
        
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")  
        main_content = soup.find('div', class_='main-content')
    
        name = main_content.find('h1', class_='document-title').find('div', class_='id-app-title').get_text()
        dev = main_content.find('div', class_='left-info').find('span', itemprop="name").get_text()
        genre = main_content.find('div', class_='left-info').find('span', itemprop="genre").get_text()
        rating_score = main_content.find('div', class_='score').get_text()
        rating_count = main_content.find('div', class_='right-info').find('span', class_='rating-count').get_text()
        print(name + " ** " + dev + " ** " + genre + " ** " + rating_score + " ** " + rating_count)
        content_dis = main_content.find('div', class_='meta-info contains-text-link')
        containers = content_dis.find_all('div', {'class' : 'content'})
        age_limit = containers[0].get_text()
        try:
            attribute = containers[1].get_text() 
        except:
            attribute = "NA"
            pass
        print(age_limit + " *** " + attribute)
        meta_infos = main_content.find_all('div', {'class' : 'meta-info'})
        for meta_info in meta_infos:
            tmp = meta_info
            if tmp.find('div', class_='title').get_text() == "설치 수":
                downloads = tmp.find('div', itemprop="numDownloads").get_text()
            elif tmp.find('div', class_='title').get_text() == "지원되는 Android 버전":
                support_version = tmp.find('div', itemprop="operatingSystems").get_text()
        print(downloads + " *** " + support_version)
        print(str(rank) + " Success!")
        
        tmp_dict = {'rank' : rank, 'name' : name, 'dev' : dev, 'genre' : genre, 'rating_score' : rating_score,
                    'rating_count' : rating_count, 'age_limit' : age_limit, 'attribute' : attribute,
                    'downloads' : downloads, 'support_version' : support_version}
        data_sets.append(tmp_dict)
        time.sleep(5) #
        rank += 1
        driver.execute_script("window.history.go(-1)")
    
start_url = 'https://play.google.com/store/apps/category/GAME/collection/topselling_free'
base_url = 'https://play.google.com'
data_sets = []
get_info(start_url)

data_keys = data_sets[0].keys()
with open('test_item_matrix_2.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, delimiter=',',lineterminator='\n', fieldnames = data_keys)
    writer.writeheader()
    writer.writerows(data_sets)